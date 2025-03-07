"""
Define the unit tests for the :mod:`colour.models.rgb.transfer_functions.dcdm`
module.
"""

import unittest

import numpy as np

from colour.constants import TOLERANCE_ABSOLUTE_TESTS
from colour.models.rgb.transfer_functions import eotf_DCDM, eotf_inverse_DCDM
from colour.utilities import domain_range_scale, ignore_numpy_errors

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "TestEotf_inverse_DCDM",
    "TestEotf_DCDM",
]


class TestEotf_inverse_DCDM(unittest.TestCase):
    """
    Define :func:`colour.models.rgb.transfer_functions.dcdm.eotf_inverse_DCDM`
    definition unit tests methods.
    """

    def test_eotf_inverse_DCDM(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.\
dcdm.eotf_inverse_DCDM` definition.
        """

        np.testing.assert_allclose(
            eotf_inverse_DCDM(0.0), 0.0, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        np.testing.assert_allclose(
            eotf_inverse_DCDM(0.18), 0.11281861, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        np.testing.assert_allclose(
            eotf_inverse_DCDM(1.0), 0.21817973, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        self.assertEqual(eotf_inverse_DCDM(0.18, out_int=True), 462)

    def test_n_dimensional_eotf_inverse_DCDM(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.dcdm.\
eotf_inverse_DCDM` definition n-dimensional arrays support.
        """

        XYZ = 0.18
        XYZ_p = eotf_inverse_DCDM(XYZ)

        XYZ = np.tile(XYZ, 6)
        XYZ_p = np.tile(XYZ_p, 6)
        np.testing.assert_allclose(
            eotf_inverse_DCDM(XYZ), XYZ_p, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        XYZ = np.reshape(XYZ, (2, 3))
        XYZ_p = np.reshape(XYZ_p, (2, 3))
        np.testing.assert_allclose(
            eotf_inverse_DCDM(XYZ), XYZ_p, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        XYZ = np.reshape(XYZ, (2, 3, 1))
        XYZ_p = np.reshape(XYZ_p, (2, 3, 1))
        np.testing.assert_allclose(
            eotf_inverse_DCDM(XYZ), XYZ_p, atol=TOLERANCE_ABSOLUTE_TESTS
        )

    def test_domain_range_scale_eotf_inverse_DCDM(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.\
dcdm.eotf_inverse_DCDM` definition domain and range scale support.
        """

        XYZ = 0.18
        XYZ_p = eotf_inverse_DCDM(XYZ)

        d_r = (("reference", 1), ("1", 1), ("100", 1))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    eotf_inverse_DCDM(XYZ * factor),
                    XYZ_p * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_nan_eotf_inverse_DCDM(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.dcdm.\
eotf_inverse_DCDM` definition nan support.
        """

        eotf_inverse_DCDM(np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]))


class TestEotf_DCDM(unittest.TestCase):
    """
    Define :func:`colour.models.rgb.transfer_functions.dcdm.eotf_DCDM`
    definition unit tests methods.
    """

    def test_eotf_DCDM(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.dcdm.eotf_DCDM`
        definition.
        """

        np.testing.assert_allclose(
            eotf_DCDM(0.0), 0.0, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        np.testing.assert_allclose(
            eotf_DCDM(0.11281861), 0.18, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        np.testing.assert_allclose(
            eotf_DCDM(0.21817973), 1.0, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        np.testing.assert_allclose(
            eotf_DCDM(462, in_int=True), 0.18, atol=1e-5
        )

    def test_n_dimensional_eotf_DCDM(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.dcdm.eotf_DCDM`
        definition n-dimensional arrays support.
        """

        XYZ_p = 0.11281861
        XYZ = eotf_DCDM(XYZ_p)

        XYZ_p = np.tile(XYZ_p, 6)
        XYZ = np.tile(XYZ, 6)
        np.testing.assert_allclose(
            eotf_DCDM(XYZ_p), XYZ, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        XYZ_p = np.reshape(XYZ_p, (2, 3))
        XYZ = np.reshape(XYZ, (2, 3))
        np.testing.assert_allclose(
            eotf_DCDM(XYZ_p), XYZ, atol=TOLERANCE_ABSOLUTE_TESTS
        )

        XYZ_p = np.reshape(XYZ_p, (2, 3, 1))
        XYZ = np.reshape(XYZ, (2, 3, 1))
        np.testing.assert_allclose(
            eotf_DCDM(XYZ_p), XYZ, atol=TOLERANCE_ABSOLUTE_TESTS
        )

    def test_domain_range_scale_eotf_DCDM(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.dcdm.eotf_DCDM`
        definition domain and range scale support.
        """

        XYZ_p = 0.11281861
        XYZ = eotf_DCDM(XYZ_p)

        d_r = (("reference", 1), ("1", 1), ("100", 1))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_allclose(
                    eotf_DCDM(XYZ_p * factor),
                    XYZ * factor,
                    atol=TOLERANCE_ABSOLUTE_TESTS,
                )

    @ignore_numpy_errors
    def test_nan_eotf_DCDM(self):
        """
        Test :func:`colour.models.rgb.transfer_functions.dcdm.eotf_DCDM`
        definition nan support.
        """

        eotf_DCDM(np.array([-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]))


if __name__ == "__main__":
    unittest.main()
