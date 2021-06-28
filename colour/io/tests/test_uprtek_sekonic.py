# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour.io.uprtek_sekonic` module.
"""
import unittest
import os
import shutil
import tempfile
import numpy as np
import json

from colour.colorimetry import SpectralDistribution
from colour.io import SpectralDistribution_UPRTek

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'resources')

FILE_HEADER = {
    'Manufacturer': 'UPRTek',
    'CatalogNumber': None,
    'Description': None,
    'DocumentCreator': None,
    'UniqueIdentifier': None,
    'MeasurementEquipment': 'CV600',
    'Laboratory': None,
    'ReportNumber': None,
    'ReportDate': '2021/01/04',
    'DocumentCreationDate': None,
    'Comments': {
        'Model Name': 'CV600',
        'Serial Number': '19J00789',
        'Time': '2021/01/04_23:14:46',
        'Memo': [],
        'LUX': 695.154907,
        'fc': 64.605476,
        'CCT': 5198.0,
        'Duv': -0.00062,
        'I-Time': 12000.0,
        'X': 682.470886,
        'Y': 695.154907,
        'Z': 631.635071,
        'x': 0.339663,
        'y': 0.345975,
        "u'": 0.209915,
        "v'": 0.481087,
        'LambdaP': 456.0,
        'LambdaPValue': 18.404581,
        'CRI': 92.956993,
        'R1': 91.651062,
        'R2': 93.014732,
        'R3': 97.032013,
        'R4': 93.513229,
        'R5': 92.48259,
        'R6': 91.48687,
        'R7': 93.016129,
        'R8': 91.459312,
        'R9': 77.613075,
        'R10': 86.981613,
        'R11': 94.841324,
        'R12': 74.139542,
        'R13': 91.073837,
        'R14': 97.064323,
        'R15': 88.615669,
        'TLCI': 97.495056,
        'TLMF-A': 1.270032,
        'SSI-A': 44.881924,
        'Rf': 87.234917,
        'Rg': 98.510712,
        'IRR': 2.607891
    }
}

SPECTRAL_DESCRIPTION = {'SpectralQuantity': 'Irradiance'}

UPRTEK_SPECTRAL_DATA = {
    380: 0.030267,
    381: 0.030267,
    382: 0.030267,
    383: 0.029822,
    384: 0.028978,
    385: 0.028623,
    386: 0.030845,
    387: 0.035596,
    388: 0.039231,
    389: 0.039064,
    390: 0.035223,
    391: 0.03158,
    392: 0.029181,
    393: 0.027808,
    394: 0.026256,
    395: 0.024526,
    396: 0.022557,
    397: 0.020419,
    398: 0.018521,
    399: 0.018149,
    400: 0.019325,
    401: 0.021666,
    402: 0.024045,
    403: 0.026473,
    404: 0.029076,
    405: 0.03184,
    406: 0.033884,
    407: 0.034038,
    408: 0.032302,
    409: 0.030383,
    410: 0.029426,
    411: 0.029979,
    412: 0.032614,
    413: 0.037204,
    414: 0.042279,
    415: 0.046029,
    416: 0.048698,
    417: 0.053064,
    418: 0.05953,
    419: 0.07084,
    420: 0.087678,
    421: 0.110043,
    422: 0.136705,
    423: 0.16518,
    424: 0.199071,
    425: 0.241976,
    426: 0.293837,
    427: 0.359177,
    428: 0.434192,
    429: 0.523828,
    430: 0.632578,
    431: 0.758893,
    432: 0.915528,
    433: 1.096489,
    434: 1.307487,
    435: 1.557125,
    436: 1.838779,
    437: 2.183382,
    438: 2.586251,
    439: 3.054022,
    440: 3.625659,
    441: 4.279538,
    442: 5.055838,
    443: 5.919301,
    444: 6.869926,
    445: 7.940298,
    446: 9.090219,
    447: 10.33667,
    448: 11.619895,
    449: 12.939739,
    450: 14.206918,
    451: 15.39666,
    452: 16.430536,
    453: 17.267374,
    454: 17.912292,
    455: 18.261185,
    456: 18.404581,
    457: 18.288025,
    458: 18.002302,
    459: 17.570372,
    460: 17.011297,
    461: 16.411137,
    462: 15.77944,
    463: 15.168951,
    464: 14.585364,
    465: 14.057872,
    466: 13.575768,
    467: 13.144953,
    468: 12.737307,
    469: 12.346188,
    470: 11.967313,
    471: 11.590308,
    472: 11.209807,
    473: 10.815372,
    474: 10.406748,
    475: 10.007284,
    476: 9.627886,
    477: 9.279286,
    478: 8.958391,
    479: 8.663115,
    480: 8.427362,
    481: 8.238759,
    482: 8.1102,
    483: 8.011048,
    484: 7.939125,
    485: 7.900343,
    486: 7.880703,
    487: 7.887271,
    488: 7.907047,
    489: 7.939895,
    490: 7.977298,
    491: 8.013443,
    492: 8.056756,
    493: 8.112617,
    494: 8.181398,
    495: 8.256148,
    496: 8.332609,
    497: 8.418014,
    498: 8.513148,
    499: 8.616785,
    500: 8.719036,
    501: 8.817776,
    502: 8.914417,
    503: 9.011255,
    504: 9.105255,
    505: 9.193217,
    506: 9.274889,
    507: 9.350751,
    508: 9.42382,
    509: 9.490992,
    510: 9.553215,
    511: 9.608335,
    512: 9.653841,
    513: 9.691347,
    514: 9.727146,
    515: 9.767722,
    516: 9.809064,
    517: 9.842565,
    518: 9.867527,
    519: 9.887219,
    520: 9.906105,
    521: 9.920433,
    522: 9.929304,
    523: 9.932856,
    524: 9.935204,
    525: 9.937991,
    526: 9.938448,
    527: 9.936127,
    528: 9.930192,
    529: 9.922665,
    530: 9.913944,
    531: 9.905774,
    532: 9.898767,
    533: 9.894219,
    534: 9.891479,
    535: 9.883711,
    536: 9.862693,
    537: 9.829168,
    538: 9.795257,
    539: 9.767633,
    540: 9.74738,
    541: 9.729669,
    542: 9.714886,
    543: 9.701355,
    544: 9.688311,
    545: 9.67367,
    546: 9.657027,
    547: 9.63331,
    548: 9.603127,
    549: 9.567823,
    550: 9.534049,
    551: 9.504526,
    552: 9.484178,
    553: 9.471739,
    554: 9.455969,
    555: 9.429557,
    556: 9.39645,
    557: 9.368848,
    558: 9.344832,
    559: 9.313942,
    560: 9.273922,
    561: 9.240767,
    562: 9.220987,
    563: 9.210749,
    564: 9.1958,
    565: 9.173392,
    566: 9.143906,
    567: 9.10971,
    568: 9.078232,
    569: 9.052593,
    570: 9.023234,
    571: 8.984895,
    572: 8.950663,
    573: 8.935179,
    574: 8.936305,
    575: 8.937272,
    576: 8.931671,
    577: 8.921451,
    578: 8.910289,
    579: 8.908619,
    580: 8.917888,
    581: 8.93453,
    582: 8.946784,
    583: 8.958764,
    584: 8.979334,
    585: 9.007913,
    586: 9.033543,
    587: 9.051113,
    588: 9.067842,
    589: 9.089899,
    590: 9.114546,
    591: 9.136106,
    592: 9.16427,
    593: 9.207536,
    594: 9.264211,
    595: 9.321528,
    596: 9.371778,
    597: 9.411209,
    598: 9.443729,
    599: 9.490623,
    600: 9.557871,
    601: 9.626752,
    602: 9.674832,
    603: 9.705856,
    604: 9.739429,
    605: 9.784062,
    606: 9.841268,
    607: 9.907084,
    608: 9.971845,
    609: 10.026823,
    610: 10.060076,
    611: 10.076903,
    612: 10.105914,
    613: 10.161287,
    614: 10.230108,
    615: 10.285982,
    616: 10.336598,
    617: 10.396016,
    618: 10.449015,
    619: 10.478296,
    620: 10.48462,
    621: 10.487537,
    622: 10.498996,
    623: 10.519572,
    624: 10.541495,
    625: 10.549863,
    626: 10.543288,
    627: 10.538241,
    628: 10.546865,
    629: 10.560687,
    630: 10.567954,
    631: 10.564369,
    632: 10.555919,
    633: 10.542054,
    634: 10.527417,
    635: 10.513332,
    636: 10.500641,
    637: 10.493341,
    638: 10.491714,
    639: 10.477033,
    640: 10.435987,
    641: 10.374922,
    642: 10.317416,
    643: 10.269583,
    644: 10.220937,
    645: 10.168004,
    646: 10.115719,
    647: 10.06174,
    648: 9.998492,
    649: 9.91903,
    650: 9.821223,
    651: 9.7168,
    652: 9.619915,
    653: 9.531602,
    654: 9.435769,
    655: 9.326644,
    656: 9.21594,
    657: 9.111384,
    658: 9.005102,
    659: 8.892046,
    660: 8.775783,
    661: 8.659118,
    662: 8.537835,
    663: 8.413469,
    664: 8.292587,
    665: 8.175849,
    666: 8.055606,
    667: 7.931369,
    668: 7.812479,
    669: 7.695505,
    670: 7.564718,
    671: 7.422195,
    672: 7.286375,
    673: 7.166087,
    674: 7.050159,
    675: 6.925609,
    676: 6.792675,
    677: 6.659946,
    678: 6.534333,
    679: 6.416044,
    680: 6.298086,
    681: 6.182296,
    682: 6.073105,
    683: 5.965933,
    684: 5.853682,
    685: 5.729931,
    686: 5.599877,
    687: 5.48067,
    688: 5.376213,
    689: 5.273221,
    690: 5.156234,
    691: 5.027091,
    692: 4.900242,
    693: 4.777046,
    694: 4.658288,
    695: 4.54701,
    696: 4.44356,
    697: 4.347722,
    698: 4.252159,
    699: 4.152643,
    700: 4.053906,
    701: 3.961853,
    702: 3.865061,
    703: 3.755302,
    704: 3.634861,
    705: 3.51936,
    706: 3.418803,
    707: 3.328571,
    708: 3.246458,
    709: 3.160225,
    710: 3.066386,
    711: 2.97029,
    712: 2.878098,
    713: 2.790311,
    714: 2.701265,
    715: 2.607646,
    716: 2.51549,
    717: 2.435313,
    718: 2.361505,
    719: 2.282271,
    720: 2.1925,
    721: 2.101594,
    722: 2.027356,
    723: 1.966553,
    724: 1.912948,
    725: 1.855193,
    726: 1.785138,
    727: 1.710667,
    728: 1.638785,
    729: 1.582385,
    730: 1.539228,
    731: 1.498548,
    732: 1.455407,
    733: 1.413034,
    734: 1.372021,
    735: 1.324772,
    736: 1.277157,
    737: 1.238888,
    738: 1.211113,
    739: 1.182541,
    740: 1.149382,
    741: 1.11849,
    742: 1.091204,
    743: 1.065539,
    744: 1.039564,
    745: 1.013148,
    746: 0.990818,
    747: 0.976522,
    748: 0.960074,
    749: 0.935639,
    750: 0.905095,
    751: 0.878893,
    752: 0.862828,
    753: 0.847588,
    754: 0.829938,
    755: 0.808772,
    756: 0.786338,
    757: 0.761752,
    758: 0.735873,
    759: 0.711232,
    760: 0.690947,
    761: 0.673476,
    762: 0.659236,
    763: 0.646735,
    764: 0.633802,
    765: 0.612864,
    766: 0.589102,
    767: 0.567989,
    768: 0.551288,
    769: 0.533479,
    770: 0.508426,
    771: 0.487143,
    772: 0.474126,
    773: 0.465145,
    774: 0.455158,
    775: 0.442994,
    776: 0.429114,
    777: 0.419402,
    778: 0.411766,
    779: 0.411766,
    780: 0.411766,
}


class TestSpectralDistribution_UPRTek(unittest.TestCase):
    """
    Defines :class:`colour.io.uprtek_sekonic.SpectralDistribution_UPRTek`
    class unit tests methods.
    """

    # maxDiff = None

    def setUp(self):
        """
        Initialises common tests attributes.
        """

        self._temporary_directory = tempfile.mkdtemp()

    def tearDown(self):
        """
        After tests actions.
        """

        shutil.rmtree(self._temporary_directory)

    def test_required_attributes(self):
        """
        Tests presence of required attributes.
        """

        required_attributes = ('mapping', 'path', 'header',
                               'spectral_quantity', 'reflection_geometry',
                               'transmission_geometry', 'bandwidth_FWHM',
                               'bandwidth_corrected')

        for attribute in required_attributes:
            self.assertIn(attribute, dir(SpectralDistribution_UPRTek))

    def test_required_methods(self):
        """
        Tests presence of required methods.
        """

        required_methods = ('__init__', 'read', 'write')

        for method in required_methods:
            self.assertIn(method, dir(SpectralDistribution_UPRTek))

    def test_read(self, sd=None):
        """
        Tests :attr:`colour.io.uprtek_sekonic.SpectralDistribution_UPRTek.read`
        method.
        """
        if sd is None:
            sd = SpectralDistribution_UPRTek(
                os.path.join(RESOURCES_DIRECTORY, 'uprtek.xls.txt')).read()

            sd_r = SpectralDistribution(UPRTEK_SPECTRAL_DATA)

            np.testing.assert_array_equal(sd_r.domain, sd.domain)
            np.testing.assert_almost_equal(sd_r.values, sd.values, decimal=6)

            for test, read in ((FILE_HEADER, sd.header), (SPECTRAL_DESCRIPTION,
                                                          sd)):
                for key, value in test.items():
                    for specification in read.mapping.elements:
                        if key == specification.element:
                            if key == 'Comments':
                                self.assertDictEqual(
                                    json.loads(read.comments), value)
                            else:
                                self.assertEqual(
                                    getattr(read, specification.attribute),
                                    value)


if __name__ == '__main__':
    unittest.main()
