from fastapi import APIRouter
from read_config import Logger
from factory_clients import xmpp_client


router = APIRouter(
    prefix="",
    tags=["Server Connections"],
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Not Found"},
        500: {"description": "XMPP client error"},
    },
)


@router.get("/get_connection_status")
async def get_connection():

    connection_status = xmpp_client.client.isConnected()
    return connection_status


@router.post("/connect_to_server")
async def connect_to_server():
    Logger.info("Connecting Client ...")
    try:
        connection_result = xmpp_client.connect_to_server()
        Logger.info(f"Client connection status: {xmpp_client.client.isConnected()}")
        callbacks = xmpp_client.register_callbacks()
    except Exception as e:
        Logger.info(f"Exception during connection attempt: {e}")
        Logger.info(f"Trying reconnect and reauth ...")
        connection_result = xmpp_client.client.reconnectAndReauth()
    return connection_result


@router.post("/disconnect_from_server")
async def disconnect_from_server():
    disconnection_result = xmpp_client.client.disconnect()
    return disconnection_result
