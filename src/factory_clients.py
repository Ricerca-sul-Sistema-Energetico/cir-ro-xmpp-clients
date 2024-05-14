from funcs.message_handlers import CIR_message_handler, RO_message_handler
from xmpp_client_module import xmppClientModule
from read_config import cfg, Logger


handlers_dict = {"cir": CIR_message_handler, "ro": RO_message_handler}
message_handler_func = handlers_dict[cfg.client_type.lower()]

if message_handler_func is not None:
    try:
        xmpp_client = xmppClientModule(
            node=cfg.node,
            domain=cfg.domain,
            password=cfg.pwd,
            server_ip=cfg.server_host,
            server_port=cfg.server_port,
            client_type=cfg.client_type.lower(),
            messages_handlers=message_handler_func,
            authorized_jids=[],
        )
        xmpp_client.assign_authorized_jids(cfg.authorized_clients)
    except Exception as e:
        Logger.info(f"Failed xmpp module creation. Error: {e}")

else:
    Logger.error(f"Failed to istantiate xmpp client! Wrong configuration settings for client type: {cfg.client_type}")
    raise SystemError
