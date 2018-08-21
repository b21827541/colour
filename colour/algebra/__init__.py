# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .coordinates import *  # noqa
from . import coordinates
from .common import spow
from .extrapolation import Extrapolator
from .geometry import (
    normalise_vector, euclidean_distance, extend_line_segment,
    LineSegmentsIntersections_Specification, intersect_line_segments)
from .interpolation import (
    kernel_nearest_neighbour, kernel_linear, kernel_sinc, kernel_lanczos,
    kernel_cardinal_spline, KernelInterpolator, NearestNeighbourInterpolator,
    LinearInterpolator, SpragueInterpolator, CubicSplineInterpolator,
    PchipInterpolator, NullInterpolator, lagrange_coefficients,
    table_interpolation_trilinear, table_interpolation_tetrahedral,
    TABLE_INTERPOLATION_METHODS, table_interpolation)
from .matrix import is_identity
from .random import random_triplet_generator
from .regression import least_square_mapping_MoorePenrose

__all__ = []
__all__ += coordinates.__all__
__all__ += ['spow']
__all__ += ['Extrapolator']
__all__ += [
    'normalise_vector', 'euclidean_distance', 'extend_line_segment',
    'LineSegmentsIntersections_Specification', 'intersect_line_segments'
]
__all__ += [
    'kernel_nearest_neighbour', 'kernel_linear', 'kernel_sinc',
    'kernel_lanczos', 'kernel_cardinal_spline', 'KernelInterpolator',
    'NearestNeighbourInterpolator', 'LinearInterpolator',
    'SpragueInterpolator', 'CubicSplineInterpolator', 'PchipInterpolator',
    'NullInterpolator', 'lagrange_coefficients',
    'table_interpolation_trilinear', 'table_interpolation_tetrahedral',
    'TABLE_INTERPOLATION_METHODS', 'table_interpolation'
]
__all__ += ['is_identity']
__all__ += ['random_triplet_generator']
__all__ += ['least_square_mapping_MoorePenrose']
