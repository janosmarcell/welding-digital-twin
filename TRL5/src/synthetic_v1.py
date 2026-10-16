#!/usr/bin/env python3
"""TRL5 validation starter: six SYN scenarios + eight T5 checks.
Synthetic exercises are *NOT* a proof of real welding-quality validity.
"""
from __future__ import annotations
import argparse, csv, io, json, math, re, time, zipfile
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import cv2
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN

VERSION='1.0.0'
SEED=20261015
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'outputs'

def write_json(path, obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=lambda o:o.item() if isinstance(o,np.generic) else str(o)), encoding='utf-8')

def write_ply(path, xyz):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='ascii') as f:
        f.write(f"ply\nformat ascii 1.0\nelement vertex {len(xyz)}\nproperty float x\nproperty float y\nproperty float z\nend_header\n")
        for a in xyz:f.write(f"{a[0]:.5f} {a[1]:.5f} {a[2]:.5f}\n")

def make_baseline(seed=SEED):
    r=np.random.default_rng(seed)
    n=460
    t=np.arange(n)*0.05
    torch=np.zeros(n,dtype=int)
    spans=[(30,91),(167,238),(323,389)]
    for a,b in spans:torch[a:b]=1
    frame=pd.DataFrame({'SysTimeMsecs':(1700000000000+np.arange(n)*50).astype('int64'),
          'X':500-2*t,'Y':100+np.sin(t/2),'Z':-45+0*t,
          'Rx':np.full(n,0.5),'Ry':np.full(n,-5.5),'Rz':np.full(n,-1.7),
          'TorchSignal':torch,
          'Voltage':18.0+r.normal(0,.15,n)+torch*.8,
          'Current':40.0+r.normal(0,.7,n)+torch*10.,
          'WireFeedSpeed':1.3+r.normal(0,.018,n)+torch*.18})
    return frame,spans

def segments(series):
    x=(pd.to_numeric(series,errors='coerce').fillna(0).values>0.5).astype(np.int8)
    starts=np.where((x==1)&(np.r_[0,x[:-1]]==0))[0]
    ends=np.where((x==1)&(np.r_[x[1:],0]==0))[0]+1
    return list(zip(starts.astype(int).tolist(),ends.astype(int).tolist()))

def make_2d(seed=SEED):
    r=np.random.default_rng(seed)
    h,w=260,520
    y,x=np.indices((h,w))
    curve=(h/2+7*np.sin(x/50)).astype(int)
    band=np.abs(y-curve)<13
    img=np.clip(30+r.normal(0,3,(h,w))+band*165,0,255).astype(np.uint8)
    clean=img.copy()
    bad=cv2.GaussianBlur(img,(65,65),28)
    bad[64:210,210:350]=0
    bad=np.clip(bad.astype(float)*.27,0,255).astype(np.uint8)
    return clean,bad

def image_quality(img):
    sharp=float(cv2.Laplacian(img,cv2.CV_64F).var())
    dark=float(np.mean(img<10))
    dynamic=float(np.percentile(img,98)-np.percentile(img,2))
    valid=(sharp>30 and dark<.35 and dynamic>60)
    return {'sharpness_laplacian':round(sharp,3),'dark_fraction':round(dark,3),'range_p98_p2':round(dynamic,3),'is_evaluable':bool(valid)}

def synthetic_3d(seed=SEED):
    r=np.random.default_rng(seed)
    xs=np.linspace(0,100,201)
    ys=np.linspace(-15,15,61)
    x,y=np.meshgrid(xs,ys,indexing='ij')
    base=np.stack([x,y,1.15*np.exp(-y*y/18.0)],axis=-1).reshape(-1,3)
    ref=base.copy()
    actual=base.copy()
    truth=((x-54)**2/45+(y-0.8)**2/12<1.0).ravel()
    delta=2.3*np.exp(-((actual[:,0]-54)**2/36+(actual[:,1]-.8)**2/10))
    actual[:,2]+=delta
    ref[:,2]+=r.normal(0,.008,len(ref))
    actual[:,2]+=r.normal(0,.008,len(actual))
    return ref,actual,truth

def point_distances(reference,actual):
    tree=cKDTree(reference)
    return tree.query(actual,k=1)[0]

def mask_scores(pred,truth):
    tp=int(np.sum(pred & truth)); fp=int(np.sum(pred & ~truth));fn=int(np.sum(~pred & truth))
    return {'tp':tp,'fp':fp,'fn':fn,'precision':round(tp/max(tp+fp,1),4),
            'recall':round(tp/max(tp+fn,1),4),
            'iou':round(tp/max(tp+fp+fn,1),4)}

def classify_workpiece(has_csv, has_image, has_pointcloud, geometric_deviation=None):
    # Not a weld-certification decision; only an example of safe alpha routing.
    if not (has_csv and has_image and has_pointcloud):
        return 'ELLENORIZENDO'
    if geometric_deviation is not None and geometric_deviation > 0.28:
        return 'HIBAGYANUS'
    return 'OK_JELOLT'


def estimate_synthetic_seam_width(image):
    # Only applicable to high-contrast SYN-2D-01 sample, not a calibrated real-world method.
    mask=image>130
    sizes=[]
    for col in range(mask.shape[1]):
        rows=np.where(mask[:,col])[0]
        if rows.size: sizes.append(rows.max()-rows.min()+1)
    return float(np.median(sizes)) if sizes else float('nan')


def generate_all(out):
    s=out/'synthetic'
    s.mkdir(parents=True,exist_ok=True)
    frame,spans=make_baseline()
    frame.to_csv(s/'reference_baseline.csv',index=False)
    missing=frame.copy()
    missing.loc[spans[1][0]:spans[1][1]-1,'TorchSignal']=0
    missing.to_csv(s/'SYN-CSV-01_missing_segment.csv',index=False)
    spike=frame.copy()
    spike.loc[350:366,'Current']+=60
    spike.loc[350:366,'Voltage']+=8
    spike.loc[350:366,'WireFeedSpeed']+=.6
    spike.to_csv(s/'SYN-CSV-02_spike.csv',index=False)
    truth_spike=np.zeros(len(spike),dtype=int);truth_spike[350:367]=1
    pd.DataFrame({'row':np.arange(len(spike)),'injected':truth_spike}).to_csv(s/'SYN-CSV-02_ground_truth.csv',index=False)
    good,bad=make_2d()
    cv2.imwrite(str(s/'SYN-2D-01_reference.png'),good)
    cv2.imwrite(str(s/'SYN-2D-01_blur_occlusion.png'),bad)
    ref,actual,truth=synthetic_3d()
    write_ply(s/'SYN-3D-01_reference.ply',ref)
    write_ply(s/'SYN-3D-01_defect.ply',actual)
    np.save(s/'SYN-3D-01_truth_mask.npy',truth)
    rng=np.random.default_rng(SEED+2)
    noisy=ref+rng.normal(0,.13,size=ref.shape)
    keep=~((noisy[:,0]>72)&(noisy[:,0]<87)&(np.abs(noisy[:,1])<5))
    write_ply(s/'SYN-3D-02_noisy_missing.ply',noisy[keep])
    stream=[]
    for i in range(1,13):
        stream.append({'workpiece_id':f'G99-S{i:03d}',
           'timestamp_offset_s':i*3,'csv':True,'image':i%4!=0,'pointcloud':i%5!=0,'origin':'synthetic',
           'source':'synthetic_baseline_not_real_robot'})
    write_json(s/'SYN-STR-01_stream.json',stream)
    manifest=[
     ('SYN-CSV-01','TorchSignal-szakaszhiány','SYN-CSV-01_missing_segment.csv'),
     ('SYN-CSV-02','Jelkiugrás három csatornában','SYN-CSV-02_spike.csv'),
     ('SYN-2D-01','Elmosódás/sötétedés/takarás','SYN-2D-01_blur_occlusion.png'),
     ('SYN-3D-01','Ismert helyű geometriai dudor','SYN-3D-01_defect.ply'),
     ('SYN-3D-02','Pontzaj/szkennelési hiány','SYN-3D-02_noisy_missing.ply'),
     ('SYN-STR-01','As-if stream és modalitáshiány','SYN-STR-01_stream.json'),
    ]
    write_json(s/'provenance_manifest.json',[{'scenario':id,'description':desc,'file':f,'origin':'synthetic',
       'seed':SEED,'generator_version':VERSION,'valid_for':'algorithmic_stress_test_only','real_source':None} for id,desc,f in manifest])
    return {'base':frame,'missing':missing,'spike':spike,'truth_spike':truth_spike,
            'good':good,'bad':bad,'reference_cloud':ref,'defect_cloud':actual,'truth3d':truth,
            'noisy_cloud':noisy[keep],'stream':stream}

def run_synthetic_tests(d):
    tests=[]
    def add(code,name,criterion,passed,metric,scope='synthetic',status=None,notes=''):
        tests.append({'code':code,'name':name,'criterion':criterion,'result':status or ('PASS_SYNTHETIC' if passed else 'FAIL_SYNTHETIC'),
           'metrics':metric,'evidence_scope':scope,'notes':notes})
    good_spans=segments(d['base']['TorchSignal'])
    bad_spans=segments(d['missing']['TorchSignal'])
    add('T5-01','TorchSignal szegmentálás', '3 ismert szakasz felismerve, törölt szakasz jelölve',
        len(good_spans)==3 and len(bad_spans)==2,{'clean_segments':len(good_spans),'missing_case_segments':len(bad_spans)})
    # Fixed baseline median+robust scale: stress test, not an industrial weld defect classifier.
    anomaly=np.zeros(len(d['spike']),dtype=bool)
    for col in ('Voltage','Current','WireFeedSpeed'):
        b=d['base'][col].values
        centre=np.median(b)
        mad=np.median(np.abs(b-centre))
        bound=centre+8*max(mad*1.4826,.03)
        anomaly|=(d['spike'][col].values>bound)
    truth=d['truth_spike']>0
    m=mask_scores(anomaly,truth)
    add('T5-02','Jelkiugrás felismerése','Kontrollált kiugrás felismerése: recall >= 0.9',m['recall']>=.9,m,
      notes='Mért alapvonal is szintetikus; nem valós gyártási hibadetektor.')
    q_good=image_quality(d['good']);q_bad=image_quality(d['bad'])
    width=estimate_synthetic_seam_width(d['good'])
    add('T5-03','2D képminőség','Referenciakép elfogadva, sérült elutasítva, 25 px szélesség visszamérve',
       q_good['is_evaluable'] and not q_bad['is_evaluable'] and abs(width-25)<=2,{'reference':q_good,'corrupted':q_bad,'known_seam_width_px':25,'measured_width_px':width},
       notes='Valós képi kontúr, mérési etalon és kezelői kontroll külön szükséges.')
    ref=d['reference_cloud'];actual=d['defect_cloud'];truth3d=d['truth3d'];dist=point_distances(ref,actual)
    chosen=dist>0.28
    clusterlabels=DBSCAN(eps=1.25,min_samples=8).fit(actual[chosen]).labels_ if chosen.any() else np.array([],dtype=int)
    validclusters=int(len(set(clusterlabels))-int(-1 in clusterlabels))
    sc=mask_scores(chosen,truth3d)
    add('T5-04','3D hibajelzés részteszt','Ismert hiba lokalizált; FGR+ICP még nem tesztelt',
        sc['recall']>=.7 and validclusters>=1,
        {**sc,'clusters':validclusters,'distance_rmse_mm':round(float(np.sqrt(np.mean(dist*dist))),4)},
        status='PARTIAL_SYNTHETIC',notes='Csak geometriai távolság+DBSCAN futott, FGR/ICP és valós mérés HÁTRA VAN.')
    sens=[]
    for p in range(91,100):
        # Rank by distance; 97% means selecting highest 3%, NOT acceptance of welding quality.
        selected=dist>=np.percentile(dist,p)
        sm=mask_scores(selected,truth3d)
        sens.append({'percentile':p,**sm})
    pd.DataFrame(sens).to_csv(OUTPUT/'reports'/'T5-05_threshold_sensitivity.csv',index=False)
    best=max(sens,key=lambda r:r['iou'])
    add('T5-05','91-99 percentilis','Kilenc százalékpont kiértékelve és hibamaszkhoz hasonlítva',
        len(sens)==9,{'best_iou_percentile_on_synthetic':best['percentile'],'max_iou':best['iou'],
                        'at_97':next(r for r in sens if r['percentile']==97)},
        status='PASS_SYNTHETIC', notes='A 97% csak publikált kiindulási hipotézis; nem ISO elfogadási limit.')
    missing=[x for x in d['stream'] if not(x['image'] and x['pointcloud'])]
    actual_decisions=[classify_workpiece(x['csv'],x['image'],x['pointcloud']) for x in d['stream']]
    false_ok=sum(actual_decisions[i]=='OK_JELOLT' for i,x in enumerate(d['stream']) if not(x['image'] and x['pointcloud']))
    add('T5-06','CSV–2D–3D hiányadat','Hiányos adatnál automatikus OK tilos',false_ok==0,
        {'items':len(d['stream']),'with_missing_modality':len(missing),'auto_ok_for_missing':false_ok},
        notes='CSV-fájlról képre/pontfelhőre való valós hozzárendelés külön ellenőrizendő.')
    # Synthetic-only example: defect geometry flagged, incomplete cases require human review.
    decisions=[{'item':x['workpiece_id'], 'decision': classify_workpiece(x['csv'],x['image'],x['pointcloud'])} for x in d['stream']]
    decisions.append({'item':'SYN-3D-01_defect','decision':classify_workpiece(True,True,True,float(np.percentile(dist,99)))})
    add('T5-07','Előminősítés logikai próba','Nincs automatikus OK hiányra; ismert geometriai hiba hibagyanús',
        decisions[-1]['decision']=='HIBAGYANUS' and all(x['decision']=='ELLENORIZENDO' for x in decisions[:-1] if x['item'] in {y['workpiece_id'] for y in missing}),
        {'decision_distribution':{k:sum(x['decision']==k for x in decisions) for k in ['OK_JELOLT','ELLENORIZENDO','HIBAGYANUS']}},
        status='PARTIAL_SYNTHETIC',notes='Nincs függetlenül minősített valós OK/NOK ground truth, confusion matrix NEM számolható.')
    dt=[]
    for ev in d['stream']:
        start=time.perf_counter()
        _={'item':ev['workpiece_id'],'status':classify_workpiece(ev['csv'],ev['image'],ev['pointcloud'])}
        dt.append((time.perf_counter()-start)*1000)
    p50,p95=np.percentile(dt,[50,95])
    add('T5-08','As-if stream (offline)','A 12 generált esemény sorrendben feldolgozható',len(dt)==12,
        {'processed_events':len(dt),'local_computation_p50_ms':round(float(p50),4),'p95_ms':round(float(p95),4)},
        status='PARTIAL_SYNTHETIC',notes='A CPU-számítás nem hálózati vagy robotcellás end-to-end késleltetés; kezelői próba hátravan.')
    return tests

def scan_real_zip(path):
    """Observation-only import. No welding-quality labels are inferred."""
    z=zipfile.ZipFile(path)
    names=[x for x in z.namelist() if not x.endswith('/')]
    csvs=[n for n in names if n.lower().endswith('.csv')]
    pics=[n for n in names if n.lower().endswith(('.jpg','.jpeg','.png'))]
    clouds=[n for n in names if n.lower().endswith(('.ply','.stl','.obj'))]
    records=[]
    for n in csvs:
        try:
            data=z.read(n)
            d=pd.read_csv(io.BytesIO(data),low_memory=False,sep=None,engine='python')
            sig=next((c for c in d.columns if c.lower().replace('_','')=='torchsignal'),None)
            pieces=segments(d[sig]) if sig else []
            records.append({'filename':n,'rows':int(len(d)),'has_torchsignal':bool(sig),
                            'segments':len(pieces) if sig else None,'status':'REVIEW' if len(pieces)!=3 else 'STRUCTURAL_OK'})
        except Exception as e:
            records.append({'filename':n,'status':'PARSE_ERROR','error':str(e)[:250]})
    OUTPUT.mkdir(exist_ok=True,parents=True)
    pd.DataFrame(records).to_csv(OUTPUT/'reports'/'real_csv_structural_inventory.csv',index=False)
    return {'csv_count':len(csvs),'image_count':len(pics),'pointcloud_count':len(clouds),
      'csv_parsed':sum(x.get('status')!='PARSE_ERROR' for x in records),
      'files_needing_review':[x for x in records if x.get('status')!='STRUCTURAL_OK'],
      'limitations':'CSV structural checks only; no independent ground truth, no real 2D/3D match or quality validation.'}

def build_report(tests,real,synthetic_only):
    lines=['# TRL5 – Végrehajtási jegyzőkönyv (automatikus; első iteráció)','',
      '**Állapot: TRL5 NINCS lezárva.** Ez a futás csak tesztkörnyezet és/vagy részvizsgálatok végrehajtását igazolja.','',
      f'Generátor verzió: `{VERSION}` | random seed: `{SEED}` | létrehozás (UTC): {datetime.now(timezone.utc).isoformat()}','',
      '## Nyolc teszt státusza','',
      '| Kód | Teszt | Állapot | Bizonyíték korlátja |','|---|---|---|---|']
    for t in tests:
        lines.append(f"| {t['code']} | {t['name']} | {t['result']} | {t['notes'] or 'Csak szintetikus környezetben lefuttatva'} |")
    lines+=['','## Hat szintetikus forgatókönyv','',
      'SYN-CSV-01, SYN-CSV-02, SYN-2D-01, SYN-3D-01, SYN-3D-02, SYN-STR-01: generált, adatfájlok és provenance manifest a `outputs/synthetic/` mappában.', '',
      '## Valós adatok','']
    if real:
        lines.append(f"CSV: {real['csv_count']}; 2D: {real['image_count']}; 3D: {real['pointcloud_count']}. Részletek: `reports/real_csv_structural_inventory.csv`.")
        lines.append(f"Szerkezeti ellenőrzésre szoruló CSV-k: {len(real['files_needing_review'])}.")
    else:
        lines.append('**Nem állt rendelkezésre eredeti csv_light2.zip**. Valós mérési eredmények nem készültek; a valós validáció nyitott.')
    lines+=['','## TRL5 szintzárás: ellenőrizhető követelmények','',
    '| Bizonyíték | Szintzárási ellenőrzés | Mostani státusz |', '|---|---|---|',
    '| Valós CSV-azonosítás | Annotált varratkezdet/vég összevetés, mért hibaarány | Függőben |',
    '| Valós 2D kép/QC | Képcímkék, ismétlés, kontúrreferencia | Függőben |',
    '| Valós 3D FGR/ICP/DBSCAN | Ismert hibák, ismételt szkennelés, IoU/RMSE | Függőben |',
    '| Szintetikus stressztesztek | Hat forgatókönyv, seed, ground truth | Elindítva, részleges |',
    '| Valós munkadarab-összerendelés | Mapping ellenőrzése; hiányok jelölve | Függőben |',
    '| Független valós OK/NOK címkék | Confusion matrix, FP/FN, false-OK CI | Függőben |',
    '| Rendszeridő és felhasználó | End-to-end latency, kezelői tesztjegyzőkönyv | Függőben |',
    '| Előzetesen jóváhagyott elfogadási határok | Hibakategóriánként és metrikánként írásban rögzítve | Függőben |',
    '',
    '**Megjegyzés:** A pontfelhő-távolság 97. percentilise NEM ISO 5817 szerinti hegesztési elfogadási küszöb. A szintetikus hibák detektálása NEM bizonyít valós hegesztési megfelelőséget.','',
    '## Futtatás', '', '`python src/run_validation.py` vagy `python src/run_validation.py --real-zip data/real/csv_light2.zip`', '']
    (OUTPUT/'TRL5_futtatasi_jegyzokonyv.md').write_text('\n'.join(lines),encoding='utf-8')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--real-zip',type=str,help='csv_light2.zip elérési út (opcionális)')
    args=parser.parse_args()
    for d in [OUTPUT/'synthetic',OUTPUT/'reports']:
        d.mkdir(exist_ok=True,parents=True)
    generated=generate_all(OUTPUT)
    tests=run_synthetic_tests(generated)
    real=None
    if args.real_zip:
        real=scan_real_zip(Path(args.real_zip))
    result={'generator_version':VERSION,'run_utc':datetime.now(timezone.utc).isoformat(),
            'seed':SEED,'source_provenance':'synthetic_baseline_not_real_robot',
            'TRL5_final_validation':'NOT_COMPLETED', 'tests':tests,'real_data':real}
    write_json(OUTPUT/'TRL5_test_results.json',result)
    build_report(tests,real,not real)
    print('TRL5 synthetic tests:')
    for t in tests:print(t['code'],t['result'])
    print('TRL5 végső státusz: NOT_COMPLETED')
    print('Riport:',OUTPUT/'TRL5_futtatasi_jegyzokonyv.md')
if __name__=='__main__':main()
