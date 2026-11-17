from fastapi import FastAPI
import models
from database import engine
from router import auth, transactions


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="Personal income & expense tracker with JWT authentication.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(transactions.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Expense Tracker API is running..."}
