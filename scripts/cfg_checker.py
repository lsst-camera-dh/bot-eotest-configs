# cfg_interp_Run6.py  11 May 2023
# Modified from cfg_interp_Run5.py for Run 6
# 21 June 2023 updated to calculate flash times from calib.cfg and
# apply them as a lower limit for the integration time

# Modified from cfg_interp.py for Run 5; includes parsing new syntax
# for specifying subset of rafts/REBs for spot acquisitions Estimates
# the time required to execute a given configuration file for BOT and
# also tallies the number of acquisitions.  The number of acquisitions
# is scaled to disk space at 15 Gbyte per full focal plane (201 CCDs)
# Does not estimate time for analysis steps data taking

# 11 May 2023 update:
# The acquisition times for flats are all specified directly as
# shutter open times and do not depend on the calib.cfg entries that
# relate desired e/pixel to exposure times Also, the parser now pays
# attention to the acquisitions that are specified in the [ACQUIRE]
# block and no longer just assumes that every defined block is part of
# the acquisition

import os
import configparser
import numpy
import sys
import glob

def vol_per_image(locations):
    # Evaluates number of Tbyte per acquisition from a simple parsing
    # of a list of locations in a section definition in the
    # configuration file
    locs = locations.split()
    reb_count = 0
    for loc in locs:
        if 'Reb' in loc:
            reb_count += 1
        else:
            reb_count += 3  # entire raft
    return reb_count*acq_size_reb


#
# Just check Run7 configs, since some files from earlier runs are
# flawed, and don't need to be tested.
#
run_folders = sorted(glob.glob(os.path.join("Run7")))

assert(run_folders)  # Ensure at least one folder is found

for run_folder in run_folders:
    infiles = (glob.glob(run_folder + '*/*cfg') +
               glob.glob(run_folder + '*/*/*cfg'))
    infiles.sort()

    calib_file = os.path.join(run_folder, 'calib.cfg')
    infiles = [_ for _ in infiles if _ != calib_file]

    acq_overhead = 2.8  # time (s) for a bias acquisition [overhead for an acquisition, FITS files now written asynchronously]
    xtalk_acq_overhead = 2.2  # From time interval between creation times of bias frames for single-REB readouts
    ccob_nb_overhead = 7.  # seconds per move (on average)
                           # in run 6874D
    #photodiode_factor = 1. # Scaling of exposure times due to readout overhead of Keithley meter buffer
    acq_size = 15./1000.  # Tbyte for full focal plane image
    acq_size_reb = 3*0.075/1000.  # Tbyte for a single REB


    # Get filter scale factor information
    config_filt = configparser.ConfigParser(allow_no_value=True)
    config_filt.read(calib_file)

    led_pairs = config_filt.items('WBLED')
    led_factors = {}

    for pair in led_pairs:
        led_factors[pair[0]] = float(pair[1].split()[0])
    source = led_factors['source']

    for infile in infiles:
        #print 'Reading:  ' + infile

        config = configparser.ConfigParser(allow_no_value=True)
        config.read(infile)

        #sections = config.sections()
        acquisition_steps = []
        for elt in config.items('ACQUIRE'):
            acquisition_steps.append(elt[0].upper())

        time_est = {}
        image_count = {}
        image_vol = {}

        for step in acquisition_steps:
            info = config.items(step)
            info_dict = {}
            for pair in info:
                info_dict[pair[0]] = pair[1]  #.split('#')[0]  # keep only the part before any #

            if 'locations' in info_dict.keys():
                vol = vol_per_image(info_dict['locations'])
            elif 'shots' in info_dict.keys():
                vol = acq_size_reb
            else:
                vol = acq_size

            if 'SHOT' in step:
                shotbcount = int(info_dict['shotbiases'].split()[0])
                shotdcount = int(info_dict['shotdarks'].split()[1])
                # dark exposure time
                shotdtime = float(info_dict['shotdarks'].split()[0])
                # integration time per shot (assumed the same for each shot)
                shotitime = float(info_dict['shots'].split('\n')[0].split()[4])
                numshots = len(info_dict['shots'].split('\n'))
                calibtime = len(info_dict['calibrate_wavelength'].split(','))*5  # assume 5 sec on average for wavelength change and calibration measurement per wavelength, for each shot group
                time_est[step] = numshots*(acq_overhead + shotitime + shotbcount*acq_overhead + shotdcount*(acq_overhead + shotdtime) + ccob_nb_overhead)
                image_count[step] = numshots*(1 + shotbcount + shotdcount)
                image_vol[step] = image_count[step]*vol
                #print(shotbcount,shotdcount,numshots)

            if 'BIAS' in step:
                bcount = float(info_dict['count'].split()[0])
                time_est[step] = bcount*acq_overhead
                image_count[step] = bcount
                image_vol[step] = image_count[step]*vol

            if 'CCOB' in step:
                bcount = int(info_dict['bcount'].split()[0])
                points = info_dict['point'].split(',\n')
                numpts = len(points)
                imcount = int(info_dict['imcount'].split()[0])
                temp = info_dict['expose'].split('\n')
                expose = []
                for elt in temp:
                    expose.append(float(elt.split()[-1].split(',')[0]))

                time_exp = 0.
                for expose1 in expose:
                    time_exp += numpts*(imcount + bcount)*(expose1 + xtalk_acq_overhead)
                time_est[step] = time_exp
                image_count[step] = numpts*(imcount + bcount)*len(expose)
                image_vol[step] = image_count[step]*vol

            if 'DARK' in step:
                bcount = int(info_dict['bcount'].split()[0].split(',')[0])
                darks = info_dict['dark'].split('\n')
                num_darks = 0
                dark_exp_time = 0
                for elt in darks:
                    num_darks += int(elt.split()[1].split(',')[0])
                    dark_exp_time += (float(elt.split()[0]) + acq_overhead)*int(elt.split()[1].split(',')[0])

                dark_exp_time += bcount*acq_overhead
                time_est[step] = dark_exp_time
                image_count[step] = num_darks + bcount
                image_vol[step] = image_count[step]*vol

            if step == 'FLAT':
                bcount = int(info_dict['bcount'].split()[0])
                FilterFactor = led_factors[info_dict['wl'].lower().split()[0]]
                flat_list = info_dict['flat'].split('\n')

                flat_time = 0.
                NDFactor = led_factors[info_dict['wl'].split()[0]]
                for elt in flat_list:
                    flat_time += (float(elt.split()[0]) + acq_overhead)*2

                flat_time += bcount*acq_overhead*len(flat_list)
                time_est[step] = flat_time
                image_count[step] = bcount*len(flat_list) + len(flat_list)*2
                image_vol[step] = image_count[step]*vol

            if 'LAMBDA' in step:
                bcount = int(info_dict['bcount'].split()[0])
                #openshutter = float(info_dict['openshutter'].split()[0])
                lambda_list = info_dict['lambda'].split('\n')
                lambda_time = 0.
                for elt in lambda_list:
                    WLFilterFactor = led_factors[elt.split()[0].lower()]
                    NDFactor = led_factors[elt.split()[0].lower()]
                    #time_exp = float(elt.split(',')[0].split()[1])/(source*WLFilterFactor*NDFactor)
                    #time_exp = max(openshutter, float(info_dict['lolim'].split('#')[0]))
                    #time_exp = min(time_exp, float(info_dict['hilim'].split('#')[0]))
                    #time_exp *= photodiode_factor
                    time_exp = 15.  # hard code for now
                    lambda_time += time_exp + acq_overhead
                time_est[step] = lambda_time
                image_count[step] = bcount*len(lambda_list) + len(lambda_list)
                image_vol[step] = image_count[step]*vol

            if step == 'PERSISTENCE':
                bcount = int(info_dict['bcount'].split()[0])
                persistence_list = info_dict['persistence'].split()
                persistence_time = 0.
                #WLFilterFactor = led_factors[info_dict['wl'].split()[0].lower()]
                #NDFactor = 1.  # 'empty' assumed #led_factors[elt.split()[3].lower().split(',')[0]]
                #time_exp = float(persistence_list[0])/(source*WLFilterFactor*NDFactor)
                ndarks = int(persistence_list[1])
                #time_exp *= photodiode_factor
                time_exp_dark = float(persistence_list[2])
                time_betw_darks = float(persistence_list[3])
                persistence_time = bcount*acq_overhead + time_exp + acq_overhead + ndarks*(time_exp_dark + time_betw_darks + acq_overhead)

                time_est[step] = persistence_time
                image_count[step] = bcount + 1 + ndarks
                image_vol[step] = image_count[step]*vol

            if step == 'SFLAT':
                bcount = int(info_dict['bcount'].split()[0])
                sflat_list = info_dict['sflat'].split('\n')
                if 'extradelay' in info_dict.keys():
                    extradelay = float(info_dict['extradelay'].split()[0])
                else:
                    extradelay = 0.

                sflat_time = 0.
                num_flats = 0
                for elt in sflat_list:
                    #print info_dict.keys()
                    #print led_factors.keys()
                    #print elt.split()[0]
                    #WLFilterFactor = led_factors[elt.split()[0].lower().split(',')[0]]
                    #time_exp = max(openshutter, float(info_dict['lolim'].split('#')[0]))
                    #time_exp = min(time_exp, float(info_dict['hilim'].split('#')[0]))
                    time_exp = 15.  # hard code for now
                    #rep_count = int(elt.split(',')[0].split()[2].split(',')[0])
                    rep_count = int(elt.split()[2].split(',')[0])
                    sflat_time += (time_exp + acq_overhead + extradelay)*rep_count
                    num_flats += rep_count
                time_est[step] = sflat_time + bcount*len(sflat_list)*acq_overhead
                image_count[step] = bcount*len(sflat_list) + num_flats  #len(sflat_list)*rep_count
                image_vol[step] = image_count[step]*vol

            if step == 'SPOT' or step == 'XTALK':
                bcount = int(info_dict['bcount'].split()[0])
                points = info_dict['point'].split(',\n')
                numpts = len(points)
                imcount = int(info_dict['imcount'].split()[0])
                temp = info_dict['expose'].split()
                expose = []
                num_rafts_to_read = points[0].count('R')
                if num_rafts_to_read > 0:
                    volb = acq_size_reb*3*num_rafts_to_read  # three REBs per raft
                else:
                    volb = vol

                # For Run 5, the expose values are actually electrons per pixel
                if 'signalpersec' in info_dict.keys():
                    exposure_scale = float(info_dict['signalpersec'])
                else:
                    exposure_scale = 1

                for elt in temp:
                    value = float(elt.split(',')[0])
                    if value > 0.0:  # exclude placeholder values of 0.0 exposure time
                        expose.append(value)

                time_exp = 0.
                for expose1 in expose:
                    time_exp += numpts*(imcount + bcount)*(expose1/exposure_scale + xtalk_acq_overhead)
                time_est[step] = time_exp
                image_count[step] = numpts*(imcount + bcount)*len(expose)
                image_vol[step] = image_count[step]*volb

        time_total = 0.
        num_acq = 0
        image_vol_total = 0.
        for key in time_est.keys():
            time_total += time_est[key]
            #print(key  + '%5.2f ' % (time_est[key]/3600))
            num_acq += image_count[key]
            image_vol_total += image_vol[key]

        #print time_est
        #print('|' + infile.split('Run6/')[1].ljust(35) + '|  {:6.1f} | {:5.0f} | {:5.2f} |'.format(time_total/60., num_acq, image_vol_total))
        print('|' + infile.split('/')[-1].ljust(35) + '|  {:6.1f} | {:5.0f} | {:5.2f} |'.format(time_total/60., num_acq, image_vol_total))
    print()
