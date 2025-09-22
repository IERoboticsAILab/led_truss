"""Dependency container for the shared LED truss controller instance.

The application uses a single controller for its entire lifetime so that
all requests operate on the same hardware state and effect thread.
"""

from .truss import truss

# Create a single instance of the truss controller for the application lifetime.
_truss_controller_instance = truss()

def get_truss_controller() -> truss:
    """Return the shared truss controller instance.

    This is intended to be used as a FastAPI dependency.
    """
    return _truss_controller_instance