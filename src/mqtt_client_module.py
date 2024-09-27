import paho.mqtt.client as mqtt
import json
import uuid
import time
import threading
import asyncio
from functools import wraps
from read_config import Logger, cfg_pjt, cfg_xmpp, cfg_mqtt
from data_models.cir_ro_message import CyclicMeasure, CommandLimitPowerDuration, CirRoMessage
from data_models.data_object import DataObjectMeasure
from enums.project_enums import CyclicEnums


# Classe per gestire l'accumulo dei dati MQTT e l'invio del messaggio XMPP
class CyclicMeasureManager:
    def __init__(self):
        self.received_data = {}
        self.lock = threading.Lock()  # Lock per gestire accesso concorrente

    # Metodo per processare ogni messaggio MQTT
    def process_mqtt_message(self, mqtt_key: str, data: dict):
        with self.lock:
            # Aggiungi il messaggio ricevuto al dizionario
            self.received_data[mqtt_key] = data
            print(f"Received {mqtt_key}: {data}")

            # Verifica se abbiamo ricevuto tutti i valori necessari
            if self.is_complete():
                self.send_xmpp_message()

    # Metodo per verificare se tutti i dati sono stati ricevuti
    def is_complete(self):
        # Controlla se abbiamo tutti i 4 valori
        #required_keys = {CyclicEnums.PWR_CSI.value, CyclicEnums.PWR_M1.value, CyclicEnums.PWR_M2.value, CyclicEnums.PWR_AV.value}
        required_keys = {'CSI', 'M1','M2','MX1'}
        return required_keys.issubset(self.received_data.keys())

    # Metodo per inviare il messaggio XMPP
    def send_xmpp_message(self):
        from api_routers.send_measures import send_cyclic_measure
        
        # Crea l'oggetto CyclicMeasure
        pwr_csi = DataObjectMeasure(Value= int(self.received_data["CSI"]["value"]), Invalidity=0, ErrorCode=0, Timetag= int(self.received_data["CSI"]["timestamp"]))
        pwr_m1  = DataObjectMeasure(Value= int(self.received_data["M1"]["value"]), Invalidity=1, ErrorCode=1, Timetag=int(self.received_data["M1"]["timestamp"]))
        pwr_m2  = DataObjectMeasure(Value= int(self.received_data["M2"]["value"]), Invalidity=1, ErrorCode=2, Timetag=int(self.received_data["M2"]["timestamp"]))
        pwr_av  = DataObjectMeasure(Value= int(self.received_data["MX1"]["value"]), Invalidity=1, ErrorCode=3, Timetag=int(self.received_data["MX1"]["timestamp"]))

        # Crea il dizionario che rappresenta i dati
        data = {
            CyclicEnums.PWR_CSI.value:  pwr_csi,
            CyclicEnums.PWR_M1.value:   pwr_m1,
            CyclicEnums.PWR_M2.value:   pwr_m2,
            CyclicEnums.PWR_AV.value:   pwr_av
        }
        
        cyclic_measure = CyclicMeasure(
            UUID=uuid.uuid4(),
            Timetag=int(time.time()),
            Data= data
        )
        
        # Invia il messaggio tramite XMPP
        Logger.debug(f"MQTT message: {cyclic_measure.json()}")
        #print(f"Sending XMPP message: {cyclic_measure.json()}")
        
        asyncio.run(send_cyclic_measure(node=cfg_pjt.jid_ro, domain=cfg_xmpp.domain, data_unit=cyclic_measure))
        
        # Resetta i dati dopo l'invio
        self.received_data.clear()

class MeasureManager:
    def __init__(self):
        self.received_data = {}
        self.lock = threading.Lock()  # Aggiungi il lock
    
    # Metodo per processare messaggio MQTT
    def process_mqtt_message(self, data: dict):
        
        # Salva dati ricevuti via mqtt
        with self.lock:
            if data["data"]:
                self.received_data = data["data"]
        
            # Verifica se abbiamo ricevuto tutti i valori necessari
            if self.is_complete():
                print(f"Received data: {data}")
                Logger.debug(f"Received data: {data}")
                self.send_xmpp_message()
            else:
                print("Wrong received MQTT message")
                Logger.error(f"MQTT message is wrong: {data}")

    # Metodo per verificare se tutti i dati sono stati ricevuti
    def is_complete(self):
        # Controlla se abbiamo i due campi "data" e "timestamp" e tutti i 4 valori
        required_keys = {'CSI', 'M1','M2','CSIStp'}
        return required_keys.issubset(self.received_data.keys())
    
    # Metodo per inviare il messaggio XMPP
    def send_xmpp_message(self):
        from api_routers.send_measures import send_cyclic_measure
        
        # Crea l'oggetto CyclicMeasure
        pwr_csi = DataObjectMeasure(Value= int(self.received_data["CSI"]["value"]), Invalidity=0, ErrorCode=0, Timetag= int(self.received_data["CSI"]["timestamp"]))
        pwr_m1  = DataObjectMeasure(Value= int(self.received_data["M1"]["value"]), Invalidity=1, ErrorCode=1, Timetag=int(self.received_data["M1"]["timestamp"]))
        pwr_m2  = DataObjectMeasure(Value= int(self.received_data["M2"]["value"]), Invalidity=1, ErrorCode=2, Timetag=int(self.received_data["M2"]["timestamp"]))
        pwr_av  = DataObjectMeasure(Value= int(self.received_data["CSIStp"]["value"]), Invalidity=1, ErrorCode=3, Timetag=int(self.received_data["CSIStp"]["timestamp"]))

        # Crea il dizionario che rappresenta i dati
        data = {
            CyclicEnums.PWR_CSI.value:  pwr_csi,
            CyclicEnums.PWR_M1.value:   pwr_m1,
            CyclicEnums.PWR_M2.value:   pwr_m2,
            CyclicEnums.PWR_AV.value:   pwr_av
        }
        
        cyclic_measure = CyclicMeasure(
            UUID=uuid.uuid4(),
            Timetag=int(time.time()),
            Data= data
        )
        
        # Invia il messaggio tramite XMPP
        Logger.debug(f"MQTT message: {cyclic_measure.json()}")
        #print(f"Sending XMPP message: {cyclic_measure.json()}")
        
        asyncio.run(send_cyclic_measure(node=cfg_pjt.jid_ro, domain=cfg_xmpp.domain, data_unit=cyclic_measure)) 
        
        # Resetta i dati dopo l'invio
        self.received_data.clear()


class MQTTClientBase:
    def __init__(self, client_id):
        self.client_id = client_id
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = self.on_connect

    def connect(self):
        self.client.username_pw_set(username=cfg_mqtt.mqtt_username, password=cfg_mqtt.mqtt_password)
        self.client.connect(cfg_mqtt.mqtt_host, port=cfg_mqtt.mqtt_port, keepalive=60)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected {self.client_id} with code {rc}")
        else:
            print(f"Bad connection for {self.client_id}. Code {rc}")
            


# Classe base per il client MQTT
class ClientMQTTsub(MQTTClientBase):
    def __init__(self, client_id, topic_list):
        super().__init__(client_id)
        self.topic_list = topic_list
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        for topic in self.topic_list:
            client.subscribe(topic, qos=cfg_mqtt.mqtt_qos)
            print(f"{self.client_id} subscribed to {topic}")

    def on_message(self, client, userdata, msg):
        message_str = msg.payload.decode("utf-8")
        message = json.loads(message_str)
        print(f"{self.client_id} received message from {msg.topic}: {message}")
        self.process_message(msg)

    def process_message(self, message):
        # Implementa la logica di gestione del messaggio per ogni client
        raise NotImplementedError
    
    
# Classe base per il client MQTT publisher
class ClientMQTTpub(MQTTClientBase):
    def __init__(self, client_id):
        super().__init__(client_id)
        self.client.on_publish = self.on_publish
        
    def on_publish(self, client, userdata, mid):
        print(f"Message published by {self.client_id}")
        
    def publish_message(self, topic, payload):
        qos=0
        retain=False
        
        self.client.publish(topic, payload, qos, retain)
        self.client.disconnect()
    
    def disconnect(self):
        # Disconnetti il client MQTT
        self.client.disconnect()
                    
            
# Client specifico per CIR
class CIRClient(ClientMQTTsub):
    def __init__(self):
        #topics = [f"{user}/load/+"]
        topics = [f"{cfg_pjt.mqtt_usr}/ems/cir"]  
        super().__init__(client_id=f"CIRClient_{cfg_pjt.mqtt_usr}", topic_list=topics)
        self.measure_manager = MeasureManager()
        #self.measure_manager = CyclicMeasureManager()
    def process_message(self, msg):
        # Logica per gestire i messaggi CIR
        message_str = msg.payload.decode("utf-8")
        message = json.loads(message_str)
        
        # Processa il messaggio:
        #mqtt_key = "porfa"
        #self.measure_manager.process_mqtt_message(mqtt_key, message)
        self.measure_manager.process_mqtt_message(message)


# Client specifico per RO
class ROClient(ClientMQTTsub):
    def __init__(self):
        topics = [f"ro/{cfg_pjt.mqtt_usr}/flexibility_service"] # sarebbe da tenere solo  ro/{user_id}/flexibility_service  
        super().__init__(client_id=f"ROClient_{cfg_pjt.mqtt_usr}", topic_list=topics)
        
    def process_message(self, msg):
        from api_routers.send_commands import send_limit_pwr_duration
        # Logica specifica per i messaggi RO
        message_str = msg.payload.decode("utf-8")
        message = json.loads(message_str)
        # print(f"ROClient processing message: {message}")
        Logger.debug(f"MQTT message: {message}")
         
        # PowerLimitDuration
        pwr_limit = CommandLimitPowerDuration(UUID=uuid.uuid4(),
                                            Timetag=int(message["timestamp"]),
                                            MaximumPower=int(message["flexibility"]["power"]),
                                            Duration=int(message["flexibility"]["duration"] ))

        """Verificare se e come inserire il nodo da file env o configurazione"""
        asyncio.run(send_limit_pwr_duration(node=cfg_pjt.jid_cir, domain=cfg_xmpp.domain, data_unit=pwr_limit))
        
        
# Creo una classe per estendere funzionalità classe xmpp_client
class SLIClientModuleMQTT:
    def __init__(self, xmpp_client):
        self.xmpp_client = xmpp_client
        
    def extend_message_handler(self, handler_func):
        """
        Decorator to extend the functionality of the XMPP message handler
        with XMPP to MQTT translation for specific data types.
        """
        @wraps(handler_func)
        def wrapper(client, msg):
            handler_func(client, msg)  # Execute the original handler

            # Extend the functionality with XMPP to MQTT translation
            sender = msg["from"]
            message_content = msg["body"]
            message_dict: dict = json.loads(message_content)
            
            try:
                message_istance = CirRoMessage(**message_dict)
                data_unit = message_istance.DataUnit

                if isinstance(data_unit, CommandLimitPowerDuration) and  (cfg_pjt.client_type.lower() == "cir"):
                    # XMPP to MQTT Translation for CommandLimitPowerDuration
                    timestamp = data_unit.dict().get("Timetag")
                    power = data_unit.dict().get("MaximumPower")
                    duration = data_unit.dict().get("Duration")
                    
                    # Prepare the MQTT message
                    message = {
                        "timestamp": timestamp,
                        "flexibility": [{"power": power, "duration": duration}]
                    }
                    topic = f"agg/{cfg_pjt.mqtt_usr}/flexibility_service"
                    payload = json.dumps(message)

                    # Create and publish the MQTT message
                    mqtt_client = ClientMQTTpub(client_id=f"Pub_CIR_{cfg_pjt.mqtt_usr}")
                    mqtt_client.connect()
                    mqtt_client.publish_message(topic, payload)
                    Logger.info(f"MQTT message sent to topic {topic} with payload {payload}")


                if isinstance(data_unit, CyclicMeasure) and  (cfg_pjt.client_type.lower() == "ro"):
                    # XMPP to MQTT Translation for CommandLimitPowerDuration
                    timestamp   =  data_unit.dict().get("Timetag")
                    data        =  data_unit.dict().get("Data")
                    
                    if isinstance(data, dict):
                        pwr_csi = data.get(CyclicEnums.PWR_CSI.value)
                        pwr_m1 = data.get(CyclicEnums.PWR_M1.value)
                        pwr_m2 = data.get(CyclicEnums.PWR_M2.value)
                        pwr_av = data.get(CyclicEnums.PWR_AV.value)
                        
                        if isinstance(pwr_csi, dict) and isinstance(pwr_m1, dict) and isinstance(pwr_m2, dict) and isinstance(pwr_av, dict):
                            message = {"timestamp": timestamp, 
                                    "data":{
                                        "M1":       {"value":pwr_csi["Value"], "timestamp":pwr_csi["Timetag"]},
                                        "M2":       {"value":pwr_m1["Value"], "timestamp": pwr_m1["Timetag"]},
                                        "CSI":      {"value":pwr_m2["Value"], "timestamp": pwr_m2["Timetag"]},
                                        "CSIStp":   {"value":pwr_av["Value"], "timestamp": pwr_av["Timetag"]}
                                    }}

                            topic = f"{cfg_pjt.mqtt_usr}/ems/cir/agg"
                            
                            #send_mqtt_message(topic, message)
                            payload = json.dumps(message)
                            
                            # Creo publisher:
                            mqtt_client = ClientMQTTpub(client_id= f"Pub_RO_{cfg_pjt.mqtt_usr}")
                            mqtt_client.connect()
                            # Pubblica un messaggio
                            mqtt_client.publish_message(topic, payload)

                    Logger.info(f"MQTT message sent to topic {topic} with payload {payload}")

                
            except Exception as e:
                Logger.error(f"Failed to extend message handler with MQTT functionality. Error: {e}")

        return wrapper