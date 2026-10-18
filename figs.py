"""Generate all figures of the numerical section from the stored results."""
import numpy as np, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from fd import Model, BASE
from common import *

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'paper', 'figs')
os.makedirs(FIG, exist_ok=True)
BLUE, ORANGE, AQUA, YELLOW = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
INK, MUTED, GRID = '#0b0b0b', '#52514e', '#dddcd6'
SEQ = LinearSegmentedColormap.from_list('seq', ['#fcfcfb', '#cde2fb', '#86b6ef', '#2a78d6', '#0d366b'])
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6, 'legend.frameon': False,
                     'lines.linewidth': 1.8, 'font.family': 'DejaVu Sans', 'mathtext.fontset': 'cm',
                     'pdf.fonttype': 42, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.03})
W = 2.5

def regions():
    d = np.load(os.path.join(OUT, 'baseline481.npz')); x = d['x']; stop = d['stop']
    X1, X2 = np.meshgrid(x, x, indexing='ij')
    lab = np.where(stop & (X1 > X2), 1.0, np.where(stop & (X1 < X2), 2.0, 0.0))
    fig, ax = plt.subplots(figsize=(4.3, 4.1))
    ax.contourf(X1, X2, lab, levels=[-0.5, 0.5, 1.5, 2.5], colors=['#fcfcfb', '#cde2fb', '#fbdccf'])
    k = x <= 2.9
    ax.plot(d['b1'][k], x[k], color=BLUE, lw=1.6); ax.plot(x[k], d['b2'][k], color=ORANGE, lw=1.6)
    ax.plot([0, 3], [0, 3], color=INK, ls='--', lw=1.0)
    s = np.linspace(1.2, 2.9, 100); pred = qval(BASE) / (4 * gamma_ac(BASE, s + 1e-9, s))
    ax.plot(s + pred, s, color=MUTED, ls=':', lw=1.3); ax.plot(s, s + pred, color=MUTED, ls=':', lw=1.3)
    g0 = (BASE['kappa'][0] * BASE['theta'][0] - BASE['c'][0]) / (BASE['r'] + BASE['kappa'][0])
    ax.plot([g0, g0], [0, g0], color=AQUA, lw=1.2, ls='-.'); ax.plot([0, g0], [g0, g0], color=AQUA, lw=1.2, ls='-.')
    ax.plot([0.9], [1.0], marker='o', ms=5, color=INK); ax.annotate(r'$x_{\rm ref}$', (0.9, 1.0), (0.62, 1.1), color=INK)
    ax.text(2.25, 0.8, r'$\mathcal{D}^{(1)}$', color=INK, fontsize=12); ax.text(0.7, 2.2, r'$\mathcal{D}^{(2)}$', color=INK, fontsize=12)
    ax.text(0.55, 0.45, r'$\mathcal{C}$', color=INK, fontsize=12)
    ax.text(2.42, 2.78, r'$\Delta_\alpha$', color=INK); ax.text(0.03, 0.9, r'$\Gamma^{\rm ac}=0$', color='#11805a', fontsize=8)
    ax.annotate(r'$q/(4\Gamma^{\rm ac})$', (1.5 + 0.28, 1.5), (1.9, 1.15), color=MUTED, fontsize=8, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
    ax.set_xlim(0, 3); ax.set_ylim(0, 3); ax.set_aspect('equal'); ax.grid(False)
    ax.set_xlabel(r'$x_1$'); ax.set_ylabel(r'$x_2$')
    fig.savefig(os.path.join(FIG, 'regions.pdf')); plt.close(fig)

def refine():
    rows = load('e1_refinement')
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    ax = axs[0]
    sty = {121: (YELLOW, ':'), 241: (ORANGE, '--'), 481: (BLUE, '-')}
    for N in [121, 241, 481]:
        m = Model(N=N); U, stop, _ = m.solve(); b1 = arm_boundary(m, U, stop, 1)
        k = (m.x >= 1.0) & (m.x <= 2.9)
        ax.plot(m.x[k], (b1 - m.x)[k], color=sty[N][0], ls=sty[N][1], label=r'$N=%d$' % N)
    s = np.linspace(1.0, 2.9, 200)
    ax.plot(s, qval(BASE) / (4 * gamma_ac(BASE, s + 1e-9, s)), color=INK, lw=1.0, ls='-.', label=r'formal $q/(4\Gamma^{\rm ac})$')
    ax.set_xlabel(r'position $x_2$ along $\Delta_\alpha$'); ax.set_ylabel(r'half-width $b_1(x_2)-x_2$'); ax.set_ylim(0, 0.6); ax.legend()
    ax = axs[1]
    r3 = [r for r in rows if r['Xmax'] == 3.0]
    h = [r['h'] for r in r3]
    ax.loglog(h, [r['raw_margin_full'] for r in r3], marker='o', color=ORANGE, label='nodal minimum, full domain')
    ax.loglog(h, [r['sub_margin_win'] for r in r3], marker='s', color=BLUE, label=r'reconstructed minimum, $[0,2.5]^2$')
    ax.loglog(h, h, color=MUTED, ls=':', lw=1.0, label=r'$h$')
    ax.set_xticks([0.00625, 0.0125, 0.025, 0.05]); ax.set_xticklabels(['0.00625', '0.0125', '0.025', '0.05']); ax.minorticks_off()
    ax.set_xlabel(r'grid spacing $h$'); ax.set_ylabel(r'distance of $\mathcal{D}^{(1)}$ from $\Delta_\alpha$'); ax.legend(fontsize=7.5, loc='center right')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'refine.pdf')); plt.close(fig)

def loss():
    d = np.load(os.path.join(OUT, 'e3_maps.npz')); x = d['x']
    X1, X2 = np.meshgrid(x, x, indexing='ij'); k = x <= W
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.75))
    for ax, key, st, title in zip(axs, ['one_retained', 'one_reopt', 'no_singular'], [None, 'stop_reopt', 'stop_ac'],
                                  ['(a) one-sided, retained arm', '(b) one-sided, re-optimised', '(c) local-time reward dropped']):
        L = 100 * d[key][np.ix_(k, k)]
        im = ax.pcolormesh(x[k], x[k], L.T, cmap=SEQ, vmin=0, vmax=max(L.max(), 1e-9), shading='auto', rasterized=True)
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03); cb.set_label('loss (%)', fontsize=7.5); cb.ax.tick_params(labelsize=7)
        ax.plot([0, W], [0, W], color=INK, ls='--', lw=0.8)
        ax.contour(x[k], x[k], d['stop'][np.ix_(k, k)].T.astype(float), levels=[0.5], colors=[MUTED], linewidths=0.7)
        if st is not None:
            ax.contour(x[k], x[k], d[st][np.ix_(k, k)].T.astype(float), levels=[0.5], colors=[ORANGE], linewidths=1.0)
        ax.set_title(title, fontsize=8.5, color=INK); ax.set_aspect('equal'); ax.grid(False)
        ax.set_xlabel(r'$x_1$'); ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 1, 2])
    axs[0].set_ylabel(r'$x_2$')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'loss.pdf'), dpi=300); plt.close(fig)

def bias():
    e = load('ex1d'); rows = load('e3c_bias')
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9))
    ax = axs[0]
    ax.axhline(0, color=MUTED, lw=0.8); ax.plot(e['curve']['b'], e['curve']['bias0'], color=BLUE)
    ax.axvline(e['bstar'], color=MUTED, ls=':', lw=1.0); ax.text(e['bstar'] + 0.03, -0.42, r'$b^\ast$', color=INK)
    ax.set_xlabel(r'threshold $b$'); ax.set_ylabel(r'$B_b(0)$'); ax.set_title('(a) closed-form example', fontsize=9)
    ax = axs[1]
    r = [x for x in rows if x['N'] == 241]
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.plot([x['shift'] for x in r], [x['B_ref'] for x in r], marker='o', ms=4, color=BLUE, label=r'$N=241$')
    for N, col, mk in [(121, YELLOW, '^'), (481, ORANGE, 's')]:
        z = [x for x in rows if x['N'] == N and x['shift'] == 0.0][0]
        ax.plot([0], [z['B_ref']], marker=mk, ms=5, color=col, ls='none', label=r'$N=%d$, no shift' % N)
    ax.set_xlabel(r'shift $\delta$ of both boundaries'); ax.set_ylabel(r'$B_b(x_{\rm ref})$'); ax.legend(fontsize=7.5)
    ax.set_title('(b) benchmark (finite differences)', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'bias.pdf')); plt.close(fig)

def rho():
    rows = [r for r in load('e4_statics') if r['case'] == 'rho']
    q = np.array([r['q'] for r in rows]); wdt = np.array([r['width1'] for r in rows]); pr = np.array([r['pred1'] for r in rows])
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9))
    ax = axs[0]
    ax.plot(q, pr, color=INK, lw=1.0, ls='-.', label=r'formal $q/(4\Gamma^{\rm ac})$')
    ax.plot(q, wdt, marker='o', ms=4, color=BLUE, ls='none', label='computed half-width')
    for r in rows:
        if abs(r['value']) in (0.8, 0.0):
            ax.annotate(r'$\rho=%.1f$' % r['value'], (r['q'], r['width1']), (r['q'] - 0.02, r['width1'] + 0.03), fontsize=7.5, color=MUTED)
    ax.set_xlabel(r'$q=\sigma_1^2-2\alpha\rho\sigma_1\sigma_2+\alpha^2\sigma_2^2$'); ax.set_ylabel(r'half-width at $(2,2)$'); ax.legend(fontsize=7.5)
    ax = axs[1]
    ax.plot(q, [r['premium_diag2'] for r in rows], marker='o', ms=4, color=BLUE, ls='none', label=r'computed $V-G$ at $(2,2)$')
    g = float(gamma_ac(BASE, 2.0 + 1e-9, 2.0)); ax.plot(q, q / (16 * g), color=INK, lw=1.0, ls='-.', label=r'formal $q/(16\Gamma^{\rm ac})$')
    ax.set_xlabel(r'$q$'); ax.set_ylabel('continuation premium'); ax.legend(fontsize=7.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'rho.pdf')); plt.close(fig)

def mcfig():
    rows = load('e5_mc'); mm = load('e5_mc_M'); ref = -load('e1_refinement')[3]['VmG_ref']
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9))
    ax = axs[0]
    cols = {0.02: YELLOW, 0.01: AQUA, 0.005: ORANGE, 0.0025: BLUE}; mk = {0.02: '^', 0.01: 'D', 0.005: 's', 0.0025: 'o'}
    for r in rows:
        o = np.argsort(r['eps']); e = np.array(r['eps'])[o]; v = np.array([x[0] for x in r['est']])[o]; ci_ = np.array([x[1] for x in r['est']])[o]
        ax.errorbar(e, v, yerr=ci_, marker=mk[r['dt']], ms=4, color=cols[r['dt']], lw=1.2, capsize=2, label=r'$\Delta t=%g$' % r['dt'])
    ax.axhline(ref, color=INK, ls='--', lw=1.0); ax.axvline(0.1, color=MUTED, ls=':', lw=1.0)
    ax.text(0.105, -0.15, r'$\varepsilon=|Y_0|$', color=MUTED, fontsize=7.5); ax.text(0.42, ref + 0.004, 'FD', color=INK, fontsize=7.5)
    ax.set_xscale('log'); ax.set_xticks([0.03, 0.1, 0.3]); ax.set_xticklabels(['0.03', '0.1', '0.3']); ax.minorticks_off(); ax.set_xlabel(r'bandwidth $\varepsilon$'); ax.set_ylabel(r'$\hat P^{\rm gain}(x_{\rm ref})$'); ax.legend(fontsize=7.5)
    ax = axs[1]
    M = [x['M'] for x in mm]; v = [x['est'][0] for x in mm]; c = [x['est'][1] for x in mm]
    ax.errorbar(M, v, yerr=c, marker='o', ms=4, color=BLUE, capsize=2); ax.axhline(ref, color=INK, ls='--', lw=1.0)
    ax.set_xscale('log'); ax.set_xlabel(r'sample size $M$'); ax.set_ylabel(r'$\hat P^{\rm gain}(x_{\rm ref})$')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'mc.pdf')); plt.close(fig)

def alg():
    a = load('alg1_wide'); b = load('alg1_narrow')
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    ax = axs[0]
    for r, col, ls, lab in [(a, BLUE, '-', 'wide start'), (b, ORANGE, '--', 'narrow start')]:
        ax.semilogy([h['k'] for h in r['hist']], [h['err_rms'] for h in r['hist']], color=col, ls=ls, label=lab)
    ax.set_xlabel('iteration'); ax.set_ylabel('r.m.s. distance to FD boundary (nodes)'); ax.legend()
    ax = axs[1]
    s = np.array(a['nodes'])
    ax.plot(a['b1_fd'], s, color=INK, lw=1.2, label='FD boundary'); ax.plot(s, a['b2_fd'], color=INK, lw=1.2)
    for r, col, mk, lab in [(a, BLUE, 'o', 'wide'), (b, ORANGE, 's', 'narrow')]:
        ax.plot(r['hist'][0]['b1'], s, color=col, ls=':', lw=1.0); ax.plot(s, r['hist'][0]['b2'], color=col, ls=':', lw=1.0)
        ax.plot(r['b1_avg'], s, marker=mk, ms=4, color=col, ls='none', label='%s: averaged iterate' % lab)
        ax.plot(s, r['b2_avg'], marker=mk, ms=4, color=col, ls='none')
    ax.plot([0, 2.7], [0, 2.7], color=MUTED, ls='--', lw=0.8)
    ax.set_xlim(0, 2.8); ax.set_ylim(0, 2.8); ax.set_aspect('equal'); ax.set_xlabel(r'$x_1$'); ax.set_ylabel(r'$x_2$'); ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'alg.pdf')); plt.close(fig)

if __name__ == '__main__':
    import sys
    for f in (sys.argv[1:] or ['regions', 'refine', 'loss', 'bias', 'rho', 'mcfig', 'alg']):
        globals()[f](); print('made', f)
