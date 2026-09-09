from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import pages, webhooks

app = FastAPI(title="Acme API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pages.router)
app.include_router(webhooks.router)

@app.get("/health")
async def health():
    return "OK"

@app.get("/cron/keep-alive")
async def keep_alive():
    return "OK"
