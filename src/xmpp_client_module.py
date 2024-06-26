from typing import Callable
from slixmpp import ClientXMPP
import ssl
from read_config import Logger
import time


class SLIClientModule(ClientXMPP):

    def __init__(
        self,
        jid: str,
        password: str,
        sasl_mech: str,
        message_handler: Callable,
        # presence_handler: Callable,
        client_type: str,
        certfile: str | None = None,
        keyfile: str | None = None,
        ca_certs: str | None = None,
    ):
        super().__init__(jid, password, sasl_mech=sasl_mech)
        self.client_type = client_type
        self.message_handler = message_handler
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        # self.add_event_handler("presence", presence_handler)

        if sasl_mech == "EXTERNAL":
            self.ssl_version = ssl.PROTOCOL_TLSv1_2  # PROTOCOL_SSLv23
            self.ssl_context = ssl.create_default_context(
                ssl.Purpose.SERVER_AUTH
            )  # ssl.Purpose.CLIENT_AUTH cafile=ca_certs
            self.ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
            self.ssl_context.load_verify_locations(cafile=ca_certs)

        else:
            self.ssl_context = ssl._create_unverified_context()

    async def start(self, event):
        Logger.info("Ready to send inital presence")
        self.send_presence()
        await self.get_roster()

    def message(self, msg):
        self.message_handler(self, msg)

    # def start_client_module(self):
    #     Logger.info("Starting the client ...")
    #     while True:
    #         try:
    #             self.process()
    #             if self.is_connected():
    #                 while self.is_connected():
    #                     Logger.info(f"Client connected. Connecion status: {self.is_connected()}. Ready to listen ...")
    #                     self.process()
    #                 Logger.info("Connection lost")
    #             Logger.info(f"Client connection status: {self.is_connected()}")
    #             time.sleep(5)
    #         except Exception as e:
    #             Logger.info(f"Caught exception! \n {e}")
