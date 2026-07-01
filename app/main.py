"""CI/CD Demo - FastAPI Application"""

from fastapi import FastAPI

app = FastAPI(title="CI/CD Demo", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Hello, CI/CD!", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"result": a + b}


@app.get("/multiply/{a}/{b}")
def multiply(a: int, b: int):
    return {"result": a * b}
