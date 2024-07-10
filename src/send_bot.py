from read_config import cfg, Logger
from slixmpp import ClientXMPP
import ssl
import sys
import asyncio
import logging
import json

jid = "ciao@testingsaslrse"  # ciao@testingsaslrse devcir@testingrse
pwd = "devcir"
certfile = cfg.cert_folder + "\\public.crt"
keyfile = cfg.cert_folder + "\\private.key"
ca_certs = cfg.cert_folder + "\\caserver.pem"
reciever = cfg.reciever

with open(f"json_examples_new\\{cfg.sending_message}.json", "r") as message:
    message_body = json.load(message)

logging.basicConfig(level="DEBUG", format="%(levelname)-8s %(message)s")


class SendBot(ClientXMPP):

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
        self.send_presence()
        await self.get_roster()

        self.send_message(mto=reciever, mbody=json.dumps(message_body))
        self.disconnect()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    xmpp = SendBot(jid=jid, password=pwd, sasl_mech="EXTERNAL", certfile=certfile, keyfile=keyfile, ca_certs=ca_certs)

    xmpp.register_plugin("xep_0030")  # Service Discovery
    xmpp.register_plugin("xep_0199")  # Ping
    xmpp.register_plugin("xep_0257")
    xmpp.register_plugin("xep_0115")  # Scram-sha-1

    # Questa va nella api di connessione
    xmpp.connect(address=(cfg.server_host, cfg.server_port))
    # Mongoose: 172.25.102.182 Prosody:172.25.100.144 / rse-testing-xmpp-server.rse-web.it
    xmpp.process()
