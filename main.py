from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import monstro as monstro_router
import logging
from api.utils.logging_tools import SensitiveDataFilter, ColoredFormatter
from api.utils.setup_logging import setup_logging

app = FastAPI()
app.include_router(router=monstro_router)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# https://redirect.processfinger.com/lk/monstro_api.php?password=FL79HgVg220930

setup_logging()

logger = logging.getLogger('my_app')


@app.get("/{name}")
async def root(name):
    return f"Hello, {name}"



@app.get("/")
async def root():
    return f"This is test api for control Monstro projects"


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Start the application")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
   
