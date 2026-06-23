"""
calibration_plot.py
Plots: raw vs ref, before/after correction, residuals, CVD inverse accuracy
Run: python plots/calibration_plot.py
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

np.random.seed(42)
R0=100; A=3.9083e-3; B=-5.7750e-7

def cvd(T): T=np.asarray(T,float); return np.where(T>=0,R0*(1+A*T+B*T**2),R0*(1+A*T+B*T**2+(-4.183e-12)*(T-100)*T**3))
def cvd_inv(R):
    R=np.asarray(R,float); a=B*R0; b=A*R0; c=R0-R
    return (-b+np.sqrt(b**2-4*a*c))/(2*a)

T_ref = np.array([0,10,20,30,40,50,60,70,80,90,100],float)
R_meas = cvd(T_ref)*1.003 + 0.5 + np.random.normal(0,0.05,len(T_ref))
T_raw = cvd_inv(R_meas)
poly = np.poly1d(np.polyfit(T_raw, T_ref, 2))
T_cor = poly(T_raw)
res_raw = T_raw - T_ref
res_cor = T_cor - T_ref

T_dns=np.linspace(0,100,500)
T_raw_dns=cvd_inv(cvd(T_dns)*1.003+0.5)
T_cor_dns=poly(T_raw_dns)

fig=plt.figure(figsize=(13,9))
fig.suptitle("RTD Calibration — Multi-Point Polynomial Correction",fontsize=13,fontweight='bold')
gs=gridspec.GridSpec(2,2,hspace=0.40,wspace=0.35)

ax1=fig.add_subplot(gs[0,0])
ax1.plot([0,100],[0,100],'k--',lw=1,label='Ideal')
ax1.plot(T_ref,T_raw,'o',color='tomato',ms=6,label='Raw DUT')
ax1.plot(T_dns,T_raw_dns,'tomato',lw=1.5,alpha=0.5)
ax1.set(xlabel='T_reference (°C)',ylabel='T_DUT raw (°C)',title='Raw DUT vs Reference')
ax1.legend(); ax1.grid(alpha=0.3)

ax2=fig.add_subplot(gs[0,1])
ax2.plot([0,100],[0,100],'k--',lw=1,label='Ideal')
ax2.plot(T_ref,T_raw,'o',color='tomato',ms=5,label='Before calibration')
ax2.plot(T_ref,T_cor,'s',color='royalblue',ms=5,label='After calibration')
ax2.plot(T_dns,T_cor_dns,'royalblue',lw=1.5,alpha=0.5)
ax2.set(xlabel='T_reference (°C)',ylabel='T_DUT (°C)',title='Before vs After Calibration')
ax2.legend(); ax2.grid(alpha=0.3)

ax3=fig.add_subplot(gs[1,0])
ax3.plot(T_ref,res_raw,'o-',color='tomato',lw=1.5,ms=5,label='Before')
ax3.plot(T_ref,res_cor,'s-',color='royalblue',lw=1.5,ms=5,label='After')
ax3.axhline(0,color='k',lw=0.8)
ax3.fill_between(T_ref,res_raw,alpha=0.1,color='tomato'); ax3.fill_between(T_ref,res_cor,alpha=0.12,color='royalblue')
ax3.set(xlabel='T_reference (°C)',ylabel='Error: T_DUT − T_ref (°C)',title='Calibration Residuals')
ax3.legend(); ax3.grid(alpha=0.3)
ax3.text(0.03,0.85,f'Max before: ±{np.abs(res_raw).max():.2f}°C\nMax after:   ±{np.abs(res_cor).max():.3f}°C',
         transform=ax3.transAxes,fontsize=9,bbox=dict(boxstyle='round',fc='lightyellow',alpha=0.8))

ax4=fig.add_subplot(gs[1,1])
T_t=np.linspace(0,100,300); err=cvd_inv(cvd(T_t))-T_t
ax4.plot(T_t,err*1e6,'forestgreen',lw=2); ax4.axhline(0,color='k',lw=0.8)
ax4.set(xlabel='Temperature (°C)',ylabel='Inversion Error (μ°C)',title='CVD Quadratic Inverse Accuracy')
ax4.grid(alpha=0.3)
ax4.text(0.05,0.88,f'Max numerical error: {np.abs(err).max()*1e6:.3f} μ°C\n(Analytic inverse is exact)',
         transform=ax4.transAxes,fontsize=9,bbox=dict(boxstyle='round',fc='lightgreen',alpha=0.5))

for ax in [ax1,ax2,ax3,ax4]:
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

plt.savefig('plots/calibration_plot.png',dpi=150,bbox_inches='tight')
plt.show()
print("Saved plots/calibration_plot.png")
print(f"\nMax error before calibration: ±{np.abs(res_raw).max():.3f}°C")
print(f"Max error after  calibration: ±{np.abs(res_cor).max():.4f}°C")
print(f"Improvement: {np.abs(res_raw).max()/np.abs(res_cor).max():.0f}×")
