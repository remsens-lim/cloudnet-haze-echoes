import numpy.ma as ma
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MultipleLocator
import cmaps
import datetime
def plot_overview(start, end , prob_calc):
    fig = plt.figure(figsize=(20, 15))

    ax1 = fig.add_subplot(4,2,1)     # 3 rows, 4 columns, 4rd cell
    ax2 = fig.add_subplot(4,2,3)

    ax3 = fig.add_subplot(4,2,5)
    ax4 = fig.add_subplot(4,2,7)     # 3 rows, 4 columns, 4rd cell

    ax5 = fig.add_subplot(4,2,2)
    ax6 = fig.add_subplot(4,2,4)
    ax7 = fig.add_subplot(4,2,6)
    ax8 = fig.add_subplot(4,2,8)

    sdate = start
    xmin, xmax = mdates.date2num(start), mdates.date2num(end)

    cp1 = ax1.pcolormesh(prob_calc.time, prob_calc.height / 1000., prob_calc.Ze.T,
                         cmap = cmaps.colorblind_jet, vmin = -70, vmax = 30)
    divider1 = make_axes_locatable(ax1)
    cax1 = divider1.append_axes("right", size="3%", pad=0.25)
    cbar1 = plt.colorbar(cp1, cax=cax1, ax=ax1, fraction=0.13, pad=0.025)
    cbar1.ax.tick_params(axis='both', which='major', labelsize=16, width=2, length=4)
    cbar1.ax.tick_params(axis='both', which='minor', width=2, length=3)
    cbar1.ax.set_ylabel('Radar reflectivity\n factor (dBZ)', fontsize=18)


    cp2 = ax2.pcolormesh(prob_calc.time, prob_calc.height / 1000., prob_calc.vel.T, cmap = cmaps.velocity_map, vmin = -3, vmax = 3)

    divider2 = make_axes_locatable(ax2)
    cax2 = divider2.append_axes("right", size="3%", pad=0.25)
    cbar2 = plt.colorbar(cp2, cax=cax2, ax=ax2, fraction=0.13, pad=0.025)
    cbar2.ax.tick_params(axis='both', which='major', labelsize=16, width=2, length=4)
    cbar2.ax.tick_params(axis='both', which='minor', width=2, length=3)
    cbar2.ax.set_ylabel('Doppler velocity (m/s)', fontsize=18)


    cp3 = ax3.pcolormesh(prob_calc.time, prob_calc.height / 1000., prob_calc.betas[:,:].T,
                         cmap =cmaps.backscatter_map, vmin = 0, vmax = 1.5e-5)
    divider3 = make_axes_locatable(ax3)
    cax3 = divider3.append_axes("right", size="3%", pad=0.25)
    cbar3 = plt.colorbar(cp3, cax=cax3, ax=ax3, fraction=0.13, pad=0.025)
    cbar3.ax.tick_params(axis='both', which='major', labelsize=16, width=2, length=4)
    cbar3.ax.tick_params(axis='both', which='minor', width=2, length=3)
    cbar3.ax.set_ylabel('Attenuated backscatter\n coefficient (sr$^{-1}$ m$^{-1}$)', fontsize=18)
    cbar3.ax.yaxis.get_offset_text().set_fontsize(16)  # Adjust the fontsize as needed





    cp4 = ax4.pcolormesh(prob_calc.time, prob_calc.height / 1000., ma.masked_where(prob_calc.new_classification==8,prob_calc.new_classification),
                         cmap = cmaps.cloudnet_haze, vmin = 0, vmax = 12)

    divider4 = make_axes_locatable(ax4)
    cax4 = divider4.append_axes("right", size="3%", pad=0.25)
    cbar4 = plt.colorbar(cp4, cax=cax4, ax=ax4, fraction=0.13, pad=0.025)
    cbar4.ax.tick_params(axis='both', which='major', labelsize=16, width=2, length=4)
    cbar4.ax.tick_params(axis='both', which='minor', width=2, length=3)
    cbar4.ax.set_ylabel('Target classification', fontsize=18)
    categories = [
                       "Clear sky",
                       "Cloud droplets only",
                       "Drizzle or rain",
                       "Drizzle/rain & cloud droplets",
                       "Ice",
                       "Ice & supercooled droplets",
                       "Melting ice",
                       "Melting ice & cloud droplets",
                       "Aerosol",
                       "Insects",
                       "Aerosol & insects",
                       "Haze echos",
                   ]

    cbar4.set_ticks(np.arange(0.5,12.5,1))
    cbar4.ax.set_yticklabels(categories)



    cp5 = ax5.pcolormesh(prob_calc.time, prob_calc.height / 1000.,
                         prob_calc.Ze_prob.T * 100, cmap = cmaps.probability_map, vmin = 0, vmax = 100)
    divider5 = make_axes_locatable(ax5)
    cax5 = divider5.append_axes("right", size="3%", pad=0.25)
    cbar5 = plt.colorbar(cp5, cax=cax5, ax=ax5, fraction=0.13, pad=0.025)
    cbar5.ax.tick_params(axis='both', which='major', labelsize=16, width=2, length=4)
    cbar5.ax.tick_params(axis='both', which='minor', width=2, length=3)
    cbar5.ax.set_ylabel('Probability (%)\n(Radar reflectivity factor)', fontsize=18)

    cp6 = ax6.pcolormesh(prob_calc.time, prob_calc.height / 1000.,
                         prob_calc.vel_prob.T * 100, cmap = cmaps.probability_map, vmin = 0, vmax = 100)
    divider6 = make_axes_locatable(ax6)
    cax6 = divider6.append_axes("right", size="3%", pad=0.25)
    cbar6 = plt.colorbar(cp6, cax=cax6, ax=ax6, fraction=0.13, pad=0.025)
    cbar6.ax.tick_params(axis='both', which='major', labelsize=16, width=2, length=4)
    cbar6.ax.tick_params(axis='both', which='minor', width=2, length=3)
    cbar6.ax.set_ylabel('Probability (%)\n(Doppler velocity)', fontsize=18)

    cp7 = ax7.pcolormesh(prob_calc.time, prob_calc.height / 1000.,
                         ma.masked_where(prob_calc.betas == False, prob_calc.beta_prob[:,:]).T * 100, cmap = cmaps.probability_map, vmin = 0, vmax = 100)
    divider7 = make_axes_locatable(ax7)
    cax7 = divider7.append_axes("right", size="3%", pad=0.25)
    cbar7 = plt.colorbar(cp7, cax=cax7, ax=ax7, fraction=0.13, pad=0.025)
    cbar7.ax.tick_params(axis='both', which='major', labelsize=16, width=2, length=4)
    cbar7.ax.tick_params(axis='both', which='minor', width=2, length=3)
    cbar7.ax.set_ylabel('Probability (%)\n(Attenuated backscatter\n coefficient) ', fontsize=18)

    combi = (prob_calc.vel_prob.T*prob_calc.Ze_prob.T*prob_calc.beta_prob.T)*100
    cp8 = ax8.pcolormesh(prob_calc.time, prob_calc.height / 1000.,
                         combi, cmap = cmaps.probability_map, vmin = 0, vmax = 100)
    divider8 = make_axes_locatable(ax8)
    cax8 = divider8.append_axes("right", size="3%", pad=0.25)
    cbar8 = plt.colorbar(cp8, cax=cax8, ax=ax8, fraction=0.13, pad=0.025)
    cbar8.ax.tick_params(axis='both', which='major', labelsize=16, width=2, length=4)
    cbar8.ax.tick_params(axis='both', which='minor', width=2, length=3)
    cbar8.ax.set_ylabel('Probaility (%)\n(Target classification)', fontsize=18)

    cbh_plot = ma.masked_where(prob_calc.cloud_base/1000.>3, prob_calc.cloud_base/1000.)
    cbh_lower = ma.masked_where(cbh_plot > 1, cbh_plot).filled(np.nan)
    cbh_upper = ma.masked_where(cbh_plot < 1, cbh_plot).filled(np.nan)

    for ax in (ax1, ax2,  ax3, ax4, ax5, ax6, ax7, ax8):

        ax.step(prob_calc.time, cbh_upper,where='mid', linewidth = 2.5, label = 'CBH', color = 'black')
        ax.step(prob_calc.time, cbh_lower,where='mid', linewidth = 2.5, label = 'CBH', color = 'black')

        ax.set_xlim(xmin, xmax)
        ax.tick_params(axis='both', which='major',  width=3, length=5.5)
        ax.tick_params(axis='both', which='minor', width=2, length=3)
        ax.set_ylabel('Height (km)')
        ax.set_xlabel('Time (UTC)')
        ax.set_ylim(0,4.5)

        time_difference = end - start
        if time_difference >= datetime.timedelta(hours=12):
            ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(matplotlib.dates.HourLocator(interval = 3))
            ax.xaxis.set_minor_locator(matplotlib.dates.MinuteLocator(interval = 30))

        elif time_difference <= datetime.timedelta(hours=12):
            ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval = 30))
            ax.xaxis.set_minor_locator(matplotlib.dates.MinuteLocator(interval = 5))

        elif time_difference <= datetime.timedelta(hours=2):
            ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval = 15))
            ax.xaxis.set_minor_locator(matplotlib.dates.SecondLocator(interval = 30))

        ax.yaxis.set_major_locator(MultipleLocator(1.))
        ax.yaxis.set_minor_locator(MultipleLocator(0.25))
        ax.tick_params(axis='both', which='major',  width=3, length=5.5)
        ax.tick_params(axis='both', which='minor', width=2, length=3)
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(18)


    ax1.annotate('a)', xy=(0.98, 0.98), xycoords='axes fraction',fontsize=18,fontweight = 'bold', ha='right', va='top')
    ax2.annotate('c)', xy=(0.98, 0.98), xycoords='axes fraction',fontsize=18,fontweight = 'bold', ha='right', va='top')
    ax3.annotate('e)', xy=(0.98, 0.98), xycoords='axes fraction',fontsize=18,fontweight = 'bold', ha='right', va='top')
    ax4.annotate('g)', xy=(0.98, 0.98), xycoords='axes fraction',fontsize=18,fontweight = 'bold', ha='right', va='top')

    ax5.annotate('b)', xy=(0.98, 0.98), xycoords='axes fraction',fontsize=18,fontweight = 'bold', ha='right', va='top')
    ax6.annotate('d)', xy=(0.98, 0.98), xycoords='axes fraction',fontsize=18,fontweight = 'bold', ha='right', va='top')
    ax7.annotate('f)', xy=(0.98, 0.98), xycoords='axes fraction',fontsize=18,fontweight = 'bold', ha='right', va='top')
    ax8.annotate('h)', xy=(0.98, 0.98), xycoords='axes fraction',fontsize=18,fontweight = 'bold', ha='right', va='top')

    plt.tight_layout()
    return fig

#def plot_prob_function(prob_calc):
