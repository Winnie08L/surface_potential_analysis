from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

import numpy as np
from surface_potential_analysis.axis.axis import (
    TransformedPositionBasis,
)
from surface_potential_analysis.axis.evenly_spaced_basis import EvenlySpacedBasis
from surface_potential_analysis.axis.stacked_axis import StackedBasis
from surface_potential_analysis.stacked_basis.build import (
    fundamental_stacked_basis_from_shape,
)
from surface_potential_analysis.state_vector.util import (
    get_most_localized_free_state_vectors,
)
from surface_potential_analysis.util.decorators import npy_cached
from surface_potential_analysis.wavepacket.localization import (
    get_localization_operator_wannier90,
    localize_single_point_projection,
    localize_tight_binding_projection,
    localize_tightly_bound_wavepacket_two_point_max,
)
from surface_potential_analysis.wavepacket.localization.localization_operator import (
    get_localized_wavepackets,
)
from surface_potential_analysis.wavepacket.wavepacket import (
    Wavepacket,
    WavepacketList,
    WavepacketWithEigenvaluesList,
    generate_wavepacket,
    get_average_eigenvalues,
    get_wavepacket,
    get_wavepacket_basis,
    get_wavepackets,
)

from .s2_hamiltonian import (
    get_hamiltonian,
)
from .surface_data import get_data_path

if TYPE_CHECKING:
    from pathlib import Path

    from surface_potential_analysis.axis.axis import (
        ExplicitBasis,
        FundamentalBasis,
    )
    from surface_potential_analysis.axis.axis_like import BasisLike
    from surface_potential_analysis.axis.stacked_axis import (
        StackedBasisLike,
    )
    from surface_potential_analysis.operator.operator import SingleBasisOperator
    from surface_potential_analysis.wavepacket.localization.localization_operator import (
        LocalizationOperator,
    )

    _HydrogenCopperWavepacketList = WavepacketWithEigenvaluesList[
        EvenlySpacedBasis[Literal[25], Literal[1], Literal[0]],
        StackedBasisLike[
            FundamentalBasis[Literal[5]],
            FundamentalBasis[Literal[5]],
            FundamentalBasis[Literal[1]],
        ],
        StackedBasisLike[
            TransformedPositionBasis[Literal[21], Literal[21], Literal[3]],
            TransformedPositionBasis[Literal[21], Literal[21], Literal[3]],
            ExplicitBasis[Literal[250], Literal[15], Literal[3]],
        ],
    ]
    _HydrogenCopperWavepacket = Wavepacket[
        StackedBasisLike[
            FundamentalBasis[Literal[5]],
            FundamentalBasis[Literal[5]],
            FundamentalBasis[Literal[1]],
        ],
        StackedBasisLike[
            TransformedPositionBasis[Literal[21], Literal[21], Literal[3]],
            TransformedPositionBasis[Literal[21], Literal[21], Literal[3]],
            ExplicitBasis[Literal[250], Literal[15], Literal[3]],
        ],
    ]


@npy_cached(get_data_path("wavepacket/wavepacket_hydrogen.npy"), load_pickle=True)  # type: ignore[misc]
def get_all_wavepackets_hydrogen() -> _HydrogenCopperWavepacketList:
    a = np.load(
        get_data_path("wavepacket/wavepacket_hydrogen_o.npy"), allow_pickle=True
    )[()]
    a["basis"] = StackedBasis(
        a["basis"][0],
        StackedBasis(
            a["basis"][1][0],
            TransformedPositionBasis(
                np.array([0, a["basis"][1][1].delta_x[0], 0]),
                a["basis"][1][1].n,
                a["basis"][1][1].fundamental_n,
            ),
            a["basis"][1][2],
        ),
    )
    return a

    def _hamiltonian_generator(
        bloch_fraction: np.ndarray[tuple[Literal[3]], np.dtype[np.float_]]
    ) -> SingleBasisOperator[Any]:
        return get_hamiltonian(
            shape=(48, 48, 251),
            bloch_fraction=bloch_fraction,
            resolution=(22, 21, 15),
        )

    return generate_wavepacket(
        _hamiltonian_generator,
        list_basis=fundamental_stacked_basis_from_shape((5, 5, 1)),
        save_bands=EvenlySpacedBasis(25, 1, 0),
    )


def get_wavepacket_hydrogen(band: int) -> _HydrogenCopperWavepacket:
    return get_wavepacket(get_all_wavepackets_hydrogen(), band)


def get_two_point_localized_wavepacket_hydrogen(
    band: int, offset: tuple[int, int] = (0, 0), angle: float = 0
) -> _HydrogenCopperWavepacket:
    wavepacket = get_wavepacket_hydrogen(band)
    return localize_tightly_bound_wavepacket_two_point_max(wavepacket, offset, angle)


def _get_wavepacket_cache_tight_binding_h(band: int) -> Path:
    return get_data_path(f"wavepacket/localized_wavepacket_tb_hydrogen_{band}.npy")


@npy_cached(_get_wavepacket_cache_tight_binding_h, load_pickle=True)
def get_tight_binding_projection_localized_wavepacket_hydrogen(
    band: int,
) -> _HydrogenCopperWavepacket:
    wavepacket = get_wavepacket_hydrogen(band)
    return localize_tight_binding_projection(wavepacket)


def _get_wavepacket_cache_single_point_h(band: int) -> Path:
    return get_data_path(
        f"wavepacket/localized_wavepacket_sp_hydrogen_{band}_five_2_symm.npy"
    )


@npy_cached(_get_wavepacket_cache_single_point_h, load_pickle=True)
def get_single_point_projection_localized_wavepacket_hydrogen(
    band: int,
) -> _HydrogenCopperWavepacket:
    wavepacket = get_wavepacket_hydrogen(band)
    return localize_single_point_projection(wavepacket)


def _get_wavepacket_cache_wannier90_h(sample_shape: tuple[int, int]) -> Path:
    return get_data_path(
        f"wavepacket/localized_wavepacket_operator_{sample_shape[0]}_{sample_shape[1]}.npy"
    )


@npy_cached(_get_wavepacket_cache_wannier90_h, load_pickle=True)
def get_localization_operator_hydrogen(
    sample_shape: tuple[int, int]
) -> LocalizationOperator[
    StackedBasisLike[
        FundamentalBasis[Literal[5]],
        FundamentalBasis[Literal[5]],
        FundamentalBasis[Literal[1]],
    ],
    StackedBasisLike[*tuple[FundamentalBasis[int], ...]],
    BasisLike[Any, Any],
]:
    n_samples = sample_shape[0] * sample_shape[1]
    wavepackets = get_all_wavepackets_hydrogen()
    projections = get_most_localized_free_state_vectors(
        get_wavepacket_basis(wavepackets), sample_shape
    )
    return get_localization_operator_wannier90(
        get_wavepackets(wavepackets, slice(n_samples)), projections
    )


def get_wannier90_localized_wavepacket_hydrogen(
    sample_shape: tuple[int, int]
) -> WavepacketList[
    StackedBasisLike[*tuple[FundamentalBasis[int], ...]],
    StackedBasisLike[
        FundamentalBasis[Literal[5]],
        FundamentalBasis[Literal[5]],
        FundamentalBasis[Literal[1]],
    ],
    StackedBasisLike[
        TransformedPositionBasis[Literal[21], Literal[21], Literal[3]],
        TransformedPositionBasis[Literal[21], Literal[21], Literal[3]],
        ExplicitBasis[Literal[250], Literal[15], Literal[3]],
    ],
]:
    n_samples = sample_shape[0] * sample_shape[1]
    wavepackets = get_all_wavepackets_hydrogen()
    operator = get_localization_operator_hydrogen(sample_shape)
    return get_localized_wavepackets(
        get_wavepackets(wavepackets, slice(n_samples)), operator
    )


def get_hydrogen_energy_difference(state_0: int, state_1: int) -> np.complex_:
    eigenvalues = get_average_eigenvalues(get_all_wavepackets_hydrogen())["data"]
    return eigenvalues[state_0] - eigenvalues[state_1]
