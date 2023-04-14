from typing import Literal, TypeVar

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import ArtistAnimation
from matplotlib.axes import Axes
from matplotlib.collections import QuadMesh
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from surface_potential_analysis.eigenstate.eigenstate import (
    convert_eigenstate_to_position_basis,
)
from surface_potential_analysis.eigenstate.plot import (
    animate_eigenstate_3d,
    plot_eigenstate_2d,
    plot_eigenstate_along_path,
    plot_eigenstate_difference_2d,
)
from surface_potential_analysis.wavepacket.eigenstate_conversion import (
    unfurl_wavepacket,
)

from .wavepacket import MomentumBasisWavepacket, get_wavepacket_sample_frequencies

_NS0 = TypeVar("_NS0", bound=int)
_NS1 = TypeVar("_NS1", bound=int)

_L0Inv = TypeVar("_L0Inv", bound=int)
_L1Inv = TypeVar("_L1Inv", bound=int)
_L2Inv = TypeVar("_L2Inv", bound=int)


def plot_wavepacket_sample_frequencies(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    *,
    ax: Axes | None = None,
) -> tuple[Figure, Axes, Line2D]:
    fig, ax = (ax.get_figure(), ax) if ax is not None else plt.subplots()

    fractions = get_wavepacket_sample_frequencies(
        wavepacket["basis"], np.array(wavepacket["vectors"].shape)[0:2]
    )
    (line,) = ax.plot(*fractions.reshape(2, -1))
    line.set_marker("x")
    line.set_linestyle("")

    return fig, ax, line


def plot_wavepacket_2d(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    idx: int,
    z_axis: Literal[0, 1, 2, -1, -2, -3],
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, QuadMesh]:
    eigenstate_momentum = unfurl_wavepacket(wavepacket)
    eigenstate = convert_eigenstate_to_position_basis(eigenstate_momentum)
    return plot_eigenstate_2d(
        eigenstate, idx, z_axis, ax=ax, measure=measure, scale=scale
    )


def plot_wavepacket_x0x1(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    x3_idx: int,
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, QuadMesh]:
    return plot_wavepacket_2d(
        wavepacket, x3_idx, 2, ax=ax, measure=measure, scale=scale
    )


def plot_wavepacket_x1x2(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    x0_idx: int,
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, QuadMesh]:
    return plot_wavepacket_2d(
        wavepacket, x0_idx, 0, ax=ax, measure=measure, scale=scale
    )


def plot_wavepacket_x2x0(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    x1_idx: int,
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, QuadMesh]:
    return plot_wavepacket_2d(
        wavepacket, x1_idx, 1, ax=ax, measure=measure, scale=scale
    )


def plot_wavepacket_difference_2d(
    wavepacket0: MomentumBasisWavepacket[_NS0, _NS1, _L0Inv, _L1Inv, _L2Inv],
    wavepacket1: MomentumBasisWavepacket[_NS0, _NS1, _L0Inv, _L1Inv, _L2Inv],
    idx: int,
    z_axis: Literal[0, 1, 2, -1, -2, -3],
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, QuadMesh]:
    eigenstate_momentum0 = unfurl_wavepacket(wavepacket0)
    eigenstate0 = convert_eigenstate_to_position_basis(eigenstate_momentum0)

    eigenstate_momentum1 = unfurl_wavepacket(wavepacket1)
    eigenstate1 = convert_eigenstate_to_position_basis(eigenstate_momentum1)

    return plot_eigenstate_difference_2d(
        eigenstate0, eigenstate1, idx, z_axis, ax=ax, measure=measure, scale=scale
    )


def animate_wavepacket_3d(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    z_axis: Literal[0, 1, 2, -1, -2, -3],
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, ArtistAnimation]:
    eigenstate_momentum = unfurl_wavepacket(wavepacket)
    eigenstate = convert_eigenstate_to_position_basis(eigenstate_momentum)
    return animate_eigenstate_3d(
        eigenstate, z_axis, ax=ax, measure=measure, scale=scale
    )


def animate_wavepacket_x0x1(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, ArtistAnimation]:
    return animate_wavepacket_3d(wavepacket, 2, ax=ax, measure=measure, scale=scale)


def animate_wavepacket_x1x2(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, ArtistAnimation]:
    return animate_wavepacket_3d(wavepacket, 0, ax=ax, measure=measure, scale=scale)


def animate_wavepacket_x2x0(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, ArtistAnimation]:
    return animate_wavepacket_3d(wavepacket, 1, ax=ax, measure=measure, scale=scale)


def plot_wavepacket_along_path(
    wavepacket: MomentumBasisWavepacket[int, int, int, int, int],
    path: np.ndarray[tuple[Literal[3], int], np.dtype[np.int_]],
    *,
    ax: Axes | None = None,
    measure: Literal["real", "imag", "abs"] = "abs",
    scale: Literal["symlog", "linear"] = "linear",
) -> tuple[Figure, Axes, Line2D]:
    eigenstate_momentum = unfurl_wavepacket(wavepacket)
    eigenstate = convert_eigenstate_to_position_basis(eigenstate_momentum)
    return plot_eigenstate_along_path(
        eigenstate, path, ax=ax, measure=measure, scale=scale
    )
