"""
Figure 3 densitometry - product band as % of total lane signal.
Input : annex_temperature_stacked.png (flattened gel montage, 4315x4623 px)
        boxes = per-lane product boxes (red) and reference boxes, in the same px space.
Method: for each lane, integrate background-subtracted darkness (net = clip(bg - gray, 0))
        over (a) the product box and (b) the full lane column (crop top->bottom),
        then report 100 * band_net / lane_net. Colour annotations (red/blue) are masked out.
        Per gel the full crop y-extent is taken from the SVG image placement.
Output: pct_total_lane.csv  (gel, signal, temp_C, design, pct_of_total_lane), n=4 designs/condition.
See Methods for full description. Author: Y. Flores Bueso.
"""
# (analysis script; box coordinates supplied separately as boxes_mapped.json)
