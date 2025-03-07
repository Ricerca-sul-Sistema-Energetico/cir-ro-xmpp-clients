import logging
from collections import namedtuple
from dotenv import dotenv_values

# logging.basicConfig(level="DEBUG", format="%(levelname)-8s %(message)s")

XMPPConfig = namedtuple("XMPPConfig", "log_level, node, domain, pwd, server_host, server_port, client_type, authorized_clients, cert_folder")
ModbusConfig = namedtuple("ModbusConfig", "device_list, address_list, port_list")
env_values: dict = dotenv_values(verbose=True)


def get_logger(logger_name: str, level: str = "DEBUG"):
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler()  # handler for output messages on stdout
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


xmpp_config = XMPPConfig(
    log_level=env_values.get("log_level", "INFO"),
    node=env_values.get("node", "cir"),
    domain=env_values.get("domain", "cirexample"),
    pwd=env_values.get("password", "cir-rse"),
    server_host=env_values.get("server_host", "172.25.102.139"),
    server_port=env_values.get("server_port", 5222),
    client_type=env_values.get("client_type", "cir"),
    authorized_clients=env_values.get("authorized_clients", []),
    cert_folder=env_values.get("cert_folder", "mongoose"),
)

modbus_config = ModbusConfig(
    device_list=[value for key, value in env_values.items() if key.startswith("MB_DEVICE_NAME")],
    address_list=[value for key, value in env_values.items() if key.startswith("MB_DEVICE_HOST")],
    port_list=[value for key, value in env_values.items() if key.startswith("MB_DEVICE_PORT")],
)

Logger = get_logger(logger_name="Managed Logger", level=xmpp_config.log_level)
