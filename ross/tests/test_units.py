import pytest
from numpy.testing import assert_allclose

from ross.units import Q, check_units, units


def test_new_units_loaded():
    speed = Q(1, "RPM")
    assert speed.value == 1
    assert speed.si.value == 0.104719755
    assert str(speed.si.unit) == "rad / s"


@pytest.fixture
def auxiliary_function():
    @check_units
    def func(
        E,
        G_s,
        rho,
        L,
        idl,
        idr,
        odl,
        odr,
        speed,
        frequency,
        m,
        mx,
        my,
        Ip,
        Id,
        width,
        i_d,
        o_d,
        kxx,
        kxy,
        kxz,
        kyx,
        kyy,
        kyz,
        kzx,
        kzy,
        kzz,
        cxx,
        cxy,
        cxz,
        cyx,
        cyy,
        cyz,
        czx,
        czy,
        czz,
        Poisson,
    ):
        return (
            E,
            G_s,
            rho,
            L,
            idl,
            idr,
            odl,
            odr,
            speed,
            frequency,
            m,
            mx,
            my,
            Ip,
            Id,
            width,
            i_d,
            o_d,
            kxx,
            kxy,
            kxz,
            kyx,
            kyy,
            kyz,
            kzx,
            kzy,
            kzz,
            cxx,
            cxy,
            cxz,
            cyx,
            cyy,
            cyz,
            czx,
            czy,
            czz,
            Poisson,
        )

    return func


def test_units(auxiliary_function):
    results = auxiliary_function(
        E=1,
        G_s=1,
        rho=1,
        L=1,
        idl=1,
        idr=1,
        odl=1,
        odr=1,
        speed=1,
        frequency=1,
        m=1,
        mx=1,
        my=1,
        Ip=1,
        Id=1,
        width=1,
        i_d=1,
        o_d=1,
        kxx=1,
        kxy=1,
        kxz=1,
        kyx=1,
        kyy=1,
        kyz=1,
        kzx=1,
        kzy=1,
        kzz=1,
        cxx=1,
        cxy=1,
        cxz=1,
        cyx=1,
        cyy=1,
        cyz=1,
        czx=1,
        czy=1,
        czz=1,
        Poisson=1,
    )
    # check if all available units are tested
    assert len(results) == len(units)

    (
        E,
        G_s,
        rho,
        L,
        idl,
        idr,
        odl,
        odr,
        speed,
        frequency,
        m,
        mx,
        my,
        Ip,
        Id,
        width,
        i_d,
        o_d,
        kxx,
        kxy,
        kxz,
        kyx,
        kyy,
        kyz,
        kzx,
        kzy,
        kzz,
        cxx,
        cxy,
        cxz,
        cyx,
        cyy,
        cyz,
        czx,
        czy,
        czz,
        Poisson,
    ) = results

    assert E.value == 1
    assert E.unit == "N / m2"

    assert G_s.value == 1
    assert G_s.unit == "N / m2"

    assert rho.value == 1
    assert rho.unit == "kilogram / m3"

    assert L.value == 1
    assert L.unit == "meter"

    assert idl.value == 1
    assert idl.unit == "meter"

    assert idr.value == 1
    assert idr.unit == "meter"

    assert odl.value == 1
    assert odl.unit == "meter"

    assert odr.value == 1
    assert odr.unit == "meter"

    assert speed.value == 1
    assert speed.unit == "radian/second"

    assert frequency.value == 1
    assert frequency.unit == "radian/second"

    assert m.value == 1
    assert m.unit == "kg"

    assert mx.value == 1
    assert mx.unit == "kg"

    assert my.value == 1
    assert my.unit == "kg"

    assert Ip.value == 1
    assert Ip.unit == "kg m2"

    assert Id.value == 1
    assert Id.unit == "kg m2"

    assert width.value == 1
    assert width.unit == "m"

    assert i_d.value == 1
    assert i_d.unit == "m"

    assert o_d.value == 1
    assert o_d.unit == "m"

    assert kxx.value == 1
    assert kxx.unit == "N / m"

    assert kxy.value == 1
    assert kxy.unit == "N / m"

    assert kxz.value == 1
    assert kxz.unit == "N / m"

    assert kyx.value == 1
    assert kyx.unit == "N / m"

    assert kyy.value == 1
    assert kyy.unit == "N / m"

    assert kyz.value == 1
    assert kyz.unit == "N / m"

    assert kzx.value == 1
    assert kzx.unit == "N / m"

    assert kzy.value == 1
    assert kzy.unit == "N / m"

    assert kzz.value == 1
    assert kzz.unit == "N / m"

    assert cxx.value == 1
    assert cxx.unit == "N s / m"

    assert cxy.value == 1
    assert cxy.unit == "N s / m"

    assert cxz.value == 1
    assert cxz.unit == "N s / m"

    assert cyx.value == 1
    assert cyx.unit == "N s / m"

    assert cyy.value == 1
    assert cyy.unit == "N s / m"

    assert cyz.value == 1
    assert cyz.unit == "N s / m"

    assert czx.value == 1
    assert czx.unit == "N s / m"

    assert czy.value == 1
    assert czy.unit == "N s / m"

    assert czz.value == 1
    assert czz.unit == "N s / m"

    assert Poisson.value == 1.0
    assert Poisson.unit == ""


def test_unit_Q_input(auxiliary_function):
    results = auxiliary_function(
        E=Q(1, "N/m**2"),
        G_s=Q(1, "N/m**2"),
        rho=Q(1, "kg/m**3"),
        L=Q(1, "meter"),
        idl=Q(1, "meter"),
        idr=Q(1, "meter"),
        odl=Q(1, "meter"),
        odr=Q(1, "meter"),
        speed=Q(1, "radian/second"),
        frequency=Q(1, "radian/second"),
        m=Q(1, "kg"),
        mx=Q(1, "kg"),
        my=Q(1, "kg"),
        Ip=Q(1, "kg*m**2"),
        Id=Q(1, "kg*m**2"),
        width=Q(1, "meter"),
        i_d=Q(1, "meter"),
        o_d=Q(1, "meter"),
        kxx=Q(1, "N/m"),
        kxy=Q(1, "N/m"),
        kxz=Q(1, "N/m"),
        kyx=Q(1, "N/m"),
        kyy=Q(1, "N/m"),
        kyz=Q(1, "N/m"),
        kzx=Q(1, "N/m"),
        kzy=Q(1, "N/m"),
        kzz=Q(1, "N/m"),
        cxx=Q(1, "N*s/m"),
        cxy=Q(1, "N*s/m"),
        cxz=Q(1, "N*s/m"),
        cyx=Q(1, "N*s/m"),
        cyy=Q(1, "N*s/m"),
        cyz=Q(1, "N*s/m"),
        czx=Q(1, "N*s/m"),
        czy=Q(1, "N*s/m"),
        czz=Q(1, "N*s/m"),
        Poisson=Q(1, ""),
    )

    # check if all available units are tested
    assert len(results) == len(units)
    (
        E,
        G_s,
        rho,
        L,
        idl,
        idr,
        odl,
        odr,
        speed,
        frequency,
        m,
        mx,
        my,
        Ip,
        Id,
        width,
        i_d,
        o_d,
        kxx,
        kxy,
        kxz,
        kyx,
        kyy,
        kyz,
        kzx,
        kzy,
        kzz,
        cxx,
        cxy,
        cxz,
        cyx,
        cyy,
        cyz,
        czx,
        czy,
        czz,
        Poisson,
    ) = results

    assert E.value == 1
    assert E.unit == "N / m2"

    assert G_s.value == 1
    assert G_s.unit == "N / m2"

    assert rho.value == 1
    assert rho.unit == "kilogram / m3"

    assert L.value == 1
    assert L.unit == "meter"

    assert idl.value == 1
    assert idl.unit == "meter"

    assert idr.value == 1
    assert idr.unit == "meter"

    assert odl.value == 1
    assert odl.unit == "meter"

    assert odr.value == 1
    assert odr.unit == "meter"

    assert speed.value == 1
    assert speed.unit == "radian/second"

    assert frequency.value == 1
    assert frequency.unit == "radian/second"

    assert m.value == 1
    assert m.unit == "kg"

    assert mx.value == 1
    assert mx.unit == "kg"

    assert my.value == 1
    assert my.unit == "kg"

    assert Ip.value == 1
    assert Ip.unit == "kg m2"

    assert Id.value == 1
    assert Id.unit == "kg m2"

    assert width.value == 1
    assert width.unit == "m"

    assert i_d.value == 1
    assert i_d.unit == "m"

    assert o_d.value == 1
    assert o_d.unit == "m"

    assert kxx.value == 1
    assert kxx.unit == "N / m"

    assert kxy.value == 1
    assert kxy.unit == "N / m"

    assert kxz.value == 1
    assert kxz.unit == "N / m"

    assert kyx.value == 1
    assert kyx.unit == "N / m"

    assert kyy.value == 1
    assert kyy.unit == "N / m"

    assert kyz.value == 1
    assert kyz.unit == "N / m"

    assert kzx.value == 1
    assert kzx.unit == "N / m"

    assert kzy.value == 1
    assert kzy.unit == "N / m"

    assert kzz.value == 1
    assert kzz.unit == "N / m"

    assert cxx.value == 1
    assert cxx.unit == "N s / m"

    assert cxy.value == 1
    assert cxy.unit == "N s / m"

    assert cxz.value == 1
    assert cxz.unit == "N s / m"

    assert cyx.value == 1
    assert cyx.unit == "N s / m"

    assert cyy.value == 1
    assert cyy.unit == "N s / m"

    assert cyz.value == 1
    assert cyz.unit == "N s / m"

    assert czx.value == 1
    assert czx.unit == "N s / m"

    assert czy.value == 1
    assert czy.unit == "N s / m"

    assert czz.value == 1
    assert czz.unit == "N s / m"

    assert Poisson.value == 1.0
    assert Poisson.unit == ""


def test_unit_Q_conversion(auxiliary_function):
    results = auxiliary_function(
        E=Q(1, "lbf/in**2"),
        G_s=Q(1, "lbf/in**2"),
        rho=Q(1, "lb/foot**3"),
        L=Q(1, "inches"),
        idl=Q(1, "inches"),
        idr=Q(1, "inches"),
        odl=Q(1, "inches"),
        odr=Q(1, "inches"),
        speed=Q(1, "RPM"),
        frequency=Q(1, "RPM"),
        m=Q(1, "lb"),
        mx=Q(1, "lb"),
        my=Q(1, "lb"),
        Ip=Q(1, "lb*in**2"),
        Id=Q(1, "lb*in**2"),
        width=Q(1, "inches"),
        i_d=Q(1, "inches"),
        o_d=Q(1, "inches"),
        kxx=Q(1, "lbf/in"),
        kxy=Q(1, "lbf/in"),
        kxz=Q(1, "lbf/in"),
        kyx=Q(1, "lbf/in"),
        kyy=Q(1, "lbf/in"),
        kyz=Q(1, "lbf/in"),
        kzx=Q(1, "lbf/in"),
        kzy=Q(1, "lbf/in"),
        kzz=Q(1, "lbf/in"),
        cxx=Q(1, "lbf*s/in"),
        cxy=Q(1, "lbf*s/in"),
        cxz=Q(1, "lbf*s/in"),
        cyx=Q(1, "lbf*s/in"),
        cyy=Q(1, "lbf*s/in"),
        cyz=Q(1, "lbf*s/in"),
        czx=Q(1, "lbf*s/in"),
        czy=Q(1, "lbf*s/in"),
        czz=Q(1, "lbf*s/in"),
        Poisson=Q(1, ""),
    )

    # check if all available units are tested
    assert len(results) == len(units)

    (
        E,
        G_s,
        rho,
        L,
        idl,
        idr,
        odl,
        odr,
        speed,
        frequency,
        m,
        mx,
        my,
        Ip,
        Id,
        width,
        i_d,
        o_d,
        kxx,
        kxy,
        kxz,
        kyx,
        kyy,
        kyz,
        kzx,
        kzy,
        kzz,
        cxx,
        cxy,
        cxz,
        cyx,
        cyy,
        cyz,
        czx,
        czy,
        czz,
        Poisson,
    ) = results

    assert E.value == 6894.757388223366
    assert E.unit == "N / m2"

    assert G_s.value == 6894.757388223366
    assert G_s.unit == "N / m2"

    assert_allclose(rho.value, 16.01846337396014)
    assert rho.unit == "kilogram / m3"

    assert L.value == 0.025400000000000002
    assert L.unit == "meter"

    assert idl.value == 0.025400000000000002
    assert idl.unit == "meter"

    assert idr.value == 0.025400000000000002
    assert idr.unit == "meter"

    assert odl.value == 0.025400000000000002
    assert odl.unit == "meter"

    assert odr.value == 0.025400000000000002
    assert odr.unit == "meter"

    assert speed.value == 0.104719755
    assert speed.unit == "radian/second"

    assert frequency.value == 0.104719755
    assert frequency.unit == "radian/second"

    assert m.value == 0.45359237
    assert m.unit == "kg"

    assert mx.value == 0.45359237
    assert mx.unit == "kg"

    assert my.value == 0.45359237
    assert my.unit == "kg"

    assert Ip.value == 0.00029263965342920005
    assert Ip.unit == "kg m2"

    assert Id.value == 0.00029263965342920005
    assert Id.unit == "kg m2"

    assert width.value == 0.025400000000000002
    assert width.unit == "m"

    assert i_d.value == 0.025400000000000002
    assert i_d.unit == "m"

    assert o_d.value == 0.025400000000000002
    assert o_d.unit == "m"

    assert kxx.value == 175.12683766087352
    assert kxx.unit == "N / m"

    assert kxy.value == 175.12683766087352
    assert kxy.unit == "N / m"

    assert kxz.value == 175.12683766087352
    assert kxz.unit == "N / m"

    assert kyx.value == 175.12683766087352
    assert kyx.unit == "N / m"

    assert kyy.value == 175.12683766087352
    assert kyy.unit == "N / m"

    assert kyz.value == 175.12683766087352
    assert kyz.unit == "N / m"

    assert kzx.value == 175.12683766087352
    assert kzx.unit == "N / m"

    assert kzy.value == 175.12683766087352
    assert kzy.unit == "N / m"

    assert kzz.value == 175.12683766087352
    assert kzz.unit == "N / m"

    assert cxx.value == 175.12683766087352
    assert cxx.unit == "N s / m"

    assert cxy.value == 175.12683766087352
    assert cxy.unit == "N s / m"

    assert cxz.value == 175.12683766087352
    assert cxz.unit == "N s / m"

    assert cyx.value == 175.12683766087352
    assert cyx.unit == "N s / m"

    assert cyy.value == 175.12683766087352
    assert cyy.unit == "N s / m"

    assert cyz.value == 175.12683766087352
    assert cyz.unit == "N s / m"

    assert czx.value == 175.12683766087352
    assert czx.unit == "N s / m"

    assert czy.value == 175.12683766087352
    assert czy.unit == "N s / m"

    assert czz.value == 175.12683766087352
    assert czz.unit == "N s / m"

    assert Poisson.value == 1.0
    assert Poisson.unit == ""
