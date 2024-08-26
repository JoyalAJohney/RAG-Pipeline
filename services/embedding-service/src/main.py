import asyncio
from fastapi import FastAPI
from .config.config import Config
from .api.routes import router
from .utils.logger import logger
from contextlib import asynccontextmanager
from .services.queue_service import process_queue

queue_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global queue_task
    logger.info("Starting background queue processing task..")
    queue_task = asyncio.create_task(process_queue())

    # Yield control back to FastAPI to start serving requests
    yield

    # Shutdown: Cancel the task when FastAPI is shutting down
    logger.info("Shutting down background queue processing task...")
    if queue_task:
        queue_task.cancel()
        try:
            await queue_task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(Config.EMBEDDING_SERVICE_PORT))