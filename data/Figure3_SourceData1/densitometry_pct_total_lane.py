#!/usr/bin/env python3
"""
Figure 3B densitometry - recombinant product band as % of total lane signal.

Input : annex_temperature_stacked.png  (flattened 4-gel temperature montage)
        boxes_mapped.json               ({'prod':[[x0,y0,x1,y1],...48], 'ref':[...4], 'W','H'})
Method: For each product box (one per design-pair) the box is split into its two
        sample lanes (left/right). For each lane, darkness is background-subtracted
        (net = clip(bg - gray, 0), bg = 85th percentile of that lane's full gel
        column) and integrated over (a) the product box and (b) the full lane column
        (gel top->bottom). Result = 100 * band_net / lane_net. Red/blue annotation
        pixels are masked out. Gel y-extents come from the SVG image placement.
Output: densitometry_pct_total_lane.csv  (gel, signal, temp_C, design, pct_of_total_lane)
        n = 4 designs per signal x temperature.
Author: Y. Flores Bueso.
"""
import numpy as np, json, csv, sys
from PIL import Image
from collections import defaultdict

PNG  = sys.argv[1] if len(sys.argv) > 1 else 'annex_temperature_stacked.png'
BOX  = sys.argv[2] if len(sys.argv) > 2 else 'boxes_mapped.json'
OUT  = sys.argv[3] if len(sys.argv) > 3 else 'densitometry_pct_total_lane.csv'

A = np.asarray(Image.open(PNG).convert('RGB')).astype(int)
R, Gc, Bc = A[:, :, 0], A[:, :, 1], A[:, :, 2]
gray = 0.299 * R + 0.587 * Gc + 0.114 * Bc
# red box strokes and blue lane labels -> excluded from integration
anno = ((R > 130) & (Gc < 95) & (Bc < 95)) | ((Bc > 130) & (R < 110) & (Gc < 130) & (Bc - R > 30))

prod = json.load(open(BOX))['prod']

# gel crop y-extents in composite px (from the SVG image transforms)
gel_ext = {'NS': (204, 1121), 'VNp15/PelB': (1356, 2415),
           'DsbA/MalE': (2634, 3419), 'OmpA/PhoA': (3608, 4461)}
gel_order = ['NS', 'VNp15/PelB', 'DsbA/MalE', 'OmpA/PhoA']
sigpair = {'NS': ('NS', 'NS'), 'VNp15/PelB': ('VNp15', 'PelB'),
           'DsbA/MalE': ('DsbA', 'MalE'), 'OmpA/PhoA': ('OmpA', 'PhoA')}
temps = ['16', '22', '37']   # three temperature blocks, left->right, 4 designs each

def gel_of(yc):
    for nm, (t, b) in gel_ext.items():
        if t <= yc <= b:
            return nm
    return min(gel_order, key=lambda nm: abs(yc - sum(gel_ext[nm]) / 2))

def netsum(x0, y0, x1, y1, bg):
    x0, x1 = sorted((int(round(x0)), int(round(x1))))
    y0, y1 = sorted((int(round(y0)), int(round(y1))))
    g = gray[y0:y1, x0:x1]; m = anno[y0:y1, x0:x1]
    v = np.clip(bg - g, 0, None); v[m] = 0
    return float(v.sum())

def lane_bg(x0, x1, gt, gb):
    x0, x1 = sorted((int(round(x0)), int(round(x1))))
    col = gray[int(gt):int(gb), x0:x1][~anno[int(gt):int(gb), x0:x1]]
    return np.percentile(col, 85) if col.size else 255

boxes = [dict(x0=x0, y0=y0, x1=x1, y1=y1, xc=(x0 + x1) / 2, g=gel_of((y0 + y1) / 2))
         for x0, y0, x1, y1 in prod]

results = []
for nm in gel_order:
    gt, gb = gel_ext[nm]
    gbx = sorted([b for b in boxes if b['g'] == nm], key=lambda b: b['xc'])
    for bi, b in enumerate(gbx):
        temp = temps[bi // 4]           # 4 designs per temperature block
        xmid = (b['x0'] + b['x1']) / 2
        for side, (lx0, lx1) in enumerate([(b['x0'], xmid), (xmid, b['x1'])]):
            bg = lane_bg(lx0, lx1, gt, gb)
            band = netsum(lx0, b['y0'], lx1, b['y1'], bg)
            lane = netsum(lx0, gt, lx1, gb, bg)
            results.append(dict(gel=nm, signal=sigpair[nm][side], temp=temp,
                                design=bi % 4 + 1,
                                pct=100 * band / lane if lane > 0 else float('nan')))

with open(OUT, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['gel', 'signal', 'temp_C', 'design', 'pct_of_total_lane'])
    for x in results:
        w.writerow([x['gel'], x['signal'], x['temp'], x['design'], round(x['pct'], 2)])

# console summary
agg = defaultdict(list)
for r in results: agg[(r['signal'], r['temp'])].append(r['pct'])
print('wrote', OUT, '(%d rows)' % len(results))
for s in ['VNp15','PelB','DsbA','MalE','OmpA','PhoA','NS']:
    print(f"  {s:6}", {t: round(np.nanmean(agg[(s,t)]),1) for t in temps})
