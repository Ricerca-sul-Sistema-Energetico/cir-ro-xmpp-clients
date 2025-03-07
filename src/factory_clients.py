from funcs.xmpp_message_handlers import CIR_message_handler, RO_message_handler, presence_handler
from xmpp_client_module import SLIClientModule
from models.base_modbus import ModbusModule, DeviceConfig
from read_config import xmpp_config, modbus_config, Logger

# from read_config import (
#     modbus_device_names,
#     modbus_device_hosts,
#     modbus_device_ports,
# )
import sys
import asyncio
from typing import Dict
import json

# XMPP Client creation
handlers_dict = {"cir": CIR_message_handler, "ro": RO_message_handler}
message_handler_func = handlers_dict[xmpp_config.client_type.lower()]
jid = "ciao@testingsaslrse"  # ciao@testingsaslrse devcir@testingrse
pwd = "devcir"
certfile = xmpp_config.cert_folder + "/client.crt"
keyfile = xmpp_config.cert_folder + "/private.key"
ca_certs = xmpp_config.cert_folder + "/caserver.pem"
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
            client_type=xmpp_config.client_type.lower(),
            certfile=certfile,
            keyfile=keyfile,
            ca_certs=ca_certs,
        )

        xmpp_client.register_plugin("xep_0030")  # Service Discovery
        xmpp_client.register_plugin("xep_0199")  # Ping
        xmpp_client.register_plugin("xep_0257")
        xmpp_client.register_plugin("xep_0115")  # Scram-sha-1
        xmpp_client.connect(address=(xmpp_config.server_host, xmpp_config.server_port))
    except Exception as e:
        Logger.info(f"Failed xmpp module creation. Error: {e}")

else:
    Logger.error(f"Failed to istantiate xmpp client! Wrong configuration settings for client type: {xmpp_config.client_type}")
    raise SystemError

# Modbus Client creation
modbus_device_names = modbus_config.device_list
modbus_device_hosts = modbus_config.address_list    
modbus_device_ports = modbus_config.port_list

modbus_module_dict: Dict[str, ModbusModule] = {}
for item in range(0, len(modbus_device_names)):
    try:
        device_name = modbus_device_names[item]
        host = modbus_device_hosts[item]
        port = int(modbus_device_ports[item])
        with open(f"modbus_maps/{device_name.lower()}.json", "r") as file:
            mb_device_config_dict = json.load(file)
            mb_device_config = DeviceConfig.from_json(mb_device_config_dict)
            modbus_module = ModbusModule(host=host, port=port, modbus_device=mb_device_config)
            modbus_module_dict[device_name] = modbus_module
            connection = modbus_module.connect()
            if connection:
                Logger.info(f"Successful modbus initial connection with server {device_name}")
                modbus_module.close()
            else:
                Logger.warning(f"Failed modbus initial connection with server {device_name}")
    except Exception as e:
        Logger.error(f"Could not load modbus configuration for device {device_name}. Exception occoured: {e}")
