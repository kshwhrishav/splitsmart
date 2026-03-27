from fastapi import FastAPI
from app.routes.users import router as users_router
from app.routes.groups import router as groups_router

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(users_router)
app.include_router(groups_router)