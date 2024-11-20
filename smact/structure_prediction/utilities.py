"""Miscellaneous tools for data parsing."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from . import logger

if TYPE_CHECKING:
    from pymatgen.core.structure import Structure


def parse_spec(species: str) -> tuple[str, int]:
    """
    Parse a species string into its element and charge.

    Args:
    ----
        species (str): String representation of a species in
            the format {element}{absolute_charge}{sign}.

    Returns:
    -------
        A tuple of (element, signed_charge).

    Examples:
    --------
        >>> parse_spec("Fe2+")
        ('Fe', 2)
        >>> parse_spec("O2-")
        ('O', -2)

    """
    ele = re.match(r"[A-Za-z]+", species).group(0)

    charge_match = re.search(r"\d+", species)
    charge = int(charge_match.group(0)) if charge_match else 0

    if "-" in species:
        charge *= -1

    return ele, charge


def unparse_spec(species: tuple[str, int], include_one: bool = True) -> str:
    """Unparse a species into a string representation.


    The analogue of :func:`parse_spec`.

    Args:
        species (tuple[str,int]): A tuple of (element, signed_charge).
        include_one (bool): If True, include charge of 1 in the output if charge is 1 or -1.


    Returns:
    -------
        String of {element}{absolute_charge}{sign}.

    Examples:
    --------
        >>> unparse_spec(("Fe", 2))
        'Fe2+'
        >>> unparse_spec(("O", -2))
        'O2-'

    """
    if include_one or abs(species[1]) != 1:
        return f"{species[0]}{abs(species[1])}{get_sign(species[1])}"
    else:
        return f"{species[0]}{get_sign(species[1])}"


def get_sign(charge: int) -> str:
    """
    Get string representation of a number's sign.

    Args:
    ----
        charge (int): The number whose sign to derive.

    Returns:
    -------
        sign (str): either '+', '-', or '' for neutral.

    """
    if charge > 0:
        return "+"
    elif charge < 0:
        return "-"
    else:
        return ""


def convert_next_gen_mprest_data(
    doc,
) -> dict[str, Structure | str | None]:
    """Converts the `MPDataDoc` object returned by a next-gen MP query to a dictionary.

    Args:
    ----
        doc (MPDataDoc): A MPDataDoc object (based on a pydantic model) with fields 'structure' and 'material_id'
    Returns:
        A dictionary containing at least the keys 'structure' and
        'material_id', with the associated values.

    """
    try:
        return doc.dict(exclude={"fields_not_requested"})
    except:
        logger.warn(f"Could not convert input:\n {doc}\n to a dictionary.")
        raise TypeError("Input is not an MPDataDoc object.")
