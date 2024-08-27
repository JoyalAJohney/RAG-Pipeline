import asyncio
from fastapi import FastAPI
from .config.config import Config
from .api.routes import router
from .utils.logger import logger
from contextlib import asynccontextmanager
from .services.queue_service import process_queue


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    import multiprocessing

    def run_queue_processor():
        asyncio.run(process_queue())

    # Start queue processor in a separate process
    queue_process = multiprocessing.Process(target=run_queue_processor)
    queue_process.start()

    # Start FastAPI server
    port = int(Config.EMBEDDING_SERVICE_PORT)
    logger.info(f"Starting FastAPI server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")