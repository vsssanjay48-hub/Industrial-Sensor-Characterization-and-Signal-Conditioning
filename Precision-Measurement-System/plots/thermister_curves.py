"""
thermistor_curves.py
Plots: NTC R(T) log curve, sensitivity, Steinhart-Hart residuals, voltage divider
Run: python plots/thermistor_curves.py
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

R_REF=10000; T_REF=298.15; B=3950
SH_A=1.129241e-3; SH_B=2.341077e-4; SH_C=8.775468e-8

def ntc(T_C):
    T = np.asarray(T_C,float)+273.15
    return R_REF*np.exp(B*(1/T-1/T_REF))

def ntc_sens(T_C):
    T = np.asarray(T_C,float)+273.15
    return -ntc(T_C)*B/T**2

def sh_T(R):
    lnR=np.log(np.asarray(R,float))
    return 1/(SH_A+SH_B*lnR+SH_C*lnR**3)-273.15

T = np.linspace(-30, 110, 600)
R = ntc(T); S = ntc_sens(T)
R_fix = np.sqrt(ntc(0)*ntc(80)); V_IN=5.0
Vdiv = V_IN*ntc(T)/(R_fix+ntc(T))

T_cal=np.linspace(0,80,100)
sh_res = sh_T(ntc(T_cal)) - T_cal

fig = plt.figure(figsize=(13,9))
fig.suptitle("NTC Thermistor (10 kΩ, B=3950 K) Characterization", fontsize=13, fontweight='bold')
gs = gridspec.GridSpec(2,2,hspace=0.38,wspace=0.32)

ax1=fig.add_subplot(gs[0,0])
ax1.semilogy(T,R,'royalblue',lw=2); ax1.axvline(25,color='gray',ls=':',lw=1); ax1.axhline(R_REF,color='gray',ls=':',lw=1)
ax1.set(xlabel='Temperature (°C)',ylabel='Resistance (Ω) log scale',title='NTC R vs T'); ax1.grid(alpha=0.3,which='both')

ax2=fig.add_subplot(gs[0,1])
ax2.plot(T,np.abs(S),'tomato',lw=2); ax2.fill_between(T,np.abs(S),alpha=0.15,color='tomato')
s25=abs(ntc_sens(25))
ax2.annotate(f'|S| at 25°C ≈ {s25:.0f} Ω/°C',xy=(25,s25),xytext=(45,s25*0.7),arrowprops=dict(arrowstyle='->',color='gray'),fontsize=8)
ax2.set(xlabel='Temperature (°C)',ylabel='|dR/dT| (Ω/°C)',title='NTC Sensitivity'); ax2.grid(alpha=0.3)

ax3=fig.add_subplot(gs[1,0])
ax3.plot(T_cal,sh_res*1000,'forestgreen',lw=2); ax3.axhline(0,color='k',lw=0.8)
ax3.set(xlabel='Temperature (°C)',ylabel='Residual (m°C)',title='Steinhart-Hart Residuals\n(vs Beta model, 3-pt cal)')
ax3.grid(alpha=0.3)
ax3.text(0.05,0.90,f'Max: ±{np.abs(sh_res).max()*1000:.2f} m°C',transform=ax3.transAxes,fontsize=9,bbox=dict(boxstyle='round',fc='lightgreen',alpha=0.5))

ax4=fig.add_subplot(gs[1,1])
ax4.plot(T,Vdiv,'royalblue',lw=2,label='Actual V_out')
ax4.plot([0,80],[Vdiv[np.argmin(np.abs(T))],Vdiv[np.argmin(np.abs(T-80))]],'tomato',lw=1.5,ls='--',label='Ideal linear')
ax4.set(xlabel='Temperature (°C)',ylabel='V_out (V)',title=f'Voltage Divider (R_fix={R_fix:.0f} Ω)')
ax4.legend(); ax4.grid(alpha=0.3)

for ax in [ax1,ax2,ax3,ax4]:
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

plt.savefig('plots/thermistor_curves.png',dpi=150,bbox_inches='tight')
plt.show()
print("Saved plots/thermistor_curves.png")
for Tp in [-20,0,25,50,100]:
    print(f"T={Tp:4}°C  R={ntc(Tp):8.0f} Ω  dR/dT={ntc_sens(Tp):8.1f} Ω/°C  α={ntc_sens(Tp)/ntc(Tp)*100:.2f}%/°C")
