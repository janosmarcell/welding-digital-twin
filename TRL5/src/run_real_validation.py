#!/usr/bin/env python3
"""TRL5 v2: real dataset structural evaluation + real-anchored synthetic stress tests.
No test grants autonomous weld-conformity qualification or closes TRL5.
"""
from __future__ import annotations
import argparse, io, json, re, hashlib, sys, time, zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import cv2
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN
import synthetic_v1 as v1

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'; REPORT=OUT/'reports'; SYN=OUT/'synthetic_real_anchored'
REQ=['SysTimeMsecs','X','Y','Z','Rx','Ry','Rz','TorchSignal','Voltage','Current','WireFeedSpeed']

def jdump(path,x):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=lambda v: v.item() if isinstance(v,np.generic) else str(v)),encoding='utf8')

def segs(arr):
 return v1.segments(pd.Series(arr))

def read_vertex_sample(z, name, cap=12000):
 """Only binary little-endian PLY vertex XYZ. No faces are interpreted.
 Return a deterministic uniformly row-sampled array; if format not supported, report unsupported.
 """
 with z.open(name) as f:
  head=b''
  while not head.endswith(b'end_header\n'):
   line=f.readline()
   if not line or len(head)>16000:raise ValueError('Invalid PLY header')
   head+=line
  header=head.decode('latin-1')
  if 'format binary_little_endian' not in header: raise ValueError('Unsupported PLY format')
  number=int(re.search(r'element vertex\s+(\d+)',header).group(1))
  props=[]; section=None
  for ln in header.splitlines():
   if ln.startswith('element '):section=ln.split()[1]
   if section=='vertex' and ln.startswith('property '):
    spl=ln.split()
    if len(spl)==3: props.append((spl[2],spl[1]))
  types={'float':'<f4','float32':'<f4','double':'<f8','float64':'<f8','uchar':'u1','uint8':'u1','int':'<i4','int32':'<i4','uint':'<u4','short':'<i2','ushort':'<u2'}
  if any(t not in types for _,t in props):raise ValueError('PLY vertex property type unsupported')
  dtype=np.dtype([(k,types[t]) for k,t in props]); raw=f.read(number*dtype.itemsize)
  if len(raw)!=number*dtype.itemsize:raise ValueError('Incomplete vertex data')
  v=np.frombuffer(raw,dtype=dtype,count=number)
  idx=np.linspace(0,len(v)-1,min(cap,len(v))).astype(int)
  xyz=np.column_stack([v['x'][idx],v['y'][idx],v['z'][idx]]).astype(np.float64)
  xyz=xyz[np.isfinite(xyz).all(axis=1)]
  if len(xyz)<20:raise ValueError('Insufficient valid vertices')
  return xyz,number,('revopoint' if 'revopoint' in header.lower() else 'vcglib' if 'vcglib' in header.lower() else 'unknown')

def analyze(zip_path):
 REPORT.mkdir(parents=True,exist_ok=True); SYN.mkdir(parents=True,exist_ok=True)
 h=hashlib.sha256()
 with open(zip_path,'rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 archive_hash=h.hexdigest()
 with zipfile.ZipFile(zip_path) as z:
  entries=[n for n in z.namelist() if not n.endswith('/')]
  paths={e.rsplit('.',1)[0]:[] for e in entries}
  exts=Counter(e.rsplit('.',1)[-1].lower() for e in entries)
  names={'csv':{e.rsplit('.',1)[0]:e for e in entries if e.endswith('.csv')},
   'jpg':{e.rsplit('.',1)[0]:e for e in entries if e.lower().endswith(('.jpg','.jpeg'))},
   'ply':{e.rsplit('.',1)[0]:e for e in entries if e.lower().endswith('.ply')}}
  rows=[]; segment_rows=[]; baseline_data={}
  for stem,n in sorted(names['csv'].items()):
   df=pd.read_csv(io.BytesIO(z.read(n)),low_memory=False)
   absent=[c for c in REQ if c not in df.columns]
   group=n.split('/')[-2]
   ts=pd.to_numeric(df['SysTimeMsecs'],errors='coerce').to_numpy() if 'SysTimeMsecs' in df else np.array([])
   tsvalid=(np.isfinite(ts).all() and np.all(np.diff(ts)>=0)) if len(ts) else False
   tdup=int(np.count_nonzero(np.diff(ts)==0)) if len(ts)>1 else 0
   signal=pd.to_numeric(df['TorchSignal'],errors='coerce').fillna(0).to_numpy() if 'TorchSignal' in df else np.array([])
   spans=segs(signal) if len(signal) else []
   if group not in baseline_data and len(spans)==3:baseline_data[group]=(n,df)
   for i,(a,b) in enumerate(spans,1):
    sel=df.iloc[a:b]
    segment_rows.append({'id':stem.rsplit('/',1)[-1],'speed_group':group,'seam':i,'start_row_zero_based':a,
      'stop_row_exclusive':b,'rows':b-a,'start_ms':float(ts[a]) if len(ts) else None,
      'end_ms':float(ts[b-1]) if len(ts) else None,
      'voltage_avg':float(sel['Voltage'].mean()) if 'Voltage' in df else None,
      'current_avg':float(sel['Current'].mean()) if 'Current' in df else None,
      'wire_feed_avg':float(sel['WireFeedSpeed'].mean()) if 'WireFeedSpeed' in df else None})
   row={'id':stem.rsplit('/',1)[-1], 'speed_group':group,'csv_zip_path':n,'rows':len(df),'columns':len(df.columns),
    'missing_required_columns':','.join(absent),'torch_segments':len(spans),
    'active_samples':int((signal>0.5).sum()) if len(signal) else None,
    'time_nondecreasing':bool(tsvalid),'duplicate_timestamp_steps':tdup,
    'duplicate_timestamp_fraction':round(tdup/max(len(ts)-1,1),4),'has_jpg':stem in names['jpg'], 'has_ply':stem in names['ply'],
    'mapping_status':'MATCHED_ALL_THREE' if stem in names['jpg'] and stem in names['ply'] else 'PARTIAL',
    'structure_status':'REVIEW' if len(spans)!=3 or absent or not tsvalid else 'STRUCTURE_OK'}
   rows.append(row)
  tab=pd.DataFrame(rows)
  tab.to_csv(REPORT/'real_csv_inventory.csv',index=False,encoding='utf-8-sig')
  pd.DataFrame(segment_rows).to_csv(REPORT/'real_seam_features.csv',index=False,encoding='utf-8-sig')
  tab[['id','speed_group','csv_zip_path','has_jpg','has_ply','mapping_status']].to_csv(REPORT/'real_modalities_mapping.csv',index=False,encoding='utf-8-sig')

  # Image descriptive QC; thresholds from synthetic_v1 are not calibrated on real workpieces.
  ims=[]; firstimg=None
  for stem,n in sorted(names['jpg'].items()):
   img=cv2.imdecode(np.frombuffer(z.read(n),np.uint8),cv2.IMREAD_GRAYSCALE)
   if img is None:ims.append({'id':stem.split('/')[-1],'file':n,'decoded':False});continue
   scaled=cv2.resize(img,(min(1200,img.shape[1]),max(1,int(img.shape[0]*min(1200,img.shape[1])/img.shape[1]))))
   q=v1.image_quality(scaled)
   ims.append({'id':stem.split('/')[-1],'file':n,'decoded':True,'width_px':img.shape[1],'height_px':img.shape[0],
     **q,'qc_status':'EXPLORATORY_UNCALIBRATED'})
   if firstimg is None:firstimg=(stem,n,scaled)
  pd.DataFrame(ims).to_csv(REPORT/'real_image_qc_exploratory.csv',index=False,encoding='utf-8-sig')

  # Real PLY metadata and geometric sanity (does NOT assert a match to a CAD reference).
  plys=[]; firstcloud=None
  for stem,n in sorted(names['ply'].items()):
   try:
    pts,count,source=read_vertex_sample(z,n,10000)
    rec={'id':stem.rsplit('/',1)[-1],'file':n,'parsed':True,'source_tag':source,'vertex_count':count,
     'sample_count':len(pts),'x_extent':round(float(np.ptp(pts[:,0])),4),
     'y_extent':round(float(np.ptp(pts[:,1])),4),'z_extent':round(float(np.ptp(pts[:,2])),4)}
    if firstcloud is None and count>20000: firstcloud=(stem,n,pts)
   except Exception as e:rec={'id':stem.rsplit('/',1)[-1],'file':n,'parsed':False,'error':repr(e)[:240]}
   plys.append(rec)
  pd.DataFrame(plys).to_csv(REPORT/'real_ply_geometry_inventory.csv',index=False,encoding='utf-8-sig')

  # Provenance-preserving real-anchored stress samples.
  stress={}
  base_name,df=baseline_data['g01_30']
  actual_spans=segs(df['TorchSignal'])
  missing=df.copy(); a,b=actual_spans[1];missing.loc[a:b-1,'TorchSignal']=0
  missing.to_csv(SYN/'SYN-REAL-CSV-01_missing_segment.csv',index=False)
  stress['missing_span']={'source_csv':base_name,'before':len(actual_spans),'after':len(segs(missing['TorchSignal']))}
  spike=df.copy(); sa,sb=actual_spans[-1];s=sa+max(0,(sb-sa)//4);e=min(sb,s+max(8,(sb-sa)//10))
  for c,k in [('Voltage',8.0),('Current',65.0),('WireFeedSpeed',1.0)]:spike.loc[s:e-1,c]+=k
  spike.to_csv(SYN/'SYN-REAL-CSV-02_spikes.csv',index=False)
  pd.DataFrame({'row':np.arange(len(df)),'injected':[(int(s<=i<e)) for i in range(len(df))]}).to_csv(SYN/'SYN-REAL-CSV-02_truth.csv',index=False)
  # Proof-of-function detector based on a sample-specific baseline from an unmodified real record.
  # This is NOT out-of-sample industrial classifier evaluation.
  truth=np.zeros(len(df),dtype=bool);truth[s:e]=True
  active=(df['TorchSignal'].to_numpy(float)>0.5)
  predicted=np.zeros(len(df),dtype=bool)
  thresholds={}
  for c,margin in [('Voltage',3.0),('Current',10.0),('WireFeedSpeed',0.40)]:
   threshold=float(np.quantile(df.loc[active,c],.999)+margin)
   predicted|=spike[c].to_numpy(float)>threshold
   thresholds[c]=round(threshold,3)
  stats=v1.mask_scores(predicted,truth)
  stats['original_false_positive_rows']=int(np.sum((df['Voltage'].to_numpy()>thresholds['Voltage']) |
     (df['Current'].to_numpy()>thresholds['Current']) |
     (df['WireFeedSpeed'].to_numpy()>thresholds['WireFeedSpeed'])))
  stress['spike_test']={**stats,'evaluation':'single-source real-anchored baseline; injected outliers only, NOT independent real anomalies',
    'thresholds_from_single_reference_csv':thresholds,'injection_row_start':s,'injection_row_end_exclusive':e}

  if firstimg:
   im_stem,im_src,img=firstimg
   bad=cv2.GaussianBlur(img,(31,31),9)
   hh,ww=bad.shape;bad[hh//3:2*hh//3,ww//3:2*ww//3]=0
   cv2.imwrite(str(SYN/'SYN-REAL-2D-01_original_downsampled.png'),img)
   cv2.imwrite(str(SYN/'SYN-REAL-2D-01_corrupted.png'),bad)
   good_q=v1.image_quality(img);bad_q=v1.image_quality(bad)
   stress['image']={'source_image':im_src,'before':good_q,'after':bad_q,
     'degradation_detected_by_sharpness':bad_q['sharpness_laplacian']<good_q['sharpness_laplacian'],
     'known_synthetic_occlusion_detected':float(np.mean(bad==0))>0.05 and float(np.mean(img==0))<=0.05,
     'synthetic_v1_qc_is_evaluable_warning':bad_q['is_evaluable'],
     'qc_decision_requires_human_review':True}

  if firstcloud:
   cloud_stem,cloud_src,ref=firstcloud
   rng=np.random.default_rng(20261015)
   xy=ref[:,:2]
   # Spatially concentrated synthetic region (not asserted to coincide with physical seam).
   focal=xy[len(xy)//2];xy_rad=np.sum((xy-focal)**2,axis=1)
   mask=xy_rad<=np.quantile(xy_rad,0.02)
   tree=cKDTree(ref)
   nn=tree.query(ref,k=2)[0][:,1]
   scale=float(np.median(nn[nn>0])) if (nn>0).any() else .2
   shifted=ref.copy();shifted[mask,2]+=max(3.0,scale*15)
   shift_dist=tree.query(shifted,k=1)[0]
   pp=[]
   for p in range(91,100):
    topk=max(1,int(np.ceil(len(shift_dist)*(100-p)/100)))
    predicted=np.zeros(len(shift_dist),dtype=bool)
    predicted[np.argsort(-shift_dist,kind='stable')[:topk]]=True
    pp.append({'percentile':p,**v1.mask_scores(predicted,mask)})
   best=max(pp,key=lambda x:x['iou']);pd.DataFrame(pp).to_csv(REPORT/'real_anchored_ply_threshold_sweep.csv',index=False)
   v1.write_ply(SYN/'SYN-REAL-3D-01_reference_sample.ply',ref)
   v1.write_ply(SYN/'SYN-REAL-3D-01_known_displacement.ply',shifted)
   np.save(SYN/'SYN-REAL-3D-01_truth_mask.npy',mask)
   # Registration not needed here because points share frame. Real unknown transforms still require FGR+ICP.
   stress['geometry']={'source_ply':cloud_src,'vertices_sampled':len(ref),'injected_points':int(mask.sum()),
     'z_displacement':max(3.0,scale*15),'best_percentile_exploratory':best['percentile'],
     'best_iou_exploratory':best['iou'],'at97':next(x for x in pp if x['percentile']==97),
     'limitations':'known coordinate frame and synthetic shifted points; FGR/ICP NOT tested, surface ground truth absent'}

 count_by_group=tab.groupby('speed_group')[['has_jpg','has_ply']].sum().to_dict(orient='index')
 three=int((tab.has_jpg&tab.has_ply).sum())
 summary={'run_utc':datetime.now(timezone.utc).isoformat(),'source_file':zip_path.name,'sha256':archive_hash,
  'csv_count':len(names['csv']),'jpg_count':len(names['jpg']),'ply_count':len(names['ply']),
  'by_group':count_by_group,'three_modality_pairs':three,
  'structural_ok_csv':int((tab.structure_status=='STRUCTURE_OK').sum()),
  'csv_needing_review':tab.loc[tab.structure_status!='STRUCTURE_OK','id'].tolist(),
  'csv_with_timestamp_duplicates':int((tab.duplicate_timestamp_steps>0).sum()),
  'all_timestamps_nondecreasing':bool(tab.time_nondecreasing.all()),
  'csvs_with_images':int(tab.has_jpg.sum()),'csvs_with_ply':int(tab.has_ply.sum()),
  'unmatched_images':sorted(set(names['jpg'])-set(names['csv'])),
  'unmatched_ply':sorted(set(names['ply'])-set(names['csv'])),
  'ply_parse_success':sum(1 for x in plys if x.get('parsed')),
  'image_decode_success':sum(1 for x in ims if x.get('decoded')),
  'real_anchored_synthetic':stress}
 jdump(REPORT/'real_data_results.json',summary)
 provenance={'source_zip_sha256':archive_hash,'created_utc':summary['run_utc'],'generator':'trl5_v2_real_anchored',
   'origin_for_generated_files':'synthetic_derived_from_real','real_data_never_claimed_as_ground_truth':True,
   'data_sources':{'csv':base_name,'jpg':firstimg[1] if firstimg else None,'ply':firstcloud[1] if firstcloud else None},
   'reproducibility_seed':20261015,'file_groups':['SYN-REAL-CSV-01','SYN-REAL-CSV-02','SYN-REAL-2D-01','SYN-REAL-3D-01']}
 jdump(SYN/'provenance_manifest.json',provenance)
 return summary

def main():
 p=argparse.ArgumentParser();p.add_argument('--real-zip',required=True,type=Path);args=p.parse_args()
 t0=time.perf_counter();r=analyze(args.real_zip)
 # Re-run original six synthetic scenarios, but keep their outputs in this copy.
 v1.OUTPUT=OUT
 d=v1.generate_all(OUT)
 old=v1.run_synthetic_tests(d)
 tests=[{'code':x['code'],'name':x['name'],'synthetic_v1_result':x['result']} for x in old]
 real_status={
  'T5-01':'REAL_STRUCTURAL_CHECK_DONE_ANNOTATIONS_PENDING',
  'T5-02':'REAL_ANCHORED_SYNTHETIC_INJECTION_DONE_REAL_LABELS_PENDING',
  'T5-03':'REAL_IMAGE_QC_EXPLORATORY_MANUAL_REFERENCES_PENDING',
  'T5-04':'REAL_PLY_PARSE_AND_SYNTHETIC_GEOMETRY_DONE_FGR_ICP_PENDING',
  'T5-05':'REAL_ANCHORED_SYNTHETIC_THRESHOLD_SWEEP_DONE_INDEPENDENT_TEST_PENDING',
  'T5-06':'REAL_FILENAME_MAPPING_DONE_IDENTITY_VERIFICATION_PENDING',
  'T5-07':'OPEN_INDEPENDENT_WELD_QUALITY_LABELS_REQUIRED',
  'T5-08':'OPEN_ROBOTCELL_REALTIME_TEST_REQUIRED'}
 for t in tests:t['real_data_status']=real_status[t['code']]
 jdump(OUT/'TRL5_v2_test_results.json',{'TRL5_FINAL_STATUS':'NOT_COMPLETED','real_dataset':r,'tests':tests,
   'warning':'No welding quality status can be inferred from file availability or source-specific synthetic injection tests.'})
 lines=['# TRL5 – valós adatos validációs jegyzőkönyv (v2)','',
  f"Futtatás: {r['run_utc']}",f"Bemeneti ZIP SHA-256: `{r['sha256']}`",'',
  '**Szintzárás: NEM TELJESÍTETT.** A valós adatok strukturális ellenőrzése és valós adatokból generált szintetikus stressztesztek készültek, nem hegesztési megfelelőségi minősítés.','',
  '## Tényadatok',
  f"- CSV: **{r['csv_count']}**; JPG: **{r['jpg_count']}**; PLY: **{r['ply_count']}**.",
  f"- Három várható aktív szakasz: **{r['structural_ok_csv']}/{r['csv_count']} CSV**; kivétel: {', '.join(r['csv_needing_review']) or 'nincs'}.",
  f"- Fájlnév szerinti párosítás: **{r['csvs_with_images']} CSV+JPG**, **{r['csvs_with_ply']} CSV+PLY**, **{r['three_modality_pairs']} mindhárom**; a közös fájlnév technikai egyezés, nem kézzel hitelesített munkadarab-azonosítás.",
  f"- Időbélyeg-ismeret: {r['csv_with_timestamp_duplicates']} CSV-ben legalább egy ismétlődő időbélyeg-átmenet; ez a nyers időfelbontás értelmezését igényli. Nem csökkenő sorrend: {r['all_timestamps_nondecreasing']}.",
  f"- PLY vertexek beolvasása **{r['ply_parse_success']}/{r['ply_count']}**, JPG dekódolás **{r['image_decode_success']}/{r['jpg_count']}**.",
  '', '## Nyolc teszt – megfigyelés', '| Azonosító | Megtörtént | Hiányzó rész |','|---|---|---|',
  '| T5-01 | 150 valós CSV TorchSignal szerkezeti ellenőrzése | Kézzel annotált kezdő/vég ellenőrzés |',
  '| T5-02 | Valós CSV-ből származtatott kontrollált jelkiugrás | Függetlenül címkézett valós anomáliák, valódi detektor pontossága |',
  '| T5-03 | 20 valós JPG leolvasás, feltáró QC és képtorzítás | Kézi referenciakontúr/skála |',
  '| T5-04 | 18 PLY leolvasása és ismert eltolású szintetikus pontfelhő | FGR + ICP valós referenciapárokon és szakértői hibatérkép |',
  '| T5-05 | 91–99% vizsgálat valósból származtatott ismert eltérésen | Független valós adatokon választott küszöb igazolása |',
  '| T5-06 | Fájlnév szerinti párosítás és teljes lefedettségi mátrix | Fizikai munkadarab-azonosító ellenőrzés |',
  '| T5-07 | Biztonságos alpha előminősítés logika szintetikus adatokon | Független valós OK/NOK címkék; fals OK statisztika |',
  '| T5-08 | Offline szintetikus stream logika | End-to-end robotcellás késleltetés és kezelői próba |',
  '', '## Kapcsolódó fájlok','',
  '- `real_csv_inventory.csv` (150 munkadarab sor)',
  '- `real_seam_features.csv` (aktív varratszakaszok)',
  '- `real_modalities_mapping.csv` (CSV/JPG/PLY fájlnév-egyezés)',
  '- `real_image_qc_exploratory.csv` (20 JPG, feltáró mutatók)',
  '- `real_ply_geometry_inventory.csv` (18 PLY metadata és alakjellemző)',
  '- `real_anchored_ply_threshold_sweep.csv` (szintetikus ismert eltolás: 91–99%)',
  '- `real_data_results.json` (gépileg feldolgozható összesítő)',
  '', '## Megkötések',
  'A 97-es érték itt távolságpercentilis, nem az ISO 5817 szerinti megfelelőségi határ. Valós felületi referencia és független hegesztési minősítés nélkül OK/NOK pontosság nem becsülhető. A fájlnév szerinti összerendelés nem bizonyítja, hogy minden kép és PLY ugyanazon varratot ábrázolja.','']
 (OUT/'TRL5_v2_futtatasi_jegyzokonyv.md').write_text('\n'.join(lines),encoding='utf8')
 print(json.dumps({'elapsed_s':round(time.perf_counter()-t0,1), 'CSV':r['csv_count'],'JPG':r['jpg_count'],'PLY':r['ply_count'],
 'three_modality':r['three_modality_pairs'],'structural_ok':r['structural_ok_csv'],'review':r['csv_needing_review'],
 'ply_loaded':r['ply_parse_success'],'image_loaded':r['image_decode_success'],
 'synthetic_ply':r['real_anchored_synthetic'].get('geometry'),'synthetic_image':r['real_anchored_synthetic'].get('image')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
