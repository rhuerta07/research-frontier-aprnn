"""Recalculate saved-evidence tables; Python 3.10+, standard library only.

No inference, model loading, training, or optimization. Hashes establish consistency
with the release's pinned evidence, not independent third-party attestation.
"""
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
SLOTS = ('P001_J0', 'P001_J1', 'P002_J0', 'P002_J1')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f'duplicate JSON key: {key}')
            result[key] = value
        return result
    def bad(value):
        raise ValueError(f'nonfinite JSON: {value}')
    try:
        return json.loads(Path(path).read_bytes(), object_pairs_hook=pairs, parse_constant=bad)
    except (OSError, ValueError) as exc:
        raise ValueError(f'{path}: {exc}') from exc


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def close(a, b, message):
    require(math.isfinite(a) and math.isfinite(b) and math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12), message)


def counts(domain, start, end):
    require(set(domain) == {'indices', 'labels', 'baseline', 'predictions'}, 'prediction fields')
    require(domain['indices'] == list(range(start, end)), 'image index alignment')
    n = end - start
    for key in ('labels', 'baseline', 'predictions'):
        require(len(domain[key]) == n, f'{key}: inconsistent denominator')
        require(all(type(x) is int and 0 <= x < 10 for x in domain[key]), f'{key}: invalid class')
    y, before, after = (domain[k] for k in ('labels', 'baseline', 'predictions'))
    base = sum(a == b for a, b in zip(before, y))
    correct = sum(a == b for a, b in zip(after, y))
    corrections = sum(a != t and b == t for a, b, t in zip(before, after, y))
    breaks = sum(a == t and b != t for a, b, t in zip(before, after, y))
    require(correct == base + corrections - breaks, 'correction/break accounting')
    return dict(baseline_correct=base, correct=correct, corrections=corrections, breaks=breaks)


def verify_integrity(root):
    manifest = load(root / 'results/evidence_manifest.json')
    for entry in manifest['included']:
        path = root / entry['repository_path']
        require(path.is_file(), f'missing evidence: {entry["repository_path"]}')
        raw = path.read_bytes()
        require(len(raw) == entry['size_bytes'], f'size mismatch: {path}')
        require(hashlib.sha256(raw).hexdigest() == entry['sha256'], f'hash mismatch: {path}')


def analyze(root=ROOT, integrity=True):
    root = Path(root)
    if integrity:
        verify_integrity(root)
    evidence = root / 'results/evidence'
    summary = load(root / 'results/rp001_summary.json')
    require(set(summary['slots']) == set(SLOTS), 'missing or unexpected repair attempts')
    require(set(summary['pairs']) == {'P001', 'P002'}, 'cohort identities')
    feature_record = load(evidence / 'FROZEN_PILOT_PRE_REPAIR_FEATURES.json')
    features = feature_record['pre_repair']
    cohorts = load(evidence / 'FROZEN_PILOT_COHORTS.json')['cohorts']
    require(set(features) == set(cohorts) == {f'P{i:03}' for i in range(1, 9)}, 'frozen cohort identities')
    for cohort, frozen in cohorts.items():
        require(len(frozen['indices']) == len(set(frozen['indices'])) == 100, 'frozen cohort size')
        require(all(100 <= i < 1100 for i in frozen['indices']), 'cohort selection pool')
        require(features[cohort]['indices'] == frozen['indices'], 'frozen feature indices')
        require(len(features[cohort]['labels']) == len(features[cohort]['true_class_margins']) == 100, 'frozen feature denominator')
        close(statistics.median(features[cohort]['true_class_margins']), features[cohort]['median_margin'], 'frozen median')
    failed = load(evidence / 'failed_P001_J0_terminal.json')
    require(failed['slot'] == 'P001_J0' and failed['status'] == 'UNRESOLVED', 'failed attempt history')
    retry = load(evidence / 'RETRY_AUTHORIZATION_AND_MANIFEST.json')
    require(retry['no_optimizer_or_checkpoint'] is True and retry['slots'] == list(SLOTS), 'retry history')
    p005 = load(evidence / 'ATTEMPT_P005_RESULT.json')
    require(p005['arm'] == 'P005' and p005['final_state'] == 'UNRESOLVED' and p005['no_retry'] is True, 'P005 attempt history')
    predictions, setups, output = {}, {}, {'verification': {'rp001': 'archived per-image predictions and selected-point logits', 'pilot': 'LOOCV recalculated from saved cohort summaries and frozen features', 'displacements': 'recorded post-repair observations; no checkpoint reload'}, 'rp001': {}, 'pilot': {}}
    for slot in SLOTS:
        cohort = slot.split('_')[0]
        saved = summary['slots'][slot]
        replay = saved['replay']
        pred = load(evidence / slot / 'independent_heldout_predictions.json')
        points = load(evidence / slot / 'independent_repair_points.json')
        setup = load(evidence / slot / 'common_setup.json')
        require(pred['run_id'] == replay['run_id'] == slot, 'altered cohort/run identity')
        require(pred['manifest_sha256'] == replay['manifest_sha256'], 'manifest identity')
        require(pred['checkpoint_sha256'] == replay['checkpoint_sha256'], 'checkpoint identity')
        require(canonical_hash(pred) == replay['heldout_predictions_sha256'], 'prediction semantic hash')
        require(canonical_hash(points) == replay['points_sha256'], 'selected points semantic hash')
        require(setup['indices'] == cohorts[cohort]['indices'] == features[cohort]['indices'], 'selected indices')
        require(setup['labels'] == features[cohort]['labels'], 'changed selected labels')
        require([p['index'] for p in points] == setup['indices'], 'selected point alignment')
        require([p['label'] for p in points] == setup['labels'], 'changed or missing image labels')
        require(len(points) == saved['selected_count'] == 100, 'selected denominator')
        margins = []
        for p in points:
            logits, label = p['logits'], p['label']
            require(len(logits) == 10 and all(math.isfinite(x) for x in logits), 'malformed logits')
            prediction = max(range(10), key=logits.__getitem__)
            margin = logits[label] - max(x for i, x in enumerate(logits) if i != label)
            close(margin, p['margin'], 'selected margin')
            require(prediction == p['prediction'] == label and p['tie'] is False, 'selected-point failure')
            require(margin >= replay['epsilon'] - replay['constraint_tolerance'], 'selected margin tolerance')
            margins.append(margin)
        close(min(margins), replay['min_margin'], 'minimum margin')
        require(set(pred['domains']) == {'fog', 'identity'}, 'evaluation domains')
        domains = {}
        for name, start in [('fog', 1100), ('identity', 0)]:
            domain = pred['domains'][name]
            full = counts(domain, start, 10000)
            check = replay['heldout'][name]
            require(check['n'] == 10000-start and check['start'] == start and check['end'] == 10000, 'inconsistent denominators')
            require(full['correct'] == check['repaired_correct'] and full['baseline_correct'] == check['original_correct'], 'replay counts')
            if name == 'identity':
                domains['identity_full'] = full
                domain = {k: v[1100:] for k, v in domain.items()}
            domains[name + '_primary'] = counts(domain, 1100, 10000)
        require(math.isfinite(replay['max_absolute_editable_delta']) and 0 <= replay['max_absolute_editable_delta'] <= replay['delta_bound'] + replay['delta_tolerance'], 'recorded displacement bound')
        output['rp001'][slot] = dict(domains=domains, selected_correct=len(points), min_margin=min(margins), observed_max_displacement=replay['max_absolute_editable_delta'])
        predictions[slot], setups[slot] = pred, setup
    reference = predictions[SLOTS[0]]['domains']
    for pred in predictions.values():
        for name, domain in pred['domains'].items():
            for key in ('indices', 'labels', 'baseline'):
                require(domain[key] == reference[name][key], f'{name}: cross-run {key} mismatch')
    # Clean/fog image labels must describe the same underlying MNIST examples.
    require(reference['fog']['labels'] == reference['identity']['labels'][1100:], 'clean/fog label alignment')
    for cohort, pair in summary['pairs'].items():
        require(setups[cohort+'_J0'] == setups[cohort+'_J1'], 'common setup mismatch')
        require(pair['common_setup_match'] is True and pair['common_sha256'] == setups[cohort+'_J0']['common_sha256'], 'common constraint identity')
        for name, recorded in pair['domains'].items():
            n = 10000 if name == 'identity_full' else 8900
            require(recorded['n'] == n, 'pair denominator')
            for obj in ('j0', 'j1'):
                computed = output['rp001'][cohort+'_'+obj.upper()]['domains'][name]
                require(computed == recorded[obj], f'{cohort}/{obj}/{name}: correction/break counts mismatch')
            source_domain = 'fog' if name == 'fog_primary' else 'identity'
            a = predictions[cohort+'_J0']['domains'][source_domain]
            b = predictions[cohort+'_J1']['domains'][source_domain]
            begin = 1100 if name == 'identity_primary' else 0
            triples = list(zip(a['labels'][begin:], a['predictions'][begin:], b['predictions'][begin:]))
            paired = dict(both_correct=sum(x == y == t for t, x, y in triples),
                          both_wrong=sum(x != t and y != t for t, x, y in triples),
                          candidate_only=sum(x != t and y == t for t, x, y in triples),
                          reference_only=sum(x == t and y != t for t, x, y in triples),
                          class_disagreement=sum(x != y for t, x, y in triples))
            require(paired == recorded['j0_vs_j1'], 'paired transition accounting')
            diff = recorded['j1']['correct'] - recorded['j0']['correct']
            require(diff == recorded['j1_minus_j0_correct'], 'difference count')
            close(100*diff/n, recorded['j1_minus_j0_pp'], 'difference percentage points')
            output['rp001'][cohort+'_'+name+'_J1_minus_J0_pp'] = 100*diff/n
    pilot = load(root / 'results/pilot_summary.json')
    require([r['id'] for r in pilot['records']] == [f'P{i:03}' for i in range(1, 9)], 'pilot cohort identities')
    missing = pilot['records'][4]
    require(missing['id'] == 'P005' and missing['outcomes'] is None and missing['status'] == 'operational_failure', 'P005 missingness')
    rows = [r for r in pilot['records'] if r['outcomes'] is not None]
    for row in rows:
        close(row['margin'], statistics.median(features[row['id']]['true_class_margins']), 'frozen feature median')
        for target, domain in row['outcomes'].items():
            require(domain['n'] == 8900 and 0 <= domain['repaired_correct'] <= domain['n'], 'pilot denominator')
            close(domain['delta'], (domain['repaired_correct']-domain['original_correct'])/domain['n'], 'pilot delta')
    for target, threshold in [('fog', .8), ('clean', .9)]:
        folds = []
        for row in rows:
            train = [r for r in rows if r['id'] != row['id']]
            xs = [r['margin'] for r in train]
            ys = [r['outcomes'][target]['delta'] for r in train]
            mx, my, sd = statistics.mean(xs), statistics.mean(ys), statistics.pstdev(xs)
            z = [(x-mx)/sd for x in xs] if sd else [0.0]*len(xs)
            slope = sum(v*(y-my) for v, y in zip(z, ys))/(sum(v*v for v in z)+1)
            prediction = my-slope*statistics.mean(z)+slope*(row['margin']-mx)/sd if sd else my
            observed = row['outcomes'][target]['delta']
            fold = next(f for f in pilot['scores'][target]['folds'] if f['id'] == row['id'])
            require(fold['training_ids'] == [r['id'] for r in train], 'LOOCV fold identities')
            close(prediction, fold['prediction'], 'LOOCV prediction')
            folds.append((abs(prediction-observed), abs(my-observed)))
        model = statistics.mean(f[0] for f in folds)
        baseline = statistics.mean(f[1] for f in folds)
        ratio = model/baseline
        recorded = pilot['scores'][target]
        for k, v in [('model_mae', model), ('baseline_mae', baseline), ('ratio', ratio), ('threshold', threshold)]:
            close(v, recorded[k], 'pilot '+k)
        require((ratio <= threshold) == recorded['passes_numerical_threshold'], 'pilot threshold decision')
        output['pilot'][target] = dict(baseline_mae_pp=100*baseline, model_mae_pp=100*model, ratio=ratio, passes=ratio <= threshold)
    joint = all(v['passes'] for v in output['pilot'].values())
    require(joint == pilot['numerical_screen'] == False, 'joint numerical NO-GO')
    require(pilot['operational_integrity_condition_met'] is False, 'operational condition')
    output['pilot']['joint_decision'] = 'NO-GO'
    return output


if __name__ == '__main__':
    try:
        print(json.dumps(analyze(), indent=2, allow_nan=False))
    except (ValueError, KeyError, TypeError, IndexError, StopIteration) as exc:
        print(f'Evidence verification failed: {exc}', file=sys.stderr)
        sys.exit(1)
