from fastapi import APIRouter
from read_config import Logger
from factory_clients import xmpp_client
import json
from slixmpp.jid import JID

router = APIRouter(
    prefix="",
    tags=["Testing"],
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Not Found"},
        500: {"description": "XMPP client error"},
    },
)


@router.post("/send_generic_xmpp")
async def send_generic_xmpp(node: str, domain: str, message: dict):

    message_body = json.dumps(message)
    Logger.info(f"Client ready to send to {node}@{domain} payload: {message_body}")
    destination = node + "@" + domain
    destination = JID(jid=destination)
    xmpp_client.send_message(mto=destination, mbody=message_body)

    return True


@router.post("/get_client_name")
async def get_client_name():

    xmpp_client_name = xmpp_client.jid
    return xmpp_client_name
