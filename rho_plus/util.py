#!/usr/bin/env python3
"""General utilities."""

import re
from typing import Iterable, Union


def labelcase(text: Union[str, Iterable[str]]):
    """Converts text to a title case and adds spacing from camel case."""
    if isinstance(text, str):
        if "_" in text:
            # snake_case
            text = text.replace("_", " ")
        return re.sub(r"([^ ])([A-Z])", r"\1 \2", text).title().strip()
    else:
        return [labelcase(t) for t in text]
