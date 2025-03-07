# !/usr/bin/env python
"""Define the unit tests for the :mod:`colour.appearance.ciecam16` module."""

import unittest
from itertools import product

import numpy as np

from colour.appearance import (
    VIEWING_CONDITIONS_CIECAM16,
    CAM_Specification_CIECAM16,
    CIECAM16_to_XYZ,
    InductionFactors_CIECAM16,
    XYZ_to_CIECAM16,
)
from colour.constants import TOLERANCE_ABSOLUTE_TESTS
from colour.utilities import (
    as_float_array,
    domain_range_scale,
    ignore_numpy_errors,
    tsplit,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestXYZ_to_CIECAM16",
    "TestCIECAM16_to_XYZ",
]


class TestXYZ_to_CIECAM16(unittest.TestCase):
    """
    Define :func:`colour.appearance.ciecam16.XYZ_to_CIECAM16` definition unit
    tests methods.
    """

    def test_XYZ_to_CIECAM16(self):
        """
        Test :func:`colour.appearance.ciecam16.XYZ_to_CIECAM16` definition.
        """

        XYZ = np.array([19.01, 20.00, 21.78])
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 318.31
        Y_b = 20
        surround = VIEWING_CONDITIONS_CIECAM16["Average"]
        np.testing.assert_allclose(
            XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround),
            np.array(
                [
                    41.73120791,
                    0.10335574,
                    217.06795977,
                    2.34501507,
                    195.37170899,
                    0.10743677,
                    275.59498615,
                    np.nan,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ = np.array([57.06, 43.06, 31.96])
        L_A = 31.83
        np.testing.assert_allclose(
            XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround),
            np.array(
                [
                    65.42828069,
                    49.67956420,
                    17.48659243,
                    52.94308868,
                    152.06985268,
                    42.62473321,
                    398.03047943,
                    np.nan,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ = np.array([3.53, 6.56, 2.14])
        XYZ_w = np.array([109.85, 100, 35.58])
        L_A = 318.31
        np.testing.assert_allclose(
            XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround),
            np.array(
                [
                    21.36052893,
                    50.99381895,
                    178.86724266,
                    61.57953092,
                    139.78582768,
                    53.00732582,
                    223.01823806,
                    np.nan,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ = np.array([19.01, 20.00, 21.78])
        L_A = 318.31
        np.testing.assert_allclose(
            XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround),
            np.array(
                [
                    41.36326063,
                    52.81154022,
                    258.88676291,
                    53.12406914,
                    194.52011798,
                    54.89682038,
                    311.24768647,
                    np.nan,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ = np.array([61.45276998, 7.00421901, 82.2406738])
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 4.074366543152521
        np.testing.assert_allclose(
            XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround),
            np.array(
                [
                    2.212842606688056,
                    597.366327557872864,
                    352.035143755398565,
                    484.428915071471351,
                    18.402345804194972,
                    431.850377022773955,
                    378.267899100834541,
                    np.nan,
                ]
            ),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ = np.array([60.70, 49.60, 10.29])
        XYZ_w = np.array([96.46, 100.00, 108.62])
        L_A = 40
        Y_b = 16
        np.testing.assert_allclose(
            XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround),
            np.array(
                [
                    70.4406,
                    58.6035,
                    57.9145,
                    54.5604,
                    172.1555,
                    51.2479,
                    50.7425,
                    np.nan,
                ]
            ),
            atol=5e-5,
        )

    def test_n_dimensional_XYZ_to_CIECAM16(self):
        """
        Test :func:`colour.appearance.ciecam16.XYZ_to_CIECAM16` definition
        n-dimensional support.
        """

        XYZ = np.array([19.01, 20.00, 21.78])
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 318.31
        Y_b = 20
        surround = VIEWING_CONDITIONS_CIECAM16["Average"]
        specification = XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround)

        XYZ = np.tile(XYZ, (6, 1))
        specification = np.tile(specification, (6, 1))
        np.testing.assert_allclose(
            XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround),
            specification,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ_w = np.tile(XYZ_w, (6, 1))
        np.testing.assert_allclose(
            XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround),
            specification,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ = np.reshape(XYZ, (2, 3, 3))
        XYZ_w = np.reshape(XYZ_w, (2, 3, 3))
        specification = np.reshape(specification, (2, 3, 8))
        np.testing.assert_allclose(
            XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround),
            specification,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    @ignore_numpy_errors
    def test_domain_range_scale_XYZ_to_CIECAM16(self):
        """
        Test :func:`colour.appearance.ciecam16.XYZ_to_CIECAM16` definition
        domain and range scale support.
        """

        XYZ = np.array([19.01, 20.00, 21.78])
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 318.31
        Y_b = 20
        surround = VIEWING_CONDITIONS_CIECAM16["Average"]
        specification = XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround)

        d_r = (
            ("reference", 1, 1),
            (
                "1",
                0.01,
                np.array(
                    [
                        1 / 100,
                        1 / 100,
                        1 / 360,
                        1 / 100,
                        1 / 100,
                        1 / 100,
                        1 / 400,
                        np.nan,
                    ]
                ),
            ),
            (
                "100",
                1,
                np.array([1, 1, 100 / 360, 1, 1, 1, 100 / 400, np.nan]),
            ),
        )
        for scale, factor_a, factor_b in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    XYZ_to_CIECAM16(
                        XYZ * factor_a, XYZ_w * factor_a, L_A, Y_b, surround
                    ),
                    as_float_array(specification) * factor_b,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_nan_XYZ_to_CIECAM16(self):
        """
        Test :func:`colour.appearance.ciecam16.XYZ_to_CIECAM16` definition
        nan support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = np.array(list(set(product(cases, repeat=3))))
        surround = InductionFactors_CIECAM16(
            cases[0, 0], cases[0, 0], cases[0, 0]
        )
        XYZ_to_CIECAM16(cases, cases, cases[..., 0], cases[..., 0], surround)


class TestCIECAM16_to_XYZ(unittest.TestCase):
    """
    Define :func:`colour.appearance.ciecam16.CIECAM16_to_XYZ` definition unit
    tests methods.
    """

    def test_CIECAM16_to_XYZ(self):
        """
        Test :func:`colour.appearance.ciecam16.CIECAM16_to_XYZ` definition.
        """

        specification = CAM_Specification_CIECAM16(
            41.73120791, 0.10335574, 217.06795977
        )
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 318.31
        Y_b = 20
        surround = VIEWING_CONDITIONS_CIECAM16["Average"]
        np.testing.assert_allclose(
            CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround),
            np.array([19.01, 20.00, 21.78]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        specification = CAM_Specification_CIECAM16(
            65.42828069, 49.67956420, 17.48659243
        )
        L_A = 31.83
        np.testing.assert_allclose(
            CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround),
            np.array([57.06, 43.06, 31.96]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        specification = CAM_Specification_CIECAM16(
            21.36052893, 50.99381895, 178.86724266
        )
        XYZ_w = np.array([109.85, 100, 35.58])
        L_A = 318.31
        np.testing.assert_allclose(
            CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround),
            np.array([3.53, 6.56, 2.14]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        specification = CAM_Specification_CIECAM16(
            41.36326063, 52.81154022, 258.88676291
        )
        L_A = 318.31
        np.testing.assert_allclose(
            CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround),
            np.array([19.01, 20.00, 21.78]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        specification = CAM_Specification_CIECAM16(
            2.212842606688056, 597.366327557872864, 352.035143755398565
        )
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 4.074366543152521
        np.testing.assert_allclose(
            CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround),
            np.array([61.45276998, 7.00421901, 82.2406738]),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        specification = CAM_Specification_CIECAM16(70.4406, 58.6035, 57.9145)
        XYZ_w = np.array([96.46, 100.00, 108.62])
        L_A = 40
        Y_b = 16
        np.testing.assert_allclose(
            CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround),
            np.array([60.70, 49.60, 10.29]),
            atol=1e-4,
        )

    def test_n_dimensional_CIECAM16_to_XYZ(self):
        """
        Test :func:`colour.appearance.ciecam16.CIECAM16_to_XYZ` definition
        n-dimensional support.
        """

        XYZ = np.array([19.01, 20.00, 21.78])
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 318.31
        Y_b = 20
        surround = VIEWING_CONDITIONS_CIECAM16["Average"]
        specification = XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround)
        XYZ = CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround)

        specification = CAM_Specification_CIECAM16(
            *np.transpose(np.tile(tsplit(specification), (6, 1))).tolist()
        )
        XYZ = np.tile(XYZ, (6, 1))
        np.testing.assert_allclose(
            CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround),
            XYZ,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        XYZ_w = np.tile(XYZ_w, (6, 1))
        np.testing.assert_allclose(
            CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround),
            XYZ,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        specification = CAM_Specification_CIECAM16(
            *tsplit(np.reshape(specification, (2, 3, 8))).tolist()
        )
        XYZ_w = np.reshape(XYZ_w, (2, 3, 3))
        XYZ = np.reshape(XYZ, (2, 3, 3))
        np.testing.assert_allclose(
            CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround),
            XYZ,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    @ignore_numpy_errors
    def test_domain_range_scale_CIECAM16_to_XYZ(self):
        """
        Test :func:`colour.appearance.ciecam16.CIECAM16_to_XYZ` definition
        domain and range scale support.
        """

        XYZ = np.array([19.01, 20.00, 21.78])
        XYZ_w = np.array([95.05, 100.00, 108.88])
        L_A = 318.31
        Y_b = 20
        surround = VIEWING_CONDITIONS_CIECAM16["Average"]
        specification = XYZ_to_CIECAM16(XYZ, XYZ_w, L_A, Y_b, surround)
        XYZ = CIECAM16_to_XYZ(specification, XYZ_w, L_A, Y_b, surround)

        d_r = (
            ("reference", 1, 1),
            (
                "1",
                np.array(
                    [
                        1 / 100,
                        1 / 100,
                        1 / 360,
                        1 / 100,
                        1 / 100,
                        1 / 100,
                        1 / 400,
                        np.nan,
                    ]
                ),
                0.01,
            ),
            (
                "100",
                np.array([1, 1, 100 / 360, 1, 1, 1, 100 / 400, np.nan]),
                1,
            ),
        )
        for scale, factor_a, factor_b in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    CIECAM16_to_XYZ(
                        specification * factor_a,
                        XYZ_w * factor_b,
                        L_A,
                        Y_b,
                        surround,
                    ),
                    XYZ * factor_b,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_raise_exception_CIECAM16_to_XYZ(self):
        """
        Test :func:`colour.appearance.ciecam16.CIECAM16_to_XYZ` definition
        raised exception.
        """

        self.assertRaises(
            ValueError,
            CIECAM16_to_XYZ,
            CAM_Specification_CIECAM16(
                41.731207905126638, None, 217.06795976739301
            ),
            np.array([95.05, 100.00, 108.88]),
            318.31,
            20.0,
            VIEWING_CONDITIONS_CIECAM16["Average"],
        )

    @ignore_numpy_errors
    def test_nan_CIECAM16_to_XYZ(self):
        """
        Test :func:`colour.appearance.ciecam16.CIECAM16_to_XYZ` definition nan
        support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = np.array(list(set(product(cases, repeat=3))))
        surround = InductionFactors_CIECAM16(
            cases[0, 0], cases[0, 0], cases[0, 0]
        )
        CIECAM16_to_XYZ(
            CAM_Specification_CIECAM16(
                cases[..., 0], cases[..., 0], cases[..., 0], M=50
            ),
            cases,
            cases[..., 0],
            cases[..., 0],
            surround,
        )


if __name__ == "__main__":
    unittest.main()
