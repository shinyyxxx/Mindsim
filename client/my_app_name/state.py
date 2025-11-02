import reflex as rx
import httpx
import os
from .mentalfactorsdata import MENTAL_FACTOR_DATA

class MindState(rx.State):
    """State management for mental factors."""
    mental_factors_map: dict[str, list[dict]] = {}  # mind_id -> list of factors
    available_factors: list[dict] = MENTAL_FACTOR_DATA
    active_mind_id: str = "mind_0"  # Currently selected mind
    
    @rx.var
    def mental_factors(self) -> list[dict]:
        """Get mental factors for the active mind."""
        return self.mental_factors_map.get(self.active_mind_id, [])
    
    @rx.var
    def mind_0_factors(self) -> list[dict]:
        """Get mental factors for mind 0."""
        return self.mental_factors_map.get("mind_0", [])
    
    @rx.var
    def mind_1_factors(self) -> list[dict]:
        """Get mental factors for mind 1."""
        return self.mental_factors_map.get("mind_1", [])
    
    def set_mind_0(self):
        """Set active mind to mind_0."""
        self.active_mind_id = "mind_0"
    
    def set_mind_1(self):
        """Set active mind to mind_1."""
        self.active_mind_id = "mind_1"
    
    def add_mental_factor(self, factor_name: str):
        """Add a mental factor to the active mind."""
        target_mind = self.active_mind_id
        
        # Initialize the mind if it doesn't exist
        if target_mind not in self.mental_factors_map:
            self.mental_factors_map[target_mind] = []
        
        # Check if factor is already added to this mind
        if any(f["name"] == factor_name for f in self.mental_factors_map[target_mind]):
            return
        
        factor = next((f for f in self.available_factors if f["name"] == factor_name), None)
        if factor:
            new_factor = {**factor, "position": [0, 0, 0]}
            self.mental_factors_map[target_mind] = self.mental_factors_map[target_mind] + [new_factor]