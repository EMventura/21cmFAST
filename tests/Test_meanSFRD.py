import os
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing
import h5py

import py21cmfast
from py21cmfast import plotting
from py21cmfast import cache_tools

import logging
from py21cmfast import UserParams, CosmoParams, FlagOptions, AstroParams, compute_SFRD
# from py21cmfast import UserParams, CosmoParams, FlagOptions, AstroParams

from py21cmfast.c_21cmfast import ffi, lib
from py21cmfast._utils import StructWithDefaults, OutputStruct as _OS, StructInstanceWrapper, StructWrapper

global_params = StructInstanceWrapper(lib.global_params, ffi)

# Most of these are not necessary, but a couple are
user_params = UserParams(
                DIM=150,
                HII_DIM=50,
                BOX_LEN=150.0,
                USE_FFTW_WISDOM=False,
                HMF=1, # Relevant for changing halo mass function
                N_THREADS=1,
                NO_RNG=False,
                PERTURB_ON_HIGH_RES=True)

# Change to whatever you need
cosmo_params = CosmoParams(OMb=0.0486,OMm=0.3075,POWER_INDEX=0.97,SIGMA_8=0.82,hlittle=0.6774)

# These should not need changing
flag_options = FlagOptions(
                    USE_MASS_DEPENDENT_ZETA=True,
                    USE_TS_FLUCT=False,
                    INHOMO_RECO=False,
                    SUBCELL_RSD=False,
                    M_MIN_in_Mass=False,
                    PHOTON_CONS=False)
    
if __name__ == '__main__':


    # I think this is the default parameters for 21cmFAST (but, I didn't double check)
    astro_params = AstroParams(
            ALPHA_ESC=-0.5, 
            ALPHA_STAR=0.5, 
            F_ESC10=-1.30102999566, 
            F_STAR10=-1.0, 
            L_X=40.5, 
            M_TURN=8.7, 
            NU_X_THRESH=500.0, 
            X_RAY_SPEC_INDEX=1.000000,
            t_STAR=0.5,
            R_BUBBLE_MAX=50.
            )

    n_xray_points = 200
    zmin = 0.01
    zmax = 20.

    redshifts = np.zeros(n_xray_points)

    for i in range(n_xray_points):
        redshifts[i] = zmin + (zmax - zmin)*float(i)/(float(n_xray_points) - 1.)
    
    SFRD = compute_SFRD(
                redshifts=redshifts,
                user_params=user_params,
                cosmo_params=cosmo_params,
                astro_params=astro_params)

    for i in range(n_xray_points):
        print(i,redshifts[i],SFRD[i])
    