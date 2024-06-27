import logging
from collections import namedtuple
from dotenv import dotenv_values

logging.basicConfig(level="DEBUG", format="%(levelname)-8s %(message)s")

Cfg = namedtuple(
    "Cfg",
    [
        "log_level",
        "node",
        "domain",
        "pwd",
        "server_host",
        "server_port",
        "client_type",
        "authorized_clients",
        "cert_folder",
    ],
)  # just the name of the namedtuple object


def get_cfg():
    """return a config namedtuple from the .env values"""
    dv: dict = dotenv_values(verbose=True)
    return Cfg(
        log_level=dv.get("log_level", "INFO"),
        node=dv.get("node", "cir"),
        domain=dv.get("domain", "cirexample"),
        pwd=dv.get("password", "cir-rse"),
        server_host=dv.get("server_host", "172.25.102.139"),
        server_port=dv.get("server_port", 5222),
        client_type=dv.get("client_type", "cir"),
        authorized_clients=dv.get("authorized_clients", []),
        cert_folder=dv.get("cert_folder", "mongoose"),
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


cfg = get_cfg()
Logger = get_logger(logger_name="APP Logger", level=cfg.log_level)
