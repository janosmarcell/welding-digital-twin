import cv2, numpy as np, subprocess, sys
from PIL import Image, ImageDraw
vid, tref, fb, t0, t1, out = sys.argv[1], float(sys.argv[2]), tuple(map(int, sys.argv[3].split(','))), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
pts = [float(x) for x in subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=pts_time','-of','csv=p=0',vid],capture_output=True,text=True).stdout.split()]
cap0 = cv2.VideoCapture(vid); k0 = 0; ref = None
ok0, f0 = cap0.read()
while ok0 and k0 < len(pts):
    if pts[k0] >= tref:
        ref = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY)[fb[1]:fb[3], fb[0]:fb[0]+150]; break
    ok0, f0 = cap0.read(); k0 += 1
cap0.release()
cap = cv2.VideoCapture(vid); tiles = []; k = 0
ok, fr = cap.read()
while ok and k < len(pts):
    t = pts[k]
    if ref is not None and t0 <= t <= t1:
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        r = cv2.matchTemplate(g, ref, cv2.TM_CCOEFF_NORMED); _, s, _, (x, y) = cv2.minMaxLoc(r)
        crop = fr[max(0,y-4):y+(fb[3]-fb[1])+4, x+120:x+(fb[2]-fb[0])+40]
        tiles.append((t, s, Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))))
    if t > t1: break
    ok, fr = cap.read(); k += 1
W = max(im.width for _, _, im in tiles); H = max(im.height for _, _, im in tiles) + 2
S = Image.new('RGB', (W + 110, H * len(tiles)), 'white'); d = ImageDraw.Draw(S)
for i, (t, s, im) in enumerate(tiles):
    S.paste(im, (110, i * H)); d.text((2, i * H + 8), f'{t:.3f} s {s:.2f}', fill='black')
S.save(out); print(len(tiles))
