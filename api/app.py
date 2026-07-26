from fastapi import FastAPI

app = FastAPI(
    title="CodePulse",
    description="Code quality monitoring platform",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "CodePulse is running!"}

@app.get("/health")
async def health():
    return {"status": "ok"}