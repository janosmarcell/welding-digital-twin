from pathlib import Path
import csv,json
from artifact_tool import Workbook,SpreadsheetFile
R=Path(__file__).resolve().parents[1]
F=R/'outputs'/'reports'
OUT=R/'outputs'/'TRL5_valos_adatos_osszefoglalo.xlsx'
with (F/'real_data_results.json').open(encoding='utf8') as f: summary=json.load(f)
with (R/'outputs'/'TRL5_v2_test_results.json').open(encoding='utf8') as f: result=json.load(f)

def csvload(name, cols):
 with (F/name).open(encoding='utf-8-sig',newline='') as f:
  dat=list(csv.DictReader(f))
 return [[(str(row.get(c,'')) if row.get(c,'') is not None else '') for c in cols] for row in dat]

def sheet(name,heads,records,widths=None):
 sh=wb.worksheets.add(name)
 rr=sh.get_range_by_indexes(0,0,1,len(heads)); rr.values=[heads]
 rr.format={'fill':'#124F55','font':{'bold':True,'color':'#FFFFFF'},'row_height':25,'vertical_alignment':'center'}
 if records:sh.get_range_by_indexes(1,0,len(records),len(heads)).values=records
 sh.freeze_panes.freeze_rows(1)
 for i,w in enumerate(widths or [22]*len(heads)):
  sh.get_range_by_indexes(0,i,len(records)+1,1).format.column_width=w
 if records: sh.get_range_by_indexes(1,0,len(records),len(heads)).format.row_height=17
 return sh

wb=Workbook.create()
over=wb.worksheets.add('Attekintes')
over.merge_cells('A1:F1')
over.get_range('A1').values=[['TRL5 – valós adatok és szintetikus tesztek | v2']]
over.get_range('A1:F1').format={'fill':'#124F55','font':{'bold':True,'color':'#FFFFFF','size':15},'row_height':39}
over.merge_cells('A2:F2'); over.get_range('A2').values=[['Státusz: TRL5 MÉG NEM LEZÁRT – valós adatok szerkezeti ellenőrzése, kiegészítő szintetikus próbák']]
over.get_range('A2:F2').format={'fill':'#FFF4CE','font':{'bold':True,'color':'#654B13'},'row_height':29}
over.get_range('A4:C4').values=[['Mutató','Eredmény','Bizonyíték / korlát']]
over.get_range('A4:C4').format={'fill':'#185C60','font':{'bold':True,'color':'#FFFFFF'},'row_height':23}
metrics=[
 ('Valós CSV-fájl','', '150 nyers állomány, nem 150 hiteles minőségcímke'),
 ('2D JPG','', 'A beolvasás igazolt; a fizikai geometriai mérés nincs kalibrálva'),
 ('3D PLY','', 'Csak beolvasás és próba; teljes FGR+ICP validáció szükséges'),
 ('3 szakaszos CSV','', 'Második lépcső: manuális eseménycímkék'),
 ('Eltérő szakaszszám', '', 'g02_s33: két hegesztési szakasz'),
 ('CSV/JPG/PLY együtt','', 'Névegyezés, nem kézzel igazolt fizikai munkadarab-párosítás'),
]
over.get_range('A5:C10').values=[list(x) for x in metrics]
for rr,formula in [(5,'=COUNTA(CSV_leltar!A2:A151)'),(6,'=COUNTA(Kepek!A2:A21)'),(7,'=COUNTA(Pontfelhok!A2:A19)'),(8,'=COUNTIF(CSV_leltar!D2:D151,3)'),(9,'=COUNTIF(CSV_leltar!D2:D151,"<>3")'),(10,'=COUNTIF(CSV_leltar!I2:I151,"MATCHED_ALL_THREE")')]:
 over.get_range(f'B{rr}').formulas=[[formula]]
over.get_range('A12:B12').values=[['Reprodukálhatóság','Érték']]
over.get_range('A12:B12').format={'fill':'#185C60','font':{'bold':True,'color':'#FFFFFF'}}
over.get_range('A13:B15').values=[['Bemenet','csv_light2.zip'],['SHA-256',summary['sha256']],['Létrehozás UTC',summary['run_utc']]]
over.get_range('A:A').format.column_width=28; over.get_range('B:B').format.column_width=35;over.get_range('C:C').format.column_width=68
over.get_range('B14').format.column_width=38

statuses=[['Teszt','Eredmény a v2-ben','Szintzáráshoz szükséges']]
missing={
'T5-01':'Manuális varratkezdet/vég annotáció; szenzitivitás mérése',
'T5-02':'Független valós hegesztési anomália-címkék',
'T5-03':'Kézi kontúr, ismert skála, fényviszonyok ismétlése',
'T5-04':'FGR+ICP valós párokon, ismert valódi hibahelyek',
'T5-05':'Független valós validáló készlet; fixált küszöb',
'T5-06':'Fizikai munkadarab-azonosítók kézi ellenőrzése',
'T5-07':'Független OK/NOK minősítések, FP/FN/CI',
'T5-08':'Robotcellás késleltetés/veszteség, kezelői jegyzőkönyv'}
for x in result['tests']:statuses.append([x['code'],x['real_data_status'],missing[x['code']]])
sh=sheet('Tesztek',statuses[0],statuses[1:],[14,66,73]);sh.get_range('A2:C9').format.row_height=34;sh.get_range('B2:C9').format.wrap_text=True
cols=['id','speed_group','rows','torch_segments','active_samples','duplicate_timestamp_steps','has_jpg','has_ply','mapping_status','structure_status','csv_zip_path']
records=csvload('real_csv_inventory.csv',cols)
# Cast numeric cells and boolean to real spreadsheet types for formulas
for record in records:
 for c in [2,3,4,5]:
  try: record[c]=int(record[c])
  except:pass
 for c in [6,7]: record[c]=(record[c]=='True')
sh=sheet('CSV_leltar',['Mintaszám','Sebességcsoport','CSV sorok','Szakaszok','Aktív sorok','Ismételt időlépések','JPG','PLY','Összerendelés','Szerkezeti státusz','ZIP-beli elérési út'],records,[17,22,13,13,16,20,10,10,27,22,45]); sh.get_range('A2:K151').format.row_height=16
# Add conditional formatting to clearly flag anomalies.
sh.get_range('D2:D151').conditional_formats.add_cell_is({'operator':'notEqual','formula':3,'format':{'fill':'#FDE9D9','font':{'color':'#B42318'}}})
imgcols=['id','file','decoded','width_px','height_px','sharpness_laplacian','dark_fraction','range_p98_p2','is_evaluable','qc_status']
ims=csvload('real_image_qc_exploratory.csv',imgcols)
sh=sheet('Kepek',['Minta','ZIP állomány','Dekódolható','Szélesség px','Magasság px','Élességi mutató','Sötét arány','Kontraszt tartomány','Heurisztikus értékelhetőség','Állapot'],ims,[17,45,16,16,16,24,18,22,35,28])
plycols=['id','file','parsed','source_tag','vertex_count','sample_count','x_extent','y_extent','z_extent']
sh=sheet('Pontfelhok',['Minta','ZIP állomány','Beolvasható','Szkenner címke','Csúcspontok','Mintapontok','X tartomány','Y tartomány','Z tartomány'],csvload('real_ply_geometry_inventory.csv',plycols),[17,50,18,21,22,17,18,18,18])
gdata=[]
for k,v in sorted(summary['by_group'].items()):gdata.append([k,30,int(v['has_jpg']),int(v['has_ply'])])
sh=sheet('Csoportok',['Sebességcsoport','CSV','JPG','PLY'],gdata,[30,18,18,18])
OVER=OUT.parent;OVER.mkdir(parents=True,exist_ok=True)
print(wb.inspect({'kind':'table','range':'Attekintes!A4:C10','include':'values,formulas','table_max_rows':8,'table_max_cols':3}).ndjson[:1800])
SpreadsheetFile.export_xlsx(wb).save(str(OUT))
print('Created',OUT,OUT.stat().st_size)
