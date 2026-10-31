import pandas as pd, numpy as np, sys
trk, csvp = sys.argv[1], sys.argv[2]; thr = float(sys.argv[3]) if len(sys.argv) > 3 else 45; smin = float(sys.argv[4]) if len(sys.argv) > 4 else 0.6
d = pd.read_csv(trk); v = d[d.label_score >= smin].copy(); v['on'] = (v.check > thr).astype(int)
ev = []
prev = None
for _, r in v.iterrows():
    if prev is not None and r.on != prev.on:
        ev.append(dict(irany='0->1' if r.on else '1->0', video_elso=r.t, video_elozo=prev.t, res=r.t - prev.t))
    prev = r
c = pd.read_csv(csvp); t = (c.SysTimeMsecs - c.SysTimeMsecs.iloc[0]) / 1000; ts = c.TorchSignal.values
ce = [(('0->1' if ts[i] else '1->0'), t.iloc[i], i) for i in range(1, len(ts)) if ts[i] != ts[i-1]]
print('VIDEO átmenetek (score>=%.2f, thr %g):' % (smin, thr))
for e in ev: print('  %s  %.3f (előző látható %.3f, rés %.3f)' % (e['irany'], e['video_elso'], e['video_elozo'], e['res']))
print('CSV átmenetek:')
for e in ce: print('  %s  %.3f  sor %d' % e)
