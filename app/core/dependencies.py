from .truss import truss

# Create a single instance of the truss controller for the application lifetime.
# This ensures all requests interact with the same hardware controller state.
_truss_controller_instance = truss()

def get_truss_controller() -> truss:
    """FastAPI dependency function that returns the shared truss controller instance."""
    return _truss_controller_instance 