import cv2, subprocess, sys
from PIL import Image, ImageDraw
vid, tref, lb, t0, t1, out = sys.argv[1], float(sys.argv[2]), tuple(map(int, sys.argv[3].split(','))), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
pts = [float(x) for x in subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=pts_time','-of','csv=p=0',vid],capture_output=True,text=True).stdout.split()]
cap = cv2.VideoCapture(vid); ref = None; tiles = []; k = 0; ok, fr = cap.read()
while ok and k < len(pts):
    t = pts[k]
    if ref is None and t >= tref: ref = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)[lb[1]:lb[3], lb[0]:lb[2]]
    if ref is not None and t0 <= t <= t1:
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY); r = cv2.matchTemplate(g, ref, cv2.TM_CCOEFF_NORMED); _, s, _, (x, y) = cv2.minMaxLoc(r)
        crop = fr[max(0, y-30):y+60, max(0, x-10):x+260]
        tiles.append((t, s, Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))))
    if t > t1: break
    ok, fr = cap.read(); k += 1
cols = 6; W = 270; H = 104
S = Image.new('RGB', (W*cols, H*((len(tiles)+cols-1)//cols)), 'white'); d = ImageDraw.Draw(S)
for i, (t, s, im) in enumerate(tiles):
    x, y = (i % cols)*W, (i//cols)*H; S.paste(im, (x, y+12)); d.text((x+2, y), f'{t:.3f} {s:.2f}', fill='black')
S.save(out); print(len(tiles))
