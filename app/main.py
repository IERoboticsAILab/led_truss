import json
import logging
 
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import effects_router, control_router
from app.effects.effect_loader import get_effects
from app.core.dependencies import get_truss_controller


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("led_truss")

# --- Application Setup ---

def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""

    # --- Initialize Hardware Controller ---
    # Perform initial clear of LEDs using the dependency getter
    # This implicitly calls get_truss_controller(), creating the instance.
    try:
        truss_controller = get_truss_controller()
        truss_controller.clear_all()
        logger.info("LED Truss controller initialized and cleared.")
    except Exception as e:
        logger.warning("Failed to initialize or clear LED Truss: %s", e)
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
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["GET", "POST"], # Restrict to needed methods
        allow_headers=["Content-Type", "Authorization"], # Restrict to needed headers
    )

    # --- Include Routers ---
    logger.info("Including API routers...")
    app.include_router(effects_router.router)
    app.include_router(control_router.router)
    logger.info("Routers included.")

    # --- Simple request logger for debugging 422 ---
    @app.middleware("http")
    async def log_heart_rate_payload(request, call_next):
        if request.url.path == "/effects/heart-rate" and request.method == "POST":
            try:
                body = await request.body()
                logger.debug("/effects/heart-rate payload: %s", body.decode("utf-8"))
            except Exception as e:
                logger.debug("Failed to read request body: %s", e)
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
        logger.error("Validation error on %s errors=%s body=%s", request.url.path, exc.errors(), body_text)
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    # (Timer functionality removed)

    # --- Root and General Endpoints ---
    @app.get("/", tags=["General"])
    def read_root() -> dict[str, str]:
        """Root endpoint, returns a simple greeting."""
        return {"message": "Welcome to the LED Truss Control API"}

    @app.get("/health", tags=["General"])
    def health() -> dict[str, str]:
        """Simple health check endpoint."""
        return {"status": "ok"}

    @app.get("/effects", tags=["General"])
    def get_effects_metadata() -> dict:
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

    @app.on_event("shutdown")
    def on_shutdown():
        try:
            tc = get_truss_controller()
            tc.stop_effect()
            tc.clear_all()
            logger.info("Shutdown: stopped current effect and cleared LEDs.")
        except Exception as e:
            logger.warning("Shutdown cleanup error: %s", e)

    logger.info("FastAPI app creation complete.")
    return app

# Create the app instance when this module is loaded
app = create_app() 