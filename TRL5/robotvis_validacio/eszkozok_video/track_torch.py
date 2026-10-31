"""RobotVis 'Torch Signal' pipa és a 'Current / Last Log File' sor követése kézi kamerás videón.
Használat: python3 track_torch.py video.mp4 ref_ido_s label_box(x0,y0,x1,y1) logfile_box(x0,y0,x1,y1) kimenet.csv
A label_box a 'Torch Signal' felirat egy referencia-képkockán; a pipa a felirattól jobbra, azonos sorban."""
import cv2, numpy as np, subprocess, sys, csv
vid, tref = sys.argv[1], float(sys.argv[2])
lb = tuple(map(int, sys.argv[3].split(','))); fb = tuple(map(int, sys.argv[4].split(','))); out = sys.argv[5]
pts = [float(x) for x in subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=pts_time','-of','csv=p=0',vid],capture_output=True,text=True).stdout.split()]
cap = cv2.VideoCapture(vid); frames_gray = []
ok, fr = cap.read(); i = 0; ref = None
while ok:
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    if ref is None and pts[i] >= tref: ref = g
    frames_gray.append(g); ok, fr = cap.read(); i += 1
n = min(len(frames_gray), len(pts))
tl = ref[lb[1]:lb[3], lb[0]:lb[2]]; tf = ref[fb[1]:fb[3], fb[0]:fb[2]]
rows = []; prev_f = None
for k in range(n):
    g = frames_gray[k]
    r = cv2.matchTemplate(g, tl, cv2.TM_CCOEFF_NORMED); _, sc, _, (x, y) = cv2.minMaxLoc(r)
    w, h = lb[2]-lb[0], lb[3]-lb[1]
    box = g[max(0,y-6):y+h+6, x+w+70:x+w+130]
    bg = g[max(0,y-6):y+h+6, x+w+10:x+w+60]
    chk = float(np.percentile(box, 99) - np.median(bg)) if box.size and bg.size else np.nan
    # naplófájl-sor: a sablon helye és a jobbra eső szöveg változása
    rf = cv2.matchTemplate(g, tf[:, :min(150, tf.shape[1])], cv2.TM_CCOEFF_NORMED); _, sf, _, (fx, fy) = cv2.minMaxLoc(rf)
    reg = g[fy:fy+tf.shape[0], fx:fx+tf.shape[1]].astype(np.float32)
    dfile = float(np.abs(reg - prev_f).mean()) if prev_f is not None and reg.shape == prev_f.shape else np.nan
    prev_f = reg
    rows.append([k, f'{pts[k]:.4f}', f'{sc:.3f}', x, y, f'{chk:.1f}', f'{sf:.3f}', f'{dfile:.2f}'])
with open(out, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['frame','t','label_score','lx','ly','check','file_score','file_diff']); w.writerows(rows)
print(n, 'képkocka')
