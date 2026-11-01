import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "mathtext.fontset": "stix",
    "font.size": 10,
    "axes.linewidth": 0.8,
    "axes.labelsize": 11,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "legend.frameon": False,
    "legend.fontsize": 9,
    "savefig.dpi": 300,
    "axes.unicode_minus": False,
})

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs", "fig")
os.makedirs(OUT, exist_ok=True)

A = (np.sqrt(6.0) + np.sqrt(2.0)) / 2.0
B = (np.sqrt(6.0) - np.sqrt(2.0)) / 2.0
ROOTS = np.array([[A, B], [B, A], [-A, -B], [-B, -A]])
ROOT_COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]


def newton_path(x0, y0, iters=100, tol=1e-10):
    """Return (points, residuals); mirrors function.cpp iteration without perturbation."""
    x, y = float(x0), float(y0)
    pts = [(x, y)]
    res = []
    for _ in range(iters):
        f1 = x * x + y * y - 4.0
        f2 = x * y - 1.0
        r = np.hypot(f1, f2)
        res.append(r)
        if r < tol:
            break
        det = 2.0 * (x * x - y * y)
        if abs(det) < 1e-10 or r > 1e9:
            break
        dx = (f1 * x - 2.0 * y * f2) / det
        dy = (2.0 * x * f2 - f1 * y) / det
        x -= dx
        y -= dy
        pts.append((x, y))
    return np.array(pts), np.array(res)


def fig_geometry():
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    t = np.linspace(0.0, 2.0 * np.pi, 400)
    ax.plot(2.0 * np.cos(t), 2.0 * np.sin(t), color="black", lw=1.2,
            label=r"$x^2+y^2=4$")
    xh = np.linspace(-3.0, -1.0 / 3.0, 400)
    ax.plot(xh, 1.0 / xh, color="black", lw=1.2, ls="--")
    xh = np.linspace(1.0 / 3.0, 3.0, 400)
    ax.plot(xh, 1.0 / xh, color="black", lw=1.2, ls="--", label=r"$xy=1$")
    ax.plot([-3, 3], [-3, 3], color="0.6", lw=0.8, ls=":")
    ax.plot([-3, 3], [3, -3], color="0.6", lw=0.8, ls=":")
    ax.text(2.45, 2.05, r"$x=y$", color="0.45", fontsize=9)
    ax.text(-2.95, 2.2, r"$x=-y$", color="0.45", fontsize=9)
    for k, (rx, ry) in enumerate(ROOTS):
        ax.plot(rx, ry, "o", ms=5, mfc=ROOT_COLORS[k], mec="black", mew=0.6)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend(loc="lower left", handlelength=1.6)
    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, "fig1_geometry.png"))
    plt.close(fig)


def fig_trajectory():
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    g = np.linspace(-3.0, 3.0, 601)
    X, Y = np.meshgrid(g, g)
    F1 = X * X + Y * Y - 4.0
    F2 = X * Y - 1.0
    level = np.log10(np.hypot(F1, F2) + 1e-12)
    cs = ax.contour(X, Y, level, levels=np.arange(-6, 4, 1), colors="0.75",
                    linewidths=0.5)
    ax.clabel(cs, inline=True, fontsize=6, fmt="%d")
    starts = [(2.5, 0.5), (3.0, 1.0), (-1.0, -2.0), (0.5, 2.5)]
    for k, (x0, y0) in enumerate(starts):
        pts, _ = newton_path(x0, y0)
        ax.plot(pts[:, 0], pts[:, 1], "-o", color=ROOT_COLORS[k], lw=1.0, ms=3,
                mfc="white", mew=0.8, label=r"$x_0=(%.1f,\,%.1f)$" % (x0, y0))
    for k, (rx, ry) in enumerate(ROOTS):
        ax.plot(rx, ry, "s", ms=5, mfc=ROOT_COLORS[k], mec="black", mew=0.6)
    ax.plot([-3, 3], [-3, 3], color="0.6", lw=0.8, ls=":")
    ax.plot([-3, 3], [3, -3], color="0.6", lw=0.8, ls=":")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend(loc="upper left", handlelength=1.8)
    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, "fig2_trajectory.png"))
    plt.close(fig)


def fig_residual():
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    starts = [(2.5, 0.5), (3.0, 1.0), (30.0, 0.05)]
    for k, (x0, y0) in enumerate(starts):
        _, res = newton_path(x0, y0)
        ax.semilogy(np.arange(res.size), res, "-o", color=ROOT_COLORS[k], lw=1.0,
                    ms=3.5, mfc="white", mew=0.9,
                    label=r"$x_0=(%.1f,\,%.1f)$" % (x0, y0))
    _, res = newton_path(1.0, 1.0 + 1e-7)
    ax.semilogy(np.arange(res.size), res, "-x", color="0.35", lw=1.0, ms=4,
                label=r"$x_0=(1,\,1+10^{-7})$")
    ax.set_xlabel("iteration $k$")
    ax.set_ylabel(r"$\|F(x_k)\|_2$")
    ax.set_xlim(-0.2, 10.5)
    ax.grid(True, which="major", color="0.9", lw=0.6)
    ax.legend(loc="lower left", handlelength=1.8)
    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, "fig3_residual.png"))
    plt.close(fig)


def fig_basin(n=241, lim=3.0):
    xs = np.linspace(-lim, lim, n)
    X, Y = np.meshgrid(xs, xs)
    x = X.copy()
    y = Y.copy()
    label = np.full(X.shape, -1, dtype=int)
    done = np.zeros(X.shape, dtype=bool)

    for _ in range(100):
        f1 = x * x + y * y - 4.0
        f2 = x * y - 1.0
        r = np.hypot(f1, f2)
        det = 2.0 * (x * x - y * y)
        conv = r < 1e-10
        bad = (np.abs(det) < 1e-10) | (r > 1e9) | ~np.isfinite(r)
        new = conv & ~done
        if new.any():
            d = np.stack([(x - rx) ** 2 + (y - ry) ** 2 for rx, ry in ROOTS])
            label[new] = np.argmin(d, axis=0)[new]
            done[new] = True
        done |= bad
        act = ~done
        if not act.any():
            break
        dx = (f1 * x - 2.0 * y * f2) / np.where(act, det, 1.0)
        dy = (2.0 * x * f2 - f1 * y) / np.where(act, det, 1.0)
        x = np.where(act, x - dx, x)
        y = np.where(act, y - dy, y)

    ok = done & (label >= 0)
    mask = np.ma.masked_where(label < 0, label)
    cmap = ListedColormap(ROOT_COLORS)
    cmap.set_bad("white")

    fig, ax = plt.subplots(figsize=(3.8, 3.3))
    ax.imshow(mask, origin="lower", extent=[-lim, lim, -lim, lim], cmap=cmap,
              vmin=-0.5, vmax=3.5, interpolation="nearest")
    ax.plot([-lim, lim], [-lim, lim], color="black", lw=0.6, ls=":")
    ax.plot([-lim, lim], [lim, -lim], color="black", lw=0.6, ls=":")
    for k, (rx, ry) in enumerate(ROOTS):
        ax.plot(rx, ry, "o", ms=5, mfc="white", mec="black", mew=1.0)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel(r"$x_0$")
    ax.set_ylabel(r"$y_0$")
    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, "fig4_basin.png"))
    plt.close(fig)
    return ok.sum() / label.size


if __name__ == "__main__":
    fig_geometry()
    fig_trajectory()
    fig_residual()
    frac = fig_basin()
    print("roots:", [tuple(np.round(r, 6)) for r in ROOTS])
    print("basin success fraction: %.2f%%" % (100.0 * frac))
