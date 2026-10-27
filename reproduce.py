"""Anonymous artifact entry point. Never changes frozen inputs or outcomes."""
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
import argparse, hashlib, importlib.util, json, sys, zipfile
ROOT=Path(__file__).resolve().parent

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def unpack():
    version=json.loads((ROOT/'VERSION.json').read_text()); target=ROOT/'work/cas'
    target.mkdir(parents=True,exist_ok=True)
    for entry in version['archives']:
        source=ROOT/entry['file']; assert digest(source)==entry['sha256'],source.name
        with zipfile.ZipFile(source) as archive:
            for member in archive.infolist():
                dest=(target/member.filename).resolve()
                assert dest.is_relative_to(target.resolve()) and not dest.is_symlink(),member.filename
                if member.is_dir():dest.mkdir(parents=True,exist_ok=True);continue
                blob=archive.read(member)
                if dest.exists():assert dest.read_bytes()==blob,member.filename
                else:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(blob)
    protocol=json.loads((target/'research/cas_component_comparison_v218/protocol_v218.json').read_text())
    for name,want in protocol['source_sha256'].items():assert digest(target/name)==want,name
    manifest=json.loads((target/'input_manifest_v230.json').read_text())
    assert len(manifest['files'])==30
    allowed={x['case']:x for x in protocol['input_allowlist']}
    assert len(allowed)==30
    for row in manifest['files']:
        assert digest(target/allowed[row['filename']]['input'])==row['sha256'],row['filename']
    return target,protocol

def summary(target):
    data=target/'analysis/data'
    rows=json.loads((data/'audited_cohort_C_v218.json').read_text())['rows']
    assert len(rows)==720 and all(r['audit_passed'] for r in rows)
    grouped=defaultdict(list)
    for row in rows:grouped[row['case'],row['method']].append(Fraction(row['best_fraction']))
    means={key:sum(vals)/len(vals) for key,vals in grouped.items()}
    reference=json.loads((data/'statistical_analysis_v231.json').read_text())
    cases=reference['cases']; report=[]
    for entry in reference['comparisons']:
        m=entry['method']; values=[100*(means[c,m]-means[c,'serial_rows'])/means[c,m] for c in cases]
        value=sum(values)/len(values)
        assert value==Fraction(entry['mean_gain_percent_fraction']),m
        report.append({'method':m,'mean_SR_gain_percent':float(value),'instances':len(values),
                       'wins':sum(x>0 for x in values),'ties':sum(x==0 for x in values),'losses':sum(x<0 for x in values)})
    print(json.dumps({'status':'verified','frozen_cells':720,'optimizer_calls':0,'comparisons':report},indent=2))

def figures(target):
    path=target/'analysis/tools/analyze_statistical_comparisons.py'
    spec=importlib.util.spec_from_file_location('artifact_plots',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    (target/'analysis/figures').mkdir(exist_ok=True)
    mod.draw_figures(json.loads((target/'analysis/data/statistical_analysis_v231.json').read_text()))
    print('Figures written to work/cas/analysis/figures; optimizer calls: 0')

def run_one(target,protocol,args):
    sys.path[:0]=[str(target/'src'),str(target/'scripts')]
    from cas_pfsp_v197.search import run_file as serial
    from cas_pfsp_v194.search import run_file as fast
    from cas_pfsp_v93.search import run_search as raw
    from cas_pfsp_v153.search import run_file as alns
    from cas_pfsp_v178.learning import run_file as ucb
    from cas_pfsp_v218.search import run_file as component
    method,case=args.run_one
    spec=next(x for x in protocol['input_allowlist'] if x['case']==case)
    p=target/spec['input'];b=args.budget;s=args.seed
    handlers={'serial_rows':lambda:serial(p,b,s),'fast_wait':lambda:fast(p,b,s),
              'local_wait_raw':lambda:raw(p,'raw',s,b),'adaptive_cp_alns':lambda:alns(p,b,seed=s),
              'lg_ucb26':lambda:ucb(p,b,s)}
    for variant in ['no_serial','no_pair','lexicographic']:
        handlers[variant]=lambda v=variant:component(p,b,s,ablation=v)
    assert method in handlers,method
    result=handlers[method]()
    import time
    dest=ROOT/'work'/('rerun_'+method+'_'+case+'_'+str(time.time_ns())+'.json')
    with dest.open('x') as stream:json.dump(result,stream,default=str)
    print('New execution saved separately:',dest.name)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true');parser.add_argument('--summary',action='store_true')
    parser.add_argument('--figures',action='store_true');parser.add_argument('--run-one',nargs=2,metavar=('METHOD','CASE'))
    parser.add_argument('--seed',type=int,default=2026102903);parser.add_argument('--budget',type=float,default=5.)
    args=parser.parse_args();target,protocol=unpack()
    if args.summary:summary(target)
    if args.figures:figures(target)
    if args.run_one:run_one(target,protocol,args)
    if not (args.summary or args.figures or args.run_one):print('Verified archives, 142 frozen hashes and exactly 30 exposed benchmark inputs; optimizer calls: 0')
if __name__=='__main__':main()
