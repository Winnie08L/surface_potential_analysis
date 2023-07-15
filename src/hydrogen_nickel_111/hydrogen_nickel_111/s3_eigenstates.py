from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypeVar

import numpy as np
from surface_potential_analysis.state_vector.eigenstate_collection import (
    calculate_eigenstate_collection,
)
from surface_potential_analysis.util.decorators import npy_cached

from .s2_hamiltonian import (
    get_hamiltonian_deuterium,
    get_hamiltonian_hydrogen,
    get_hamiltonian_hydrogen_sho,
)
from .surface_data import get_data_path

if TYPE_CHECKING:
    from pathlib import Path

    from surface_potential_analysis.axis.axis import (
        ExplicitAxis,
        MomentumAxis,
    )
    from surface_potential_analysis.operator.operator import SingleBasisOperator
    from surface_potential_analysis.state_vector.eigenstate_collection import (
        EigenstateColllection,
    )

    _L0 = TypeVar("_L0", bound=int)
    _L1 = TypeVar("_L1", bound=int)
    _L2 = TypeVar("_L2", bound=int)


def _get_eigenstate_collection_h_sho_cache(shape: tuple[_L0, _L1, _L2]) -> Path:
    return get_data_path(
        f"eigenstates/eigenstates_hydrogen_sho_{shape[0]}_{shape[1]}_{shape[2]}.npy"
    )


@npy_cached(_get_eigenstate_collection_h_sho_cache, load_pickle=True)  # type: ignore[misc]
def get_eigenstate_collection_hydrogen_sho(
    shape: tuple[_L0, _L1, _L2],
) -> EigenstateColllection[
    tuple[
        MomentumAxis[_L0, _L0, Literal[3]],
        MomentumAxis[_L1, _L1, Literal[3]],
        ExplicitAxis[Literal[250], _L2, Literal[3]],
    ],
    Literal[11],
]:
    bloch_fractions_x = np.linspace(-0.5, 0.5, 11)[[0, 5]]
    bloch_fractions = np.array([[f, 0, 0] for f in bloch_fractions_x])

    def hamiltonian_generator(
        bloch_fraction: np.ndarray[tuple[Literal[3]], np.dtype[np.float_]]
    ) -> SingleBasisOperator[
        tuple[
            MomentumAxis[_L0, _L0, Literal[3]],
            MomentumAxis[_L1, _L1, Literal[3]],
            ExplicitAxis[Literal[250], _L2, Literal[3]],
        ]
    ]:
        return get_hamiltonian_hydrogen_sho(
            shape=(250, 250, 250),
            bloch_fraction=bloch_fraction,
            resolution=shape,
        )

    return calculate_eigenstate_collection(
        hamiltonian_generator, bloch_fractions, subset_by_index=(0, 10)  # type: ignore[arg-type]
    )


def _get_eigenstate_collection_h_cache(shape: tuple[_L0, _L1, _L2]) -> Path:
    return get_data_path(
        f"eigenstates/eigenstates_hydrogen_{shape[0]}_{shape[1]}_{shape[2]}.npy"
    )


@npy_cached(_get_eigenstate_collection_h_cache, load_pickle=True)  # type: ignore[misc]
def get_eigenstate_collection_hydrogen(
    shape: tuple[_L0, _L1, _L2],
) -> EigenstateColllection[
    tuple[
        MomentumAxis[_L0, _L0, Literal[3]],
        MomentumAxis[_L1, _L1, Literal[3]],
        ExplicitAxis[Literal[250], _L2, Literal[3]],
    ],
    Literal[11],
]:
    bloch_fractions_x = np.linspace(-0.5, 0.5, 11)
    bloch_fractions = np.array([[f, 0, 0] for f in bloch_fractions_x])

    def hamiltonian_generator(
        bloch_fraction: np.ndarray[tuple[Literal[3]], np.dtype[np.float_]]
    ) -> SingleBasisOperator[
        tuple[
            MomentumAxis[_L0, _L0, Literal[3]],
            MomentumAxis[_L1, _L1, Literal[3]],
            ExplicitAxis[Literal[250], _L2, Literal[3]],
        ]
    ]:
        return get_hamiltonian_hydrogen(
            shape=(250, 250, 250),
            bloch_fraction=bloch_fraction,
            resolution=shape,
        )

    return calculate_eigenstate_collection(
        hamiltonian_generator, bloch_fractions, subset_by_index=(0, 10)  # type: ignore[arg-type]
    )


def _get_eigenstate_collection_d_cache(shape: tuple[_L0, _L1, _L2]) -> Path:
    return get_data_path(
        f"eigenstates/eigenstates_deuterium_{shape[0]}_{shape[1]}_{shape[2]}.npy"
    )


@npy_cached(_get_eigenstate_collection_d_cache, load_pickle=True)  # type: ignore[misc]
def get_eigenstate_collection_deuterium(
    shape: tuple[_L0, _L1, _L2],
) -> EigenstateColllection[
    tuple[
        MomentumAxis[_L0, _L0, Literal[3]],
        MomentumAxis[_L1, _L1, Literal[3]],
        ExplicitAxis[Literal[250], _L2, Literal[3]],
    ],
    Literal[11],
]:
    bloch_fractions_x = np.linspace(-0.5, 0.5, 11)
    bloch_fractions = np.array([[f, 0, 0] for f in bloch_fractions_x])

    def hamiltonian_generator(
        bloch_fraction: np.ndarray[tuple[Literal[3]], np.dtype[np.float_]]
    ) -> SingleBasisOperator[
        tuple[
            MomentumAxis[_L0, _L0, Literal[3]],
            MomentumAxis[_L1, _L1, Literal[3]],
            ExplicitAxis[Literal[250], _L2, Literal[3]],
        ]
    ]:
        return get_hamiltonian_deuterium(
            shape=(250, 250, 250),
            bloch_fraction=bloch_fraction,
            resolution=shape,
        )

    return calculate_eigenstate_collection(
        hamiltonian_generator, bloch_fractions, subset_by_index=(0, 99)  # type: ignore[arg-type]
    )
