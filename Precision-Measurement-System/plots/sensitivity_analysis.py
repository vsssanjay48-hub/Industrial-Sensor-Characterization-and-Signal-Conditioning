"""
sensitivity_analysis.py
Plots: sensitivity comparison RTD/NTC/TC, RTD dR/dT full range, NTC, ADC resolution
Run: python plots/sensitivity_analysis.py
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

R0=100; A=3.9083e-3; B=-5.775e-7; alpha=3.850e-3
R_NTC=10000; T_NTC=298.15; B_NTC=3950
V_EX=5; G=10; V_FS=5
TC_T=np.array([-200,-100,0,100,300,500,700,1000,1260]); TC_S=np.array([25.3,38,39.4,41.3,41,43.1,41.7,38.3,37])

def rtd_R(T): T=np.asarray(T,float); return np.where(T>=0,R0*(1+A*T+B*T**2),R0*(1+A*T+B*T**2+(-4.183e-12)*(T-100)*T**3))
def rtd_S(T): T=np.asarray(T,float); return np.where(T>=0,R0*(A+2*B*T),R0*(A+2*B*T+4*(-4.183e-12)*(T-100)*T**2+3*(-4.183e-12)*T**3))
def ntc_R(T): T=np.asarray(T,float)+273.15; return R_NTC*np.exp(B_NTC*(1/T-1/T_NTC))
def ntc_S(T): T=np.asarray(T,float)+273.15; return -ntc_R(np.asarray(T,float)-273.15)*B_NTC/T**2
def bridge_S_rtd(T):
    dR=rtd_R(T)-R0; dVdR=V_EX*4*R0/(4*R0+2*dR)**2
    return dVdR*rtd_S(T)*1000
def bridge_S_ntc(T):
    R=ntc_R(T); dR=R-R_NTC; dVdR=V_EX*4*R_NTC/(4*R_NTC+2*dR)**2
    return abs(dVdR*ntc_S(T))*1000
def sk_K(T): return np.interp(T,TC_T,TC_S)

T_comp=np.linspace(0,100,300); T_rtd=np.linspace(-200,850,800); T_ntc=np.linspace(-30,110,500)
S_ina=bridge_S_rtd(T_comp)*G
res12=(V_FS*1000/4096)/S_ina; res16=(V_FS*1000/65536)/S_ina

fig=plt.figure(figsize=(13,9))
fig.suptitle("Sensor Sensitivity Comparison — RTD / NTC / Thermocouple",fontsize=13,fontweight='bold')
gs=gridspec.GridSpec(2,2,hspace=0.40,wspace=0.32)

ax1=fig.add_subplot(gs[0,0])
ax1.plot(T_comp,bridge_S_rtd(T_comp),'royalblue',lw=2,label='RTD bridge (G=1)')
ax1.plot(T_comp,bridge_S_ntc(T_comp),'tomato',lw=2,label='NTC bridge (G=1)')
ax1.plot(T_comp,sk_K(T_comp)/1000*100*1000,'forestgreen',lw=2,label='Type K (G=100 amp)')
ax1.set(xlabel='Temperature (°C)',ylabel='Output Sensitivity (mV/°C)',title='Sensor+Bridge Sensitivity (0–100°C)')
ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

ax2=fig.add_subplot(gs[0,1])
ax2.plot(T_rtd,rtd_S(T_rtd),'royalblue',lw=2)
ax2.axhline(R0*alpha,color='tomato',ls='--',lw=1.5,label=f'Mean α×R₀={R0*alpha:.4f} Ω/°C')
ax2.set(xlabel='Temperature (°C)',ylabel='dR/dT (Ω/°C)',title='RTD PT100 Sensitivity — Full Range')
ax2.legend(); ax2.grid(alpha=0.3)

ax3=fig.add_subplot(gs[1,0])
ax3.semilogy(T_ntc,np.abs(ntc_S(T_ntc)),'tomato',lw=2)
ax3.set(xlabel='Temperature (°C)',ylabel='|dR/dT| (Ω/°C) log scale',title='NTC Sensitivity — 10kΩ B=3950K')
for Tp in [0,25,50,100]:
    s=abs(ntc_S(Tp)); ax3.annotate(f'{Tp}°C\n{s:.0f}',xy=(Tp,s),xytext=(Tp+6,s*1.4),arrowprops=dict(arrowstyle='->',color='gray'),fontsize=7)
ax3.grid(alpha=0.3,which='both')

ax4=fig.add_subplot(gs[1,1])
ax4.plot(T_comp,res12*1000,'darkorange',lw=2,label='12-bit ADC')
ax4.plot(T_comp,res16*1000,'royalblue',lw=2,label='16-bit ADC')
ax4.axhline(100,color='gray',ls=':',lw=1,label='100 m°C')
ax4.axhline(10,color='lightgray',ls=':',lw=1,label='10 m°C')
ax4.set(xlabel='Temperature (°C)',ylabel='Resolution per LSB (m°C)',title=f'ADC Resolution (PT100, G={G}, V_ex={V_EX}V)')
ax4.legend(fontsize=8); ax4.grid(alpha=0.3); ax4.set_ylim(bottom=0)

for ax in [ax1,ax2,ax3,ax4]:
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

plt.savefig('plots/sensitivity_analysis.png',dpi=150,bbox_inches='tight')
plt.show()
print("Saved plots/sensitivity_analysis.png")
print(f"\nAt 25°C:  RTD bridge={bridge_S_rtd(25):.3f} mV/°C  |  NTC bridge={bridge_S_ntc(25):.2f} mV/°C")
print(f"16-bit resolution at 25°C: {(V_FS*1000/65536)/(bridge_S_rtd(25)*G)*1000:.2f} m°C/LSB")
