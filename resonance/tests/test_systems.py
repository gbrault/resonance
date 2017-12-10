from math import isclose

import numpy as np
import matplotlib.pyplot as plt
import pytest

from ..system import (System, _ConstantsDict, _MeasurementsDict,
                      _SingleDoFCoordinatesDict, _StatesDict)


def test_nonvalid_parameters_key():
    p = _ConstantsDict({})
    with pytest.raises(ValueError):
        p['ben stiller'] = 12.0
    with pytest.raises(ValueError):
        p['time'] = 12.0
    with pytest.raises(ValueError):
        p['time__hist'] = 12.0
    p['a'] = 1.0
    if 'a' in p:
        pass
    del p['a']


def test_setting_measurements_item():
    m = _MeasurementsDict({})
    # not allowed to set measurements
    with pytest.raises(ValueError):
        m['a'] = 12.0


def test_setting_coordinates_item():
    c = _SingleDoFCoordinatesDict({})

    # not a python identifier
    with pytest.raises(ValueError):
        c['a '] = 12.0

    # reserved variable name
    with pytest.raises(ValueError):
        c['time'] = 12.0

    # reserved variable name
    with pytest.raises(ValueError):
        c['time__hist'] = 12.0

    # can only add one coordinate
    c['first_key'] = 12.0
    with pytest.raises(ValueError):
        c['second_key'] = 12.0

    assert 'first_key' in c

    del c['first_key']

    assert 'first_key' not in c


def test_setting_state_item():
    s = _StatesDict({})
    with pytest.raises(ValueError):
        s['a'] = 0.0


def test_system():
    sys = System()
    sys.constants['a'] = 1.0
    assert isclose(sys._time['t'], 0.0)
    assert isclose(sys._get_par_vals('time'), 0.0)

    def plot(a):
        fig, ax = plt.subplots(1, 1)
        return fig

    def update(a):
        pass

    sys.config_plot_func = None
    sys.config_plot_update_func = None
    with pytest.raises(ValueError):
        sys.animate_configuration()

    sys.config_plot_func = plot
    sys.config_plot_update_func = None
    with pytest.raises(ValueError):
        sys.animate_configuration()

    # no trajectory computed
    sys.config_plot_func = plot
    sys.config_plot_update_func = update
    with pytest.raises(AttributeError):
        sys.animate_configuration()

    # no speed is set
    sys.coordinates['x'] = 1.0
    with pytest.raises(ValueError):
        sys._check_system()


def test_add_measurement():
    sys = System()
    sys.constants['a'] = 1.0
    sys.constants['b'] = 2.0

    def meas1(a, b):
        return np.array([a + b])

    with pytest.raises(TypeError):
        sys.add_measurement('meas1', meas1)

    def meas2(a, b):
        return np.sum([a, b])

    with pytest.raises(TypeError):
        sys.add_measurement('meas2', meas2)

    def meas3(a, b):
        if isinstance(b, np.ndarray):
            a = 5.2324 * np.ones_like(b)
        else:
            a = 1.23
        return a + b

    with pytest.raises(TypeError):
        sys.add_measurement('meas3', meas3)
