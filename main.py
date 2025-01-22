import os
import redis
import fastapi
import uvicorn
import logging
import datetime
from routes import *
from fastapi.middleware.cors import CORSMiddleware
from helpers import RemovePyExtensionFilter

app = fastapi.FastAPI()
app.include_router(spotify_router)
#TODO: Include all other routers
init_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#TODO: Add ratelimit service

stream_handler = logging.StreamHandler()
stream_handler.addFilter(RemovePyExtensionFilter())
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s.%(funcName)s - %(levelname)s - %(message)s",
    handlers=[stream_handler],
)
logger = logging.getLogger(__name__)

@app.get("/health")
def health(request: fastapi.Request):
    logger.info(f"Health check invoked by {request.client.host}")
    return fastapi.responses.JSONResponse(content={"status": "OK", "up_since": init_time}, status_code=200)

if __name__ == "__main__": #? Used for local testing
    uvicorn.run(app, host="0.0.0.0", port=8000)