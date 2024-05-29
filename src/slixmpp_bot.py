import sys
import asyncio
import logging
from slixmpp import ClientXMPP
import ssl


# from slixmpp.clientxmpp import ClientXMPP

"""Here we will create out echo bot class"""
sasl_external = False


class EchoBot(ClientXMPP):

    def __init__(
        self,
        jid: str,
        password: str,
        certfile: str | None = None,
        keyfile: str | None = None,
        ca_certs: str | None = None,
    ):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

        if sasl_external:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
            self.ssl_context.load_verify_locations(cafile=ca_certs)
            print(self.get_ssl_context())
            # Enable SASL EXTERNAL mechanism
            self.use_sasl = True
            self.sasl_mech = "EXTERNAL"
        else:
            self.ssl_context = ssl._create_unverified_context()

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

    def message(self, msg):
        if msg["type"] in ("normal", "chat"):
            self.send_message(mto=msg["from"], mbody="Thanks for sending:\n%s" % msg["body"])


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    """Here we will configure and read command line options"""
    logging.basicConfig(level="DEBUG", format="%(levelname)-8s %(message)s")
    jid = "elsa@saslprova"
    pwd = "elsa"
    certfile = "certs/xmppadr.crt"
    keyfile = "certs/xmppadr.key"
    ca_certs = "certs/ca.crt"
    """Here we will instantiate our echo bot"""
    xmpp = EchoBot(jid=jid, password=pwd, certfile=certfile, keyfile=keyfile, ca_certs=ca_certs)

    xmpp.register_plugin("xep_0030")  # Service Discovery
    xmpp.register_plugin("xep_0199")  # Ping

    """Finally, we connect the bot and start listening for messages"""
    xmpp.connect(address=("10.0.2.43", 5222))  # 10.0.2.43 , force_starttls=True 172.25.100.144
    xmpp.process()  # timeout=10
