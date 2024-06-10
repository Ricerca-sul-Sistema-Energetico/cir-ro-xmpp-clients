from funcs.message_handlers import handle_presences
from typing import List, Callable
from read_config import Logger
import time
import traceback
import xmpp


class xmppClientModule:

    def __init__(
        self,
        node: str,
        domain: str,
        password: str,
        server_ip: str,
        server_port: int,
        client_type: str,
        messages_handlers: Callable,
        authorized_jids: List[str],
    ):

        self.jid = xmpp.protocol.JID(node=node, domain=domain)
        self.password = password
        self.server_ip = server_ip
        self.server_port = server_port
        self.client = xmpp.Client(self.jid.getDomain(), debug=[])
        self.authorized_jids = authorized_jids
        self.client_type = client_type
        self.message_callback = messages_handlers

    def connect_to_server(self) -> bool:

        connection = self.client.connect(server=(self.server_ip, self.server_port))
        authentication = self.client.auth(self.jid.getNode(), self.password)  # , resource="TestBot"
        if not connection:
            return False
        if not authentication:
            return False
        Logger.info(f"Connection: {connection} \n authentication: {authentication}")
        return True

    def assign_authorized_jids(self, new_auth_jids: List[str]):
        self.authorized_jids += new_auth_jids

    def start_listening(self):
        if self.client is not None:
            # Register the message handler which is used to respond to messages from the authorized contacts.
            # message_callback = handle_RO_messages()
            self.client.RegisterHandler("message", self.message_callback)

            # Register the presence handler which is used to automatically authorize presence-subscription requests from authorized contacts.
            presence_callback = handle_presences(jids=self.authorized_jids)
            self.client.RegisterHandler("presence", presence_callback)

            # Go "online".
            self.client.sendInitPresence()
            self.client.Process()

            while self.client.isConnected():
                self.client.Process()
                time.sleep(1)

    async def send_message(
        self, node: str | None = None, domain: str | None = None, message_type: str | None = None, body: str = ""
    ):

        if node is not None and domain is not None:
            jid_destinatario = xmpp.protocol.JID(node=node, domain=domain)
        else:
            Logger.error(
                f"Tried sending message without specifying destination node and domain \n Node: {node}; Domain: {domain}"
            )
            jid_destinatario = None

        if jid_destinatario is not None:
            try:
                message = xmpp.protocol.Message(
                    to=jid_destinatario, body=body, typ=message_type
                )  # Tipo di messaggio (chat)
                self.client.send(message)
                return True
            except Exception as e:
                Logger.error(
                    f"Error while sending message to node: {node}, domain: {domain}, Message_type: {message_type}\n Error: {e}"
                )
        return False

    def start_client_module(self):
        while True:
            try:
                Logger.info("Beginning listening ...")
                self.start_listening()
                Logger.info("Not connected - attempting reconnect in a moment.")
                reconnection = self.connect_to_server()
                if not reconnection:
                    raise ConnectionError
            except ConnectionError:
                Logger.info("Could not reconnect after disconnection")
            except Exception as e:
                Logger.info(f"Caught exception! \n {e}")
                traceback.print_exc()


# import asyncio
# import logging

# from slixmpp.clientxmpp import ClientXMPP


# class EchoBot(ClientXMPP):

#     def __init__(self, jid, password):
#         ClientXMPP.__init__(self, jid, password)

#         self.add_event_handler("session_start", self.session_start)
#         self.add_event_handler("message", self.message)

#         # If you wanted more functionality, here's how to register plugins:
#         # self.register_plugin('xep_0030') # Service Discovery
#         # self.register_plugin('xep_0199') # XMPP Ping

#         # Here's how to access plugins once you've registered them:
#         # self['xep_0030'].add_feature('echo_demo')

#     def session_start(self, event):
#         self.send_presence()
#         self.get_roster()

#         # Most get_*/set_* methods from plugins use Iq stanzas, which
#         # are sent asynchronously. You can almost always provide a
#         # callback that will be executed when the reply is received.

#     def message(self, msg):
#         if msg["type"] in ("chat", "normal"):
#             msg.reply("Thanks for sending\n%(body)s" % msg).send()


# if __name__ == "__main__":
#     # Ideally use optparse or argparse to get JID,
#     # password, and log level.

#     logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")

#     xmpp = EchoBot("somejid@example.com", "use_getpass")
#     xmpp.connect()
#     xmpp.process()
