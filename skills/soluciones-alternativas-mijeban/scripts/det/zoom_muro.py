import sys, ezdxf, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
doc = ezdxf.readfile(sys.argv[1]); msp = doc.modelspace()
fig = plt.figure(figsize=(12, 9)); ax = fig.add_axes([0.06, 0.05, 0.92, 0.92])
Frontend(RenderContext(doc), MatplotlibBackend(ax)).draw_layout(msp)
ax.set_xlim(421708.15, 421709.75); ax.set_ylim(4412054.6, 4412055.8)
ax.set_aspect('equal'); ax.grid(True, lw=0.3)
for x in (421708.3468, 421708.4718, 421708.4918, 421708.6218, 421708.6918, 421708.7468):
    ax.axvline(x, color='red', lw=0.4, ls=':')
fig.savefig(sys.argv[2], dpi=110)
