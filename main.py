from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from db.db_helper import create_tables, drop_tables
from referral_codes.router import router as refcodes_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan, title="Referral Codes API", )
app.include_router(refcodes_router)

# Using FastAPI instance
@app.get("/")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)