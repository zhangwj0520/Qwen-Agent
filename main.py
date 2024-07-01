from fastapi import FastAPI
from typing import Union

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from examples.react_data_analysis import test


app = FastAPI(
    title="Gen UI Backend",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
    # lifespan=lifespan,
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return StreamingResponse(test(), media_type="text/event-stream")


@app.get("/api")
def read_root():
    return {"Hello": "World111"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
