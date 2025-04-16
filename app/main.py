from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import effects_router, control_router
from app.effects.effect_loader import load_effects_map, get_effects
from app.core.dependencies import get_truss_controller 

# Load effects map on startup
try:
    effects_map = load_effects_map()
except Exception as e:
    print(f"FATAL: Error loading effects map: {e}")
    # Consider exiting if the map is crucial
    import sys
    sys.exit(1)

# Perform initial clear using the dependency getter
get_truss_controller().clear_all()

app = FastAPI(
    title="LED Truss Control API",
    description="API for controlling WS2813 LED strips on a truss structure.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(effects_router.router)
app.include_router(control_router.router)

# Add root and effects metadata endpoints
@app.get("/", tags=["General"])
def read_root():
    return {"Hello": "World"}

@app.get("/effects", tags=["General"])
def get_effects_main():
    """Returns the metadata for all available effects."""
    return get_effects() 