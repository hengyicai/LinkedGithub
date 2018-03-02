"""
================================================================
Demo of the histogram function's different ``histtype`` settings
================================================================

* Histogram with step curve that has a color fill.
* Histogram with custom and unequal bin widths.

Selecting different bin counts and sizes can significantly affect the
shape of a histogram. The Astropy docs have a great section on how to
select these parameters:
http://docs.astropy.org/en/stable/visualization/histogram.html
"""

import numpy as np
import matplotlib.pyplot as plt

import issue_link_count

data_map = issue_link_count.read_map("./result/issue_unit_map_link_count.csv")

x = [int(item) for item in data_map.values()]

fig, (ax1) = plt.subplots(ncols=1, figsize=(6, 4))

# ax0.hist(x, 20, normed=1, histtype='stepfilled', facecolor='g', alpha=0.75)
# ax0.set_title('stepfilled')

# Create a histogram by providing the bin edges (unequally spaced).
# bins = [100, 150, 180, 195, 205, 220, 250, 300]
ax1.hist(x, bins=10, log=True, histtype='bar', rwidth=0.8)
ax1.set_title('#issue_units of different #links')
ax1.set_ylabel('#issue_units')
ax1.set_xlabel('#links')

fig.tight_layout()
plt.show()
