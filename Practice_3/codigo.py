import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
from pathlib import Path
from astropy.timeseries import LombScargle

tess_list = sorted(glob.glob('/Users/rm/U/Astroinformatica/Practice_2/tess_curve*.csv'))
frames = []
for path in tess_list:
    tmp = pd.read_csv(path, usecols=['TIME', 'PDCSAP_FLUX', 'PDCSAP_FLUX_ERR'])
    tmp = tmp.dropna(subset=['TIME', 'PDCSAP_FLUX', 'PDCSAP_FLUX_ERR'])
    tmp['CURVE'] = Path(path).stem
    frames.append(tmp)

df = pd.concat(frames, ignore_index=True)

for i in np.unique(df['CURVE']):
    time = df[df['CURVE'] == i]['TIME'].to_numpy()
    flux = df[df['CURVE'] == i]['PDCSAP_FLUX'].to_numpy()
    error = df[df['CURVE'] == i]['PDCSAP_FLUX_ERR'].to_numpy()

    #Statistics

    mean_flux = np.mean(flux)
    median_flux = np.median(flux)
    std_flux = np.std(flux)
    upper_limit = mean_flux + 3 * std_flux
    lower_limit = mean_flux - 3 * std_flux

    outliers = (flux > upper_limit) | (flux < lower_limit)

    fig = plt.figure(figsize=(13, 8))

    #Light Curve Plot

    gs = fig.add_gridspec(2, 2, height_ratios=[1.3, 1], hspace=0.3, wspace=0.3)
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])

    ax1.errorbar(time, flux, yerr=error, ecolor='0.5', elinewidth=0.8, capsize=0, zorder=1, fmt='none', alpha=0.5, label='Flux with error bars')
    ax1.scatter(time[outliers], flux[outliers], color='red', marker='*', s=6, alpha=0.5, label='Outliers')
    ax1.axhline(mean_flux, color='g', linestyle='--', label=f'Mean Flux: {mean_flux:.2f}')
    ax1.axhline(median_flux, color='b', linestyle='--', label=f'Median Flux: {median_flux:.2f}')
    ax1.axhline(upper_limit, color='r', linestyle='--', label=r'Upper Limit (Mean + $3\sigma$)')
    ax1.axhline(lower_limit, color='r', linestyle='--', label=r'Lower Limit (Mean - $3\sigma$)')
    ax1.set_title(f'Light Curve: {i}')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('PDCSAP_FLUX')
    ax1.legend()

    #Lomb-Scargle Periodogram

    ls = LombScargle(time, flux, error)
    frec, power = ls.autopower(samples_per_peak=10, normalization='psd')

    period = 1 / frec

    best_idx = np.argmax(power)
    best_period = period[best_idx]
    best_power = power[best_idx]

    fap01 = ls.false_alarm_level(0.1)
    fap = ls.false_alarm_probability(best_power)

    # Plotting the Lomb-Scargle periodogram and phase-folded light curve

    ax2.plot(period, power, color='k', lw=1)
    ax2.axhline(fap01, color='r', linestyle='--', label='FAP = 1%')
    ax2.axvline(best_period, color='b', linestyle='--', label=f'Best Period: {best_period:.4f}')
    ax2.set_title('Lomb-Scargle Periodogram')
    ax2.set_xlabel('Period')
    ax2.set_ylabel('Power')
    ax2.legend()
    ax2.set_xscale('log')

    # Phase

    phase = (time % best_period) / best_period

    idx = np.argsort(phase)
    phase_sorted = phase[idx]
    flux_sorted = flux[idx]
    error_sorted = error[idx]

    phase_plot = np.concatenate([phase_sorted, phase_sorted + 1])
    flux_plot = np.concatenate([flux_sorted, flux_sorted])
    error_plot = np.concatenate([error_sorted, error_sorted])

    # Phase-Folded Light Curve

    ax3.errorbar(phase_plot, flux_plot, yerr=error_plot, ecolor='0.7', elinewidth=0.5, capsize=0, zorder=1, fmt='none', alpha=0.5)
    ax3.scatter(phase_plot, flux_plot, color='k', s=1, alpha=0.5)
    ax3.set_title(f'Phase-Folded Light Curve (Period = {best_period:.4f})')
    ax3.set_xlabel('Phase')
    ax3.set_ylabel('PDCSAP_FLUX')

    plt.tight_layout()
    plt.savefig(f'light_curve_{i}.pdf', format='pdf', dpi=300)

    plt.show()