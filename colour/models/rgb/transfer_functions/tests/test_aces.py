"""
Define the unit tests for the :mod:`colour.models.rgb.transfer_functions.aces`
module.
"""

import unittest

import numpy as np

from colour.constants import TOLERANCE_ABSOLUTE_TESTS
from colour.models.rgb.transfer_functions import (
    log_decoding_ACEScc,
    log_decoding_ACEScct,
    log_decoding_ACESproxy,
    log_encoding_ACEScc,
    log_encoding_ACEScct,
    log_encoding_ACESproxy,
)
from colour.utilities import domain_range_scale, ignore_numpy_errors

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestLogEncoding_ACESproxy",
    "TestLogDecoding_ACESproxy",
    "TestLogEncoding_ACEScc",
    "TestLogDecoding_ACEScc",
    "TestLogDecoding_ACEScct",
]


class TestLogEncoding_ACESproxy(unittest.TestCase):
    """
    Define :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACESproxy`
    definition unit tests methods.
    """

    def test_log_encoding_ACESproxy(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACESproxy` definition.
        """

        np.testing.assert_allclose(
            log_encoding_ACESproxy(0.0),
            0.062561094819159,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_encoding_ACESproxy(0.18),
            0.416422287390029,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_encoding_ACESproxy(0.18, 12),
            0.416361416361416,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_encoding_ACESproxy(1.0),
            0.537634408602151,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        self.assertEqual(log_encoding_ACESproxy(0.18, out_int=True), 426)

    def test_n_dimensional_log_encoding_ACESproxy(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACESproxy` definition n-dimensional arrays support.
        """

        lin_AP1 = 0.18
        ACESproxy = log_encoding_ACESproxy(lin_AP1)

        lin_AP1 = np.tile(lin_AP1, 6)
        ACESproxy = np.tile(ACESproxy, 6)
        np.testing.assert_allclose(
            log_encoding_ACESproxy(lin_AP1),
            ACESproxy,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        lin_AP1 = np.reshape(lin_AP1, (2, 3))
        ACESproxy = np.reshape(ACESproxy, (2, 3))
        np.testing.assert_allclose(
            log_encoding_ACESproxy(lin_AP1),
            ACESproxy,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        lin_AP1 = np.reshape(lin_AP1, (2, 3, 1))
        ACESproxy = np.reshape(ACESproxy, (2, 3, 1))
        np.testing.assert_allclose(
            log_encoding_ACESproxy(lin_AP1),
            ACESproxy,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_log_encoding_ACESproxy(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACESproxy` definition domain and range scale support.
        """

        lin_AP1 = 0.18
        ACESproxy = log_encoding_ACESproxy(lin_AP1)

        d_r = (("reference", 1), ("1", 1), ("100", 100))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    log_encoding_ACESproxy(lin_AP1 * factor),
                    ACESproxy * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_nan_log_encoding_ACESproxy(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACESproxy` definition nan support.
        """

        log_encoding_ACESproxy(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan])
        )


class TestLogDecoding_ACESproxy(unittest.TestCase):
    """
    Define :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACESproxy`
    definition unit tests methods.
    """

    def test_log_decoding_ACESproxy(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACESproxy` definition.
        """

        np.testing.assert_allclose(
            log_decoding_ACESproxy(0.062561094819159),
            0.0,
            atol=0.01,
        )

        np.testing.assert_allclose(
            log_decoding_ACESproxy(0.416422287390029),
            0.18,
            atol=0.01,
        )

        np.testing.assert_allclose(
            log_decoding_ACESproxy(0.416361416361416, 12),
            0.18,
            atol=0.01,
        )

        np.testing.assert_allclose(
            log_decoding_ACESproxy(0.537634408602151),
            1.0,
            atol=0.01,
        )

        np.testing.assert_allclose(
            log_decoding_ACESproxy(426, in_int=True),
            0.18,
            atol=0.01,
        )

    def test_n_dimensional_log_decoding_ACESproxy(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACESproxy` definition n-dimensional arrays support.
        """

        ACESproxy = 0.416422287390029
        lin_AP1 = log_decoding_ACESproxy(ACESproxy)

        ACESproxy = np.tile(ACESproxy, 6)
        lin_AP1 = np.tile(lin_AP1, 6)
        np.testing.assert_allclose(
            log_decoding_ACESproxy(ACESproxy),
            lin_AP1,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        ACESproxy = np.reshape(ACESproxy, (2, 3))
        lin_AP1 = np.reshape(lin_AP1, (2, 3))
        np.testing.assert_allclose(
            log_decoding_ACESproxy(ACESproxy),
            lin_AP1,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        ACESproxy = np.reshape(ACESproxy, (2, 3, 1))
        lin_AP1 = np.reshape(lin_AP1, (2, 3, 1))
        np.testing.assert_allclose(
            log_decoding_ACESproxy(ACESproxy),
            lin_AP1,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_log_decoding_ACESproxy(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACESproxy` definition domain and range scale support.
        """

        ACESproxy = 426.0
        lin_AP1 = log_decoding_ACESproxy(ACESproxy)

        d_r = (("reference", 1), ("1", 1), ("100", 100))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    log_decoding_ACESproxy(ACESproxy * factor),
                    lin_AP1 * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_nan_log_decoding_ACESproxy(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACESproxy` definition nan support.
        """

        log_decoding_ACESproxy(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan])
        )


class TestLogEncoding_ACEScc(unittest.TestCase):
    """
    Define :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScc` definition unit tests methods.
    """

    def test_log_encoding_ACEScc(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScc` definition.
        """

        np.testing.assert_allclose(
            log_encoding_ACEScc(0.0),
            -0.358447488584475,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_encoding_ACEScc(0.18),
            0.413588402492442,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_encoding_ACEScc(1.0),
            0.554794520547945,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_n_dimensional_log_encoding_ACEScc(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScc` definition n-dimensional arrays support.
        """

        lin_AP1 = 0.18
        ACEScc = log_encoding_ACEScc(lin_AP1)

        lin_AP1 = np.tile(lin_AP1, 6)
        ACEScc = np.tile(ACEScc, 6)
        np.testing.assert_allclose(
            log_encoding_ACEScc(lin_AP1), ACEScc, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        lin_AP1 = np.reshape(lin_AP1, (2, 3))
        ACEScc = np.reshape(ACEScc, (2, 3))
        np.testing.assert_allclose(
            log_encoding_ACEScc(lin_AP1), ACEScc, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        lin_AP1 = np.reshape(lin_AP1, (2, 3, 1))
        ACEScc = np.reshape(ACEScc, (2, 3, 1))
        np.testing.assert_allclose(
            log_encoding_ACEScc(lin_AP1), ACEScc, atol=TOLERANCE_ABSOLUTE_TESTS
        )

    def test_domain_range_scale_log_encoding_ACEScc(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScc` definition domain and range scale support.
        """

        lin_AP1 = 0.18
        ACEScc = log_encoding_ACEScc(lin_AP1)

        d_r = (("reference", 1), ("1", 1), ("100", 100))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    log_encoding_ACEScc(lin_AP1 * factor),
                    ACEScc * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_nan_log_encoding_ACEScc(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScc` definition nan support.
        """

        log_encoding_ACEScc(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan])
        )


class TestLogDecoding_ACEScc(unittest.TestCase):
    """
    Define :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScc` definition unit tests methods.
    """

    def test_log_decoding_ACEScc(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScc` definition.
        """

        np.testing.assert_allclose(
            log_decoding_ACEScc(-0.358447488584475),
            0.0,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_decoding_ACEScc(0.413588402492442),
            0.18,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_decoding_ACEScc(0.554794520547945),
            1.0,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_n_dimensional_log_decoding_ACEScc(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScc` definition n-dimensional arrays support.
        """

        ACEScc = 0.413588402492442
        lin_AP1 = log_decoding_ACEScc(ACEScc)

        ACEScc = np.tile(ACEScc, 6)
        lin_AP1 = np.tile(lin_AP1, 6)
        np.testing.assert_allclose(
            log_decoding_ACEScc(ACEScc), lin_AP1, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        ACEScc = np.reshape(ACEScc, (2, 3))
        lin_AP1 = np.reshape(lin_AP1, (2, 3))
        np.testing.assert_allclose(
            log_decoding_ACEScc(ACEScc), lin_AP1, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        ACEScc = np.reshape(ACEScc, (2, 3, 1))
        lin_AP1 = np.reshape(lin_AP1, (2, 3, 1))
        np.testing.assert_allclose(
            log_decoding_ACEScc(ACEScc), lin_AP1, atol=TOLERANCE_ABSOLUTE_TESTS
        )

    def test_domain_range_scale_log_decoding_ACEScc(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScc` definition domain and range scale support.
        """

        ACEScc = 0.413588402492442
        lin_AP1 = log_decoding_ACEScc(ACEScc)

        d_r = (("reference", 1), ("1", 1), ("100", 100))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    log_decoding_ACEScc(ACEScc * factor),
                    lin_AP1 * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_nan_log_decoding_ACEScc(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScc` definition nan support.
        """

        log_decoding_ACEScc(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan])
        )


class TestLogEncoding_ACEScct(unittest.TestCase):
    """
    Define :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScct` definition unit tests methods.
    """

    def test_log_encoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScct` definition.
        """

        np.testing.assert_allclose(
            log_encoding_ACEScct(0.0),
            0.072905534195835495,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_encoding_ACEScct(0.18),
            0.413588402492442,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_encoding_ACEScct(1.0),
            0.554794520547945,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_n_dimensional_log_encoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScct` definition n-dimensional arrays support.
        """

        lin_AP1 = 0.18
        ACEScct = log_encoding_ACEScct(lin_AP1)

        lin_AP1 = np.tile(lin_AP1, 6)
        ACEScct = np.tile(ACEScct, 6)
        np.testing.assert_allclose(
            log_encoding_ACEScct(lin_AP1),
            ACEScct,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        lin_AP1 = np.reshape(lin_AP1, (2, 3))
        ACEScct = np.reshape(ACEScct, (2, 3))
        np.testing.assert_allclose(
            log_encoding_ACEScct(lin_AP1),
            ACEScct,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        lin_AP1 = np.reshape(lin_AP1, (2, 3, 1))
        ACEScct = np.reshape(ACEScct, (2, 3, 1))
        np.testing.assert_allclose(
            log_encoding_ACEScct(lin_AP1),
            ACEScct,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_log_encoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScct` definition domain and range scale support.
        """

        lin_AP1 = 0.18
        ACEScct = log_encoding_ACEScct(lin_AP1)

        d_r = (("reference", 1), ("1", 1), ("100", 100))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    log_encoding_ACEScct(lin_AP1 * factor),
                    ACEScct * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    def test_ACEScc_equivalency_log_encoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScct` definition ACEScc equivalency, and explicit requirement
        specified by AMPAS ACES specification S-2016-001
        (https://github.com/ampas/aces-dev/blob/v1.0.3/documents/LaTeX/\
S-2016-001/introduction.tex#L14)
        """

        equiv = np.linspace(0.0078125, 222.86094420380761, 100)
        np.testing.assert_allclose(
            log_encoding_ACEScct(equiv),
            log_encoding_ACEScc(equiv),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    @ignore_numpy_errors
    def test_nan_log_encoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_encoding_ACEScct` definition nan support.
        """

        log_encoding_ACEScct(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan])
        )


class TestLogDecoding_ACEScct(unittest.TestCase):
    """
    Define :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScct` definition unit tests methods.
    """

    def test_log_decoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScct` definition.
        """

        np.testing.assert_allclose(
            log_decoding_ACEScct(0.072905534195835495),
            0.0,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_decoding_ACEScct(0.41358840249244228),
            0.18,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        np.testing.assert_allclose(
            log_decoding_ACEScct(0.554794520547945),
            1.0,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_n_dimensional_log_decoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScct` definition n-dimensional arrays support.
        """

        ACEScct = 0.413588402492442
        lin_AP1 = log_decoding_ACEScct(ACEScct)

        ACEScct = np.tile(ACEScct, 6)
        lin_AP1 = np.tile(lin_AP1, 6)
        np.testing.assert_allclose(
            log_decoding_ACEScct(ACEScct),
            lin_AP1,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        ACEScct = np.reshape(ACEScct, (2, 3))
        lin_AP1 = np.reshape(lin_AP1, (2, 3))
        np.testing.assert_allclose(
            log_decoding_ACEScct(ACEScct),
            lin_AP1,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

        ACEScct = np.reshape(ACEScct, (2, 3, 1))
        lin_AP1 = np.reshape(lin_AP1, (2, 3, 1))
        np.testing.assert_allclose(
            log_decoding_ACEScct(ACEScct),
            lin_AP1,
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    def test_domain_range_scale_log_decoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScct` definition domain and range scale support.
        """

        ACEScc = 0.413588402492442
        lin_AP1 = log_decoding_ACEScct(ACEScc)

        d_r = (("reference", 1), ("1", 1), ("100", 100))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    log_decoding_ACEScct(ACEScc * factor),
                    lin_AP1 * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    def test_ACEScc_equivalency_log_decoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScct` definition ACEScc equivalency, and explicit requirement
        specified by AMPAS ACES specification S-2016-001
        (https://github.com/ampas/aces-dev/blob/v1.0.3/documents/LaTeX/\
S-2016-001/introduction.tex#L14)
        """

        equiv = np.linspace(0.15525114155251146, 1.0, 100)
        np.testing.assert_allclose(
            log_decoding_ACEScct(equiv),
            log_decoding_ACEScc(equiv),
            atol=TOLERANCE_ABSOLUTE_TESTS,
        )

    @ignore_numpy_errors
    def test_nan_log_decoding_ACEScct(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.aces.\
log_decoding_ACEScct` definition nan support.
        """

        log_decoding_ACEScct(
            np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan])
        )


if __name__ == "__main__":
    unittest.main()
