#!/usr/bin/env python3
"""Quasi-static 2D field solve of a grounded coplanar waveguide (CPWG) cross-section.
Finite-volume Laplace on a uniform grid, conjugate gradient, C from field energy; Z0 = 1/(c*sqrt(C*Ca))."""
import numpy as np, sys
# Model: In1 ground plane at y=0, dielectric h, trace and side grounds of thickness t on top, LPI mask (er 3.8) 30 um over the
# substrate in the gaps and 15 um over copper (JLCPCB C1/C3 = 1.2 mil, C2 = 0.6 mil). Discretisation error is first order in d;
# solve at two grid sizes and extrapolate (Richardson) for a sub-ohm estimate.
EPS0, C0 = 8.854187817e-12, 299792458.0
def solve(W, s, h, er, t=0.035, mask=True, er_mask=3.8, m_sub=0.030, m_cu=0.015, d=0.005, half=1.5, top=1.0):
    h = round(h / d) * d; t = max(round(t / d), 1) * d                     # snap the layers to the grid
    nx = int(round(2 * half / d)) + 1; ny = int(round((h + t + top) / d)) + 1
    x = np.linspace(-half, half, nx); y = np.linspace(0, h + t + top, ny)
    cx = (x[:-1] + x[1:]) / 2; cy = (y[:-1] + y[1:]) / 2
    CX, CY = np.meshgrid(cx, cy, indexing='ij')
    def build(dielectric):
        e = np.ones((nx - 1, ny - 1))
        if not dielectric: return e
        e[CY < h] = er
        if mask:
            sig = np.abs(CX) <= W / 2; gnd = np.abs(CX) >= W / 2 + s
            cu = sig | gnd
            e[(~cu) & (CY >= h) & (CY < h + m_sub)] = er_mask                 # mask in the gaps (C1/C3)
            e[cu & (CY >= h + t) & (CY < h + t + m_cu)] = er_mask             # mask over the copper (C2)
        return e
    X, Y = np.meshgrid(x, y, indexing='ij')
    incu = (Y >= h - 1e-9) & (Y <= h + t + 1e-9)
    sig = incu & (np.abs(X) <= W / 2 + 1e-9)
    gnd = incu & (np.abs(X) >= W / 2 + s - 1e-9)
    fixed = sig | gnd; fixed[:, 0] = True; fixed[:, -1] = True; fixed[0, :] = True; fixed[-1, :] = True
    V0 = np.where(sig, 1.0, 0.0)
    def caps(e):
        # edge coefficients
        ex = np.zeros((nx - 1, ny)); ex[:, 1:-1] = (e[:, :-1] + e[:, 1:]) / 2; ex[:, 0] = e[:, 0] / 2; ex[:, -1] = e[:, -1] / 2
        ey = np.zeros((nx, ny - 1)); ey[1:-1, :] = (e[:-1, :] + e[1:, :]) / 2; ey[0, :] = e[0, :] / 2; ey[-1, :] = e[-1, :] / 2
        def A(V):
            out = np.zeros_like(V)
            fx = ex * (V[1:, :] - V[:-1, :]); fy = ey * (V[:, 1:] - V[:, :-1])
            out[:-1, :] -= fx; out[1:, :] += fx; out[:, :-1] -= fy; out[:, 1:] += fy
            return -out
        free = ~fixed
        b = -A(V0); b[fixed] = 0
        xk = np.zeros_like(V0); r = b.copy(); p = r.copy(); rr = (r * r).sum()
        for it in range(20000):
            Ap = A(p); Ap[fixed] = 0
            a = rr / (p * Ap).sum(); xk += a * p; r -= a * Ap; rn = (r * r).sum()
            if rn < 1e-20 * b.size: break
            p = r + rn / rr * p; rr = rn
        V = V0 + xk
        Wn = (ex * (V[1:, :] - V[:-1, :]) ** 2).sum() + (ey * (V[:, 1:] - V[:, :-1]) ** 2).sum()
        return EPS0 * Wn
    C = caps(build(True)); Ca = caps(build(False))
    return 1 / (C0 * np.sqrt(C * Ca)), C / Ca
if __name__ == '__main__':
    W, s, h, er = map(float, sys.argv[1:5]); z, ee = solve(W, s, h, er); print(f'W={W} s={s} h={h} er={er}: Z0={z:.2f} ohm eeff={ee:.3f}')
