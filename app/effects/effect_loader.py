import json
import os
from typing import Dict, Any
from pathlib import Path

_effects_map = None

def load_effects_map():
    global _effects_map
    if _effects_map is None:
        # Assume effects_map.json is in the root directory relative to the 'app' directory
        # Adjust this path if your project structure is different
        project_root = Path(__file__).parent.parent.parent
        effects_file = project_root / 'effects_map.json'

        if not effects_file.exists():
            raise FileNotFoundError(f"Effects map not found at {effects_file}")

        try:
            with open(effects_file) as f:
                _effects_map = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Failed to parse effects map: {str(e)}",
                e.doc,
                e.pos
            )
    return _effects_map

def get_effects() -> Dict[str, Any]:
    """Return the loaded effects map. Loads it if not already loaded."""
    return load_effects_map() 