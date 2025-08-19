import sys
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import effects_router, control_router
from app.effects.effect_loader import get_effects
from app.core.dependencies import get_truss_controller

# --- Application Setup ---

def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""

    # --- Initialize Hardware Controller ---
    # Perform initial clear of LEDs using the dependency getter
    # This implicitly calls get_truss_controller(), creating the instance.
    try:
        truss_controller = get_truss_controller()
        truss_controller.clear_all()
        print("LED Truss controller initialized and cleared.")
    except Exception as e:
        print(f"WARNING: Failed to initialize or clear LED Truss: {e}")
        # Decide if this should be fatal - for now, allow startup

    # --- Create FastAPI App ---    
    app = FastAPI(
        title="LED Truss Control API",
        description="API for controlling WS281x LED strips on a truss structure.",
        version="1.0.0",
    )

    # --- Configure Middleware ---
    # Configure CORS (Cross-Origin Resource Sharing)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Allow all origins for simplicity (adjust for production)
        allow_credentials=True,
        allow_methods=["*"], # Allow all methods
        allow_headers=["*"], # Allow all headers
    )

    # --- Include Routers ---
    print("Including API routers...")
    app.include_router(effects_router.router)
    app.include_router(control_router.router)
    print("Routers included.")

    # --- Simple request logger for debugging 422 ---
    @app.middleware("http")
    async def log_heart_rate_payload(request, call_next):
        if request.url.path == "/effects/heart-rate" and request.method == "POST":
            try:
                body = await request.body()
                print("/effects/heart-rate payload:", body.decode("utf-8"))
            except Exception as e:
                print("Failed to read request body:", e)
        response = await call_next(request)
        return response

    # --- Validation error logger ---
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        try:
            body = await request.body()
            body_text = body.decode("utf-8")
        except Exception:
            body_text = "<unavailable>"
        print("Validation error on", request.url.path, "errors=", exc.errors(), "body=", body_text)
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    # --- Root and General Endpoints ---
    @app.get("/", tags=["General"])
    def read_root():
        """Root endpoint, returns a simple greeting."""
        return {"message": "Welcome to the LED Truss Control API"}

    @app.get("/effects", tags=["General"])
    def get_effects_metadata():
        """Returns the metadata for all available effects.
        
        Loads the effects map from JSON on the first call.
        Raises relevant errors if loading fails.
        """
        try:
            # get_effects handles loading/caching
            return get_effects()
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            # If map loading fails on request, return an error response
            raise HTTPException(status_code=500, detail=f"Failed to load effects map: {e}")
        except Exception as e:
            # Catch any other unexpected errors during map loading
             raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    print("FastAPI app creation complete.")
    return app

# Create the app instance when this module is loaded
app = create_app() 