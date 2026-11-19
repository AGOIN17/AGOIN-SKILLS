import sys, ezdxf, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy
from ezdxf import bbox
doc = ezdxf.readfile(sys.argv[1]); b = doc.blocks['P-B PR. EJECUCION']
def recorte(x0, x1, y0, y1, nombre):
    ents = []
    for e in b:
        bb = bbox.extents([e], fast=True)
        if bb.has_data and bb.extmax.x > x0 and bb.extmin.x < x1 and bb.extmax.y > y0 and bb.extmin.y < y1:
            ents.append(e)
    fig = plt.figure(figsize=(9, 6)); ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK)
    fr = Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg)
    fr.draw_entities(ents)
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect('equal', adjustable='datalim')
    fig.savefig(nombre, dpi=110); plt.close(fig)
recorte(-31.6, -27.6, -38.6, -35.8, sys.argv[2] + '_oeste.png')
recorte(-24.2, -20.2, -40.6, -37.8, sys.argv[2] + '_pasillo.png')
