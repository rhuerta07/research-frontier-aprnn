"""Approved, fixed-rule NumPy calibration on archived logits; no model inference."""
import csv
import hashlib
import json
import pathlib
import platform
import signal
import time
import traceback

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(__file__).resolve().parent
PUBLIC = ROOT / 'aprnn_review_37d8165/results/evidence'
PACKET = ROOT / 'reviewer_packet_v2r1'
NPZ = ROOT / 'upload/ORIGINAL_LOGITS.npz'
LAMBDA = .01
ETA = 100 / 51
START = time.monotonic()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def loss_gradient(z, y, b):
    x = z + b
    m = x.max(axis=1, keepdims=True)
    e = np.exp(x - m)
    p = e / e.sum(axis=1, keepdims=True)
    ce = np.mean(np.log(e.sum(axis=1)) + m[:, 0] - x[np.arange(len(y)), y])
    g = p.mean(axis=0) - np.bincount(y, minlength=10) / len(y) + LAMBDA * b
    g -= g.mean()
    return float(ce + LAMBDA / 2 * (b @ b)), g, float(ce)


def numerical_checks():
    z = np.arange(40, dtype=np.float64).reshape(4, 10) / 7
    y = np.array([0, 4, 9, 3])
    b = np.linspace(-.2, .2, 10)
    f, g, ce = loss_gradient(z, y, b)
    fd = np.zeros(10)
    for k in range(10):
        h = np.zeros(10); h[k] = 1e-5
        fd[k] = (loss_gradient(z, y, b+h)[0] - loss_gradient(z, y, b-h)[0]) / 2e-5
    require(np.max(np.abs(g-fd)) < 1e-8, 'synthetic gradient mismatch')
    require(abs(loss_gradient(z+10000, y, b)[0]-f) < 1e-10, 'unstable logsumexp')
    require(np.array_equal(np.argmax(z+b, axis=1), np.argmax(z+b+13, axis=1)), 'gauge invariance')
    try:
        require(False, 'intentional input rejection')
    except ValueError:
        pass
    else:
        raise AssertionError('input rejection broken')
    return {'gradient_max_error': float(np.max(np.abs(g-fd))), 'checks': 4}


def fit(z, y):
    require(z.shape == (100, 10) and y.shape == (100,), 'fit shape')
    require(z.dtype == np.float64 and np.isfinite(z).all(), 'fit logits')
    require(np.all((y >= 0) & (y < 10)), 'fit labels')
    t = time.monotonic()
    b = np.zeros(10, dtype=np.float64)
    initial, _, initial_ce = loss_gradient(z, y, b)
    previous = initial
    for step in range(10001):
        require(time.monotonic()-t < 60, 'fit exceeded 60 seconds')
        f, g, ce = loss_gradient(z, y, b)
        require(np.isfinite(f) and np.isfinite(g).all(), 'nonfinite fit')
        require(f <= previous + 1e-10, 'objective increased')
        if np.max(np.abs(g)) <= 1e-8 and abs(b.mean()) <= 1e-12:
            return {'offsets': b.tolist(), 'updates': step, 'seconds': time.monotonic()-t,
                    'initial_objective': initial, 'final_objective': f,
                    'initial_selected_cross_entropy': initial_ce, 'final_selected_cross_entropy': ce,
                    'penalty': float(LAMBDA/2*(b@b)), 'projected_gradient_inf': float(np.max(np.abs(g))),
                    'mean_offset': float(b.mean()), 'selected_correct': int((np.argmax(z+b, axis=1)==y).sum()),
                    'selected_class_counts': np.bincount(y, minlength=10).tolist(), 'termination': 'converged'}
        require(step < 10000, 'fit did not converge')
        previous = f
        b -= ETA * g
        b -= b.mean()


def stats(y, pred, baseline, mask):
    correct = pred == y
    old = baseline == y
    return {'n': int(mask.sum()), 'correct': int((correct & mask).sum()),
            'baseline_correct': int((old & mask).sum()),
            'corrections': int((correct & ~old & mask).sum()),
            'breaks': int((~correct & old & mask).sum())}


def write_csv(name, rows):
    with (OUT/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def run():
    inputs = {str(p.relative_to(ROOT)): sha(p) for p in [NPZ, OUT/'FROZEN_PILOT_COHORTS.json',
              PUBLIC/'FROZEN_PILOT_PRE_REPAIR_FEATURES.json', PACKET/'TEN_BIAS_DESIGN_FOR_APPROVAL.md',
              PACKET/'D1_SELECTION.csv', PACKET/'D2_CLASS_TABLE.csv']}
    require(sha(NPZ) == 'ef356769710266f255539755b3a035975ac37814d49a4e46ad5fe46c30659e6b', 'NPZ hash mismatch')
    require(NPZ.stat().st_size == 2084250, 'NPZ size mismatch')
    require(sha(OUT/'FROZEN_PILOT_COHORTS.json') == '3192c9f24785b16dea74bbc86d05e40c08926a007af2ec8d2bfb770a8a4a3fb6', 'cohort hash mismatch')
    cohorts = json.loads((OUT/'FROZEN_PILOT_COHORTS.json').read_text())['cohorts']
    features = json.loads((PUBLIC/'FROZEN_PILOT_PRE_REPAIR_FEATURES.json').read_text())['pre_repair']
    with np.load(NPZ, allow_pickle=False) as data:
        a = {k: data[k].copy() for k in data.files}
    for domain in ['fog', 'identity']:
        ids, y, z = (a[domain+'_'+k] for k in ['indices', 'labels', 'logits'])
        require(np.array_equal(ids, np.arange(10000)), 'NPZ index order mismatch')
        require(y.shape == (10000,) and np.all((y>=0)&(y<10)), 'NPZ labels invalid')
        require(z.shape == (10000,10) and z.dtype == np.float64 and np.isfinite(z).all(), 'NPZ logits invalid')
        require(np.array_equal(np.argmax(z, axis=1), a[domain+'_predictions']), 'NPZ baseline mismatch')
    repairs = {}
    for c in ['P001','P002']:
        ids = np.array(cohorts[c]['indices'])
        require(len(set(ids.tolist())) == 100 and np.all((ids>=100)&(ids<1100)), 'selected IDs invalid')
        require(np.array_equal(ids, a[c+'_selected_indices']), 'selected binding mismatch')
        require(np.array_equal(a['fog_labels'][ids], features[c]['labels']), 'selected label mismatch')
        require(np.array_equal(a['fog_predictions'][ids], features[c]['predictions']), 'selected winner mismatch')
        for j in ['J0','J1']:
            name = c+'_'+j
            path = PUBLIC/name/'independent_heldout_predictions.json'
            inputs[str(path.relative_to(ROOT))] = sha(path)
            domains = json.loads(path.read_text())['domains']
            repairs[name] = {}
            for domain, d in domains.items():
                ix = np.array(d['indices'])
                require(np.array_equal(a[domain+'_labels'][ix], d['labels']), 'archived labels mismatch')
                require(np.array_equal(a[domain+'_predictions'][ix], d['baseline']), 'archived baseline mismatch')
                repairs[name][domain] = dict(indices=ix, predictions=np.array(d['predictions']))
    scalar = {}
    choices = list(csv.DictReader((PACKET/'D1_SELECTION.csv').open()))
    tab = list(csv.DictReader((PACKET/'D2_CLASS_TABLE.csv').open()))
    for choice in choices:
        c, kind = choice['cohort'], choice['diagnostic']
        scalar[c,kind] = {}
        for domain in ['fog','identity']:
            z = a[domain+'_logits'].copy(); z[:,8] -= float(choice['tau'])
            scalar[c,kind][domain] = np.argmax(z, axis=1)
        ids = a[c+'_selected_indices']
        require(int((scalar[c,kind]['fog'][ids]==a['fog_labels'][ids]).sum()) == int(choice['selected_correct']), 'scalar selected mismatch')
        for row in [r for r in tab if r['cohort']==c and r['diagnostic']==kind]:
            domain = 'fog' if row['population']=='fog_primary' else 'identity'
            ix = np.arange(10000) if row['population']=='clean_full' else np.arange(1100,10000)
            y, pred, baseline = a[domain+'_labels'][ix], scalar[c,kind][domain][ix], a[domain+'_predictions'][ix]
            group = row['group']; mask = np.ones(len(ix),dtype=bool)
            if group=='true8': mask=y==8
            elif group=='non8': mask=y!=8
            elif group.startswith('class_'): mask=y==int(group[6:])
            got=stats(y,pred,baseline,mask)
            require(all(got[k]==int(row[k]) for k in got), 'scalar class reconstruction mismatch')
    save('PREFLIGHT.json', {'passed': True, 'scalar_class_rows_reconstructed': len(tab),
         'input_hashes':inputs, 'numerical_checks': numerical_checks(), 'python':platform.python_version(),
         'numpy':np.__version__, 'source_sha256':sha(pathlib.Path(__file__))})
    fits = {}
    for c in ['P001','P002']:
        ix=a[c+'_selected_indices']
        fits[c]=fit(a['fog_logits'][ix].copy(),a['fog_labels'][ix].copy())
        save(c+'_FIT.json',fits[c])
    save('FITS_FROZEN_BEFORE_HELDOUT_EVALUATION.json', {'fits':fits, 'protocol_sha256':sha(PACKET/'TEN_BIAS_DESIGN_FOR_APPROVAL.md')})
    class_rows, comparisons, predictions, summary = [], [], {}, {}
    for c in ['P001','P002']:
        b=np.array(fits[c]['offsets']); summary[c]={}; predictions[c]={}
        for population, domain, ix in [('fog_primary','fog',np.arange(1100,10000)), ('clean_primary','identity',np.arange(1100,10000)),('clean_full','identity',np.arange(10000))]:
            y=a[domain+'_labels'][ix]; baseline=a[domain+'_predictions'][ix]
            pred=np.argmax(a[domain+'_logits'][ix]+b,axis=1)
            predictions[c][population]={'indices':ix.tolist(),'labels':y.tolist(),'predictions':pred.tolist()}
            groups={'all':np.ones(len(y),dtype=bool),'true8':y==8,'non8':y!=8,
                    'classes_0167':np.isin(y,[0,1,6,7]),'classes_23459':np.isin(y,[2,3,4,5,9])}
            groups.update({f'class_{k}':y==k for k in range(10)})
            for group, mask in groups.items():
                r=stats(y,pred,baseline,mask)
                class_rows.append({'cohort':c,'population':population,'group':group,**r,'accuracy':r['correct']/r['n']})
            total=stats(y,pred,baseline,groups['all'])
            summary[c][population]={**total,'accuracy':total['correct']/len(y), 'predicted_class_counts':np.bincount(pred,minlength=10).tolist()}
            others={'original':baseline, 'scalar_bounded':scalar[c,'bounded'][domain][ix], 'scalar_unrestricted':scalar[c,'unrestricted'][domain][ix]}
            for j in ['J0','J1']:
                r=repairs[c+'_'+j][domain]
                lookup=dict(zip(r['indices'].tolist(),r['predictions'].tolist()))
                others[j]=np.array([lookup[int(i)] for i in ix])
            for name, other in others.items():
                disagree=pred!=other; correct=pred==y; oldcorrect=other==y
                comparisons.append({'cohort':c,'population':population,'comparator':name,
                   'n':len(y),'calibrated_correct':int(correct.sum()),'comparator_correct':int(oldcorrect.sum()),
                   'delta_correct':int(correct.sum()-oldcorrect.sum()),'delta_accuracy_pp':float(100*(correct.mean()-oldcorrect.mean())),
                   'disagreements':int(disagree.sum()),'both_correct':int((correct&oldcorrect).sum()),
                   'only_calibrated_correct':int((correct&~oldcorrect).sum()),'only_comparator_correct':int((~correct&oldcorrect).sum()),
                   'non8_non8_disagreements':int((disagree&(pred!=8)&(other!=8)).sum()),
                   'changed_originally_non8':int((disagree&(baseline!=8)).sum())})
    save('PREDICTIONS.json',predictions); save('SUMMARY.json',summary)
    write_csv('CLASS_OUTCOMES.csv',class_rows); write_csv('COMPARISONS.csv',comparisons)
    save('RUN_STATUS.json',{'status':'success','seconds':time.monotonic()-START,'calibration_fits':2,'model_inference_runs':0,'licensed_solver_runs':0})
    save('OUTPUT_HASHES.json',{p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='OUTPUT_HASHES.json'})
    print(json.dumps({'fits':fits,'summary':summary,'seconds':time.monotonic()-START},indent=2))


if __name__=='__main__':
    def timeout(signum,frame):
        raise TimeoutError('whole analysis exceeded 300 seconds')
    signal.signal(signal.SIGALRM,timeout); signal.alarm(300)
    try:
        run()
    except Exception:
        save('FAILURE.json',{'status':'failed','seconds':time.monotonic()-START,'traceback':traceback.format_exc()})
        raise
