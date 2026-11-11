"""Verify released saved records; optionally replay authenticated private logits.

No model loading or solver use. The optional refit uses only the archived frozen
selected-only NumPy procedure. Reviewer vectors and retrospective search records
are unavailable and are deliberately not reconstructed here.
"""
import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import reproduce_tables as v1

ROOT = Path(__file__).resolve().parents[1]
LOGITS_SHA = 'ef356769710266f255539755b3a035975ac37814d49a4e46ad5fe46c30659e6b'
require = v1.require
load = v1.load


def rows(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def integrity(root):
    manifest = load(root / 'results/v2/manifest.json')
    for name, entry in manifest['included'].items():
        path = root / name
        require(path.is_file(), f'missing v2 file: {name}')
        raw = path.read_bytes()
        require(len(raw) == entry['bytes'], f'v2 size mismatch: {name}')
        require(hashlib.sha256(raw).hexdigest() == entry['sha256'], f'v2 hash mismatch: {name}')
    return manifest


def check_accounting(row):
    n, correct, baseline, corrections, breaks = (int(row[k]) for k in
        ('n', 'correct', 'baseline_correct', 'corrections', 'breaks'))
    require(n > 0 and all(0 <= x <= n for x in (correct, baseline, corrections, breaks)), 'invalid counts')
    require(correct == baseline + corrections - breaks, 'correction/break accounting')
    v1.close(float(row['accuracy']), correct / n, 'accuracy/count disagreement')


def group_mask(labels, group):
    if group == 'all':
        return [True] * len(labels)
    if group == 'true8':
        return [y == 8 for y in labels]
    if group == 'non8':
        return [y != 8 for y in labels]
    if group.startswith('class_'):
        return [y == int(group[6:]) for y in labels]
    if group.startswith('classes_'):
        return [str(y) in group[8:] for y in labels]
    raise ValueError(f'unknown group {group}')


def stats(y, pred, base, mask):
    triples = [(t, a, b) for t, a, b, keep in zip(y, pred, base, mask) if keep]
    return dict(n=len(triples), correct=sum(t == a for t, a, b in triples),
        baseline_correct=sum(t == b for t, a, b in triples),
        corrections=sum(t == a and t != b for t, a, b in triples),
        breaks=sum(t != a and t == b for t, a, b in triples))


def records(root):
    return {s: load(root / 'results/evidence' / s / 'independent_heldout_predictions.json')['domains']
            for s in v1.SLOTS}


def saved_checks(root):
    v1.analyze(root)
    manifest = integrity(root)
    audit = load(root / 'results/v2/class_audit/CLASS_AUDIT_RESULTS.json')
    repairs = records(root)
    for domain, entry in audit['domains'].items():
        for slot, record in entry['runs'].items():
            d = repairs[slot][domain]
            start = 1100 if domain == 'identity' else 0
            y, a, b = [d[k][start:] for k in ('labels', 'predictions', 'baseline')]
            for c, expected in record['per_true_class'].items():
                require(stats(y, a, b, group_mask(y, 'class_'+c)) == expected, 'class audit mismatch')
            for group, expected in record['groups'].items():
                require(stats(y, a, b, group_mask(y, group)) == expected, 'group audit mismatch')
            observed = dict(original_predicted8=b.count(8), repaired_predicted8=a.count(8),
                original8_to_non8=sum(x == 8 and z != 8 for x, z in zip(b, a)),
                original_non8_to8=sum(x != 8 and z == 8 for x, z in zip(b, a)),
                changes_among_original_non8=sum(x != 8 and x != z for x, z in zip(b, a)),
                corrections_among_original_non8=sum(x != 8 and x != t and z == t for x, z, t in zip(b, a, y)),
                breaks_among_original_non8=sum(x != 8 and x == t and z != t for x, z, t in zip(b, a, y)))
            require(all(record[k] == value for k, value in observed.items()), 'transition audit mismatch')
        for cohort, pair in entry['pairs'].items():
            start = 1100 if domain == 'identity' else 0
            a, b = [repairs[cohort+'_'+j][domain]['predictions'][start:] for j in ('J0', 'J1')]
            require(pair['disagreement'] == sum(x != y for x, y in zip(a, b)), 'pair disagreement')
            require(pair['disagreement_both_non8'] == sum(x != y and x != 8 and y != 8 for x, y in zip(a, b)), 'non8 disagreement')
    total = 0
    for name in ('scalar/D2_CLASS_TABLE.csv', 'ten_bias/CLASS_OUTCOMES.csv'):
        table = rows(root / 'results/v2' / name)
        for row in table:
            check_accounting(row)
        total += len(table)
        keys = ['cohort', 'population'] + (['diagnostic'] if name.startswith('scalar') else [])
        partitions = {}
        for row in table:
            partitions.setdefault(tuple(row[k] for k in keys), {})[row['group']] = row
        for partition in partitions.values():
            for field in ('n', 'correct', 'baseline_correct', 'corrections', 'breaks'):
                require(sum(int(partition['class_'+str(c)][field]) for c in range(10)) == int(partition['all'][field]), 'class partition mismatch')
                require(int(partition['true8'][field])+int(partition['non8'][field]) == int(partition['all'][field]), 'group partition mismatch')
    for cohort in ('P001', 'P002'):
        fit = load(root / f'results/v2/ten_bias/{cohort}_FIT.json')
        frozen = load(root / 'results/v2/ten_bias/FITS_FROZEN_BEFORE_HELDOUT_EVALUATION.json')
        require(fit == frozen['fits'][cohort], 'frozen fit mismatch')
        require(len(fit['offsets']) == 10, 'offset count')
        require(abs(sum(fit['offsets'])) < 1e-12, 'zero-sum gauge')
        v1.close(fit['penalty'], .01/2*sum(b*b for b in fit['offsets']), 'penalty convention')
        v1.close(fit['final_objective'], fit['final_selected_cross_entropy']+fit['penalty'], 'CE plus penalty')
    return dict(public_checks='PASS', accounting_rows=total, v1='unchanged saved-evidence checks passed',
        limitations=manifest['omitted'])


def candidates(np, z, bounded):
    thresholds = z[:, 8] - np.max(z[:, [0,1,2,3,4,5,6,7,9]], axis=1)
    endpoints = {0.0, 3.0} if bounded else {0.0}
    endpoints.update(float(t) for t in thresholds if t >= 0 and (not bounded or t <= 3))
    points = sorted(endpoints)
    values = set(points)
    values.update((a+b)/2 for a, b in zip(points, points[1:]))
    if not bounded:
        values.add(points[-1]+max(1, abs(points[-1])))
    return sorted(values)


def shifted(np, z, tau):
    copy = z.copy()
    copy[:, 8] -= tau
    return np.argmax(copy, axis=1)


def numerical_checks(root, path, refit=False):
    require(hashlib.sha256(path.read_bytes()).hexdigest() == LOGITS_SHA, 'private logits hash mismatch')
    import numpy as np
    repairs = records(root)
    with np.load(path, allow_pickle=False) as archive:
        a = {k: archive[k] for k in archive.files}
    expected = {d+'_'+k for d in ('fog','identity') for k in ('indices','labels','logits','predictions')}
    expected.update(c+'_selected_indices' for c in ('P001','P002'))
    require(set(a) == expected, 'NPZ schema mismatch')
    for domain in ('fog','identity'):
        z, y = a[domain+'_logits'], a[domain+'_labels']
        require(z.shape == (10000,10) and z.dtype == np.float64 and np.isfinite(z).all(), 'invalid logits')
        require(y.shape == (10000,) and np.issubdtype(y.dtype, np.integer) and ((y >= 0)&(y < 10)).all(), 'invalid labels')
        require(np.array_equal(a[domain+'_indices'], np.arange(10000)), 'NPZ indices')
        require(np.array_equal(np.argmax(z, axis=1), a[domain+'_predictions']), 'NPZ argmax')
        for slot, data in repairs.items():
            d = data[domain]; ix = np.array(d['indices'])
            require(np.array_equal(y[ix], d['labels']), 'public label alignment')
            require(np.array_equal(a[domain+'_predictions'][ix], d['baseline']), 'public baseline disagreement')
    features = load(root / 'results/evidence/FROZEN_PILOT_PRE_REPAIR_FEATURES.json')['pre_repair']
    selection = load(root / 'results/v2/scalar/CALIBRATION_SELECTION.json')
    cohorts = load(root / 'results/evidence/FROZEN_PILOT_COHORTS.json')['cohorts']
    predictions = {}
    selected_counts = {}
    for cohort in ('P001', 'P002'):
        ids = a[cohort+'_selected_indices']
        require(ids.shape == (100,) and len(set(ids.tolist())) == 100 and ((ids >= 0)&(ids < 1100)).all(), 'selected indices')
        require(np.array_equal(ids, cohorts[cohort]['indices']), 'frozen cohort alignment')
        z, y = a['fog_logits'][ids], a['fog_labels'][ids]
        require(np.array_equal(y, features[cohort]['labels']), 'selected labels')
        require(np.array_equal(np.argmax(z,axis=1), features[cohort]['predictions']), 'selected baseline')
        for kind in ('bounded', 'unrestricted'):
            grid = candidates(np, z, kind == 'bounded')
            recorded = selection[cohort][kind]['candidates']
            require(len(grid) == len(recorded), 'candidate count')
            scored = []
            for tau, entry in zip(grid, recorded):
                errors = int((shifted(np,z,tau) != y).sum())
                require(tau.hex() == entry['tau_hex'] and errors == entry['errors'], 'selected candidate replay')
                scored.append((errors,tau))
            errors, tau = min(scored)
            selected_counts[cohort+'_'+kind] = dict(tau=tau, selected_correct=100-errors)
            predictions[cohort,kind] = {d:shifted(np,a[d+'_logits'],tau) for d in ('fog','identity')}
        fit = load(root / f'results/v2/ten_bias/{cohort}_FIT.json')
        b = np.array(fit['offsets'])
        require(int((np.argmax(z+b,axis=1)==y).sum()) == fit['selected_correct'], 'ten-bias selected replay')
        predictions[cohort,'ten_bias'] = {d:np.argmax(a[d+'_logits']+b,axis=1) for d in ('fog','identity')}
    for row in rows(root / 'results/v2/scalar/D1_SELECTION.csv'):
        result = selected_counts[row['cohort']+'_'+row['diagnostic']]
        require(result['tau'].hex() == row['tau_hex'] and result['selected_correct'] == int(row['selected_correct']), 'D1 selected optimum mismatch')
    checked = 0
    for file, kind in [('scalar/D2_CLASS_TABLE.csv',None),('ten_bias/CLASS_OUTCOMES.csv','ten_bias')]:
        for row in rows(root / 'results/v2' / file):
            domain = 'fog' if row['population']=='fog_primary' else 'identity'
            ix = slice(0 if row['population']=='clean_full' else 1100,10000)
            y = a[domain+'_labels'][ix].tolist()
            p = predictions[row['cohort'],kind or row['diagnostic']][domain][ix].tolist()
            baseline = a[domain+'_predictions'][ix].tolist()
            actual = stats(y,p,baseline,group_mask(y,row['group']))
            require(all(actual[k]==int(row[k]) for k in actual), 'numerical class table mismatch')
            checked += 1
    # Verify all recorded scalar-versus-repair paired agreements from saved predictions.
    for row in rows(root / 'results/v2/scalar/D3_COMPARISONS.csv'):
        domain = 'fog' if row['population']=='fog_primary' else 'identity'
        d = repairs[row['repair']][domain]
        ix = np.array(d['indices']); keep = ix >= (0 if row['population']=='clean_full' else 1100)
        p = predictions[row['cohort'],row['diagnostic']][domain][ix][keep]
        q = np.array(d['predictions'])[keep]
        require(int((p==q).sum()) == int(row['agreement']), 'paired scalar agreement')
        y = np.array(d['labels'])[keep]
        require(int((p==y).sum())-int((q==y).sum()) == int(row['delta_correct']), 'scalar/repair delta')
    for row in rows(root / 'results/v2/ten_bias/COMPARISONS.csv'):
        cohort = row['cohort']
        domain = 'fog' if row['population']=='fog_primary' else 'identity'
        ix = np.arange(0 if row['population']=='clean_full' else 1100,10000)
        p = predictions[cohort,'ten_bias'][domain][ix]
        comparator = row['comparator']
        if comparator == 'original':
            q = a[domain+'_predictions'][ix]
        elif comparator.startswith('scalar_'):
            q = predictions[cohort,comparator[7:]][domain][ix]
        else:
            d = repairs[cohort+'_'+comparator][domain]
            lookup = dict(zip(d['indices'],d['predictions']))
            q = np.array([lookup[int(i)] for i in ix])
        y = a[domain+'_labels'][ix]
        original = a[domain+'_predictions'][ix]
        values = dict(n=len(ix), calibrated_correct=int((p==y).sum()), comparator_correct=int((q==y).sum()),
            delta_correct=int((p==y).sum())-int((q==y).sum()), disagreements=int((p!=q).sum()),
            both_correct=int(((p==y)&(q==y)).sum()), only_calibrated_correct=int(((p==y)&(q!=y)).sum()),
            only_comparator_correct=int(((p!=y)&(q==y)).sum()),
            non8_non8_disagreements=int(((p!=q)&(p!=8)&(q!=8)).sum()),
            changed_originally_non8=int(((original!=8)&(p!=q)).sum()))
        require(all(int(row[k])==v for k,v in values.items()), 'ten-bias paired comparison')
    refits = {}
    if refit:
        spec = importlib.util.spec_from_file_location('frozen_ten_bias', root / 'results/v2/sources/ten_bias_original.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        for cohort in ('P001','P002'):
            ids = a[cohort+'_selected_indices']
            actual = module.fit(a['fog_logits'][ids],a['fog_labels'][ids])
            expected_fit = load(root / f'results/v2/ten_bias/{cohort}_FIT.json')
            require(np.allclose(actual['offsets'],expected_fit['offsets'],rtol=1e-10,atol=1e-10), 'frozen refit offsets')
            require(actual['updates']==expected_fit['updates'] and actual['selected_correct']==expected_fit['selected_correct'], 'frozen refit termination')
            refits[cohort] = actual
    return dict(numpy=np.__version__, numerical_rows=checked, selected=selected_counts,
        refits=refits, retrospective_and_reviewer_claims='NOT VERIFIED: companion artifacts absent')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--logits', type=Path, help='private authenticated ORIGINAL_LOGITS.npz; never downloaded automatically')
    parser.add_argument('--refit-ten-bias', action='store_true', help='repeat only the frozen selected-only NumPy fit')
    args = parser.parse_args()
    require(not args.refit_ten_bias or args.logits is not None, '--refit-ten-bias requires --logits')
    result = saved_checks(ROOT)
    if args.logits:
        result['private_logits'] = numerical_checks(ROOT,args.logits,args.refit_ten_bias)
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError) as exc:
        print(f'FAILED: {exc}',file=sys.stderr)
        sys.exit(1)
