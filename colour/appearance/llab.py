"""
:math:`LLAB(l:c)` Colour Appearance Model
=========================================

Defines the *:math:`LLAB(l:c)`* colour appearance model objects:

-   :class:`colour.appearance.InductionFactors_LLAB`
-   :attr:`colour.VIEWING_CONDITIONS_LLAB`
-   :class:`colour.CAM_Specification_LLAB`
-   :func:`colour.XYZ_to_LLAB`

References
----------
-   :cite:`Fairchild2013x` : Fairchild, M. D. (2013). LLAB Model. In Color
    Appearance Models (3rd ed., pp. 6025-6178). Wiley. ISBN:B00DAYO8E2
-   :cite:`Luo1996b` : Luo, Ming Ronnier, Lo, M.-C., & Kuo, W.-G. (1996). The
    LLAB (l:c) colour model. Color Research & Application, 21(6), 412-429.
    doi:10.1002/(SICI)1520-6378(199612)21:6<412::AID-COL4>3.0.CO;2-Z
-   :cite:`Luo1996c` : Luo, Ming Ronnier, & Morovic, J. (1996). Two Unsolved
    Issues in Colour Management - Colour Appearance and Gamut Mapping.
    Conference: 5th International Conference on High Technology: Imaging
    Science and Technology - Evolution & Promise, 136-147.
    http://www.researchgate.net/publication/\
236348295_Two_Unsolved_Issues_in_Colour_Management__\
Colour_Appearance_and_Gamut_Mapping
"""

from collections import namedtuple
from dataclasses import dataclass, field

import numpy as np

from colour.algebra import (
    polar_to_cartesian,
    sdiv,
    sdiv_mode,
    spow,
    vector_dot,
)
from colour.hints import ArrayLike, NDArrayFloat, Optional, Union
from colour.utilities import (
    CanonicalMapping,
    MixinDataclassArithmetic,
    as_float,
    as_float_array,
    from_range_degrees,
    to_domain_100,
    tsplit,
    tstack,
)

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "InductionFactors_LLAB",
    "VIEWING_CONDITIONS_LLAB",
    "MATRIX_XYZ_TO_RGB_LLAB",
    "MATRIX_RGB_TO_XYZ_LLAB",
    "CAM_ReferenceSpecification_LLAB",
    "CAM_Specification_LLAB",
    "XYZ_to_LLAB",
    "XYZ_to_RGB_LLAB",
    "chromatic_adaptation",
    "f",
    "opponent_colour_dimensions",
    "hue_angle",
    "chroma_correlate",
    "colourfulness_correlate",
    "saturation_correlate",
    "final_opponent_signals",
]


class InductionFactors_LLAB(
    namedtuple("InductionFactors_LLAB", ("D", "F_S", "F_L", "F_C"))
):
    """
    *:math:`LLAB(l:c)`* colour appearance model induction factors.

    Parameters
    ----------
    D
         *Discounting-the-Illuminant* factor :math:`D`.
    F_S
        Surround induction factor :math:`F_S`.
    F_L
        *Lightness* induction factor :math:`F_L`.
    F_C
        *Chroma* induction factor :math:`F_C`.

    References
    ----------
    :cite:`Fairchild2013x`, :cite:`Luo1996b`, :cite:`Luo1996c`
    """


VIEWING_CONDITIONS_LLAB: CanonicalMapping = CanonicalMapping(
    {
        "Reference Samples & Images, Average Surround, Subtending > 4": (
            InductionFactors_LLAB(1, 3, 0, 1)
        ),
        "Reference Samples & Images, Average Surround, Subtending < 4": (
            InductionFactors_LLAB(1, 3, 1, 1)
        ),
        "Television & VDU Displays, Dim Surround": (
            InductionFactors_LLAB(0.7, 3.5, 1, 1)
        ),
        "Cut Sheet Transparency, Dim Surround": (
            InductionFactors_LLAB(1, 5, 1, 1.1)
        ),
        "35mm Projection Transparency, Dark Surround": (
            InductionFactors_LLAB(0.7, 4, 1, 1)
        ),
    }
)
VIEWING_CONDITIONS_LLAB.__doc__ = """
Reference :math:`LLAB(l:c)` colour appearance model viewing conditions.

References
----------
:cite:`Fairchild2013x`, :cite:`Luo1996b`, :cite:`Luo1996c`

Aliases:

-   'ref_average_4_plus':
    'Reference Samples & Images, Average Surround, Subtending > 4'
-   'ref_average_4_minus':
    'Reference Samples & Images, Average Surround, Subtending < 4'
-   'tv_dim': 'Television & VDU Displays, Dim Surround'
-   'sheet_dim': 'Cut Sheet Transparency, Dim Surround'
-   'projected_dark': '35mm Projection Transparency, Dark Surround'
"""
VIEWING_CONDITIONS_LLAB["ref_average_4_plus"] = VIEWING_CONDITIONS_LLAB[
    "Reference Samples & Images, Average Surround, Subtending > 4"
]
VIEWING_CONDITIONS_LLAB["ref_average_4_minus"] = VIEWING_CONDITIONS_LLAB[
    "Reference Samples & Images, Average Surround, Subtending < 4"
]
VIEWING_CONDITIONS_LLAB["tv_dim"] = VIEWING_CONDITIONS_LLAB[
    "Television & VDU Displays, Dim Surround"
]
VIEWING_CONDITIONS_LLAB["sheet_dim"] = VIEWING_CONDITIONS_LLAB[
    "Cut Sheet Transparency, Dim Surround"
]
VIEWING_CONDITIONS_LLAB["projected_dark"] = VIEWING_CONDITIONS_LLAB[
    "35mm Projection Transparency, Dark Surround"
]

MATRIX_XYZ_TO_RGB_LLAB: NDArrayFloat = np.array(
    [
        [0.8951, 0.2664, -0.1614],
        [-0.7502, 1.7135, 0.0367],
        [0.0389, -0.0685, 1.0296],
    ]
)
"""
LLAB(l:c) colour appearance model *CIE XYZ* tristimulus values to normalised
cone responses matrix.
"""

MATRIX_RGB_TO_XYZ_LLAB: NDArrayFloat = np.linalg.inv(MATRIX_XYZ_TO_RGB_LLAB)
"""
LLAB(l:c) colour appearance model normalised cone responses to *CIE XYZ*
tristimulus values matrix.
"""


@dataclass
class CAM_ReferenceSpecification_LLAB(MixinDataclassArithmetic):
    """
    Define the *:math:`LLAB(l:c)`* colour appearance model reference
    specification.

    This specification has field names consistent with *Fairchild (2013)*
    reference.

    Parameters
    ----------
    L_L
        Correlate of *Lightness* :math:`L_L`.
    Ch_L
        Correlate of *chroma* :math:`Ch_L`.
    h_L
        *Hue* angle :math:`h_L` in degrees.
    s_L
        Correlate of *saturation* :math:`s_L`.
    C_L
        Correlate of *colourfulness* :math:`C_L`.
    HC
        *Hue* :math:`h` composition :math:`H^C`.
    A_L
        Opponent signal :math:`A_L`.
    B_L
        Opponent signal :math:`B_L`.

    References
    ----------
    :cite:`Fairchild2013x`, :cite:`Luo1996b`, :cite:`Luo1996c`
    """

    L_L: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    Ch_L: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    h_L: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    s_L: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    C_L: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    HC: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    A_L: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    B_L: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )


@dataclass
class CAM_Specification_LLAB(MixinDataclassArithmetic):
    """
    Define the *:math:`LLAB(l:c)`* colour appearance model specification.

    This specification has field names consistent with the remaining colour
    appearance models in :mod:`colour.appearance` but diverge from
    *Fairchild (2013)* reference.

    Parameters
    ----------
    J
        Correlate of *Lightness* :math:`L_L`.
    C
        Correlate of *chroma* :math:`Ch_L`.
    h
        *Hue* angle :math:`h_L` in degrees.
    s
        Correlate of *saturation* :math:`s_L`.
    M
        Correlate of *colourfulness* :math:`C_L`.
    HC
        *Hue* :math:`h` composition :math:`H^C`.
    a
        Opponent signal :math:`A_L`.
    b
        Opponent signal :math:`B_L`.

    Notes
    -----
    -   This specification is the one used in the current model implementation.

    References
    ----------
    :cite:`Fairchild2013x`, :cite:`Luo1996b`, :cite:`Luo1996c`
    """

    J: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    C: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    h: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    s: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    M: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    HC: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    a: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )
    b: Optional[Union[float, NDArrayFloat]] = field(
        default_factory=lambda: None
    )


def XYZ_to_LLAB(
    XYZ: ArrayLike,
    XYZ_0: ArrayLike,
    Y_b: ArrayLike,
    L: ArrayLike,
    surround: InductionFactors_LLAB = VIEWING_CONDITIONS_LLAB[
        "Reference Samples & Images, Average Surround, Subtending < 4"
    ],
) -> CAM_Specification_LLAB:
    """
    Compute the *:math:`LLAB(l:c)`* colour appearance model correlates.

    Parameters
    ----------
    XYZ
        *CIE XYZ* tristimulus values of test sample / stimulus.
    XYZ_0
        *CIE XYZ* tristimulus values of reference white.
    Y_b
        Luminance factor of the background in :math:`cd/m^2`.
    L
        Absolute luminance :math:`L` of reference white in :math:`cd/m^2`.
    surround
         Surround viewing conditions induction factors.

    Returns
    -------
    :class:`colour.CAM_Specification_LLAB`
        *:math:`LLAB(l:c)`* colour appearance model specification.

    Notes
    -----
    +------------+-----------------------+---------------+
    | **Domain** | **Scale - Reference** | **Scale - 1** |
    +============+=======================+===============+
    | ``XYZ``    | [0, 100]              | [0, 1]        |
    +------------+-----------------------+---------------+
    | ``XYZ_0``  | [0, 100]              | [0, 1]        |
    +------------+-----------------------+---------------+

    +------------------------------+-----------------------+---------------+
    | **Range**                    | **Scale - Reference** | **Scale - 1** |
    +==============================+=======================+===============+
    | ``CAM_Specification_LLAB.h`` | [0, 360]              | [0, 1]        |
    +------------------------------+-----------------------+---------------+

    References
    ----------
    :cite:`Fairchild2013x`, :cite:`Luo1996b`, :cite:`Luo1996c`

    Examples
    --------
    >>> XYZ = np.array([19.01, 20.00, 21.78])
    >>> XYZ_0 = np.array([95.05, 100.00, 108.88])
    >>> Y_b = 20.0
    >>> L = 318.31
    >>> surround = VIEWING_CONDITIONS_LLAB["ref_average_4_minus"]
    >>> XYZ_to_LLAB(XYZ, XYZ_0, Y_b, L, surround)  # doctest: +ELLIPSIS
    CAM_Specification_LLAB(J=37.3668650..., C=0.0089496..., h=270..., \
s=0.0002395..., M=0.0190185..., HC=None, a=..., b=-0.0190185...)
    """

    _X, Y, _Z = tsplit(to_domain_100(XYZ))
    RGB = XYZ_to_RGB_LLAB(to_domain_100(XYZ))
    RGB_0 = XYZ_to_RGB_LLAB(to_domain_100(XYZ_0))

    # Reference illuminant *CIE Standard Illuminant D Series* *D65*.
    XYZ_0r = np.array([95.05, 100.00, 108.88])
    RGB_0r = XYZ_to_RGB_LLAB(XYZ_0r)

    # Computing chromatic adaptation.
    XYZ_r = chromatic_adaptation(RGB, RGB_0, RGB_0r, Y, surround.D)

    # -------------------------------------------------------------------------
    # Computing the correlate of *Lightness* :math:`L_L`.
    # -------------------------------------------------------------------------
    # Computing opponent colour dimensions.
    L_L, a, b = tsplit(
        opponent_colour_dimensions(XYZ_r, Y_b, surround.F_S, surround.F_L)
    )

    # Computing perceptual correlates.
    # -------------------------------------------------------------------------
    # Computing the correlate of *chroma* :math:`Ch_L`.
    # -------------------------------------------------------------------------
    Ch_L = chroma_correlate(a, b)

    # -------------------------------------------------------------------------
    # Computing the correlate of *colourfulness* :math:`C_L`.
    # -------------------------------------------------------------------------
    C_L = colourfulness_correlate(L, L_L, Ch_L, surround.F_C)

    # -------------------------------------------------------------------------
    # Computing the correlate of *saturation* :math:`s_L`.
    # -------------------------------------------------------------------------
    s_L = saturation_correlate(Ch_L, L_L)

    # -------------------------------------------------------------------------
    # Computing the *hue* angle :math:`h_L`.
    # -------------------------------------------------------------------------
    h_L = hue_angle(a, b)
    # TODO: Implement hue composition computation.

    # -------------------------------------------------------------------------
    # Computing final opponent signals.
    # -------------------------------------------------------------------------
    A_L, B_L = tsplit(final_opponent_signals(C_L, h_L))

    return CAM_Specification_LLAB(
        L_L,
        Ch_L,
        as_float(from_range_degrees(h_L)),
        s_L,
        C_L,
        None,
        A_L,
        B_L,
    )


def XYZ_to_RGB_LLAB(XYZ: ArrayLike) -> NDArrayFloat:
    """
    Convert from *CIE XYZ* tristimulus values to normalised cone responses.

    Parameters
    ----------
    XYZ
        *CIE XYZ* tristimulus values.

    Returns
    -------
    :class:`numpy.ndarray`
        Normalised cone responses.

    Examples
    --------
    >>> XYZ = np.array([19.01, 20.00, 21.78])
    >>> XYZ_to_RGB_LLAB(XYZ)  # doctest: +ELLIPSIS
    array([ 0.9414279...,  1.0404012...,  1.0897088...])
    """

    XYZ = as_float_array(XYZ)

    with sdiv_mode():
        return vector_dot(MATRIX_XYZ_TO_RGB_LLAB, sdiv(XYZ, XYZ[..., 1, None]))


def chromatic_adaptation(
    RGB: ArrayLike,
    RGB_0: ArrayLike,
    RGB_0r: ArrayLike,
    Y: ArrayLike,
    D: ArrayLike = 1,
) -> NDArrayFloat:
    """
    Apply chromatic adaptation to given *RGB* normalised cone responses
    array.

    Parameters
    ----------
    RGB
        *RGB* normalised cone responses array of test sample / stimulus.
    RGB_0
        *RGB* normalised cone responses array of reference white.
    RGB_0r
        *RGB* normalised cone responses array of reference illuminant
        *CIE Standard Illuminant D Series* *D65*.
    Y
        Tristimulus values :math:`Y` of the stimulus.
    D
         *Discounting-the-Illuminant* factor normalised to domain [0, 1].

    Returns
    -------
    :class:`numpy.ndarray`
        Adapted *CIE XYZ* tristimulus values.

    Examples
    --------
    >>> RGB = np.array([0.94142795, 1.04040120, 1.08970885])
    >>> RGB_0 = np.array([0.94146023, 1.04039386, 1.08950293])
    >>> RGB_0r = np.array([0.94146023, 1.04039386, 1.08950293])
    >>> Y = 20.0
    >>> chromatic_adaptation(RGB, RGB_0, RGB_0r, Y)  # doctest: +ELLIPSIS
    array([ 19.01,  20.  ,  21.78])
    """

    R, G, B = tsplit(RGB)
    R_0, G_0, B_0 = tsplit(RGB_0)
    R_0r, G_0r, B_0r = tsplit(RGB_0r)
    Y = as_float_array(Y)
    D = as_float_array(D)

    beta = spow(B_0 / B_0r, 0.0834)

    R_r = (D * R_0r / R_0 + 1 - D) * R
    G_r = (D * G_0r / G_0 + 1 - D) * G
    B_r = (D * B_0r / spow(B_0, beta) + 1 - D) * spow(B, beta)

    RGB_r = tstack([R_r, G_r, B_r])

    Y = tstack([Y, Y, Y])

    XYZ_r = vector_dot(MATRIX_RGB_TO_XYZ_LLAB, RGB_r * Y)

    return XYZ_r


def f(x: ArrayLike, F_S: ArrayLike) -> NDArrayFloat:
    """
    Define the nonlinear response function of the *:math:`LLAB(l:c)`* colour
    appearance model used to model the nonlinear behaviour of various visual
    responses.

    Parameters
    ----------
    x
        Visual response variable :math:`x`.
    F_S
        Surround induction factor :math:`F_S`.

    Returns
    -------
    :class:`numpy.ndarray`
        Modeled visual response variable :math:`x`.

    Examples
    --------
    >>> x = np.array([0.23350512, 0.23351103, 0.23355179])
    >>> f(0.200009186234000, 3)  # doctest: +ELLIPSIS
    0.5848125...
    """

    x = as_float_array(x)
    F_S = as_float_array(F_S)

    one_F_s = 1 / F_S

    x_m = np.where(
        x > 0.008856,
        spow(x, one_F_s),
        ((spow(0.008856, one_F_s) - (16 / 116)) / 0.008856) * x + (16 / 116),
    )

    return as_float(x_m)


def opponent_colour_dimensions(
    XYZ: ArrayLike,
    Y_b: ArrayLike,
    F_S: ArrayLike,
    F_L: ArrayLike,
) -> NDArrayFloat:
    """
    Return opponent colour dimensions from given adapted *CIE XYZ* tristimulus
    values.

    The opponent colour dimensions are based on a modified *CIE L\\*a\\*b\\**
    colourspace formulae.

    Parameters
    ----------
    XYZ
        Adapted *CIE XYZ* tristimulus values.
    Y_b
        Luminance factor of the background in :math:`cd/m^2`.
    F_S
        Surround induction factor :math:`F_S`.
    F_L
        Lightness induction factor :math:`F_L`.

    Returns
    -------
    :class:`numpy.ndarray`
        Opponent colour dimensions.

    Examples
    --------
    >>> XYZ = np.array([19.00999572, 20.00091862, 21.77993863])
    >>> Y_b = 20.0
    >>> F_S = 3.0
    >>> F_L = 1.0
    >>> opponent_colour_dimensions(XYZ, Y_b, F_S, F_L)  # doctest: +ELLIPSIS
    array([  3.7368047...e+01,  -4.4986443...e-03,  -5.2604647...e-03])
    """

    X, Y, Z = tsplit(XYZ)
    Y_b = as_float_array(Y_b)
    F_S = as_float_array(F_S)
    F_L = as_float_array(F_L)

    # Account for background lightness contrast.
    z = 1 + F_L * spow(Y_b / 100, 0.5)

    # Computing modified *CIE L\\*a\\*b\\** colourspace array.
    L = 116 * spow(f(Y / 100, F_S), z) - 16
    a = 500 * (f(X / 95.05, F_S) - f(Y / 100, F_S))
    b = 200 * (f(Y / 100, F_S) - f(Z / 108.88, F_S))

    Lab = tstack([L, a, b])

    return Lab


def hue_angle(a: ArrayLike, b: ArrayLike) -> NDArrayFloat:
    """
    Return the *hue* angle :math:`h_L` in degrees.

    Parameters
    ----------
    a
        Opponent colour dimension :math:`a`.
    b
        Opponent colour dimension :math:`b`.

    Returns
    -------
    :class:`numpy.ndarray`
        *Hue* angle :math:`h_L` in degrees.

    Examples
    --------
    >>> hue_angle(-4.49864756e-03, -5.26046353e-03)  # doctest: +ELLIPSIS
    229.4635727...
    """

    a = as_float_array(a)
    b = as_float_array(b)

    h_L = np.degrees(np.arctan2(b, a)) % 360

    return as_float(h_L)


def chroma_correlate(a: ArrayLike, b: ArrayLike) -> NDArrayFloat:
    """
    Return the correlate of *chroma* :math:`Ch_L`.

    Parameters
    ----------
    a
        Opponent colour dimension :math:`a`.
    b
        Opponent colour dimension :math:`b`.

    Returns
    -------
    :class:`numpy.ndarray`
        Correlate of *chroma* :math:`Ch_L`.

    Examples
    --------
    >>> a = -4.49864756e-03
    >>> b = -5.26046353e-03
    >>> chroma_correlate(a, b)  # doctest: +ELLIPSIS
    0.0086506...
    """

    a = as_float_array(a)
    b = as_float_array(b)

    c = spow(a**2 + b**2, 0.5)
    Ch_L = 25 * np.log1p(0.05 * c)

    return as_float(Ch_L)


def colourfulness_correlate(
    L: ArrayLike,
    L_L: ArrayLike,
    Ch_L: ArrayLike,
    F_C: ArrayLike,
) -> NDArrayFloat:
    """
    Return the correlate of *colourfulness* :math:`C_L`.

    Parameters
    ----------
    L
        Absolute luminance :math:`L` of reference white in :math:`cd/m^2`.
    L_L
        Correlate of *Lightness* :math:`L_L`.
    Ch_L
        Correlate of *chroma* :math:`Ch_L`.
    F_C
        Chroma induction factor :math:`F_C`.

    Returns
    -------
    :class:`numpy.ndarray`
        Correlate of *colourfulness* :math:`C_L`.

    Examples
    --------
    >>> L = 318.31
    >>> L_L = 37.368047493928195
    >>> Ch_L = 0.008650662051714
    >>> F_C = 1.0
    >>> colourfulness_correlate(L, L_L, Ch_L, F_C)  # doctest: +ELLIPSIS
    0.0183832...
    """

    L = as_float_array(L)
    L_L = as_float_array(L_L)
    Ch_L = as_float_array(Ch_L)
    F_C = as_float_array(F_C)

    S_C = 1 + 0.47 * np.log10(L) - 0.057 * np.log10(L) ** 2
    S_M = 0.7 + 0.02 * L_L - 0.0002 * L_L**2
    C_L = Ch_L * S_M * S_C * F_C

    return as_float(C_L)


def saturation_correlate(Ch_L: ArrayLike, L_L: ArrayLike) -> NDArrayFloat:
    """
    Return the correlate of *saturation* :math:`S_L`.

    Parameters
    ----------
    Ch_L
        Correlate of *chroma* :math:`Ch_L`.
    L_L
        Correlate of *Lightness* :math:`L_L`.

    Returns
    -------
    :class:`numpy.ndarray`
        Correlate of *saturation* :math:`S_L`.

    Examples
    --------
    >>> Ch_L = 0.008650662051714
    >>> L_L = 37.368047493928195
    >>> saturation_correlate(Ch_L, L_L)  # doctest: +ELLIPSIS
    0.0002314...
    """

    Ch_L = as_float_array(Ch_L)
    L_L = as_float_array(L_L)

    S_L = Ch_L / L_L

    return S_L


def final_opponent_signals(C_L: ArrayLike, h_L: ArrayLike) -> NDArrayFloat:
    """
    Return the final opponent signals :math:`A_L` and :math:`B_L`.

    Parameters
    ----------
    C_L
        Correlate of *colourfulness* :math:`C_L`.
    h_L
        Correlate of *hue* :math:`h_L` in degrees.

    Returns
    -------
    :class:`numpy.ndarray`
        Final opponent signals :math:`A_L` and :math:`B_L`.

    Examples
    --------
    >>> C_L = 0.0183832899143
    >>> h_L = 229.46357270858391
    >>> final_opponent_signals(C_L, h_L)  # doctest: +ELLIPSIS
    array([-0.0119478..., -0.0139711...])
    """

    AB_L = polar_to_cartesian(tstack([as_float_array(C_L), np.radians(h_L)]))

    return AB_L
