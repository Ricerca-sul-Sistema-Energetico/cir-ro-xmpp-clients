from fastapi import APIRouter
from read_config import Logger
from factory_clients import xmpp_client
import json

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
    sent_attempt = await xmpp_client.send_message(node=node, domain=domain, message_type="message", body=message_body)
    return sent_attempt
