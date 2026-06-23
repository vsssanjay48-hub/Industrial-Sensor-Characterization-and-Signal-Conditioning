"""
error_propagation.py
Plots: error budget, self-heating vs current, lead R error vs length, noise vs BW
Run: python plots/error_propagation.py
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

kB=1.38e-23; T_AMB=300; R0=100; alpha=3.85e-3; rho_Cu=1.72e-8
V_EX=5.0; G_INA=10; S_bridge=V_EX*alpha/4; S_total=G_INA*S_bridge

# Error budget
labels = ['RTD Class B tolerance','Lead R (10m 0.5mm²)','Self-heating (1mA air)','Amp offset drift','Ref voltage error','EMI/noise']
v2w = np.array([0.30, 1.79, 0.02, 0.05, 0.10, 0.05])
v4w = np.array([0.30, 0.00, 0.02, 0.05, 0.10, 0.05])
rss2=np.sqrt((v2w**2).sum()); rss4=np.sqrt((v4w**2).sum())

I   = np.linspace(0.1e-3, 5e-3, 400)
Rth = {'Still air (200K/W)':200,'Flowing air (80K/W)':80,'Still water (30K/W)':30,'Flowing water (10K/W)':10}
L   = np.linspace(1,100,200)
gauges = {'0.5 mm²':0.5e-6,'1.0 mm²':1.0e-6,'2.5 mm²':2.5e-6}
BW  = np.logspace(-2,3,400); en=10e-9

fig = plt.figure(figsize=(13,9))
fig.suptitle("Error Propagation Analysis — RTD Measurement System", fontsize=13, fontweight='bold')
gs = gridspec.GridSpec(2,2,hspace=0.42,wspace=0.35)

ax1=fig.add_subplot(gs[0,0])
x=np.arange(len(labels))
ax1.barh(x+0.2,v2w,0.38,label=f'2-Wire RSS={rss2:.2f}°C',color='tomato',alpha=0.85)
ax1.barh(x-0.2,v4w,0.38,label=f'4-Wire RSS={rss4:.2f}°C',color='steelblue',alpha=0.85)
ax1.axvline(rss2,color='tomato',ls='--',lw=1.5); ax1.axvline(rss4,color='steelblue',ls='--',lw=1.5)
ax1.set_yticks(x); ax1.set_yticklabels(labels,fontsize=8)
ax1.set(xlabel='Error (°C)',title='Error Budget: 2-Wire vs 4-Wire RTD'); ax1.legend(fontsize=8); ax1.grid(alpha=0.3,axis='x')

ax2=fig.add_subplot(gs[0,1])
colors=['royalblue','steelblue','tomato','orangered']
for (lbl,rth),c in zip(Rth.items(),colors):
    ax2.plot(I*1000, rth*I**2*R0, lw=2, label=lbl, color=c)
ax2.axhline(0.1,color='gray',ls=':',lw=1.5,label='0.1°C limit')
ax2.set(xlabel='Excitation Current (mA)',ylabel='Self-Heating Error (°C)',title='Self-Heating vs Current (PT100)')
ax2.legend(fontsize=8); ax2.grid(alpha=0.3); ax2.set_ylim(bottom=0)

ax3=fig.add_subplot(gs[1,0])
colors3=['royalblue','forestgreen','tomato']
for (lbl,A_w),c in zip(gauges.items(),colors3):
    ax3.plot(L, 2*rho_Cu*L/A_w/(alpha*R0), lw=2, label=lbl, color=c)
ax3.axhline(0.5,color='gray',ls=':',lw=1.5,label='0.5°C limit')
ax3.set(xlabel='Cable Length (m)',ylabel='Temperature Error (°C)',title='2-Wire Lead R Error vs Length (PT100, Cu)')
ax3.legend(fontsize=8); ax3.grid(alpha=0.3); ax3.set_ylim(bottom=0)

ax4=fig.add_subplot(gs[1,1])
Vn_RTD = np.sqrt(4*kB*T_AMB*R0*BW)
Vn_INA = en*np.sqrt(BW)
Vn_tot = np.sqrt(Vn_RTD**2+Vn_INA**2)
ax4.loglog(BW,Vn_RTD/S_bridge*1000,'royalblue',lw=1.5,ls='--',label='RTD Johnson noise')
ax4.loglog(BW,Vn_INA/S_bridge*1000,'tomato',lw=1.5,ls='--',label='INA noise (10nV/√Hz)')
ax4.loglog(BW,Vn_tot/S_bridge*1000,'k',lw=2,label='Total')
ax4.set(xlabel='Bandwidth (Hz)',ylabel='Temp noise floor (m°C rms)',title='Noise-Limited Resolution vs BW')
ax4.legend(fontsize=8); ax4.grid(alpha=0.3,which='both')

for ax in [ax1,ax2,ax3,ax4]:
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

plt.savefig('plots/error_propagation.png',dpi=150,bbox_inches='tight')
plt.show()
print(f"Saved plots/error_propagation.png")
print(f"2-wire RSS: ±{rss2:.3f}°C  |  4-wire RSS: ±{rss4:.3f}°C  |  Improvement: {rss2/rss4:.1f}×")
