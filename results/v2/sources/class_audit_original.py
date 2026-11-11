import json, math, statistics
from pathlib import Path
R=Path('/workspace/scratch/cbe605b32df0/aprnn_review_37d8165/results')
slots=['P001_J0','P001_J1','P002_J0','P002_J1']
data={s:json.loads((R/'evidence'/s/'independent_heldout_predictions.json').read_text()) for s in slots}
features=json.loads((R/'evidence/FROZEN_PILOT_PRE_REPAIR_FEATURES.json').read_text())['pre_repair']
summary=json.loads((R/'rp001_summary.json').read_text())
def transitions(y,b,a,keep):
    ids=[i for i,t in enumerate(y) if keep(t)]
    return {'n':len(ids),'baseline_correct':sum(b[i]==y[i] for i in ids),'correct':sum(a[i]==y[i] for i in ids),'corrections':sum(b[i]!=y[i] and a[i]==y[i] for i in ids),'breaks':sum(b[i]==y[i] and a[i]!=y[i] for i in ids)}
out={'domains':{},'mathematics':{},'selected_margins':{}}
for domain in ['fog','identity']:
    records={}
    for s in slots:
        d=data[s]['domains'][domain];start=1100 if domain=='identity' else 0
        y,b,a=[d[k][start:] for k in ['labels','baseline','predictions']]
        per={str(c):transitions(y,b,a,lambda t,c=c:t==c) for c in range(10)}
        groups={name:transitions(y,b,a,f) for name,f in [('true8',lambda t:t==8),('non8',lambda t:t!=8),('all',lambda t:True)]}
        records[s]={'per_true_class':per,'groups':groups,'original_predicted8':b.count(8),'repaired_predicted8':a.count(8),'original8_to_non8':sum(x==8 and z!=8 for x,z in zip(b,a)),'original_non8_to8':sum(x!=8 and z==8 for x,z in zip(b,a)),'changes_among_original_non8':sum(x!=8 and x!=z for x,z in zip(b,a)),'corrections_among_original_non8':sum(x!=8 and x!=t and z==t for x,z,t in zip(b,a,y)),'breaks_among_original_non8':sum(x!=8 and x==t and z!=t for x,z,t in zip(b,a,y))}
    pairs={}
    for c in ['P001','P002']:
        d0=data[c+'_J0']['domains'][domain];d1=data[c+'_J1']['domains'][domain];start=1100 if domain=='identity' else 0
        y,a,b=[d0['labels'][start:],d0['predictions'][start:],d1['predictions'][start:]]
        plus=sum(x!=t and z==t for x,z,t in zip(a,b,y));minus=sum(x==t and z!=t for x,z,t in zip(a,b,y));n=len(y);m=plus+minus
        p=min(1.,2*sum(math.comb(m,k) for k in range(min(plus,minus)+1))/2**m) if m else 1.
        d=(plus-minus)/n;se=math.sqrt((m/n-d*d)/n)
        pairs[c]={'disagreement':sum(x!=z for x,z in zip(a,b)),'n':n,'accuracy_difference_pp':100*d,'image_iid_normal95_pp':[100*(d-1.96*se),100*(d+1.96*se)],'mcnemar_exact':p,'true8_delta':records[c+'_J1']['groups']['true8']['correct']-records[c+'_J0']['groups']['true8']['correct'],'non8_delta':records[c+'_J1']['groups']['non8']['correct']-records[c+'_J0']['groups']['non8']['correct'],'disagreement_both_non8':sum(x!=z and x!=8 and z!=8 for x,z in zip(a,b))}
    out['domains'][domain]={'runs':records,'pairs':pairs}
for c in ['P001','P002']:
    worst=min(features[c]['true_class_margins']);L=(.001-worst)/2
    j0=summary['slots'][c+'_J0']['solver']['objective'];j1=summary['slots'][c+'_J1']['solver']['objective'];mx=summary['slots'][c+'_J1']['replay']['max_absolute_editable_delta']
    f=features[c]
    sum_deficits=sum(max(0,.001-m) for m in f['true_class_margins'])
    scalar_lower=max([0]+[.001-m for y,p,m in zip(f['labels'],f['predictions'],f['true_class_margins']) if y!=8 and p==8])
    scalar_upper=min(m-.001 for y,m in zip(f['labels'],f['true_class_margins']) if y==8)
    out['mathematics'][c]={'min_original_margin':worst,'logit_linf_lower_bound':L,'max_bias_gap_allowed':6,'bias_only_box_infeasible':.001-worst>6,'class8_decrease_necessary_interval':[scalar_lower,scalar_upper],'class8_only_selected_constraints_infeasible':scalar_lower>scalar_upper,'sum_positive_deficits':sum_deficits,'J0_objective':j0,'J0_parameter_L1_upper_bound':11110*(j0-L)-sum_deficits,'J1_objective':j1,'J1_L1_if_epigraph_tight':10110*(j1-mx),'J1_L1_upper_bound_from_observed_max_and_objective':10110*(j1-mx)}
for s in slots:
    p=json.loads((R/'evidence'/s/'independent_repair_points.json').read_text());v=[x['margin'] for x in p]
    out['selected_margins'][s]={'median':statistics.median(v),'within_1e6_of_epsilon':sum(abs(x-.001)<=1e-6 for x in v)}
Path('/workspace/scratch/cbe605b32df0/post_review_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'math':out['mathematics'],'pairs':{k:v['pairs'] for k,v in out['domains'].items()},'fog_runs':{s:{k:v for k,v in r.items() if k!='per_true_class'} for s,r in out['domains']['fog']['runs'].items()},'clean_groups':{s:r['groups'] for s,r in out['domains']['identity']['runs'].items()},'margins':out['selected_margins']},indent=2))
