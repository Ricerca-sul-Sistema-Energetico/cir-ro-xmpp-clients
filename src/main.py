from factory_clients import ClientFactory
from read_config import cfg_pjt
from read_config import Logger
import threading
from fastapi import FastAPI
import uvicorn
from api_routers import test_apis, connections, send_measures, send_commands

def start_fastapi():
    Logger.info("Uvicorn ready to be launched")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port= cfg_pjt.fastapi_port,
        log_level="debug",
        reload=False,
        lifespan="on",
    )

if cfg_pjt.fastapi:
    app = FastAPI(
        title="XMPP bidirectional client",
        description=""" Rest-API backend for simulating a XMPP client according to CEI 0-21 Annex X perscriptions""",
        version="Florencio",
    )
    app.include_router(test_apis.router)
    app.include_router(connections.router)
    
    if cfg_pjt.client_type == "cir":
        app.include_router(send_measures.router)
        
    if cfg_pjt.client_type == "ro":
        app.include_router(send_commands.router)
        
if __name__ == "__main__":
    
    if cfg_pjt.mqtt:
        xmpp_client, mqtt_client  = ClientFactory.create_clients(cfg_pjt.client_type)
        mqtt_thread = threading.Thread(target=mqtt_client.connect)
        mqtt_thread.start()
    else:
        xmpp_client = ClientFactory.create_xmpp_client(cfg_pjt.client_type)
    
    xmpp_thread = threading.Thread(target=xmpp_client.process)
    xmpp_thread.start()
    
    if cfg_pjt.fastapi:
        start_fastapi()
