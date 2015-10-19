# Standard
import os
import sys
import gc

# Third Party
import numpy as np
from netCDF4 import Dataset
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns
import pyfilm as pf
plt.rcParams.update({'figure.autolayout': True})
mpl.rcParams['axes.unicode_minus']=False

#local
from run import Run
import plot_style
import field_helper as field
plot_style.white()

def phi_film(run):
    """
    Create film of electrostatic potential.
    """
    print('Reading phi...')
    run.phi = field.get_field(run.cdf_file, 'phi_igomega_by_mode', None)
    run.phi = field.field_to_real_space(run.phi)*run.rho_star

    contours = field.calculate_contours(run.phi)

    plot_options = {'levels':contours, 'cmap':'seismic'}
    options = {'file_name':'phi',
               'film_dir':'analysis/moments',
               'frame_dir':'analysis/moments/film_frames',
               'aspect':'equal',
               'xlabel':r'$x (m)$',
               'ylabel':r'$y (m)$',
               'cbar_ticks':5,
               'cbar_label':r'$\varphi$',
               'bbox_inches':'tight',
               'fps':30}

    options['title'] = []
    for it in range(run.nt):
        options['title'].append(r'Time = {0:04d} $\mu s$'.format(
                                int(np.round((run.t[it]-run.t[0])*1e6))))

    pf.make_film_2d(run.x, run.y, run.phi, plot_options=plot_options, options=options)

    run.phi = None
    gc.collect()

def ntot_film(run):
    """
    Create film of density fluctuations.
    """

    print('Reading ntot_i...')
    run.ntot_i = field.get_field(run.cdf_file, 'ntot_igomega_by_mode', 0)
    print('Reading ntot_e...')
    run.ntot_e = field.get_field(run.cdf_file, 'ntot_igomega_by_mode', 1)

    # Convert to real space
    run.ntot_i = field.field_to_real_space(run.ntot_i)*run.rho_star
    run.ntot_e = field.field_to_real_space(run.ntot_e)*run.rho_star

    # Ion density film
    contours = field.calculate_contours(run.ntot_i)

    plot_options = {'levels':contours, 'cmap':'seismic'}
    options = {'file_name':'ntot_i',
               'film_dir':'analysis/moments',
               'frame_dir':'analysis/moments/film_frames',
               'aspect':'equal',
               'xlabel':r'$x (m)$',
               'ylabel':r'$y (m)$',
               'cbar_ticks':5,
               'cbar_label':r'$\delta n_i / n_r$',
               'bbox_inches':'tight',
               'fps':30}

    options['title'] = []
    for it in range(run.nt):
        options['title'].append(r'Time = {0:04d} $\mu s$'.format(
                                int(np.round((run.t[it]-run.t[0])*1e6))))

    pf.make_film_2d(run.x, run.y, run.ntot_i, plot_options=plot_options, options=options)

    run.ntot_i = None
    gc.collect()

    #Electron density film
    contours = field.calculate_contours(run.ntot_e)

    plot_options = {'levels':contours, 'cmap':'seismic'}
    options = {'file_name':'ntot_e',
               'film_dir':'analysis/moments',
               'frame_dir':'analysis/moments/film_frames',
               'aspect':'equal',
               'xlabel':r'$x (m)$',
               'ylabel':r'$y (m)$',
               'cbar_ticks':5,
               'cbar_label':r'$\delta n_e / n_r$',
               'bbox_inches':'tight',
               'fps':30}

    options['title'] = []
    for it in range(run.nt):
        options['title'].append(r'Time = {0:04d} $\mu s$'.format(
                                int(np.round((run.t[it]-run.t[0])*1e6))))

    pf.make_film_2d(run.x, run.y, run.ntot_e, plot_options=plot_options, options=options)

    run.ntot_e = None
    gc.collect()

def upar_film(run):
    """
    Make film of parallel velocity.
    """

    run.upar_i = field.get_field(run.cdf_file, 'upar_igomega_by_mode', 0)
    run.upar_e = field.get_field(run.cdf_file, 'upar_igomega_by_mode', 1)

    run.upar_i = field.field_to_real_space(run.upar_i)*run.rho_star
    run.upar_e = field.field_to_real_space(run.upar_e)*run.rho_star

    # Ion upar film
    contours = field.calculate_contours(run.upar_i)

    plot_options = {'levels':contours, 'cmap':'seismic'}
    options = {'file_name':'upar_i',
               'film_dir':'analysis/moments',
               'frame_dir':'analysis/moments/film_frames',
               'aspect':'equal',
               'xlabel':r'$x (m)$',
               'ylabel':r'$y (m)$',
               'cbar_ticks':5,
               'cbar_label':r'$u_{i, \parallel}$',
               'bbox_inches':'tight',
               'fps':30}

    options['title'] = []
    for it in range(run.nt):
        options['title'].append(r'Time = {0:04d} $\mu s$'.format(
                                int(np.round((run.t[it]-run.t[0])*1e6))))

    pf.make_film_2d(run.x, run.y, run.upar_i, plot_options=plot_options, options=options)

    run.upar_i = None
    gc.collect()

    # Electron upar film
    contours = field.calculate_contours(run.upar_e)

    plot_options = {'levels':contours, 'cmap':'seismic'}
    options = {'file_name':'upar_e',
               'film_dir':'analysis/moments',
               'frame_dir':'analysis/moments/film_frames',
               'aspect':'equal',
               'xlabel':r'$x (m)$',
               'ylabel':r'$y (m)$',
               'cbar_ticks':5,
               'cbar_label':r'$u_{e, \parallel}$',
               'bbox_inches':'tight',
               'fps':30}

    options['title'] = []
    for it in range(run.nt):
        options['title'].append(r'Time = {0:04d} $\mu s$'.format(
                                int(np.round((run.t[it]-run.t[0])*1e6))))

    pf.make_film_2d(run.x, run.y, run.upar_e, plot_options=plot_options, options=options)

    run.upar_e = None
    gc.collect()

def tpar_film(run):
    """
    Make film of parallel temperature.
    """

    run.tpar_i = field.get_field(run.cdf_file, 'tpar_igomega_by_mode', 0)
    run.tpar_e = field.get_field(run.cdf_file, 'tpar_igomega_by_mode', 1)

    # Convert to real space
    run.tpar_i = field.field_to_real_space(run.tpar_i)*run.rho_star
    run.tpar_e = field.field_to_real_space(run.tpar_e)*run.rho_star

    # Ion updar film
    contours = field.calculate_contours(run.tpar_i)

    plot_options = {'levels':contours, 'cmap':'seismic'}
    options = {'file_name':'tpar_i',
               'film_dir':'analysis/moments',
               'frame_dir':'analysis/moments/film_frames',
               'aspect':'equal',
               'xlabel':r'$x (m)$',
               'ylabel':r'$y (m)$',
               'cbar_ticks':5,
               'cbar_label':r'$\delta T_{i, \parallel} / T_r$',
               'bbox_inches':'tight',
               'fps':30}

    options['title'] = []
    for it in range(run.nt):
        options['title'].append(r'Time = {0:04d} $\mu s$'.format(
                                int(np.round((run.t[it]-run.t[0])*1e6))))

    pf.make_film_2d(run.x, run.y, run.tpar_i, plot_options=plot_options, options=options)

    run.tpar_i = None
    gc.collect()

    # Electron updar film
    contours = field.calculate_contours(run.tpar_e)

    plot_options = {'levels':contours, 'cmap':'seismic'}
    options = {'file_name':'tpar_e',
               'film_dir':'analysis/moments',
               'frame_dir':'analysis/moments/film_frames',
               'aspect':'equal',
               'xlabel':r'$x (m)$',
               'ylabel':r'$y (m)$',
               'cbar_ticks':5,
               'cbar_label':r'$\delta T_{e, \parallel} / T_r$',
               'bbox_inches':'tight',
               'fps':30}

    options['title'] = []
    for it in range(run.nt):
        options['title'].append(r'Time = {0:04d} $\mu s$'.format(
                                int(np.round((run.t[it]-run.t[0])*1e6))))

    pf.make_film_2d(run.x, run.y, run.tpar_e, plot_options=plot_options, options=options)

    run.tpar_e = None
    gc.collect()

def tperp_film(run):
    """
    Make film of perpendicular temperature.
    """

    run.tperp_i = field.get_field(run.cdf_file, 'tperp_igomega_by_mode', 0)
    run.tperp_e = field.get_field(run.cdf_file, 'tperp_igomega_by_mode', 1)

    # Convert to real space
    run.tperp_i = field.field_to_real_space(run.tperp_i)*run.rho_star
    run.tperp_e = field.field_to_real_space(run.tperp_e)*run.rho_star

    # Ion updar film
    contours = field.calculate_contours(run.tperp_i)

    plot_options = {'levels':contours, 'cmap':'seismic'}
    options = {'file_name':'tperp_i',
               'film_dir':'analysis/moments',
               'frame_dir':'analysis/moments/film_frames',
               'aspect':'equal',
               'xlabel':r'$x (m)$',
               'ylabel':r'$y (m)$',
               'cbar_ticks':5,
               'cbar_label':r'$\delta T_{i, \perp} / T_r$',
               'bbox_inches':'tight',
               'fps':30}

    options['title'] = []
    for it in range(run.nt):
        options['title'].append(r'Time = {0:04d} $\mu s$'.format(
                                int(np.round((run.t[it]-run.t[0])*1e6))))

    pf.make_film_2d(run.x, run.y, run.tperp_i, plot_options=plot_options, options=options)

    run.tperp_i = None
    gc.collect()

    # Electron updar film
    contours = field.calculate_contours(run.tperp_e)

    plot_options = {'levels':contours, 'cmap':'seismic'}
    options = {'file_name':'tperp_e',
               'film_dir':'analysis/moments',
               'frame_dir':'analysis/moments/film_frames',
               'aspect':'equal',
               'xlabel':r'$x (m)$',
               'ylabel':r'$y (m)$',
               'cbar_ticks':5,
               'cbar_label':r'$\delta T_{e, \perp} / T_r$',
               'bbox_inches':'tight',
               'fps':30}

    options['title'] = []
    for it in range(run.nt):
        options['title'].append(r'Time = {0:04d} $\mu s$'.format(
                                int(np.round((run.t[it]-run.t[0])*1e6))))

    pf.make_film_2d(run.x, run.y, run.tperp_e, plot_options=plot_options, options=options)

    run.tperp_e = None
    gc.collect()

run = Run(sys.argv[1])
phi_film(run)
ntot_film(run)
upar_film(run)
tpar_film(run)
tperp_film(run)

