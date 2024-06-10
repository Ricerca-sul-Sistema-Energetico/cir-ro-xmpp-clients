import sys
import asyncio
import logging
from slixmpp import ClientXMPP
from slixmpp.jid import JID
import ssl
import os

"""Here we will create out echo bot class"""


class EchoBot(ClientXMPP):

    def __init__(
        self,
        jid: str,
        password: str,
        sasl_mech: str,
        certfile: str | None = None,
        keyfile: str | None = None,
        ca_certs: str | None = None,
    ):
        super().__init__(jid, password, sasl_mech=sasl_mech)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

        if sasl_mech == "EXTERNAL":
            self.ssl_version = ssl.PROTOCOL_SSLv23
            self.ssl_context = ssl.create_default_context()  # ssl.Purpose.CLIENT_AUTH cafile=ca_certs
            self.ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
            # self.ssl_context.load_verify_locations(cafile=ca_certs)

        else:
            self.ssl_context = ssl._create_unverified_context()

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

    def message(self, msg):
        sender = msg["from"]
        body = msg["body"]
        print(f"\n Arrived message from {sender}, body {body}")
        if msg["type"] in ("normal", "chat"):
            self.send_message(mto=msg["from"], mbody="Thanks for sending:\n%s" % msg["body"])


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    """Here we will configure and read command line options"""
    logging.basicConfig(level="DEBUG", format="%(levelname)-8s %(message)s")
    jid = "devro@saslprova"
    pwd = "devro"
    certfile = "src\\certs\\devro.crt"
    keyfile = "src\\certs\\devro.key"
    ca_certs = "src\\certs\\ca-certificatiutenti.crt"
    print(certfile + keyfile + ca_certs)
    """Here we will instantiate our echo bot"""
    xmpp = EchoBot(jid=jid, password=pwd, sasl_mech="EXTERNAL", certfile=certfile, keyfile=keyfile, ca_certs=ca_certs)

    xmpp.register_plugin("xep_0030")  # Service Discovery
    xmpp.register_plugin("xep_0199")  # Ping
    xmpp.register_plugin("xep_0257")
    # xmpp.register_plugin("xep_0115")  # Scram-sha-1

    """Finally, we connect the bot and start listening for messages"""

    xmpp.connect(address=("172.25.102.182", 5222))
    xmpp.process()
