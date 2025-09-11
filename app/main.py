from contextlib import asynccontextmanager
from redis.asyncio import Redis
from fastapi import FastAPI
import app.constants as const
from app.api.endpoints import dataset



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to Redis
    redis_client = Redis(host=const.REDIS_HOST,
                                   port=const.REDIS_PORT,
                                   db=const.REDIS_DB,
                                   decode_responses=True,
                                   encoding="UTF-8"
                                   )


    await redis_client.ping()
    app.state.redis_client = redis_client
    print("Redis connection opened")
    yield
    # Disconnect from Redis
    await app.state.redis_client.close()
    print("Redis connection closed")

app = FastAPI(lifespan=lifespan,
              title=const.PROJECT_NAME,
              version=const.VERSION)


@app.get("/")
async def read_root():
    return {"Synthetic": f"version {const.VERSION}"}

# router for forex dataset
app.include_router(dataset.router, prefix="/api/v1/forex", tags=["forex-dataset"])


