#!/usr/bin/env python
# Using the ase spacegroup module this can build the structure, from
# the composition, as defined in the smact_lattice module.
#TODO:
# Estimate the cell parameters based on radii from tables.
# Add further types, Spinnel, Flourite, Delafossite ....
# Implement Structure class, c.f. dev_docs.
################################################################################
# Copyright Keith T Butler, Adam J Jackson    (2013)                           #
#                                                                              #
# This file is part of SMACT: builder.py is free software: you can             #
# redistribute it and/or modify it under the terms of the GNU General Public   #
# License as published by the Free Software Foundation, either version 3 of    #
# the License, or (at your option) any later version.                          #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for    #
# more details.                                                                #
# You should have received a copy of the GNU General Public License along with #
# this program.  If not, see <http://www.gnu.org/licenses/>.                   #
#                                                                              #
################################################################################

import typing
from typing import List, Tuple, Union

# First example: using ase

from ase.spacegroup import crystal
from smact.lattice import Lattice, Site
from smact import Species


class SmactStructure:
    """SMACT implementation inspired by pymatgen Structure class."""

    def __init__(self, species: List[Union[Tuple[str, int, int], Tuple[Species, int]]]):
        """Initialize class with constituent species."""
        if not isinstance(species, list):
            raise TypeError(f"`species` must be a list, got {type(species)}.")
        if len(species) == 0:
            raise ValueError("`species` cannot be empty.")
        if not isinstance(species[0], tuple):
            raise TypeError(f"`species` must be a list of tuples, got list of {type(species[0])}.")

        species_error = (
            "`species` list of tuples must contain either "
            "2-tuples of Species objects and stoichiometries, "
            "or 3-tuples of elements, oxidations and stoichiometries."
        )
        if len(species[0]) not in {2, 3}:
            raise ValueError(species_error)

        if isinstance(species[0][0], str):  # String variation of instantiation
            self.species = sorted(species, key=lambda x: x[0])

        elif isinstance(species[0][0], Species):  # Species class variation of instantiation
            self.species = sorted(species, key=lambda x: x.symbol)

        else:
            raise TypeError(species_error)


def cubic_perovskite(species, cell_par=[6, 6, 6, 90, 90, 90], repetitions=[1, 1, 1]):
    """
    Build a perovskite cell using the crystal function in ASE.

    Args:
        species (str): Element symbols
        cell_par (list): Six floats/ints specifying 3 unit cell lengths and 3 unit cell angles.
        repetitions (list): Three floats specifying the expansion of the cell in x,y,z directions.
    Returns:
        SMACT Lattice object of the unit cell,
        ASE crystal system of the unit cell.

    """
    system = crystal((species),
                     basis=[(0, 0, 0), (0.5, 0.5, 0.5), (0.5, 0.5, 0)],
                     spacegroup=221,
                     size=repetitions,
                     cellpar=cell_par)

    sites_list = []
    oxidation_states = [[2]] + [[4]] + [[-2]] * 3
    for site in zip(system.get_scaled_positions(), oxidation_states):
        sites_list.append(Site(site[0], site[1]))

    return Lattice(sites_list, oxidation_states), system


def wurtzite(species, cell_par=[2, 2, 6, 90, 90, 120], repetitions=[1, 1, 1]):
    """
    Build a wurzite cell using the crystal function in ASE.

    Args:
        species (str): Element symbols
        cell_par (list): Six floats/ints specifying 3 unit cell lengths and 3 unit cell angles.
        repetitions (list): Three floats specifying the expansion of the cell in x,y,z directions.
    Returns:
        SMACT Lattice object of the unit cell,
        ASE crystal system of the unit cell.

    """
    system = crystal((species),
                     basis=[(2. / 3., 1. / 3., 0), (2. / 3., 1. / 3., 5. / 8.)],
                     spacegroup=186,
                     size=repetitions,
                     cellpar=[3, 3, 6, 90, 90, 120])

    sites_list = []
    oxidation_states = [[1], [2], [3], [4]] + [[-1], [-2], [-3], [-4]]

    for site in zip(system.get_scaled_positions(), oxidation_states):
        sites_list.append(Site(site[0], site[1]))
    return Lattice(sites_list, oxidation_states), system
