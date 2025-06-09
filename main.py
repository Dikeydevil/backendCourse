from fastapi import FastAPI, Query, Body
from typing import Optional
import uvicorn

from hotels import hotels as router_hotels
app = FastAPI()
app.include_router(router_hotels)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
