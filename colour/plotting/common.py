"""
Common Plotting
===============

Defines the common plotting objects:

-   :func:`colour.plotting.colour_style`
-   :func:`colour.plotting.override_style`
-   :func:`colour.plotting.font_scaling`
-   :func:`colour.plotting.XYZ_to_plotting_colourspace`
-   :class:`colour.plotting.ColourSwatch`
-   :func:`colour.plotting.colour_cycle`
-   :func:`colour.plotting.artist`
-   :func:`colour.plotting.camera`
-   :func:`colour.plotting.decorate`
-   :func:`colour.plotting.boundaries`
-   :func:`colour.plotting.display`
-   :func:`colour.plotting.render`
-   :func:`colour.plotting.label_rectangles`
-   :func:`colour.plotting.uniform_axes3d`
-   :func:`colour.plotting.plot_single_colour_swatch`
-   :func:`colour.plotting.plot_multi_colour_swatches`
-   :func:`colour.plotting.plot_single_function`
-   :func:`colour.plotting.plot_multi_functions`
-   :func:`colour.plotting.plot_image`
"""

from __future__ import annotations

import contextlib
import functools
import itertools
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import partial
from pathlib import Path

import matplotlib.cm
import matplotlib.font_manager
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
from cycler import cycler
from matplotlib.axes import Axes
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure, SubFigure
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.axes3d import Axes3D

from colour.characterisation import CCS_COLOURCHECKERS, ColourChecker
from colour.colorimetry import (
    MSDS_CMFS,
    SDS_ILLUMINANTS,
    SDS_LIGHT_SOURCES,
    MultiSpectralDistributions,
    SpectralDistribution,
)
from colour.hints import (
    Any,
    ArrayLike,
    Callable,
    Dict,
    Generator,
    List,
    Literal,
    LiteralChromaticAdaptationTransform,
    LiteralFontScaling,
    LiteralRGBColourspace,
    Mapping,
    NDArrayFloat,
    Sequence,
    Tuple,
    TypedDict,
    cast,
)
from colour.models import RGB_COLOURSPACES, RGB_Colourspace, XYZ_to_RGB
from colour.utilities import (
    CanonicalMapping,
    Structure,
    as_float_array,
    as_int_scalar,
    attest,
    filter_mapping,
    first_item,
    is_sibling,
    is_string,
    optional,
    runtime_warning,
    validate_method,
)
from colour.utilities.deprecation import handle_arguments_deprecation

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "CONSTANTS_COLOUR_STYLE",
    "CONSTANTS_ARROW_STYLE",
    "colour_style",
    "override_style",
    "font_scaling",
    "XYZ_to_plotting_colourspace",
    "ColourSwatch",
    "colour_cycle",
    "KwargsArtist",
    "artist",
    "KwargsCamera",
    "camera",
    "KwargsRender",
    "render",
    "label_rectangles",
    "uniform_axes3d",
    "filter_passthrough",
    "filter_RGB_colourspaces",
    "filter_cmfs",
    "filter_illuminants",
    "filter_colour_checkers",
    "update_settings_collection",
    "plot_single_colour_swatch",
    "plot_multi_colour_swatches",
    "plot_single_function",
    "plot_multi_functions",
    "plot_image",
]

CONSTANTS_COLOUR_STYLE: Structure = Structure(
    **{
        "colour": Structure(
            **{
                "darkest": "#111111",
                "darker": "#222222",
                "dark": "#333333",
                "dim": "#505050",
                "average": "#808080",
                "light": "#D5D5D5",
                "bright": "#EEEEEE",
                "brighter": "#F0F0F0",
                "brightest": "#F5F5F5",
                "cycle": (
                    "#F44336",
                    "#9C27B0",
                    "#3F51B5",
                    "#03A9F4",
                    "#009688",
                    "#8BC34A",
                    "#FFEB3B",
                    "#FF9800",
                    "#795548",
                    "#607D8B",
                ),
                "map": LinearSegmentedColormap.from_list(
                    "colour",
                    (
                        "#F44336",
                        "#9C27B0",
                        "#3F51B5",
                        "#03A9F4",
                        "#009688",
                        "#8BC34A",
                        "#FFEB3B",
                        "#FF9800",
                        "#795548",
                        "#607D8B",
                    ),
                ),
                "colourspace": RGB_COLOURSPACES["sRGB"],
            }
        ),
        "font": Structure(
            {
                "size": 10,
                "scaling": Structure(
                    **{
                        "xx_small": 0.579,
                        "x_small": 0.694,
                        "small": 0.833,
                        "medium": 1,
                        "large": 1 / 0.579,
                        "x_large": 1 / 0.694,
                        "xx_large": 1 / 0.833,
                    }
                ),
            }
        ),
        "opacity": Structure(**{"high": 0.75, "medium": 0.5, "low": 0.25}),
        "geometry": Structure(**{"long": 5, "medium": 2.5, "short": 1}),
        "hatch": Structure(
            **{
                "patterns": (
                    "\\\\",
                    "o",
                    "x",
                    ".",
                    "*",
                    "//",
                )
            }
        ),
        "zorder": Structure(
            {
                "background_polygon": -140,
                "background_scatter": -130,
                "background_line": -120,
                "background_annotation": -110,
                "background_label": -100,
                "midground_polygon": -90,
                "midground_scatter": -80,
                "midground_line": -70,
                "midground_annotation": -60,
                "midground_label": -50,
                "foreground_polygon": -40,
                "foreground_scatter": -30,
                "foreground_line": -20,
                "foreground_annotation": -10,
                "foreground_label": 0,
            }
        ),
    }
)
"""Various defaults settings used across the plotting sub-package."""

# NOTE: Adding our font scaling items so that they can be tweaked without
# affecting *Matplotplib* ones.
for _scaling, _value in CONSTANTS_COLOUR_STYLE.font.scaling.items():
    matplotlib.font_manager.font_scalings[
        f'{_scaling.replace("_", "-")}-colour-science'
    ] = _value

del _scaling, _value

CONSTANTS_ARROW_STYLE: Structure = Structure(
    **{
        "color": CONSTANTS_COLOUR_STYLE.colour.dark,
        "headwidth": CONSTANTS_COLOUR_STYLE.geometry.short * 4,
        "headlength": CONSTANTS_COLOUR_STYLE.geometry.long,
        "width": CONSTANTS_COLOUR_STYLE.geometry.short * 0.5,
        "shrink": CONSTANTS_COLOUR_STYLE.geometry.short * 0.1,
        "connectionstyle": "arc3,rad=-0.2",
    }
)
"""Annotation arrow settings used across the plotting sub-package."""


def colour_style(use_style: bool = True) -> dict:
    """
    Return *Colour* plotting style.

    Parameters
    ----------
    use_style
        Whether to use the style and load it into *Matplotlib*.

    Returns
    -------
    :class:`dict`
        *Colour* style.
    """

    constants = CONSTANTS_COLOUR_STYLE
    style = {
        # Figure Size Settings
        "figure.figsize": (12.80, 7.20),
        "figure.dpi": 100,
        "savefig.dpi": 100,
        "savefig.bbox": "standard",
        # Font Settings
        # 'font.size': 12,
        "axes.titlesize": "x-large",
        "axes.labelsize": "larger",
        "legend.fontsize": "small",
        "xtick.labelsize": "medium",
        "ytick.labelsize": "medium",
        # Text Settings
        "text.color": constants.colour.darkest,
        # Tick Settings
        "xtick.top": False,
        "xtick.bottom": True,
        "ytick.right": False,
        "ytick.left": True,
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": constants.geometry.long * 1.25,
        "xtick.minor.size": constants.geometry.long * 0.75,
        "ytick.major.size": constants.geometry.long * 1.25,
        "ytick.minor.size": constants.geometry.long * 0.75,
        "xtick.major.width": constants.geometry.short,
        "xtick.minor.width": constants.geometry.short,
        "ytick.major.width": constants.geometry.short,
        "ytick.minor.width": constants.geometry.short,
        # Spine Settings
        "axes.linewidth": constants.geometry.short,
        "axes.edgecolor": constants.colour.dark,
        # Title Settings
        "axes.titlepad": plt.rcParams["font.size"] * 0.75,
        # Axes Settings
        "axes.facecolor": constants.colour.brightest,
        "axes.grid": True,
        "axes.grid.which": "major",
        "axes.grid.axis": "both",
        # Grid Settings
        "axes.axisbelow": True,
        "grid.linewidth": constants.geometry.short * 0.5,
        "grid.linestyle": "--",
        "grid.color": constants.colour.light,
        # Legend
        "legend.frameon": True,
        "legend.framealpha": constants.opacity.high,
        "legend.fancybox": False,
        "legend.facecolor": constants.colour.brighter,
        "legend.borderpad": constants.geometry.short * 0.5,
        # Lines
        "lines.linewidth": constants.geometry.short,
        "lines.markersize": constants.geometry.short * 3,
        "lines.markeredgewidth": constants.geometry.short * 0.75,
        # Cycle
        "axes.prop_cycle": cycler(color=constants.colour.cycle),
    }

    if use_style:
        plt.rcParams.update(style)

    return style


def override_style(**kwargs: Any) -> Callable:
    """
    Decorate a function to override *Matplotlib* style.

    Other Parameters
    ----------------
    kwargs
        Keywords arguments.

    Returns
    -------
    Callable

    Examples
    --------
    >>> @override_style(**{"text.color": "red"})
    ... def f(*args, **kwargs):
    ...     plt.text(0.5, 0.5, "This is a text!")
    ...     plt.show()
    ...
    >>> f()  # doctest: +SKIP
    """

    keywords = dict(kwargs)

    def wrapper(function: Callable) -> Callable:
        """Wrap given function wrapper."""

        @functools.wraps(function)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            """Wrap given function."""

            keywords.update(kwargs)

            style_overrides = {
                key: value
                for key, value in keywords.items()
                if key in plt.rcParams
            }

            with plt.style.context(style_overrides):
                return function(*args, **kwargs)

        return wrapped

    return wrapper


@contextmanager
def font_scaling(scaling: LiteralFontScaling, value: float) -> Generator:
    """
    Define a context manager setting temporarily a *Matplotlib* font scaling.

    Parameters
    ----------
    scaling
        Font scaling to temporarily set.
    value
        Value to temporarily set the font scaling with.

    Yields
    ------
    Generator.

    Examples
    --------
    >>> with font_scaling("medium-colour-science", 2):
    ...     print(
    ...         matplotlib.font_manager.font_scalings["medium-colour-science"]
    ...     )
    ...
    2
    >>> print(matplotlib.font_manager.font_scalings["medium-colour-science"])
    1
    """

    current_value = matplotlib.font_manager.font_scalings[scaling]

    matplotlib.font_manager.font_scalings[scaling] = value

    yield

    matplotlib.font_manager.font_scalings[scaling] = current_value


def XYZ_to_plotting_colourspace(
    XYZ: ArrayLike,
    illuminant: ArrayLike = RGB_COLOURSPACES["sRGB"].whitepoint,
    chromatic_adaptation_transform: LiteralChromaticAdaptationTransform
    | str
    | None = "CAT02",
    apply_cctf_encoding: bool = True,
) -> NDArrayFloat:
    """
    Convert from *CIE XYZ* tristimulus values to the default plotting
    colourspace.

    Parameters
    ----------
    XYZ
        *CIE XYZ* tristimulus values.
    illuminant
        Source illuminant chromaticity coordinates.
    chromatic_adaptation_transform
        *Chromatic adaptation* transform.
    apply_cctf_encoding
        Apply the default plotting colourspace encoding colour component
        transfer function / opto-electronic transfer function.

    Returns
    -------
    :class:`numpy.ndarray`
        Default plotting colourspace colour array.

    Examples
    --------
    >>> import numpy as np
    >>> XYZ = np.array([0.20654008, 0.12197225, 0.05136952])
    >>> XYZ_to_plotting_colourspace(XYZ)  # doctest: +ELLIPSIS
    array([ 0.7057393...,  0.1924826...,  0.2235416...])
    """

    return XYZ_to_RGB(
        XYZ,
        CONSTANTS_COLOUR_STYLE.colour.colourspace,
        illuminant,
        chromatic_adaptation_transform,
        apply_cctf_encoding,
    )


@dataclass
class ColourSwatch:
    """
    Define a data structure for a colour swatch.

    Parameters
    ----------
    RGB
        RGB Colour.
    name
        Colour name.
    """

    RGB: ArrayLike
    name: str | None = field(default_factory=lambda: None)


def colour_cycle(**kwargs: Any) -> itertools.cycle:
    """
    Return a colour cycle iterator using given colour map.

    Other Parameters
    ----------------
    colour_cycle_map
        Matplotlib colourmap name.
    colour_cycle_count
        Colours count to pick in the colourmap.

    Returns
    -------
    :class:`itertools.cycle`
        Colour cycle iterator.
    """

    settings = Structure(
        **{
            "colour_cycle_map": CONSTANTS_COLOUR_STYLE.colour.map,
            "colour_cycle_count": len(CONSTANTS_COLOUR_STYLE.colour.cycle),
        }
    )
    settings.update(kwargs)

    samples = np.linspace(0, 1, settings.colour_cycle_count)
    if isinstance(settings.colour_cycle_map, LinearSegmentedColormap):
        cycle = settings.colour_cycle_map(samples)
    else:
        cycle = getattr(plt.cm, settings.colour_cycle_map)(samples)

    return itertools.cycle(cycle)


class KwargsArtist(TypedDict):
    """
    Define the keyword argument types for the :func:`colour.plotting.artist`
    definition.

    Parameters
    ----------
    axes
        Axes that will be passed through without creating a new figure.
    uniform
        Whether to create the figure with an equal aspect ratio.
    """

    axes: Axes
    uniform: bool


def artist(**kwargs: KwargsArtist | Any) -> Tuple[Figure, Axes]:
    """
    Return the current figure and its axes or creates a new one.

    Other Parameters
    ----------------
    kwargs
        {:func:`colour.plotting.common.KwargsArtist`},
        See the documentation of the previously listed class.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.
    """

    width, height = plt.rcParams["figure.figsize"]

    figure_size = (width, width) if kwargs.get("uniform") else (width, height)

    axes = kwargs.get("axes")
    if axes is None:
        figure = plt.figure(figsize=figure_size)

        return figure, figure.gca()
    else:
        axes = cast(Axes, axes)
        figure = axes.figure

        if isinstance(figure, SubFigure):
            figure = figure.get_figure()

        return cast(Figure, figure), axes


class KwargsCamera(TypedDict):
    """
    Define the keyword argument types for the :func:`colour.plotting.camera`
    definition.

    Parameters
    ----------
    figure
        Figure to apply the render elements onto.
    axes
        Axes to apply the render elements onto.
    azimuth
        Camera azimuth.
    elevation
        Camera elevation.
    camera_aspect
        Matplotlib axes aspect. Default is *equal*.
    """

    figure: Figure
    axes: Axes
    azimuth: float | None
    elevation: float | None
    camera_aspect: Literal["equal"] | str


def camera(**kwargs: KwargsCamera | Any) -> Tuple[Figure, Axes3D]:
    """
    Set the camera settings.

    Other Parameters
    ----------------
    kwargs
        {:func:`colour.plotting.common.KwargsCamera`},
        See the documentation of the previously listed class.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.
    """

    figure = cast(Figure, kwargs.get("figure", plt.gcf()))
    axes = cast(Axes3D, kwargs.get("axes", plt.gca()))

    settings = Structure(
        **{"camera_aspect": "equal", "elevation": None, "azimuth": None}
    )
    settings.update(kwargs)

    if settings.camera_aspect == "equal":
        uniform_axes3d(axes=axes)

    axes.view_init(elev=settings.elevation, azim=settings.azimuth)

    return figure, axes


class KwargsRender(TypedDict):
    """
    Define the keyword argument types for the :func:`colour.plotting.render`
    definition.

    Parameters
    ----------
    figure
        Figure to apply the render elements onto.
    axes
        Axes to apply the render elements onto.
    filename
        Figure will be saved using given ``filename`` argument.
    show
        Whether to show the figure and call :func:`matplotlib.pyplot.show`
        definition.
    block
        Whether to block on `show`ing the plot.
    aspect
        Matplotlib axes aspect.
    axes_visible
        Whether the axes are visible. Default is *True*.
    bounding_box
        Array defining current axes limits such
        `bounding_box = (x min, x max, y min, y max)`.
    tight_layout
        Whether to invoke the :func:`matplotlib.pyplot.tight_layout`
        definition.
    legend
        Whether to display the legend. Default is *False*.
    legend_columns
        Number of columns in the legend. Default is *1*.
    transparent_background
        Whether to turn off the background patch. Default is *True*.
    title
        Figure title.
    wrap_title
        Whether to wrap the figure title. Default is *True*.
    x_label
        *X* axis label.
    y_label
        *Y* axis label.
    x_ticker
        Whether to display the *X* axis ticker. Default is *True*.
    y_ticker
        Whether to display the *Y* axis ticker. Default is *True*.
    """

    figure: Figure
    axes: Axes
    filename: str | Path
    show: bool
    block: bool
    aspect: Literal["auto", "equal"] | float
    axes_visible: bool
    bounding_box: ArrayLike
    tight_layout: bool
    legend: bool
    legend_columns: int
    transparent_background: bool
    title: str
    wrap_title: bool
    x_label: str
    y_label: str
    x_ticker: bool
    y_ticker: bool


def render(
    **kwargs: KwargsRender | Any,
) -> Tuple[Figure, Axes] | Tuple[Figure, Axes3D]:
    """
    Render the current figure while adjusting various settings such as the
    bounding box, the title or background transparency.

    Other Parameters
    ----------------
    kwargs
        {:func:`colour.plotting.common.KwargsRender`},
        See the documentation of the previously listed class.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.
    """

    figure = cast(Figure, kwargs.get("figure", plt.gcf()))
    axes = cast(Axes, kwargs.get("axes", plt.gca()))

    kwargs = handle_arguments_deprecation(
        {
            "ArgumentRenamed": [["standalone", "show"]],
        },
        **kwargs,
    )

    settings = Structure(
        **{
            "filename": None,
            "show": True,
            "block": True,
            "aspect": None,
            "axes_visible": True,
            "bounding_box": None,
            "tight_layout": True,
            "legend": False,
            "legend_columns": 1,
            "transparent_background": True,
            "title": None,
            "wrap_title": True,
            "x_label": None,
            "y_label": None,
            "x_ticker": True,
            "y_ticker": True,
        }
    )
    settings.update(kwargs)

    if settings.aspect:
        axes.set_aspect(settings.aspect)
    if not settings.axes_visible:
        axes.set_axis_off()
    if settings.bounding_box:
        axes.set_xlim(settings.bounding_box[0], settings.bounding_box[1])
        axes.set_ylim(settings.bounding_box[2], settings.bounding_box[3])

    if settings.title:
        axes.set_title(settings.title, wrap=settings.wrap_title)
    if settings.x_label:
        axes.set_xlabel(settings.x_label)
    if settings.y_label:
        axes.set_ylabel(settings.y_label)
    if not settings.x_ticker:
        axes.set_xticks([])
    if not settings.y_ticker:
        axes.set_yticks([])
    if settings.legend:
        axes.legend(ncol=settings.legend_columns)

    if settings.tight_layout:
        figure.tight_layout()

    if settings.transparent_background:
        figure.patch.set_alpha(0)

    if settings.filename is not None:
        figure.savefig(str(settings.filename))

    if settings.show:
        plt.show(block=settings.block)

    return figure, axes


def label_rectangles(
    labels: Sequence[str],
    rectangles: Sequence[Patch],
    rotation: Literal["horizontal", "vertical"] | str = "vertical",
    text_size: float = CONSTANTS_COLOUR_STYLE.font.scaling.medium,
    offset: ArrayLike | None = None,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """
    Add labels above given rectangles.

    Parameters
    ----------
    labels
        Labels to display.
    rectangles
        Rectangles to used to set the labels value and position.
    rotation
        Labels orientation.
    text_size
        Labels text size.
    offset
        Labels offset as percentages of the largest rectangle dimensions.

    Other Parameters
    ----------------
    figure
        Figure to apply the render elements onto.
    axes
        Axes to apply the render elements onto.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.
    """

    rotation = validate_method(
        rotation,
        ("horizontal", "vertical"),
        '"{0}" rotation is invalid, it must be one of {1}!',
    )

    figure = kwargs.get("figure", plt.gcf())
    axes = kwargs.get("axes", plt.gca())

    offset = as_float_array(optional(offset, (0.0, 0.025)))

    x_m, y_m = 0, 0
    for rectangle in rectangles:
        x_m = max(x_m, rectangle.get_width())  # pyright: ignore
        y_m = max(y_m, rectangle.get_height())  # pyright: ignore

    for i, rectangle in enumerate(rectangles):
        x = rectangle.get_x()  # pyright: ignore
        height = rectangle.get_height()  # pyright: ignore
        width = rectangle.get_width()  # pyright: ignore
        axes.text(
            x + width / 2 + offset[0] * width,
            height + offset[1] * y_m,
            labels[i],
            ha="center",
            va="bottom",
            rotation=rotation,
            fontsize=text_size,
            clip_on=True,
            zorder=CONSTANTS_COLOUR_STYLE.zorder.midground_label,
        )

    return figure, axes


def uniform_axes3d(**kwargs: Any) -> Tuple[Figure, Axes]:
    """
    Set equal aspect ratio to given 3d axes.

    Other Parameters
    ----------------
    figure
        Figure to apply the render elements onto.
    axes
        Axes to apply the render elements onto.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.
    """

    figure = kwargs.get("figure", plt.gcf())
    axes = kwargs.get("axes", plt.gca())

    with contextlib.suppress(NotImplementedError):  # pragma: no cover
        # TODO: Reassess according to
        # https://github.com/matplotlib/matplotlib/issues/1077
        axes.set_aspect("equal")

    extents = np.array([getattr(axes, f"get_{axis}lim")() for axis in "xyz"])

    centers = np.mean(extents, axis=1)
    extent = np.max(np.abs(extents[..., 1] - extents[..., 0]))

    for center, axis in zip(centers, "xyz"):
        getattr(axes, f"set_{axis}lim")(
            center - extent / 2, center + extent / 2
        )

    return figure, axes


def filter_passthrough(
    mapping: Mapping,
    filterers: Any | str | Sequence[Any | str],
    allow_non_siblings: bool = True,
) -> dict:
    """
    Return mapping objects matching given filterers while passing through
    class instances whose type is one of the mapping element types.

    This definition allows passing custom but compatible objects to the various
    plotting definitions that by default expect the key from a dataset element.

    For example, a typical call to :func:`colour.plotting.\
plot_multi_illuminant_sds` definition is as follows:

    >>> import colour
    >>> colour.plotting.plot_multi_illuminant_sds(["A"])
    ... # doctest: +SKIP

    With the previous example, it is also possible to pass a custom spectral
    distribution as follows:

    >>> data = {
    ...     500: 0.0651,
    ...     520: 0.0705,
    ...     540: 0.0772,
    ...     560: 0.0870,
    ...     580: 0.1128,
    ...     600: 0.1360,
    ... }
    >>> colour.plotting.plot_multi_illuminant_sds(
    ...     ["A", colour.SpectralDistribution(data)]
    ... )
    ... # doctest: +SKIP

    Similarly, a typical call to :func:`colour.plotting.\
plot_planckian_locus_in_chromaticity_diagram_CIE1931` definition is as follows:

    >>> colour.plotting.plot_planckian_locus_in_chromaticity_diagram_CIE1931(
    ...     ["A"]
    ... )
    ... # doctest: +SKIP

    But it is also possible to pass a custom whitepoint as follows:

    >>> colour.plotting.plot_planckian_locus_in_chromaticity_diagram_CIE1931(
    ...     ["A", {"Custom": np.array([1 / 3 + 0.05, 1 / 3 + 0.05])}]
    ... )
    ... # doctest: +SKIP

    Parameters
    ----------
    mapping
        Mapping to filter.
    filterers
        Filterer or object class instance (which is passed through directly if
        its type is one of the mapping element types) or list
        of filterers.
    allow_non_siblings
        Whether to allow non-siblings to be also passed through.

    Returns
    -------
    :class:`dict`
        Filtered mapping.

    Notes
    -----
    -   If the mapping passed is a :class:`colour.utilities.CanonicalMapping`
        class instance, then the lower, slugified and canonical keys are also
        used for matching.
    """

    if is_string(filterers) or not isinstance(filterers, (list, tuple)):
        filterers = [filterers]

    string_filterers: List[str] = [
        cast(str, filterer) for filterer in filterers if is_string(filterer)
    ]

    object_filterers: List[Any] = [
        filterer for filterer in filterers if is_sibling(filterer, mapping)
    ]

    if allow_non_siblings:
        non_siblings = [
            filterer
            for filterer in filterers
            if filterer not in string_filterers
            and filterer not in object_filterers
        ]

        if non_siblings:
            runtime_warning(
                f'Non-sibling elements are passed-through: "{non_siblings}"'
            )

            object_filterers.extend(non_siblings)

    filtered_mapping = filter_mapping(mapping, string_filterers)

    for filterer in object_filterers:
        # TODO: Consider using "MutableMapping" here.
        if isinstance(filterer, (dict, CanonicalMapping)):
            for key, value in filterer.items():
                filtered_mapping[key] = value
        else:
            try:
                name = filterer.name
            except AttributeError:
                try:
                    name = filterer.__name__
                except AttributeError:
                    name = str(id(filterer))

            filtered_mapping[name] = filterer

    return filtered_mapping


def filter_RGB_colourspaces(
    filterers: RGB_Colourspace
    | LiteralRGBColourspace
    | str
    | Sequence[RGB_Colourspace | LiteralRGBColourspace | str],
    allow_non_siblings: bool = True,
) -> Dict[str, RGB_Colourspace]:
    """
    Return the *RGB* colourspaces matching given filterers.

    Parameters
    ----------
    filterers
        Filterer or :class:`colour.RGB_Colourspace` class instance (which is
        passed through directly if its type is one of the mapping element
        types) or list of filterers. ``filterers`` elements can also be of any
        form supported by the :func:`colour.plotting.common.filter_passthrough`
        definition.
    allow_non_siblings
        Whether to allow non-siblings to be also passed through.

    Returns
    -------
    :class:`dict`
        Filtered *RGB* colourspaces.
    """

    return filter_passthrough(RGB_COLOURSPACES, filterers, allow_non_siblings)


def filter_cmfs(
    filterers: MultiSpectralDistributions
    | str
    | Sequence[MultiSpectralDistributions | str],
    allow_non_siblings: bool = True,
) -> Dict[str, MultiSpectralDistributions]:
    """
    Return the colour matching functions matching given filterers.

    Parameters
    ----------
    filterers
        Filterer or :class:`colour.LMS_ConeFundamentals`,
        :class:`colour.RGB_ColourMatchingFunctions` or
        :class:`colour.XYZ_ColourMatchingFunctions` class instance (which is
        passed through directly if its type is one of the mapping element
        types) or list of filterers. ``filterers`` elements can also be of any
        form supported by the :func:`colour.plotting.common.filter_passthrough`
        definition.
    allow_non_siblings
        Whether to allow non-siblings to be also passed through.

    Returns
    -------
    :class:`dict`
        Filtered colour matching functions.
    """

    return filter_passthrough(MSDS_CMFS, filterers, allow_non_siblings)


def filter_illuminants(
    filterers: SpectralDistribution
    | str
    | Sequence[SpectralDistribution | str],
    allow_non_siblings: bool = True,
) -> Dict[str, SpectralDistribution]:
    """
    Return the illuminants matching given filterers.

    Parameters
    ----------
    filterers
        Filterer or :class:`colour.SpectralDistribution` class instance
        (which is passed through directly if its type is one of the mapping
        element types) or list of filterers. ``filterers`` elements can also be
        of any form supported by the
        :func:`colour.plotting.common.filter_passthrough` definition.
    allow_non_siblings
        Whether to allow non-siblings to be also passed through.

    Returns
    -------
    :class:`dict`
        Filtered illuminants.
    """

    illuminants = {}

    illuminants.update(
        filter_passthrough(SDS_ILLUMINANTS, filterers, allow_non_siblings)
    )

    illuminants.update(
        filter_passthrough(SDS_LIGHT_SOURCES, filterers, allow_non_siblings)
    )

    return illuminants


def filter_colour_checkers(
    filterers: ColourChecker | str | Sequence[ColourChecker | str],
    allow_non_siblings: bool = True,
) -> Dict[str, ColourChecker]:
    """
    Return the colour checkers matching given filterers.

    Parameters
    ----------
    filterers
        Filterer or :class:`colour.characterisation.ColourChecker` class
        instance (which is passed through directly if its type is one of the
        mapping element types) or list of filterers. ``filterers`` elements
        can also be of any form supported by the
        :func:`colour.plotting.common.filter_passthrough` definition.
    allow_non_siblings
        Whether to allow non-siblings to be also passed through.

    Returns
    -------
    :class:`dict`
        Filtered colour checkers.
    """

    return filter_passthrough(
        CCS_COLOURCHECKERS, filterers, allow_non_siblings
    )


def update_settings_collection(
    settings_collection: dict | List[dict],
    keyword_arguments: dict | List[dict],
    expected_count: int,
):
    """
    Update given settings collection, *in-place*, with given keyword arguments
    and expected count of settings collection elements.

    Parameters
    ----------
    settings_collection
        Settings collection to update.
    keyword_arguments
        Keyword arguments to update the settings collection.
    expected_count
        Expected count of settings collection elements.

    Examples
    --------
    >>> settings_collection = [{1: 2}, {3: 4}]
    >>> keyword_arguments = {5: 6}
    >>> update_settings_collection(settings_collection, keyword_arguments, 2)
    >>> print(settings_collection)
    [{1: 2, 5: 6}, {3: 4, 5: 6}]
    >>> settings_collection = [{1: 2}, {3: 4}]
    >>> keyword_arguments = [{5: 6}, {7: 8}]
    >>> update_settings_collection(settings_collection, keyword_arguments, 2)
    >>> print(settings_collection)
    [{1: 2, 5: 6}, {3: 4, 7: 8}]
    """

    if not isinstance(keyword_arguments, dict):
        attest(
            len(keyword_arguments) == expected_count,
            "Multiple keyword arguments defined, but they do not "
            "match the expected count!",
        )

    for i, settings in enumerate(settings_collection):
        if isinstance(keyword_arguments, dict):
            settings.update(keyword_arguments)
        else:
            settings.update(keyword_arguments[i])


@override_style(
    **{
        "axes.grid": False,
        "xtick.bottom": False,
        "ytick.left": False,
        "xtick.labelbottom": False,
        "ytick.labelleft": False,
    }
)
def plot_single_colour_swatch(
    colour_swatch: ArrayLike | ColourSwatch, **kwargs: Any
) -> Tuple[Figure, Axes]:
    """
    Plot given colour swatch.

    Parameters
    ----------
    colour_swatch
        Colour swatch, either a regular `ArrayLike` or a
        :class:`colour.plotting.ColourSwatch` class instance.

    Other Parameters
    ----------------
    kwargs
        {:func:`colour.plotting.artist`,
        :func:`colour.plotting.plot_multi_colour_swatches`,
        :func:`colour.plotting.render`},
        See the documentation of the previously listed definitions.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.

    Examples
    --------
    >>> RGB = ColourSwatch((0.45620519, 0.03081071, 0.04091952))
    >>> plot_single_colour_swatch(RGB)  # doctest: +ELLIPSIS
    (<Figure size ... with 1 Axes>, <...Axes...>)

    .. image:: ../_static/Plotting_Plot_Single_Colour_Swatch.png
        :align: center
        :alt: plot_single_colour_swatch
    """

    return plot_multi_colour_swatches((colour_swatch,), **kwargs)


@override_style(
    **{
        "axes.grid": False,
        "xtick.bottom": False,
        "ytick.left": False,
        "xtick.labelbottom": False,
        "ytick.labelleft": False,
    }
)
def plot_multi_colour_swatches(
    colour_swatches: Sequence[ArrayLike | ColourSwatch],
    width: float = 1,
    height: float = 1,
    spacing: float = 0,
    columns: int | None = None,
    direction: Literal["+y", "-y"] | str = "+y",
    text_kwargs: dict | None = None,
    background_colour: ArrayLike = (1.0, 1.0, 1.0),
    compare_swatches: Literal["Diagonal", "Stacked"] | str | None = None,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """
    Plot given colours swatches.

    Parameters
    ----------
    colour_swatches
        Colour swatch sequence, either a regular `ArrayLike` or a sequence of
        :class:`colour.plotting.ColourSwatch` class instances.
    width
        Colour swatch width.
    height
        Colour swatch height.
    spacing
        Colour swatches spacing.
    columns
        Colour swatches columns count, defaults to the colour swatch count or
        half of it if comparing.
    direction
        Row stacking direction.
    text_kwargs
        Keyword arguments for the :func:`matplotlib.pyplot.text` definition.
        The following special keywords can also be used:

        -   ``offset``: Sets the text offset.
        -   ``visible``: Sets the text visibility.
    background_colour
        Background colour.
    compare_swatches
        Whether to compare the swatches, in which case the colour swatch
        count must be an even number with alternating reference colour swatches
        and test colour swatches. *Stacked* will draw the test colour swatch in
        the center of the reference colour swatch, *Diagonal* will draw
        the reference colour swatch in the upper left diagonal area and the
        test colour swatch in the bottom right diagonal area.

    Other Parameters
    ----------------
    kwargs
        {:func:`colour.plotting.artist`, :func:`colour.plotting.render`},
        See the documentation of the previously listed definitions.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.

    Examples
    --------
    >>> RGB_1 = ColourSwatch((0.45293517, 0.31732158, 0.26414773))
    >>> RGB_2 = ColourSwatch((0.77875824, 0.57726450, 0.50453169))
    >>> plot_multi_colour_swatches([RGB_1, RGB_2])  # doctest: +ELLIPSIS
    (<Figure size ... with 1 Axes>, <...Axes...>)

    .. image:: ../_static/Plotting_Plot_Multi_Colour_Swatches.png
        :align: center
        :alt: plot_multi_colour_swatches
    """

    direction = validate_method(
        direction,
        ("+y", "-y"),
        '"{0}" direction is invalid, it must be one of {1}!',
    )

    if compare_swatches is not None:
        compare_swatches = validate_method(
            compare_swatches,
            ("Diagonal", "Stacked"),
            '"{0}" compare swatches method is invalid, it must be one of {1}!',
        )

    _figure, axes = artist(**kwargs)

    # Handling case where `colour_swatches` is a regular *ArrayLike*.
    colour_swatches = list(colour_swatches)
    colour_swatches_converted = []
    if not isinstance(first_item(colour_swatches), ColourSwatch):
        for _i, colour_swatch in enumerate(
            as_float_array(cast(ArrayLike, colour_swatches))[..., :3].reshape(
                [-1, 3]
            )
        ):
            colour_swatches_converted.append(ColourSwatch(colour_swatch))
    else:
        colour_swatches_converted = cast(List[ColourSwatch], colour_swatches)

    colour_swatches = colour_swatches_converted

    if compare_swatches is not None:
        attest(
            len(colour_swatches) % 2 == 0,
            "Cannot compare an odd number of colour swatches!",
        )

        colour_swatches_reference = colour_swatches[0::2]
        colour_swatches_test = colour_swatches[1::2]
    else:
        colour_swatches_reference = colour_swatches_test = colour_swatches

    columns = optional(columns, len(colour_swatches_reference))

    text_settings = {
        "offset": 0.05,
        "visible": True,
        "zorder": CONSTANTS_COLOUR_STYLE.zorder.midground_label,
    }
    if text_kwargs is not None:
        text_settings.update(text_kwargs)
    text_offset = text_settings.pop("offset")

    offset_X: float = 0
    offset_Y: float = 0
    x_min, x_max, y_min, y_max = 0, width, 0, height
    y = 1 if direction == "+y" else -1
    for i, colour_swatch in enumerate(colour_swatches_reference):
        if i % columns == 0 and i != 0:
            offset_X = 0
            offset_Y += (height + spacing) * y

        x_0, x_1 = offset_X, offset_X + width
        y_0, y_1 = offset_Y, offset_Y + height * y

        axes.fill(
            (x_0, x_1, x_1, x_0),
            (y_0, y_0, y_1, y_1),
            color=np.clip(colour_swatches_reference[i].RGB, 0, 1),
            zorder=CONSTANTS_COLOUR_STYLE.zorder.midground_polygon,
        )

        if compare_swatches == "stacked":
            margin_X = width * 0.25
            margin_Y = height * 0.25
            axes.fill(
                (
                    x_0 + margin_X,
                    x_1 - margin_X,
                    x_1 - margin_X,
                    x_0 + margin_X,
                ),
                (
                    y_0 + margin_Y * y,
                    y_0 + margin_Y * y,
                    y_1 - margin_Y * y,
                    y_1 - margin_Y * y,
                ),
                color=np.clip(colour_swatches_test[i].RGB, 0, 1),
                zorder=CONSTANTS_COLOUR_STYLE.zorder.midground_polygon,
            )
        else:
            axes.fill(
                (x_0, x_1, x_1),
                (y_0, y_0, y_1),
                color=np.clip(colour_swatches_test[i].RGB, 0, 1),
                zorder=CONSTANTS_COLOUR_STYLE.zorder.midground_polygon,
            )

        if colour_swatch.name is not None and text_settings["visible"]:
            axes.text(
                x_0 + text_offset,
                y_0 + text_offset * y,
                colour_swatch.name,
                verticalalignment="bottom" if y == 1 else "top",
                clip_on=True,
                **text_settings,
            )

        offset_X += width + spacing

    x_max = min(len(colour_swatches), as_int_scalar(columns))
    x_max = x_max * width + x_max * spacing - spacing
    y_max = offset_Y

    axes.patch.set_facecolor(background_colour)  # pyright: ignore

    if y == 1:
        bounding_box = [
            x_min - spacing,
            x_max + spacing,
            y_min - spacing,
            y_max + spacing + height,
        ]
    else:
        bounding_box = [
            x_min - spacing,
            x_max + spacing,
            y_max - spacing - height,
            y_min + spacing,
        ]

    settings: Dict[str, Any] = {
        "axes": axes,
        "bounding_box": bounding_box,
        "aspect": "equal",
    }
    settings.update(kwargs)

    return render(**settings)


@override_style()
def plot_single_function(
    function: Callable,
    samples: ArrayLike | None = None,
    log_x: int | None = None,
    log_y: int | None = None,
    plot_kwargs: dict | List[dict] | None = None,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """
    Plot given function.

    Parameters
    ----------
    function
        Function to plot.
    samples
        Samples to evaluate the functions with.
    log_x
        Log base to use for the *x* axis scale, if *None*, the *x* axis scale
        will be linear.
    log_y
        Log base to use for the *y* axis scale, if *None*, the *y* axis scale
        will be linear.
    plot_kwargs
        Keyword arguments for the :func:`matplotlib.pyplot.plot` definition,
        used to control the style of the plotted function.

    Other Parameters
    ----------------
    kwargs
        {:func:`colour.plotting.artist`,
        :func:`colour.plotting.plot_multi_functions`,
        :func:`colour.plotting.render`},
        See the documentation of the previously listed definitions.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.

    Examples
    --------
    >>> from colour.models import gamma_function
    >>> plot_single_function(partial(gamma_function, exponent=1 / 2.2))
    ... # doctest: +ELLIPSIS
    (<Figure size ... with 1 Axes>, <...Axes...>)

    .. image:: ../_static/Plotting_Plot_Single_Function.png
        :align: center
        :alt: plot_single_function
    """

    try:
        name = function.__name__
    except AttributeError:
        name = "Unnamed"

    settings: Dict[str, Any] = {
        "title": f"{name} - Function",
        "legend": False,
    }
    settings.update(kwargs)

    return plot_multi_functions(
        {name: function}, samples, log_x, log_y, plot_kwargs, **settings
    )


@override_style()
def plot_multi_functions(
    functions: Dict[str, Callable],
    samples: ArrayLike | None = None,
    log_x: int | None = None,
    log_y: int | None = None,
    plot_kwargs: dict | List[dict] | None = None,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """
    Plot given functions.

    Parameters
    ----------
    functions
        Functions to plot.
    samples
        Samples to evaluate the functions with.
    log_x
        Log base to use for the *x* axis scale, if *None*, the *x* axis scale
        will be linear.
    log_y
        Log base to use for the *y* axis scale, if *None*, the *y* axis scale
        will be linear.
    plot_kwargs
        Keyword arguments for the :func:`matplotlib.pyplot.plot` definition,
        used to control the style of the plotted functions. ``plot_kwargs``
        can be either a single dictionary applied to all the plotted functions
        with the same settings or a sequence of dictionaries with different
        settings for each plotted function.

    Other Parameters
    ----------------
    kwargs
        {:func:`colour.plotting.artist`, :func:`colour.plotting.render`},
        See the documentation of the previously listed definitions.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.

    Examples
    --------
    >>> functions = {
    ...     "Gamma 2.2": lambda x: x ** (1 / 2.2),
    ...     "Gamma 2.4": lambda x: x ** (1 / 2.4),
    ...     "Gamma 2.6": lambda x: x ** (1 / 2.6),
    ... }
    >>> plot_multi_functions(functions)
    ... # doctest: +ELLIPSIS
    (<Figure size ... with 1 Axes>, <...Axes...>)

    .. image:: ../_static/Plotting_Plot_Multi_Functions.png
        :align: center
        :alt: plot_multi_functions
    """

    settings: Dict[str, Any] = dict(kwargs)

    _figure, axes = artist(**settings)

    plot_settings_collection = [
        {
            "label": f"{name}",
            "zorder": CONSTANTS_COLOUR_STYLE.zorder.midground_label,
        }
        for name in functions
    ]

    if plot_kwargs is not None:
        update_settings_collection(
            plot_settings_collection, plot_kwargs, len(functions)
        )

    if log_x is not None and log_y is not None:
        attest(
            log_x >= 2 and log_y >= 2,
            "Log base must be equal or greater than 2.",
        )

        plotting_function = axes.loglog

        axes.set_xscale("log", base=log_x)
        axes.set_yscale("log", base=log_y)
    elif log_x is not None:
        attest(log_x >= 2, "Log base must be equal or greater than 2.")

        plotting_function = partial(axes.semilogx, base=log_x)
    elif log_y is not None:
        attest(log_y >= 2, "Log base must be equal or greater than 2.")

        plotting_function = partial(axes.semilogy, base=log_y)
    else:
        plotting_function = axes.plot

    samples = optional(samples, np.linspace(0, 1, 1000))

    for i, (_name, function) in enumerate(functions.items()):
        plotting_function(
            samples, function(samples), **plot_settings_collection[i]
        )

    x_label = (
        f"x - Log Base {log_x} Scale"
        if log_x is not None
        else "x - Linear Scale"
    )
    y_label = (
        f"y - Log Base {log_y} Scale"
        if log_y is not None
        else "y - Linear Scale"
    )
    settings = {
        "axes": axes,
        "legend": True,
        "title": f"{', '.join(functions)} - Functions",
        "x_label": x_label,
        "y_label": y_label,
    }
    settings.update(kwargs)

    return render(**settings)


@override_style()
def plot_image(
    image: ArrayLike,
    imshow_kwargs: dict | None = None,
    text_kwargs: dict | None = None,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """
    Plot given image.

    Parameters
    ----------
    image
        Image to plot.
    imshow_kwargs
        Keyword arguments for the :func:`matplotlib.pyplot.imshow` definition.
    text_kwargs
        Keyword arguments for the :func:`matplotlib.pyplot.text` definition.
        The following special keyword arguments can also be used:

        -   ``offset`` : Sets the text offset.

    Other Parameters
    ----------------
    kwargs
        {:func:`colour.plotting.artist`, :func:`colour.plotting.render`},
        See the documentation of the previously listed definitions.

    Returns
    -------
    :class:`tuple`
        Current figure and axes.

    Examples
    --------
    >>> import os
    >>> import colour
    >>> from colour import read_image
    >>> path = os.path.join(
    ...     colour.__path__[0],
    ...     "examples",
    ...     "plotting",
    ...     "resources",
    ...     "Ishihara_Colour_Blindness_Test_Plate_3.png",
    ... )
    >>> plot_image(read_image(path))  # doctest: +ELLIPSIS
    (<Figure size ... with 1 Axes>, <...Axes...>)

    .. image:: ../_static/Plotting_Plot_Image.png
        :align: center
        :alt: plot_image
    """

    _figure, axes = artist(**kwargs)

    imshow_settings = {
        "interpolation": "nearest",
        "cmap": matplotlib.colormaps["Greys_r"],
        "zorder": CONSTANTS_COLOUR_STYLE.zorder.background_polygon,
    }
    if imshow_kwargs is not None:
        imshow_settings.update(imshow_kwargs)

    text_settings = {
        "text": None,
        "offset": 0.005,
        "color": CONSTANTS_COLOUR_STYLE.colour.brightest,
        "alpha": CONSTANTS_COLOUR_STYLE.opacity.high,
        "zorder": CONSTANTS_COLOUR_STYLE.zorder.midground_label,
    }
    if text_kwargs is not None:
        text_settings.update(text_kwargs)
    text_offset = text_settings.pop("offset")

    image = as_float_array(image)

    axes.imshow(np.clip(image, 0, 1), **imshow_settings)

    if text_settings["text"] is not None:
        text = text_settings.pop("text")

        axes.text(
            text_offset,
            text_offset,
            text,
            transform=axes.transAxes,
            ha="left",
            va="bottom",
            **text_settings,
        )

    settings: Dict[str, Any] = {
        "axes": axes,
        "axes_visible": False,
    }
    settings.update(kwargs)

    return render(**settings)
