from fastapi import FastAPI
from api_routers import send_measures, send_commands
from read_config import Logger
from factory_clients import xmpp_client
import threading
import uvicorn

app = FastAPI(
    title="XMPP bidirectional client",
    description=""" Rest-API backend for simulating a XMPP client according to CEI 0-21 Annex X perscriptions""",
    version="Florencio",
)

if xmpp_client.client_type == "cir":
    app.include_router(send_measures.router)

if xmpp_client.client_type == "ro":
    app.include_router(send_commands.router)

if __name__ == "__main__":
    threading.Thread(target=xmpp_client.start_client_module).start()
    Logger.info("running uvicorn programmatically - DEBUG mode only")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=False,
        lifespan="on",
    )
