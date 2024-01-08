# *****************************************************************************
# Copyright (C) 2023 Ambra Di Piano
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import shutil
import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter

class Mapper():
    '''Class that read, writes and manages the FITS data format.'''
    def __init__(self, logger) -> None:
        self.hdr_fits_keys = ['NAXIS1', 'NAXIS2', 'CRPIX1', 'CRPIX2', 'CDELT1', 'CDELT2', 'CRVAL1', 'CRVAL2', 'DATE-OBS', 'TIME-OBS', 'DATE-END', 'TIME-END', 'TELAPSE', 'ONTIME', 'LIVETIME', 'EXPOSURE', 'DEADC', 'E_MIN', 'E_MAX']
    
        self.set_logger(logger=logger)
        pass

    def set_logger(self, logger):
        self.log = logger
        return self

    def empty_header(self, hdr):
        hdr['NAXIS1'] = 0
        hdr['NAXIS2'] = 0
        hdr['CRPIX1'] = 0.0
        hdr['CRPIX2'] = 0.0
        hdr['CDELT1'] = 0.0
        hdr['CDELT2'] = 0.0
        hdr['CRVAL1'] = 0.0
        hdr['CRVAL2'] = 0.0
        #hdr['LONPOLE'] = 0.0
        #hdr['LATPOLE'] = 0.0
        hdr['CREATOR'] = 'RTAPH'
        hdr['DATE-OBS'] = '2000-01-01'
        hdr['TIME-OBS'] = '00:00:00'
        hdr['DATE-END'] = '2000-01-01'
        hdr['TIME-END'] = '00:00:00'
        hdr['TELAPSE'] = 0.0
        hdr['ONTIME'] = 0.0
        hdr['LIVETIME'] = 0.0
        hdr['EXPOSURE'] = 0.0
        hdr['DEADC'] = 0.0
        hdr['E_MIN'] = 0.0
        hdr['E_MAX'] = 0.0
        return hdr

    def get_template(self):
        '''TODO'''
        return 

    def convert_countmap_in_template(self, skymap, template):
        shutil.copy(skymap, template)
        with fits.open(template, mode='update') as h:
            h['SKYMAP'].data = np.empty_like(h['SKYMAP'].data)
            h['SKYMAP'].header = self.empty_header(h['SKYMAP'].header)
            h.flush()
        return self

    def update_countmap_hdr(self, hdr, hdr_info):
        hdr['NAXIS1'] = hdr_info['nbins']
        hdr['NAXIS2'] = hdr_info['nbins']
        hdr['CRPIX1'] = hdr_info['xref']
        hdr['CRPIX2'] = hdr_info['yref']
        hdr['CDELT1'] = hdr_info['pixelsize']
        hdr['CDELT2'] = hdr_info['pixelsize']
        hdr['CRVAL1'] = hdr_info['point_ra']
        hdr['CRVAL2'] = hdr_info['point_dec']
        #hdr['LONPOLE'] = hdr_info['lonpole']
        #hdr['LATPOLE'] = hdr_info['latpole']
        hdr['CREATOR'] = 'RTAPH'
        hdr['DATE-OBS'] = hdr_info['date_obs']
        hdr['TIME-OBS'] = hdr_info['time_obs']
        hdr['DATE-END'] = hdr_info['date_end']
        hdr['TIME-END'] = hdr_info['time_end']
        hdr['TELAPSE'] = hdr_info['telapse']
        hdr['ONTIME'] = hdr_info['ontime']
        hdr['LIVETIME'] = hdr_info['livetime']
        hdr['EXPOSURE'] = hdr_info['exposure']
        hdr['DEADC'] = hdr_info['deadc']
        hdr['E_MIN'] = hdr_info['emin']
        hdr['E_MAX'] = hdr_info['emax']
        return hdr

    def get_header_info_from_dl3(self, hdr):
        hdr_info = {}
        for k in self.hdr_fits_keys:
            hdr_info[k] = hdr[k]
        return hdr_info

    def get_dl3_hdr(self, dl3_file):
        with fits.open(dl3_file) as h:
            hdr = h['EVENTS'].header
        return hdr

    def set_dl3_hdr(self, dl3_file, hdr_fits):
        with fits.open(dl3_file, mode='update') as h:
            for k in hdr_fits.keys():
                h['EVENTS'].header[k] = hdr_fits[k]
            h.flush()
        return self

    def get_dl3_data(self, dl3_file):
        with fits.open(dl3_file) as h:
            data = h['EVENTS'].data
        return data

    def set_dl3_data(self, dl3_file, data, GTI=None):
        with fits.open(dl3_file, mode='update') as h:
            h['EVENTS'].data = data
            if GTI is not None:
                h['GTI'].data[0] = GTI
            h.flush()
        return self

    def get_dl4_hdr(self, dl4_file):
        with fits.open(dl4_file) as h:
            hdr = h['SKYMAP'].header
        return hdr

    def set_dl4_hdr(self, dl4_file, hdr_fits):
        with fits.open(dl4_file, mode='update') as h:
            for k in hdr_fits.keys():
                h['SKYMAP'].header[k] = hdr_fits[k]
            h.flush()
        return self

    def get_dl4_data(self, dl4_file):
        with fits.open(dl4_file) as h:
            data = h['SKYMAP'].data
        return data

    def set_dl4_data(self, dl4_file, data):
        with fits.open(dl4_file, mode='update') as h:
            h['SKYMAP'].data = data
            h.flush()
        return self

    def get_binning_size(self, maproi=5, pixelsize=0.02):
        nbins = int(maproi*2/pixelsize)
        return nbins

    def get_pixel_reference_point(self, nbins):
        return nbins/2+0.5, nbins/2+0.5

    def store_hdr_in_dict(self, dl3_hdr, maproi=5, pixelsize=0.02):
        hdr_fits = {}
        nbins = self.get_binning_size(maproi=maproi, pixelsize=pixelsize)
        hdr_fits['NAXIS1'] = nbins
        hdr_fits['NAXIS2'] = nbins
        xref, yref = self.get_pixel_reference_point(nbins=nbins)
        hdr_fits['CRPIX1'] = xref
        hdr_fits['CRPIX2'] = yref
        hdr_fits['CDELT1'] = pixelsize
        hdr_fits['CDELT2'] = pixelsize
        hdr_fits['CRVAL1'] = float(dl3_hdr['RA_PNT'])
        hdr_fits['CRVAL2'] = float(dl3_hdr['DEC_PNT'])
        hdr_fits['CREATOR'] = 'ASTRORT'
        hdr_fits['TSTART'] = float(dl3_hdr['TSTART'])
        hdr_fits['TSTOP'] = float(dl3_hdr['TSTOP'])
        hdr_fits['TELAPSE'] = dl3_hdr['TELAPSE']
        hdr_fits['ONTIME'] = dl3_hdr['ONTIME']
        hdr_fits['LIVETIME'] = dl3_hdr['LIVETIME']
        hdr_fits['EXPOSURE'] = dl3_hdr['LIVETIME']
        hdr_fits['DEADC'] = dl3_hdr['DEADC']
        erange = dl3_hdr['DSVAL2'].split(':')
        hdr_fits['E_MIN'] = float(erange[0])
        hdr_fits['E_MAX'] = float(erange[1])
        hdr_fits['RADESYS'] = dl3_hdr['RADECSYS']
        return hdr_fits

    def get_countmap_in_fits(self, dl3_file, template, pixelsize=0.02, maproi=5, trange=None, erange=None, sigma=1, fitsname='skymap.fits'):
        shutil.copy(template, fitsname)
        dl3_hdr = self.get_dl3_hdr(dl3_file=dl3_file)
        pointing = {'ra': float(dl3_hdr['RA_PNT']), 'dec': float(dl3_hdr['DEC_PNT'])}
        hdr_fits = self.store_hdr_in_dict(dl3_hdr=dl3_hdr, maproi=maproi, pixelsize=pixelsize)
        dl3_data = self.get_dl3_data(dl3_file=dl3_file)
        dl3_data = self.selection_cuts(dl3_data=dl3_data, pointing=pointing, trange=trange, erange=erange, maproi=maproi)
        if sigma != 0:
            dl4_data = self.from_dl3_to_dl4(dl3_data=dl3_data, pointing=pointing, maproi=maproi, pixelsize=0.02, sigma=sigma)
        else:
            dl4_data = self.from_dl3_to_dl4(dl3_data=dl3_data, pointing=pointing, maproi=maproi, pixelsize=pixelsize)
        self.set_dl4_hdr(dl4_file=fitsname, hdr_fits=hdr_fits)
        self.set_dl4_data(dl4_file=fitsname, data=dl4_data)
        return

    def get_extent(self, pointing, roi):
        extent = [pointing['ra']-roi, pointing['ra']+roi, pointing['dec']-roi, pointing['dec']+roi]
        return extent

    def get_heatmap(self, x, y, extent, sigma=0, bins=1000):
        r = [[extent[0], extent[1]], [extent[2], extent[3]]]
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
        if sigma != 0:
            heatmap = gaussian_filter(heatmap, sigma=sigma)
        return heatmap.T

    def from_dl3_to_dl4(self, dl3_data, pointing, maproi=5, pixelsize=0.02, sigma=0):
        ra = np.array(dl3_data.field('RA')).flatten()
        dec = np.array(dl3_data.field('DEC')).flatten()
        nbins = self.get_binning_size(maproi=maproi, pixelsize=pixelsize)
        extent = self.get_extent(pointing=pointing, roi=maproi)
        dl4_data = self.get_heatmap(ra, dec, extent=extent, bins=nbins, sigma=sigma)
        return dl4_data

    def selection_cuts(self, dl3_data, pointing, trange=None, erange=None, maproi=None):
        if trange != None:
            dl3_data = dl3_data[(dl3_data['TIME'] > trange[0]) & (dl3_data['TIME'] < trange[1])] 
        if erange != None:
            dl3_data = dl3_data[(dl3_data['ENERGY'] > erange[0]) & (dl3_data['ENERGY'] < erange[1])] 
        if maproi != None:
            dl3_data = dl3_data[(np.abs(np.abs(dl3_data['RA'])-np.abs(pointing['ra'])) < maproi)]
            dl3_data = dl3_data[(np.abs(np.abs(dl3_data['DEC'])-np.abs(pointing['dec'])) < maproi)]
        if len(dl3_data) == 0:
            self.log.warning("Empty photon list selection.")
        return dl3_data

    def get_countmap_in_npy(self, dl3_file, pixelsize=0.02, maproi=5, trange=None, erange=None, sigma=1, npyname='heatmap.npy'):
        dl3_hdr = self.get_dl3_hdr(dl3_file=dl3_file)
        pointing = {'ra': float(dl3_hdr['RA_PNT']), 'dec': float(dl3_hdr['DEC_PNT'])}
        dl3_data = self.get_dl3_data(dl3_file=dl3_file)
        dl3_data = self.selection_cuts(dl3_data=dl3_data, pointing=pointing, trange=trange, erange=erange, maproi=maproi)
        if sigma != 0:
            dl4_data = self.from_dl3_to_dl4(dl3_data=dl3_data, pointing=pointing, maproi=maproi, pixelsize=0.02, sigma=sigma)
        else:
            dl4_data = self.from_dl3_to_dl4(dl3_data=dl3_data, pointing=pointing, maproi=maproi, pixelsize=pixelsize)
        np.save(npyname, dl4_data, allow_pickle=True, fix_imports=True)
        return
