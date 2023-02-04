#![warn(clippy::all, clippy::pedantic, clippy::nursery, clippy::cargo)]

use std::{collections::HashMap, f64::consts::PI};

use num_complex::{Complex, Complex64};
use pyo3::prelude::*;

fn factorial(n: u64) -> u64 {
    (1..=n).product()
}
#[must_use]
const fn hermite_coefficient(n: i64, m: i64) -> i64 {
    match (n, m) {
        (0, 0) => 1,
        (1, 0) => 0,
        (1, 1) => 2,
        (_, 0) => -hermite_coefficient(n - 1, m + 1),
        (n, m) if n >= m => {
            2 * hermite_coefficient(n - 1, m - 1) - (m + 1) * hermite_coefficient(n - 1, m + 1)
        }
        _ => 0,
    }
}
#[allow(clippy::cast_precision_loss)]
fn hermite_val(x: f64, n: u32) -> f64 {
    (0..=n)
        .map(|m| (hermite_coefficient(n.into(), m.into()) as f64) * x.powi(m.try_into().unwrap()))
        .sum()
}

fn calculate_sho_wavefunction(z_points: &Vec<f64>, sho_omega: f64, mass: f64, n: u32) -> Vec<f64> {
    let norm = ((sho_omega * mass) / REDUCED_PLANCK_CONSTANT).sqrt();
    let factorial: f64 = factorial(n.into()) as f64;
    let prefactor = (norm / factorial) / (PI.sqrt() * 2_f64.powi(n.try_into().unwrap()));
    let sqrt_prefactor = prefactor.sqrt();

    z_points
        .into_iter()
        .map(|p| -> f64 {
            let normalized_p = p * norm;
            let hermite_val = hermite_val(normalized_p, n);
            sqrt_prefactor * hermite_val * f64::exp(-normalized_p.powi(2) / 2.0)
        })
        .collect()
}

const PLANCK_CONSTANT: f64 = 6.626_070_15E-34;
const REDUCED_PLANCK_CONSTANT: f64 = PLANCK_CONSTANT / (2.0 * PI);

struct EigenstateResolution(i64, i64, usize);

impl EigenstateResolution {
    fn coordinates(&self) -> Vec<(i64, i64, usize)> {
        (-self.0..=self.0)
            .flat_map(|x| (-self.1..=self.1).flat_map(move |y| (0..self.2).map(move |z| (x, y, z))))
            .collect()
    }
}

struct EigenstateConfig {
    sho_omega: f64,
    mass: f64,
    delta_x1: (f64, f64),
    delta_x2: (f64, f64),
}

struct Eigenstate {
    config: EigenstateConfig,
    resolution: EigenstateResolution,
    vector: Vec<num_complex::Complex64>,
    kx: f64,
    ky: f64,
}

impl Eigenstate {
    fn calculate_wavefunction(&self, points: &Vec<[f64; 3]>) -> Vec<Complex64> {
        let coordinates = self.resolution.coordinates();
        let z_points: Vec<f64> = points.iter().map(|p| p[2]).collect();

        let cache: Vec<Vec<f64>> = (0..self.resolution.2)
            .map(|nz| -> Vec<f64> {
                calculate_sho_wavefunction(
                    &z_points,
                    self.config.sho_omega,
                    self.config.mass,
                    nz as u32,
                )
            })
            .collect();

        let dkx1 = self.config.dkx1();
        let dkx2 = self.config.dkx2();

        let mut out: Vec<Complex64> = vec![Complex::default(); points.len()];
        for (eig, (nkx1, nkx2, nz)) in self.vector.iter().zip(coordinates) {
            for (i, wfn) in cache[nz].iter().enumerate() {
                out[i] += wfn
                    * eig
                    * Complex {
                        re: 0.0, //TODO
                        im: ((nkx1 as f64) * dkx1.0 + (nkx2 as f64) * dkx2.0 + self.kx)
                            * points[i][0]
                            + ((nkx1 as f64) * dkx1.1 + (nkx2 as f64) * dkx2.1 + self.ky)
                                * points[i][1],
                    }
                    .exp();
            }
        }

        out
    }
}

impl EigenstateConfig {
    fn dk_prefactor(&self) -> f64 {
        let x1_part = self.delta_x1.0 * self.delta_x2.1;
        let x2_part = self.delta_x1.1 * self.delta_x2.0;
        (2.0 * PI) / (x1_part - x2_part)
    }
    fn dkx1(&self) -> (f64, f64) {
        let prefactor = self.dk_prefactor();
        (prefactor * self.delta_x2.1, -prefactor * self.delta_x2.0)
    }

    fn dkx2(&self) -> (f64, f64) {
        let prefactor = self.dk_prefactor();
        (-prefactor * self.delta_x1.1, prefactor * self.delta_x1.0)
    }
}

struct SurfaceHamiltonian {
    sho_config: EigenstateConfig,
    resolution: EigenstateResolution,
    ft_potential: Vec<Vec<Vec<f64>>>,
    dz: f64,
    z_offset: f64,
}

impl SurfaceHamiltonian {
    fn get_nx1(&self) -> usize {
        self.ft_potential.len()
    }

    fn get_nx2(&self) -> usize {
        self.ft_potential[0].len()
    }

    fn get_nz(&self) -> usize {
        self.ft_potential[0][0].len()
    }

    fn get_z_points(&self) -> Vec<f64> {
        (0..self.get_nz())
            .map(|i| self.dz.mul_add(i as f64, self.z_offset))
            .collect()
    }

    fn calculate_sho_wavefunction(&self, n: u32) -> Vec<f64> {
        calculate_sho_wavefunction(
            &self.get_z_points(),
            self.sho_config.sho_omega,
            self.sho_config.mass,
            n,
        )
    }

    fn calculate_off_diagonal_energies(&self) -> Vec<Vec<f64>> {
        let coordinates = self.resolution.coordinates();
        let cache: Vec<Vec<f64>> = (0..self.resolution.2)
            .map(|nz| -> Vec<f64> { self.calculate_sho_wavefunction(nz.try_into().unwrap()) })
            .collect();

        let mut g_points: HashMap<(usize, usize, usize, usize), f64> = HashMap::new();

        coordinates
            .iter()
            .map(|(nkx1_1, nkx2_1, nz1)| -> Vec<f64> {
                coordinates
                    .iter()
                    .map(|(nkx1_2, nkx2_2, nz2)| -> f64 {
                        let n_dkx1 = (nkx1_2 - nkx1_1).rem_euclid(self.get_nx1() as i64) as usize;
                        let n_dkx2 = (nkx2_2 - nkx2_1).rem_euclid(self.get_nx2() as i64) as usize;
                        if let Some(a) = g_points.get(&(n_dkx1, n_dkx2, *nz1, *nz2)) {
                            return *a;
                        }

                        let ft_pot_points = &self.ft_potential[n_dkx1][n_dkx2];

                        let sho1: &Vec<f64> = &cache[*nz1];
                        let sho2: &Vec<f64> = &cache[*nz2];

                        let out = ft_pot_points
                            .iter()
                            .zip(sho1)
                            .zip(sho2)
                            .map(|((i, j), k)| i * j * k)
                            .sum::<f64>()
                            * self.dz;
                        g_points.insert((n_dkx1, n_dkx2, *nz1, *nz2), out);
                        out
                    })
                    .collect()
            })
            .collect()
    }
}

#[pyfunction]
fn get_hermite_val(x: f64, n: u32) -> f64 {
    hermite_val(x, n)
}

#[pyfunction]
#[allow(clippy::needless_pass_by_value)]
fn get_sho_wavefunction(z_points: Vec<f64>, sho_omega: f64, mass: f64, n: u32) -> Vec<f64> {
    calculate_sho_wavefunction(&z_points, sho_omega, mass, n)
}

#[pyfunction]
fn calculate_off_diagonal_energies(
    ft_potential: Vec<Vec<Vec<f64>>>,
    resolution: [usize; 3],
    dz: f64,
    mass: f64,
    sho_omega: f64,
    z_offset: f64,
) -> Vec<Vec<f64>> {
    let sho_config = EigenstateConfig {
        mass,
        sho_omega,
        delta_x1: (1.0, 0.0),
        delta_x2: (0.0, 1.0),
    };
    let hamiltonian = SurfaceHamiltonian {
        dz,
        ft_potential,
        resolution: EigenstateResolution(
            resolution[0].try_into().unwrap(),
            resolution[1].try_into().unwrap(),
            resolution[2],
        ),
        sho_config,
        z_offset,
    };
    hamiltonian.calculate_off_diagonal_energies()
}

#[pyfunction]
#[allow(clippy::too_many_arguments)]
fn get_eigenstate_wavefunction(
    resolution: [usize; 3],
    delta_x1: (f64, f64),
    delta_x2: (f64, f64),
    mass: f64,
    sho_omega: f64,
    kx: f64,
    ky: f64,
    vector: Vec<Complex64>,
    points: Vec<[f64; 3]>,
) -> Vec<Complex64> {
    let eigenstate = Eigenstate {
        config: EigenstateConfig {
            sho_omega,
            mass,
            delta_x1,
            delta_x2,
        },
        kx,
        ky,
        resolution: EigenstateResolution(
            resolution[0].try_into().unwrap(),
            resolution[1].try_into().unwrap(),
            resolution[2],
        ),
        vector,
    };

    eigenstate.calculate_wavefunction(&points)
}

/// A Python module implemented in Rust.
#[pymodule]
fn hamiltonian_generator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_off_diagonal_energies, m)?)?;
    m.add_function(wrap_pyfunction!(get_sho_wavefunction, m)?)?;
    m.add_function(wrap_pyfunction!(get_hermite_val, m)?)?;
    m.add_function(wrap_pyfunction!(get_eigenstate_wavefunction, m)?)?;
    Ok(())
}

#[cfg(test)]
mod test {
    use crate::{EigenstateConfig, EigenstateResolution, SurfaceHamiltonian};

    #[test]
    fn test_calculate_off_diagonal_energies() {
        let sho_config = EigenstateConfig {
            mass: 1.0,
            sho_omega: 1.0,
            delta_x1: (1.0, 0.0),
            delta_x2: (0.0, 1.0),
        };
        let hamiltonian = SurfaceHamiltonian {
            dz: 1.0,
            ft_potential: vec![
                vec![vec![0.0, 0.0], vec![0.0, 0.0]],
                vec![vec![0.0, 0.0], vec![0.0, 0.0]],
            ],
            resolution: EigenstateResolution(2, 2, 2),
            sho_config,
            z_offset: 0.0,
        };

        hamiltonian.calculate_off_diagonal_energies();
    }
}
