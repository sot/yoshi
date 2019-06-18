import numpy as np
from astropy.table import Table
from chandra_aca.transform import calc_aca_from_targ
from chandra_aca.drift import get_aca_offsets
import proseco


def run_one_yoshi(**kw):
    """
    Run proseco and sparkles for an observation request in a roll/temperature/man_angle
    scenario.

    :param detector: detector (ACIS-I|ACIS-S|HRC-I|HRC-S)
    :param chipx: chipx from zero-offset aimpoint table entry for obsid
    :param chipy: chipy from zero-offset aimpoint table entry for obsid
    :param chip_id: chip_id from zero-offset aimpoint table entry for obsid
    :param ra_targ: target RA (degrees)
    :param dec_targ: target Dec (degrees)
    :param roll_targ: target Roll (degrees)
    :param offset_y: target offset_y (arcmin)
    :param offset_z: target offset_z (arcmin)
    :param sim_offset: SIM Z offset (steps)
    :param focus_offset: SIM focus offset (steps)
    :param dither_y: Y amplitude dither (arcsec)
    :param dither_z: Z amplitude dither (arcsec)
    :param obs_date: observation date (for proper motion and ACA offset projection)
    :param t_ccd: ACA CCD temperature (degrees C)
    :param man_angle: maneuver angle (degrees)
    :returns: dictionary of (ra_pnt, dec_pnt, roll_pnt,
                             N_critical, N_warning, N_caution, N_info,
                             P2, guide_count)

    """

    # Calculate dynamic offsets using the supplied temperature.
    aca_offset_y, aca_offset_z = get_aca_offsets(kw['detector'],
                                                 kw['chip_id'], kw['chipx'], kw['chipy'],
                                                 kw['obs_date'], kw['t_ccd'])

    # Get the ACA quaternion using target offsets and dynamic offsets.
    # Note that calc_aca_from_targ expects target offsets in degrees and obs is now in arcmin
    q_pnt = calc_aca_from_targ((kw['ra_targ'], kw['dec_targ'], kw['roll_targ']),
                               (kw['offset_y'] / 60.) + (aca_offset_y / 3600.),
                               (kw['offset_z'] / 60.) + (aca_offset_z / 3600.))

    # Run proseco and sparkles
    aca = proseco.get_aca_catalog(obsid=0,
                                  att=q_pnt,
                                  man_angle=kw['man_angle'],
                                  date=kw['obs_date'],
                                  t_ccd_acq=kw['t_ccd'],
                                  t_ccd_guide=kw['t_ccd'],
                                  dither_acq=(kw['dither_y'], kw['dither_z']),
                                  dither_guide=(kw['dither_y'], kw['dither_z']),
                                  detector=kw['detector'],
                                  sim_offset=kw['sim_offset'],
                                  focus_offset=kw['focus_offset'],
                                  n_acq=8, n_guide=5, n_fid=3)
    acar = aca.get_review_table()
    acar.run_aca_review()

    # Get values for report
    report = {'ra_pnt': q_pnt.ra,
              'dec_pnt': q_pnt.dec,
              'roll_pnt': q_pnt.roll,
              'N_critical': len(acar.messages == 'critical'),
              'N_warning': len(acar.messages == 'warning'),
              'N_caution': len(acar.messages == 'caution'),
              'N_info': len(acar.messages == 'info'),
              'P2': -np.log10(acar.acqs.calc_p_safe()),
              'guide_count': acar.guide_count}
    return report
