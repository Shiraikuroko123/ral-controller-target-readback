"""Draw Figure 1 from the bundled six-run extract. Requires Matplotlib."""
import csv
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
with (root / 'franka-filter-runs.csv').open(encoding='utf-8-sig') as stream:
    runs = list(csv.DictReader(stream))
mpl.rcParams.update({'font.family': 'Times New Roman', 'font.size': 8.12, 'pdf.fonttype': 42,
                     'axes.linewidth': 0.65, 'xtick.major.width': 0.65})
ink, teal, slate = '#172c38', '#006a75', '#546572'
fig = plt.figure(figsize=(3.40, 2.28))
flow = fig.add_axes([.025, .53, .95, .445]); flow.set(xlim=(0,1), ylim=(0,1)); flow.axis('off')
flow.text(0, 1, '(a) Reconstructing the command origin', fontweight='bold', color=ink, va='top')
for left, title, detail in [(.01,'Telemetry','field + cycle'),(.285,'Infer origin','point or box'),(.55,'Test rewrite','bound D'),(.82,'Delivery','score write')]:
    flow.text(left,.53,title,fontsize=8.12,fontweight='bold',color=teal,va='center')
    flow.text(left,.29,detail,color=slate,fontsize=8.12,va='center')
for start,end in [(.215,.275),(.48,.54),(.745,.805)]:
    flow.annotate('',xy=(end,.53),xytext=(start,.53),arrowprops={'arrowstyle':'-|>', 'lw':.9,'color':slate,'mutation_scale':7})
flow.plot([0,1],[.06,.06], lw=.65, c='#9eaeb4')
fig.text(.027,.51,'(b) Franka filter on six software runs',fontweight='bold',color=ink,va='top')
ax=fig.add_axes([.29,.24,.65,.205]); ax.spines[['top','right','left']].set_visible(False)
ax.set_xlim(-.055,.87); ax.set_ylim(-.5,1.5); ax.set_yticks([0,1],['Every 10 cycles','Every cycle']);ax.tick_params(axis='y',length=0,pad=4);ax.set_xticks([0,.2,.4,.6,.8]);ax.tick_params(axis='x',length=2,pad=2)
ax.set_xlabel('Target reconstruction RMS (mm)',labelpad=1.3); ax.set_axisbelow(True);ax.grid(axis='x',lw=.45,color='#d4dce0')
for period,y in [(1,1),(10,0)]:
    subset=[r for r in runs if int(r['callback_period_cycles'])==period]
    assert len(subset)==3
    for offset,r in zip([-.15,0,.15],subset):
        ax.scatter(float(r['send_rms_mm']),y+offset,s=11,c=slate,marker='o',zorder=3)
        ax.scatter(float(r['application_cycle_rms_mm']),y+offset,s=14,facecolors='white',edgecolors=teal,marker='D',linewidth=.85,zorder=4)
ax.plot([],[], 'o',color=slate,ms=3,label='Send time');ax.plot([],[], 'D',mfc='white',mec=teal,ms=3.3,label='Application cycle');fig.legend(*ax.get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.55,-.012),ncol=2,frameon=False,handletextpad=.25,columnspacing=1.2,fontsize=8.12)
fig.savefig(root/'origin-readback.pdf',metadata={'Title':'Telemetry, origin inference and delivered writes','Author':'','CreationDate':None,'ModDate':None})