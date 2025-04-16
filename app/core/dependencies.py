from .truss import truss

# Create a single instance of the truss controller for the application
_truss_controller_instance = truss()

def get_truss_controller():
    """Dependency function to get the shared truss controller instance."""
    return _truss_controller_instance 