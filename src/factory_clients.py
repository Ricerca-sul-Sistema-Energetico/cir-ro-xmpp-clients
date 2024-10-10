from read_config import Logger, cfg_pjt, cfg_xmpp
from xmpp_client_module import SLIClientModule
from mqtt_client_module import ROClient, CIRClient, SLIClientModuleMQTT
from funcs.xmpp_message_handlers import CIR_message_handler, RO_message_handler, presence_handler
import asyncio
import sys
import os               # To ensure compatibility with both Windows and Linux 

handlers_dict = {"cir": CIR_message_handler, "ro": RO_message_handler}
message_handler_func = handlers_dict[cfg_pjt.client_type.lower()]

jid = "ciao@testingsaslrse" #ciao@testingsaslrse devcir@testingrse
pwd = "devcir"
certfile = os.path.join(cfg_pjt.cert_folder, "public.crt")
keyfile = os.path.join(cfg_pjt.cert_folder, "private.key")
ca_certs = os.path.join(cfg_pjt.cert_folder, "caserver.pem")


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if message_handler_func is not None:
    try:
        xmpp_client = SLIClientModule(
            jid=jid,
            password=pwd,
            sasl_mech="EXTERNAL",
            message_handler=message_handler_func,
            # presence_handler=presence_handler,
            client_type= cfg_pjt.client_type.lower(),
            certfile=certfile,
            keyfile=keyfile,
            ca_certs=ca_certs,
        )

        xmpp_client.register_plugin("xep_0030")  # Service Discovery
        xmpp_client.register_plugin("xep_0199")  # Ping
        xmpp_client.register_plugin("xep_0257")
        xmpp_client.register_plugin("xep_0115")  # Scram-sha-1
        xmpp_client.connect(address=(cfg_xmpp.server_host, cfg_xmpp.server_port))
        
    
    except Exception as e:
        Logger.info(f"Failed xmpp module creation. Error: {e}")

else:
    Logger.error(f"Failed to istantiate xmpp client! Wrong configuration settings for client type: {cfg_pjt.client_type}")
    raise SystemError


class ClientFactory:
    @staticmethod
    def create_clients(client_type: str):
        xmpp_client = ClientFactory.create_xmpp_client(client_type)
        mqtt_client = ClientFactory.create_mqtt_client(client_type)
        client_base = SLIClientModuleMQTT(xmpp_client)  # Estende l'istanza xmpp_client
        xmpp_client.message_handler = client_base.extend_message_handler(xmpp_client.message_handler)  # Applica il decoratore
        return xmpp_client, mqtt_client

    @staticmethod
    def create_xmpp_client(client_type: str):
        return xmpp_client

    @staticmethod
    def create_mqtt_client(client_type: str):
        if client_type == "cir":
            return CIRClient()
        elif client_type == "ro":
            return ROClient()
        else:
            raise ValueError(f"Unknown client type: {client_type}")
