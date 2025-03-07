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

    connection_status = xmpp_client.is_connected()
    return connection_status


@router.post("/disconnect_from_server")
async def disconnect_from_server():
    disconnection_result = xmpp_client.disconnect()
    return disconnection_result
