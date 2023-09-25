# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.ndimage import gaussian_filter
from astropy.wcs import WCS
from matplotlib.colors import SymLogNorm
from astropy import units as u

class Plotter():
    def __init__(self, logger) -> None:
        self.set_logger(logger=logger)
        pass

    def set_logger(self, logger):
        self.log = logger
        return self

    def set_target(self, ra=83.63, dec=22.01, rad=0.2, color='white'):
        self.target = {'ra': ra, 'dec': dec, 'rad': rad, 'color': color}
        return self

    def set_target_from_dict(self, target, rad=0.2, color='white'):
        self.target = target
        self.target['rad'] = rad
        self.target['color'] = color
        return self

    def set_pointing(self, ra=83.63, dec=22.51):
        self.pointing = {'ra': ra, 'dec': dec, 'ftm': 'k+'}
        return self

    def set_pointing_from_dict(self, pointing):
        self.pointing = pointing
        return self

    def __check_target(self):
        assert isinstance(self.target, dict) is True, 'check that you have set the target correctly.'
        return self

    def __check_pointing(self):
        assert isinstance(self.pointing, dict) is True, 'check that you have set the pointing correctly.'
        return self

    def set_path(self, path):
        self.path = path
        return self
        
    def load_fits(self, filename, extension='SKYMAP'):
        h = fits.open(filename)
        h.info()
        data = h[extension].data
        return data

    def heatmap_with_smoothing(self, x, y, sigma, extent, bins=1000):
        r = [[extent[0], extent[1]], [extent[2], extent[3]]]
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
        heatmap = gaussian_filter(heatmap, sigma=sigma)
        return heatmap.T, extent

    def heatmap(self, x, y, extent, bins=1000):
        r = [[extent[0], extent[1]], [extent[2], extent[3]]]
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
        return heatmap.T, extent

    def get_extent(self, roi):
        extent = [self.pointing['ra']-roi, self.pointing['ra']+roi, self.pointing['dec']-roi, self.pointing['dec']+roi]
        return extent

    def set_wcs(self, point_ref, pixelsize):
        w = WCS(naxis=2)
        w.wcs.ctype = ['RA---CAR', 'DEC--CAR']
        w.wcs.crpix = [point_ref, point_ref]
        w.wcs.crval = [self.pointing['ra'], self.pointing['dec']]
        w.wcs.cdelt = [-pixelsize, pixelsize]
        w.wcs.lonpole = 0.0
        w.wcs.latpole = 67.49
        return w

    def reshape_coords(self, ra, dec):
        assert np.shape(ra) == np.shape(dec), 'RA and DEC shapes do not match'
        coords = np.array([ra, dec])
        coords = coords.reshape((len(ra), 2))
        return coords

    def reshape_ra_dec(self, coords):
        ra, dec = [], []
        for i in range(len(coords)):
            ra.append(coords[i][0])
            dec.append(coords[i][1])
        ra = np.array(ra)
        dec = np.array(dec)
        return ra, dec

    def counts_map(self, file, trange=None, erange=None, roi=5, name='skymap.png', title=None, xlabel='right ascension (deg)', ylabel='declination (deg)', figsize=(10, 10), fontsize=20, cmap='CMRmap', pixelsize=0.02, sigma=1):
        self.__check_pointing()
        extent = self.get_extent(roi)
        # counts map
        data = self.get_phlist_data(file=file)
        # select counts map
        data = self.phlist_selection_cuts(data=data, trange=trange, erange=erange, roi=roi)
        # axis and binning
        ra = np.array(data.field('RA')).flatten()
        dec = np.array(data.field('DEC')).flatten()
        bins = int(roi*2/pixelsize)
        # plot
        fig = plt.figure(figsize=figsize) 
        ax = plt.subplot()
        if sigma != 0:
            hist = self.heatmap_with_smoothing(ra, dec, sigma=sigma, extent=extent, bins=bins)
        else:
            hist = self.heatmap(ra, dec, extent=extent, bins=bins)
        img = ax.imshow(hist[0], norm=SymLogNorm(1, base=10), origin='lower', extent=extent, cmap=cmap)
        cb = plt.colorbar(img, ax=ax)
        # axis
        ax.tick_params(axis='both', labelsize=fontsize)
        cb.ax.tick_params(labelsize=fontsize) 
        cb.set_label('counts', fontsize=fontsize)
        ax.set_xlabel(xlabel, fontsize=fontsize)
        ax.set_ylabel(ylabel, fontsize=fontsize)
        ax.set_title(title, fontsize=fontsize)
        # pointing
        ax.plot([self.pointing['ra']], [self.pointing['dec']], 'k+', markersize=fontsize)
        ax.set_xlim((extent[0], extent[1]))
        ax.set_ylim((extent[2], extent[3]))
        ax.set_aspect('equal')
        #ax.invert_xaxis()
        ax.grid(color='grey', ls='solid')
        #fig.tight_layout()
        fig.savefig(name)
        plt.close()
        return self

    def counts_map_with_wcs(self, file, trange=None, erange=None, roi=5, name='skymap.png', title=None, xlabel='right ascension (deg)', ylabel='declination (deg)', figsize=(10, 10), fontsize=20, cmap='CMRmap', pixelsize=0.02, sigma=1):
        self.__check_pointing()
        extent = self.get_extent(roi=roi)
        # counts map
        data = self.get_phlist_data(file=file)
        # select counts map
        data = self.phlist_selection_cuts(data=data, trange=trange, erange=erange, roi=roi)
        # axis and binning
        ra = np.array(data.field('RA')).flatten()
        dec = np.array(data.field('DEC')).flatten()
        bins = int(roi*2/pixelsize)
        # wcs
        wcs = self.set_wcs(point_ref=bins/2+0.5, pixelsize=pixelsize)
        # plot
        fig = plt.figure(figsize=figsize) 
        ax = plt.subplot(projection=wcs)
        if sigma != 0:
            hist = self.heatmap_with_smoothing(ra, dec, sigma=sigma, extent=extent, bins=bins)
        else:
            hist = self.heatmap(ra, dec, extent=extent, bins=bins)
        ax.coords[0].set_format_unit(u.deg)
        ax.coords[1].set_format_unit(u.deg)
        img = ax.imshow(hist[0], norm=SymLogNorm(1, base=10), interpolation='gaussian', extent=extent, cmap=cmap)
        cb = plt.colorbar(img, ax=ax)
        # axis
        ax.tick_params(axis='both', labelsize=fontsize)
        cb.ax.tick_params(labelsize=fontsize) 
        cb.set_label('counts', fontsize=fontsize)
        ax.set_xlabel(xlabel, fontsize=fontsize)
        ax.set_ylabel(ylabel, fontsize=fontsize)
        ax.set_title(title, fontsize=fontsize)
        # pointing
        ax.plot([self.pointing['ra']], [self.pointing['dec']], 'k+', markersize=fontsize)
        ax.set_aspect('equal')
        #ax.invert_xaxis()
        ax.grid(color='grey', ls='solid')
        #fig.tight_layout()
        fig.savefig(name)
        plt.close()
        return self

    def plot_fits_skymap(self, file, name='skymap.png', title=None, xlabel='right ascension (deg)', ylabel='declination (deg)', figsize=(10, 10), fontsize=20, cmap='CMRmap', logbar=False):

        # get map
        data, wcs = self.get_skymap_data_with_wcs(file=file)
        # plot
        fig = plt.figure(figsize=figsize) 
        ax = plt.subplot(projection=wcs)
        ax.coords[0].set_format_unit(u.deg)
        ax.coords[1].set_format_unit(u.deg)
        if logbar:
            img = plt.imshow(data, norm=SymLogNorm(1, base=10), origin='lower', interpolation='gaussian', cmap=cmap)
        else: 
            img = plt.imshow(data, interpolation='gaussian', cmap=cmap)
        cb = plt.colorbar(img, ax=ax)
        # axis
        ax.tick_params(axis='both', labelsize=fontsize)
        cb.ax.tick_params(labelsize=fontsize) 
        cb.set_label('counts', fontsize=fontsize)
        ax.set_xlabel(xlabel, fontsize=fontsize)
        ax.set_ylabel(ylabel, fontsize=fontsize)
        ax.set_title(title, fontsize=fontsize)
        ax.set_aspect('equal')
        #ax.invert_xaxis()
        ax.grid(color='grey', ls='solid')
        #fig.tight_layout()
        fig.savefig(name)
        plt.close()
        return self

    def get_skymap_data_with_wcs(self, file):
        with fits.open(file) as h:
            try:
                w = WCS(h['SKYMAP'].header)
                print(h['SKYMAP'].header)
                data = h['SKYMAP'].data
            except KeyError as e:
                self.log.error(f'Missing "SKYMAP" extention, the input file may not be a compatible counts map. {e}')
                raise KeyError(f'Missing "SKYMAP" extention, the input file may not be a compatible counts map. {e}')
        return data, w

    def get_phlist_data(self, file):
        with fits.open(file) as h:
            try:
                data = h['EVENTS'].data
            except KeyError as e:
                self.log.error(f'Missin "EVENTS" extention, the input file may not be a compatible photon list. {e}')
                raise KeyError(f'Missin "EVENTS" extention, the input file may not be a compatible photon list. {e}')
            if len(data) == 0:
                self.log.warning("Empty photon list.")
        return data

    def phlist_selection_cuts(self, data, trange=None, erange=None, roi=None):
        if trange != None:
            data = data[(data['TIME'] > trange[0]) & (data['TIME'] < trange[1])] 
        if erange != None:
            data = data[(data['ENERGY'] > erange[0]) & (data['ENERGY'] < erange[1])] 
        if roi != None:
            data = data[(np.abs(np.abs(data['RA'])-np.abs(self.pointing['ra'])) < roi)]
            data = data[(np.abs(np.abs(data['DEC'])-np.abs(self.pointing['dec'])) < roi)]
        if len(data) == 0:
            self.log.warning("Empty photon list selection.")
        return data
