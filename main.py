from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from db.database import create_tables, drop_tables
from router import router as refcodes_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    #await drop_tables()
    #print("Drop tables")
    await create_tables()
    print("Create tables")
    yield
    print("Closing connection")

app = FastAPI(lifespan=lifespan)
app.include_router(refcodes_router)
