"""Miscellaneous tools for data parsing."""

import re
from typing import Dict, Optional, Tuple, Union

import pymatgen

from . import logger


def parse_spec(species: str) -> Tuple[str, int]:
    """Parse a species string into its element and charge.

    Args:
        species (str): String representation of a species in
            the format {element}{absolute_charge}{sign}.

    Returns:
        A tuple of (element, signed_charge).

    Examples:
        >>> parse_spec("Fe2+")
        ('Fe', 2)
        >>> parse_spec("O2-")
        ('O', -2)

    """
    ele, oxi_state = re.match(r"([A-Za-z]+)([0-9]*[\+\-])", species).groups()
    if oxi_state[-1] in ["+", "-"]:
        charge = (int(oxi_state[:-1]) or 1) * (-1 if "-" in oxi_state else 1)
        return ele, charge
    else:
        return ele, 0


def unparse_spec(species: Tuple[str, int]) -> str:
    """Unparse a species into a string representation.

    The analogue of :func:`parse_spec`.

    Args:
        A tuple of (element, signed_charge).

    Returns:
        String of {element}{absolute_charge}{sign}.

    Examples:
        >>> unparse_spec(("Fe", 2))
        'Fe2+'
        >>> unparse_spec(("O", -2))
        'O2-'

    """
    return f"{species[0]}{abs(species[1])}{get_sign(species[1])}"


def get_sign(charge: int) -> str:
    """Get string representation of a number's sign.

    Args:
        charge (int): The number whose sign to derive.

    Returns:
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
) -> Dict[str, Union[pymatgen.core.Structure, Optional[str]]]:
    """Converts the `MPDataDoc` object returned by a next-gen MP query to a dictionary

    Args:
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
