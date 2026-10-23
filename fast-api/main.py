from fastapi import FastAPI
from routers import arrays_hashing

app = FastAPI(
    title="NeetCode API Solvers",
    description="Endpoints distributed by algorithm categories",
    version="1.0.0"
)
app.include_router(arrays_hashing.router)

@app.get("/")
def root():
    return {"message": "Welcome to Neetcode API"}
