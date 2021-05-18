import numpy as np
from PyAstronomy.pyasl import dopplerShift as dop

def A_template0(wavelength, flux_spectra, v_prim):
    """Return first iteration of template spectrum for the main component of a system
    wavelength : np.array. dispersion axis
    flux_spectra : np.ndarray. array of observed spectra
    v_prim : np.array. array of velocities for primary component
    returns:
        A : first iteration of template spectrum A
    """
    for spectrum in flux_spectra:
        if len(wavelength) != len(spectrum):
            print("The dimensions of wavelenght and spectra arrays must be the same")
            raise
    A_arrays = np.array(
        [dop(wavelength, spec, -v)[0] for spec, v in zip(flux_spectra, v_prim)]
    )
    N = np.nansum((~np.isnan(A_arrays)).astype(int), axis=0)
    A = np.nansum(A_arrays, axis=0)

    return A / N

def B_template(wavelength, flux_spectra, v_prim, v_sec, A, **kwargs):
    """Return template spectrum for the secondary component of a system

    wavelength : np.array. dispersion axis
    flux_spectra : np.ndarray. array of observed spectra
    A : np.array. template of the primary component
    v_prim : np.array. array of velocities for primary component
    v_sec : np.array. array of velocities for secondary component

    returns:
        B : iteration of template spectrum B
    """
    for spectrum in flux_spectra:
        if len(wavelength) != len(spectrum):
            print(
                "The dimensions of wavelenght and" + "spectra arrays must be the same"
            )
            raise
    B_arrays = np.array(
        [
            dop(wavelength, spec, -vs)[0] - dop(wavelength, A, vp - vs)[0]
            for spec, vp, vs in zip(flux_spectra, v_prim, v_sec)
        ]
    )
    M = np.nansum((~np.isnan(B_arrays)).astype(int), axis=0)
    B = np.nansum(B_arrays, axis=0)
    return B / M


def A_template(wavelength, flux_spectra, v_prim, v_sec, B, **kwargs):
    """Return template spectrum for the primary component of a system

    wavelength : np.array. dispersion axis
    flux_spectra : np.ndarray. array of observed spectra
    v_prim : np.array. array of velocities for primary component
    v_sec : np.array. array of velocities for secondary component
    B : np.array. template of the secondary component
    A_continuum : float continuum of the main component


    returns:
        A : iteration of template spectrum B
    """
    for spectrum in flux_spectra:
        if len(wavelength) != len(spectrum):
            raise (
                "The dimensions of wavelenght and " + "spectra arrays must be the same"
            )
    A_arrays = np.array(
        [
            dop(wavelength, spec, -vp)[0] - dop(wavelength, B, vs - vp)[0]
            for spec, vp, vs in zip(flux_spectra, v_prim, v_sec)
        ]
    )
    N = np.nansum((~np.isnan(A_arrays)).astype(int), axis=0)
    A = np.nansum(A_arrays, axis=0)
    return A / N
