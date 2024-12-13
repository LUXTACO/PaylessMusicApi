import fastapi
import uvicorn
import logging
import datetime
from routes import *
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()
init_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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