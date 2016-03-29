import os
import sys
import gc

# Third Party
import numpy as np
from netCDF4 import Dataset

# Local
from run import Run
import field_helper as field

run = Run(sys.argv[1])
run.lab_frame = False
version = 1

run.read_ntot()
run.read_phi()
run.read_q()

# Heat flux to SI
hflux_SI = run.q_i * (run.nref*run.tref*run.vth*run.rhoref**2/run.amin**2)

# Write
os.system('mkdir -p ' + run.run_dir + 'analysis/exp_bes_write')
nc_file = Dataset(run.run_dir + 'analysis/exp_bes_write/gs2_27268_0.25_' +
                  str(np.around(run.tprim_1, 2)) + '_' +
                  str(np.around(run.g_exb, 2)) + '_' + str(version) +
                  '.cdf', 'w')

nc_file.createDimension('NR', run.nx)
nc_file.createDimension('NZ', run.ny)
nc_file.createDimension('NT', run.nt)
nc_file.createDimension('none', 1)
nc_file.createDimension('species', 2)
nc_file.createDimension('dimpsi', 1)

nc_nref = nc_file.createVariable('nref_m-3','d', ('none',))
nc_tref = nc_file.createVariable('tref_eV','d', ('none',))
nc_g_exb = nc_file.createVariable('g_exb','d', ('none',))
nc_lab = nc_file.createVariable('lab_frame','i', ('none',))
nc_lab.units = '0 - rot frame, 1 - lab frame'
nc_phinorm_V = nc_file.createVariable('phinorm_V','d', ('none',))
nc_hflux = nc_file.createVariable('qheat','d', ('dimpsi',))
nc_hflux.units = 'W/m^2'
nc_dhflux = nc_file.createVariable('dqheat','d', ('dimpsi',))
nc_dhflux.units = 'W/m^2'
nc_psi = nc_file.createVariable('psi','d', ('dimpsi',))
nc_x = nc_file.createVariable('r','d',('NR',))
nc_y = nc_file.createVariable('z','d',('NZ',))
nc_t = nc_file.createVariable('times','d',('NT',))
nc_charge = nc_file.createVariable('charge','d',('species',))
nc_mass = nc_file.createVariable('mass','d',('species',))
nc_dens = nc_file.createVariable('dens','d',('species',))
nc_temp = nc_file.createVariable('temp','d',('species',))
nc_tprim = nc_file.createVariable('tprim','d',('species',))
nc_fprim = nc_file.createVariable('fprim','d',('species',))
nc_ntot = nc_file.createVariable('ntot','d',('NT', 'NR', 'NZ',))
nc_phi = nc_file.createVariable('phi','d',('NT', 'NR', 'NZ',))

nc_nref[:] = run.nref
nc_tref[:] = run.tref
nc_g_exb[:] = run.g_exb
if run.lab_frame:
    nc_lab[:] = 1
else:
    nc_lab[:] = 0
nc_phinorm_V[:] = 2.2054e+02
nc_psi[:] = 0.49
nc_hflux[:] = np.trapz(hflux_SI, x=run.t)/(run.t[-1] - run.t[0])
nc_dhflux[:] = np.std(hflux_SI)
nc_charge[:] = [1, 1]
nc_mass[:] = [run.mass_1, run.mass_2]
nc_dens[:] = [1, 1]
nc_temp[:] = [1, 1]
nc_tprim[:] = run.tprim_1
nc_fprim[:] = run.fprim_1
nc_x[:] = run.x[:] + run.rmaj
nc_y[:] = run.y[:]
nc_t[:] = run.t[:] - run.t[0]
nc_ntot[:,:,:] = run.ntot_i[:,:,:]
nc_phi[:,:,:] = run.phi[:,:,:]

nc_file.close()
