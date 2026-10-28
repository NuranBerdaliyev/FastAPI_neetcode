from fastapi import FastAPI
from pydantic import BaseModel, Field
from routers import arrays_hashing, two_pointers

app = FastAPI(
    title="NeetCode API Solvers",
    description="Endpoints distributed by algorithm categories",
    version="1.0.0"
)
all_modules=[arrays_hashing, two_pointers]

for module in all_modules:
    app.include_router(module.router)

class RootOutput(BaseModel):
    message: str = Field(..., description="Intro message", examples=["Welcome to Neetcode API"])
@app.get("/", response_model=RootOutput)
def root():
    return RootOutput(
        message="Welcome to Neetcode API"
    )
