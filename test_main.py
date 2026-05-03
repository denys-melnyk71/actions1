import pytest
from main import init, upd, run, delta_t, SIMULATION_TIME


def test_init():
    x_init, y_init, z_init = 1, 1, 1
    x_res, y_res, z_res, time_steps = init(x_init, y_init, z_init)

    # перевірка довжини
    assert len(x_res) == 1
    assert len(y_res) == 1
    assert len(z_res) == 1
    assert len(time_steps) == 1

    # перевірка значень
    assert x_res[-1] == x_init
    assert y_res[-1] == y_init
    assert z_res[-1] == z_init
    assert time_steps[-1] == 0


def test_upd():
    x_res, y_res, z_res, time_steps = init(1, 1, 1)
    upd(x_res, y_res, z_res, time_steps)

    assert len(x_res) == 2
    assert len(y_res) == 2
    assert len(z_res) == 2
    assert len(time_steps) == 2

    assert time_steps[-1] == pytest.approx(time_steps[-2] + delta_t)


def test_run():
    x_res, y_res, z_res, time_steps = run(1, 1, 1)

    iterations_num = int(SIMULATION_TIME / delta_t)
    check_len = iterations_num + 1

    assert len(x_res) == check_len
    assert len(y_res) == check_len
    assert len(z_res) == check_len
    assert len(time_steps) == check_len

    assert time_steps[-1] == pytest.approx(time_steps[0] + SIMULATION_TIME)
