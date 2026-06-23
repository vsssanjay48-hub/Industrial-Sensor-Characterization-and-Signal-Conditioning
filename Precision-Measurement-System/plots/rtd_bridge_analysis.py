"""
rtd_bridge_analysis.py
Plots: RTD R(T), bridge output, non-linearity error, sensitivity vs temperature
Run: python plots/rtd_bridge_analysis.py
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

R0 = 100.0; A = 3.9083e-3; B = -5.7750e-7; alpha = 3.850e-3; V_EX = 5.0

def rtd_R(T):
    T = np.asarray(T, float)
    return np.where(T >= 0, R0*(1+A*T+B*T**2), R0*(1+A*T+B*T**2+(-4.183e-12)*(T-100)*T**3))

def bridge_exact(dR):   return V_EX * dR / (4*R0 + 2*dR)
def bridge_lin(dR):     return V_EX * dR / (4*R0)
def bridge_sens(T):
    T = np.asarray(T, float)
    dR = rtd_R(T) - R0
    dVdR = V_EX * 4*R0 / (4*R0 + 2*dR)**2
    dRdT = np.where(T>=0, R0*(A+2*B*T), R0*(A+2*B*T+4*(-4.183e-12)*(T-100)*T**2+3*(-4.183e-12)*T**3))
    return dVdR * dRdT * 1000  # mV/°C

T_full = np.linspace(-200, 850, 1000)
T_rng  = np.linspace(0, 100, 500)
dR     = rtd_R(T_rng) - R0
Vexact = bridge_exact(dR)*1000
Vlin   = bridge_lin(dR)*1000
NL_mV  = Vlin - Vexact
NL_pct = NL_mV / (bridge_exact(rtd_R(100)-R0)*1000) * 100

fig = plt.figure(figsize=(13, 9))
fig.suptitle("PT100 RTD + Wheatstone Bridge Analysis", fontsize=13, fontweight='bold')
gs  = gridspec.GridSpec(2, 2, hspace=0.38, wspace=0.32)

ax1 = fig.add_subplot(gs[0,0])
ax1.plot(T_full, rtd_R(T_full), 'royalblue', lw=2, label='CVD Equation')
ax1.plot(T_full, R0*(1+alpha*T_full), 'tomato', lw=1.5, ls='--', label='Linear approx')
ax1.set(xlabel='Temperature (°C)', ylabel='Resistance (Ω)', title='PT100 R vs T')
ax1.legend(); ax1.grid(alpha=0.3)

ax2 = fig.add_subplot(gs[0,1])
ax2.plot(T_rng, Vexact, 'royalblue', lw=2, label='Exact bridge')
ax2.plot(T_rng, Vlin, 'tomato', lw=1.5, ls='--', label='Linearized')
ax2.fill_between(T_rng, Vexact, Vlin, alpha=0.15, color='tomato')
ax2.set(xlabel='Temperature (°C)', ylabel='V_out (mV)', title=f'Bridge Output (V_ex={V_EX}V)')
ax2.legend(); ax2.grid(alpha=0.3)

ax3 = fig.add_subplot(gs[1,0])
ax3b = ax3.twinx()
l1, = ax3.plot(T_rng, NL_mV, 'tomato', lw=2, label='NL error (mV)')
l2, = ax3b.plot(T_rng, NL_pct, 'darkorange', lw=1.5, ls=':', label='NL error (%FS)')
ax3.set(xlabel='Temperature (°C)', ylabel='NL Error (mV)')
ax3b.set_ylabel('NL Error (%FS)', color='darkorange')
ax3.set_title('Bridge Non-Linearity Error'); ax3.grid(alpha=0.3)
ax3.legend([l1,l2], [l.get_label() for l in [l1,l2]])

ax4 = fig.add_subplot(gs[1,1])
ax4.plot(T_rng, bridge_sens(T_rng), 'royalblue', lw=2, label='Exact')
ax4.axhline(V_EX*alpha/4*1000, color='tomato', ls='--', lw=1.5, label=f'Constant ({V_EX*alpha/4*1000:.2f} mV/°C)')
ax4.set(xlabel='Temperature (°C)', ylabel='dV/dT (mV/°C)', title='Bridge Sensitivity vs T')
ax4.legend(); ax4.grid(alpha=0.3)

for ax in [ax1,ax2,ax3,ax4]:
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

plt.savefig('plots/rtd_bridge_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved plots/rtd_bridge_analysis.png")
print(f"Max NL error: {NL_mV.max():.2f} mV = {NL_pct.max():.2f}%FS at {T_rng[NL_mV.argmax()]:.1f}°C")
print(f"Sensitivity drop 0→100°C: {(1-bridge_sens(100)/bridge_sens(0))*100:.1f}%")
