from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    def __lt__(self, other: Mountain) -> bool:
        """
        Magic method to compare between Mountains using "<" or ">"
        Complexity: O(1)
        """
        if self.length < other.length:
            return True
        elif self.length == other.length:
            return self.name < other.name
        return False
    
    def __le__(self, other: Mountain) -> bool:
        """
        Magic method to compare between Mountains using "<=" or ">="
        Complexity: O(1)
        """
        if self.length <= other.length:
            return True
        elif self.length == other.length:
            return self.name <= other.name
        return False
    
    def __eq__(self, other: Mountain) -> bool:
        """
        Magic method to compare between Mountains using "=="
        Complexity: O(1)
        """
        return self.length == other.length and self.name == other.name