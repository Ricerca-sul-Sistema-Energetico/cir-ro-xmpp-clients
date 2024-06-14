from funcs.xmpp_message_handlers import CIR_message_handler, RO_message_handler, presence_handler
from xmpp_client_module import SLIClientModule
from read_config import cfg, Logger


handlers_dict = {"cir": CIR_message_handler, "ro": RO_message_handler}
message_handler_func = handlers_dict[cfg.client_type.lower()]

jid = "elsa@localhost"
pwd = "elsa"
certfile = "certs\\pier_prosody.pem"
keyfile = "certs\\pier_prosody.key"
ca_certs = "certs\\caserver.pem"


if message_handler_func is not None:
    xmpp_client = SLIClientModule(
        jid=jid,
        password=pwd,
        sasl_mech="EXTERNAL",
        message_hanler=message_handler_func,
        presence_handler=presence_handler,
        client_type=cfg.client_type.lower(),
        certfile=certfile,
        keyfile=keyfile,
        ca_certs=ca_certs,
    )

    xmpp_client.register_plugin("xep_0030")  # Service Discovery
    xmpp_client.register_plugin("xep_0199")  # Ping
    xmpp_client.register_plugin("xep_0257")
    xmpp_client.register_plugin("xep_0115")  # Scram-sha-1

    xmpp_client.connect(address=(cfg.server_host, cfg.server_port))
    Logger.info(f"Client connection: {xmpp_client.is_connected()}")

else:
    Logger.error(f"Failed to istantiate xmpp client! Wrong configuration settings for client type: {cfg.client_type}")
    raise SystemError
