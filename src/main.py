from funcs.xmpp_message_handlers import CIR_message_handler, RO_message_handler, presence_handler
from xmpp_client_module import SLIClientModule
from read_config import cfg, Logger
import sys
import asyncio

handlers_dict = {"cir": CIR_message_handler, "ro": RO_message_handler}
message_handler_func = handlers_dict[cfg.client_type.lower()]

jid = "ciao@testingsaslrse"  # ciao@testingsaslrse devcir@testingrse
pwd = "devcir"
certfile = cfg.cert_folder + "\\public.crt"
keyfile = cfg.cert_folder + "\\private.key"
ca_certs = cfg.cert_folder + "\\caserver.pem"

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if message_handler_func is not None:
    try:
        xmpp_client = SLIClientModule(
            jid=jid,
            password=pwd,
            sasl_mech="EXTERNAL",
            message_handler=CIR_message_handler,
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
    except Exception as e:
        Logger.info(f"Failed xmpp module creation. Error: {e}")

else:
    Logger.error(f"Failed to istantiate xmpp client! Wrong configuration settings for client type: {cfg.client_type}")
    raise SystemError


xmpp_client.connect(address=(cfg.server_host, cfg.server_port))
xmpp_client.process()
