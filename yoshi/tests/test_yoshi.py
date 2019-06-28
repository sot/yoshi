import numpy as np
from yoshi.yoshi import run_one_yoshi


def test_run_one_yoshi():
    """Regression test a single run for a real obsid"""
    request = {
        'chip_id': 3,
        'chipx': 970.0,
        'chipy': 975.0,
        'dec_targ': 66.35,
        'detector': 'ACIS-I',
        'dither_y': 8,
        'dither_z': 8,
        'focus_offset': 0,
        'man_angle': 175.0,
        'obs_date': '2019:174:00:32:23.789',
        'offset_y': -2.3,
        'offset_z': 3.0,
        'ra_targ': 239.06125,
        'roll_targ': 197.12,
        'sim_offset': 0,
        't_ccd': -9.1}

    expected = {'ra_pnt': 238.96459762180638,
                'dec_pnt': 66.400811774068146,
                'roll_pnt': 197.20855489084187,
                'n_critical': 2,
                'n_warning': 2,
                'n_caution': 0,
                'n_info': 1,
                'P2': 1.212575909121556,
                'guide_count': 3.6262975526400014}

    actual = run_one_yoshi(**request)

    for key in expected:
        val = expected[key]
        val2 = actual[key]
        if isinstance(val, float):
            assert np.isclose(val, val2, atol=1e-3)
        else:
            assert val == val2

