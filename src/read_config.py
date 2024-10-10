import logging
from collections import namedtuple
from dotenv import dotenv_values

logging.basicConfig(level="DEBUG", format="%(levelname)-8s %(message)s")

Cfg_pjt = namedtuple(
    "Cfg",
    [
        "fastapi",
        "fastapi_port",
        "log_level",
        "client_type",
        "cert_folder",
        "jid_ro",
        "jid_cir",
        "mqtt",
        "mqtt_usr"
        ],
)  # just the name of the namedtuple object


Cfg_xmpp = namedtuple(
    "Cfg",
    [
        "node",
        "domain",
        "pwd",
        "server_host",
        "server_port",
        "authorized_clients",
    ],
)  # just the name of the namedtuple object

Cfg_mqtt = namedtuple(
    "Cfg",
    [
        'mqtt_host',
        'mqtt_port',
        'mqtt_username',
        'mqtt_password',
        'mqtt_qos',
    ],
)  # just the name of the namedtuple object



def get_cfg_pjt():
    """return a config namedtuple from the .env values"""
    dv: dict = dotenv_values(".env.project")
    return Cfg_pjt(
        fastapi=dv.get("fastapi", False),
        fastapi_port = int(dv.get("fastapi_port", 8001)),
        cert_folder=dv.get("cert_folder", "certs"),
        jid_ro=dv.get("jid_ro"),
        jid_cir=dv.get("jid_cir"),
        log_level=dv.get("log_level", "INFO"),
        client_type=dv.get("client_type", "cir"),
        mqtt=dv.get("mqtt", False),
        mqtt_usr = dv.get('mqtt_usr')
    )

def get_cfg_xmpp():
    """return a config namedtuple from the .env values"""
    dv: dict = dotenv_values(".env.xmpp")
    return Cfg_xmpp(
        node=dv.get("node", "cir"),
        domain=dv.get("domain", "cirexample"),
        pwd=dv.get("password", "cir-rse"),
        server_host=dv.get("server_host", "172.25.102.139"),
        server_port=dv.get("server_port", 5222),
        authorized_clients=dv.get("authorized_clients", []),
    )

def get_cfg_mqtt():
    """return a config namedtuple from the .env values"""
    dv: dict = dotenv_values(".env.mqtt")
    return Cfg_mqtt(
        mqtt_host = dv.get('mqtt_host', '0.0.0.0'),
        mqtt_port = int(dv.get('mqtt_port', 1883)),
        mqtt_username= dv.get('mqtt_username'),
        mqtt_password=  dv.get('mqtt_password'),
        mqtt_qos = int(dv.get('mqtt_qos', 1)),

    )


def get_logger(logger_name: str, level: str = "DEBUG"):
    """
    :param logger_name: the name of the module (or method) where the logger was executed
    :param level: the logger level
    :return: the logger object
    """
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler()  # handler for output messages on stdout
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


cfg_pjt = get_cfg_pjt()
cfg_xmpp = get_cfg_xmpp()
cfg_mqtt = get_cfg_mqtt()

Logger = get_logger(logger_name="APP Logger", level=cfg_pjt.log_level)
