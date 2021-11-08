"""
This module provides utility functions.
"""

from __future__ import annotations

from abc import ABC
from typing import Dict, Any, List


class JSON(ABC):
    """
    Provides utility functions for json.
    """

    @classmethod
    def deepsort(cls, obj: Dict[str, Any] | List[Any]) -> List[Any]:
        """
        Recursively sort the given json.
        In particular it sorts any list it finds in the json, and converts dicts to lists of (key, value) pairs in order
        to make them orderable.

        :param obj: the json
        :return: the sorted json in format of a list of (key, value) pairs
        """
        if isinstance(obj, dict):
            return sorted((k, cls.deepsort(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(cls.deepsort(x) for x in obj)
        else:
            return obj
