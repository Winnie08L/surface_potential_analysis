from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from surface_potential_analysis.probability_vector.plot import (
    plot_probability_against_time,
)
from surface_potential_analysis.probability_vector.probability_vector import (
    ProbabilityVectorList,
    average_probabilities,
    sum_probabilities_over_axis,
)

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from matplotlib.lines import Line2D

    from surface_potential_analysis.axis.axis_like import AxisLike
    from surface_potential_analysis.axis.time_axis_like import (
        AxisWithTimeLike,
        FundamentalTimeAxis,
    )
    from surface_potential_analysis.dynamics.tunnelling_basis import (
        TunnellingSimulationBasis,
    )
    from surface_potential_analysis.util.plot import Scale

    _B1Inv = TypeVar("_B1Inv", bound=TunnellingSimulationBasis[Any, Any, Any])
    _B0Inv = TypeVar("_B0Inv", bound=tuple[AxisWithTimeLike[int, int]])
    _B0StackedInv = TypeVar(
        "_B0StackedInv", bound=tuple[AxisLike[Any, Any], FundamentalTimeAxis[int]]
    )


def plot_probability_per_band(
    probability: ProbabilityVectorList[_B0Inv, _B1Inv],
    *,
    ax: Axes | None = None,
    scale: Scale = "linear",
) -> tuple[Figure, Axes, list[Line2D]]:
    """
    Plot the occupation of each band in the simulation.

    Parameters
    ----------
    probability : ProbabilityVectorList[_B0Inv, _L0Inv]
    times : np.ndarray[tuple[_L0Inv], np.dtype[np.float_]]
    ax : Axes | None, optional
        plot axis, by default None
    scale : Scale, optional
        scale, by default "linear"

    Returns
    -------
    tuple[Figure, Axes, list[Line2D]]
    """
    probability_per_band = sum_probabilities_over_axis(probability, (2,))
    fig, ax, lines = plot_probability_against_time(
        probability_per_band, ax=ax, scale=scale
    )

    for n, line in enumerate(lines):
        line.set_label(f"band {n}")

    ax.legend()
    ax.set_title("Plot of occupation of each band against time")
    return fig, ax, lines


def plot_average_probability_per_band(
    probability: ProbabilityVectorList[_B0StackedInv, _B1Inv],
    *,
    ax: Axes | None = None,
    scale: Scale = "linear",
) -> tuple[Figure, Axes, list[Line2D]]:
    """
    Plot average probability of each band.

    Parameters
    ----------
    probability : list[ProbabilityVectorList[_B0StackedInv, _L0Inv]]
    times : np.ndarray[tuple[_L0Inv], np.dtype[np.float_]]
    ax : Axes | None, optional
        plot axis, by default None
    scale : Scale, optional
        scale, by default "linear"

    Returns
    -------
    tuple[Figure, Axes, list[Line2D]]
    """
    averaged = average_probabilities(probability, axis=(0,))
    fig, ax, lines = plot_probability_per_band(averaged, ax=ax, scale=scale)

    ax.set_title(
        "Plot of occupation of each band against time,\n"
        f"averaged over {len(probability)} repeats"
    )
    return fig, ax, lines


def plot_probability_per_site(
    probability: ProbabilityVectorList[_B0Inv, _B1Inv],
    *,
    ax: Axes | None = None,
    scale: Scale = "linear",
) -> tuple[Figure, Axes, list[Line2D]]:
    """
     Plot the occupation of each site in the simulation.

    Parameters
    ----------
    probability : ProbabilityVectorList[_B0Inv, _L0Inv]
    times : np.ndarray[tuple[_L0Inv], np.dtype[np.float_]]
    ax : Axes | None, optional
        plot axis, by default None
    scale : Scale, optional
        scale, by default "linear"

    Returns
    -------
    tuple[Figure, Axes, list[Line2D]]
    """
    probability_per_site = sum_probabilities_over_axis(probability, (0, 1))
    fig, ax, lines = plot_probability_against_time(
        probability_per_site, ax=ax, scale=scale
    )

    for n, line in enumerate(lines):
        line.set_label(f"site {n}")

    ax.legend()
    ax.set_title("Plot of occupation of each site against time")
    return fig, ax, lines
