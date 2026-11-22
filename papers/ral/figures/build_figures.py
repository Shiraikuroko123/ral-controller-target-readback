"""Regenerate the RA-L figures from bundled measurements and archived native renders."""
from pathlib import Path
import csv
import runpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Patch
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'inputs'
WIDTH = 3.40  # 244.8 PDF points, effectively the ieeeconf column width.
FONT_SIZE = 8.12
META = {'CreationDate': None, 'ModDate': None, 'Author': ''}


def style():
    font_manager.findfont('Times New Roman', fallback_to_default=False)
    plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': FONT_SIZE,
                         'axes.labelsize': FONT_SIZE, 'axes.titlesize': FONT_SIZE,
                         'legend.fontsize': FONT_SIZE, 'pdf.fonttype': 42,
                         'axes.linewidth': .65, 'xtick.major.width': .6, 'ytick.major.width': .6})


def rows(name):
    with (DATA / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def save(fig, name):
    fig.savefig(ROOT / f'{name}.pdf', metadata=META, dpi=300)
    plt.close(fig)


def ambiguity():
    measures = rows('ambiguity.csv')
    fig, ax = plt.subplots(figsize=(WIDTH, 1.94))
    fig.subplots_adjust(left=.17, right=.97, bottom=.25, top=.88)
    x = np.linspace(-1, 9, 201)
    for history, offset, color, ls, name in [(0, 0, '#286782', '-', 'Target intact'), (1, 8, '#ae5727', '--', 'Target shifted 8 mm')]:
        ax.plot(x, np.abs(x-offset), color=color, ls=ls, label=name, lw=1.25)
        for record in measures:
            if int(record['history']) == history:
                disp = {'copy': 0, 'midpoint': 4, 'readback': offset}[record['method']]
                ax.plot(disp, float(record['residual_mm']), 'o', ms=3.5, c=color)
    ax.axvline(4, color='.62', ls=':', lw=.75)
    ax.set(xlim=(-1,9), ylim=(-.35,9.6), xticks=[0,2,4,6,8], yticks=[0,2,4,6,8],
           xlabel='Displacement on affected axis (mm)', ylabel='Target error (mm)')
    ax.spines[['right','top']].set_visible(False)
    fig.legend(*ax.get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.55,1.035),ncol=2,
               columnspacing=1.15,handlelength=1.4,handletextpad=.45,frameon=False)
    save(fig,'ambiguity')


def fetch_views():
    fig, axes=plt.subplots(2,2,figsize=(WIDTH,2.19))
    fig.subplots_adjust(left=.01, bottom=.01, right=.99, top=.91, wspace=.02, hspace=.03)
    for row, method in enumerate(['copy','reencoded']):
        for col,step in enumerate(['step14','final']):
            ax=axes[row,col]
            ax.imshow(plt.imread(DATA/f'fetch-{method}-{step}.png')); ax.axis('off')
            label=(['Copy','Re-encode'] if col==0 else ['Miss','Success'])[row]
            ax.text(.025,.065,label,color='white',transform=ax.transAxes,
                    bbox=dict(facecolor='#202326',edgecolor='none',pad=1.1,alpha=.85))
    for ax,title in zip(axes[0],['Last overwritten action','End of replay (detail)']):
        ax.set_title(title,pad=3)
    save(fig,'fetch-example')


def sawyer_case():
    measures=rows('sawyer-trace.csv'); fig=plt.figure(figsize=(WIDTH,2.73))
    grid=fig.add_gridspec(2,2,left=.19,right=.97,top=.91,bottom=.17,height_ratios=[.91,1],wspace=.17,hspace=.22)
    ax=fig.add_subplot(grid[1,:]); styles=[('eventp','Event-triggered','event','#00796e','-'),('s2_p','Scheduled','scheduled','#b04e26','--')]
    for i,(method,title,image,color,ls) in enumerate(styles):
        branch=[r for r in measures if r['mode']==method]; times=[int(r['t']) for r in branch]; values=[float(r['object_to_goal_mm']) for r in branch]
        assert len(values)==150
        photo=fig.add_subplot(grid[0,i]); photo.imshow(plt.imread(DATA/f'sawyer-{image}.png'));photo.axis('off')
        photo.set_title(f'{title}  /  {values[-1]:.0f} mm',color=color,pad=3)
        ax.plot(times,values,c=color,ls=ls,lw=1.35,label=title)
    ax.axvspan(8.5,13.5,color='.65',alpha=.23,lw=0); ax.axhline(70,c='.36',ls=':',lw=.8)
    ax.text(3,79,'70 mm criterion',color='.2');ax.set(xlabel='Control step',ylabel='Object to goal (mm)', xlim=(-1,150),ylim=(0,365),xticks=[0,50,100,149],yticks=[0,100,200,300]);ax.spines[['right','top']].set_visible(False)
    ax.legend(frameon=False,loc='upper right',bbox_to_anchor=(1.01,1.07),handlelength=1.4,handletextpad=.45,labelspacing=.1,borderpad=.1)
    save(fig,'sawyer-case')


def panda():
    d=rows('panda-phases.csv'); fig, ax=plt.subplots(figsize=(WIDTH,2.04));fig.subplots_adjust(left=.19,right=.96,top=.71,bottom=.24)
    colors=['#2d566e','#aa4b25']; marks=['o','s']
    for phase,y in [('descend',1),('raise',0)]:
        vs=[float(r['rms_mm']) for r in d if r['phase']==phase];assert len(vs)==2 and all(int(r['terminal'])==8 for r in d)
        ax.plot(vs,[y,y],c='.65',lw=1.15)
        for value,c,m,off in zip(vs,colors,marks,[11,-11]):
            ax.scatter(value,y,c=c,marker=m,s=21);ax.annotate(f'{value:.2f}',(value,y),xytext=(0,off),textcoords='offset points',ha='center',va='center',color=c)
    ax.set(yticks=[1,0],yticklabels=['Descent','Lift'],ylim=(-.6,1.6),xlim=(9.7,19.1),xticks=[10,12,14,16,18],xlabel='Mean hand-path RMS error (mm)');ax.tick_params(length=0,pad=2.6);ax.grid(axis='x',c='.9',lw=.55);ax.spines[['top','right','left']].set_visible(False)
    fig.text(.03,.95,'Both policies lifted 8 of 8 cubes per phase',weight='bold');handles=[Line2D([],[],marker=m,color=c,ls='',markersize=4,label=l) for m,c,l in zip(marks,colors,['Hand observer','Observer + one read'])];fig.legend(handles=handles,frameon=False,ncol=2,loc='upper left',bbox_to_anchor=(.02,.914),columnspacing=.9,handletextpad=.3,handlelength=.9)
    save(fig,'replay-comparison')


def confirmation():
    d=rows('sawyer-paired-outcomes.csv');fig=plt.figure(figsize=(WIDTH,2.30));ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,WIDTH*72),ylim=(2.30*72,0));ax.axis('off')
    edge='#83989e'; gain='#006a75'; fill='#dbe3e5'
    for cohort,y,title in [('Exploration',4,'Development'),('Confirmation',78,'Independent confirmation')]:
        cohort_rows=[r for r in d if r['cohort']==cohort];assert len(cohort_rows)==96
        a=sum(int(r['no_read']) for r in cohort_rows);b=sum(int(r['event']) for r in cohort_rows)
        ax.text(2,y,title,weight='bold',va='top');ax.text(242,y,f'No read {a}, event {b}',ha='right',va='top')
        for idx,(task,title2,left) in enumerate([('push','Push layouts',51),('pick-place','Pick-and-place layouts',151)]):
            ax.text(left+41,y+14,title2,ha='center',va='top'); subset=[r for r in cohort_rows if r['task']==task];seeds=sorted({int(r['seed']) for r in subset});assert len(seeds)==12
            for row, (cond,lab) in enumerate([('clean','Clean'),('override','Override'),('push','Force'),('combined','Both')]):
                yy=y+26+10.6*row
                if idx==0:ax.text(2,yy+2.4,lab,va='center')
                for i,seed in enumerate(seeds):
                    record=next(r for r in subset if int(r['seed'])==seed and r['condition']==cond);first,second=int(record['no_read']),int(record['event']); xx=left+7.25*i; box=4.6
                    if first and second or second and not first: ax.add_patch(Rectangle((xx,yy),box,box,edgecolor=edge if first else gain,facecolor=fill if first else gain,lw=.45))
                    elif not first and not second: ax.plot([xx,xx+box],[yy,yy+box],c='.2',lw=.85);ax.plot([xx,xx+box],[yy+box,yy],c='.2',lw=.85)
                    else:raise ValueError('Unexpected no-read-only cell')
    markers=[Patch(facecolor=fill,edgecolor=edge),Patch(facecolor=gain,edgecolor=gain),Line2D([],[],c='.2',ls='',marker='x',markersize=4)]
    ax.legend(markers,['Both succeed','Event read only','Both fail'],frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,-.012),columnspacing=1,handlelength=.75,handletextpad=.4)
    save(fig,'sawyer-confirmation')


if __name__=='__main__':
    style();runpy.run_path(str(ROOT/'build_telemetry.py'),run_name='__main__');style()
    ambiguity();fetch_views();sawyer_case();panda();confirmation()