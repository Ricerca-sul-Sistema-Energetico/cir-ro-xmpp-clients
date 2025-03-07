from factory_clients import xmpp_client, modbus_module_dict
from pas_functions.send_measures import send_cyclic_measure
from read_config import Logger

import threading
import asyncio
from data_models.cir_ro_message import CyclicMeasure
import uuid
import time


async def main():
    while True:
        Logger.info("Inizio ciclo di acquisizione dati modbus")
        acquired_data = modbus_module_dict["Janitza_light"].read_device_config_measurements()
        corrected_data = modbus_module_dict["Janitza_light"].convert_unit_of_measure(acquired_data)
        corrected_data_value = int(corrected_data[0]["value"])

        Logger.info(f"Data read: {corrected_data_value}")
        data_cyclic = {
            "LD_CIR/CSIMMXU1.TotW.mag": {"Value": 234, "Invalidity": 0, "ErrorCode": 0, "Timetag": 1668779108},
            "LD_CIR/M1MMXU1.TotW.mag": {"Value": corrected_data_value, "Invalidity": 1, "ErrorCode": 1, "Timetag": 1668779108},
            "LD_CIR/M2MMXU1.TotW.mag": {"Value": 254, "Invalidity": 1, "ErrorCode": 2, "Timetag": 1668779108},
            "LD_CIR/M1DWMX1.WMaxSpt.setMag": {"Value": 254, "Invalidity": 1, "ErrorCode": 3, "Timetag": 1668779108},
        }

        cyclic_measure = CyclicMeasure(UUID=uuid.uuid4(), Timetag=int(time.time()), Data=data_cyclic)
        if corrected_data is not None:
            await send_cyclic_measure("testro", "testingsaslrse", cyclic_measure)

        # Attendi prima del prossimo ciclo
        await asyncio.sleep(20)


if __name__ == "__main__":

    Logger.info("Avvio del client XMPP...")
    asyncio.ensure_future(main())
    xmpp_client.process(forever=True)
    # xmpp_thread = threading.Thread(target=xmpp_client.process)
    # xmpp_thread.start()
    # Avvia il ciclo principale
    # asyncio.ensure_future(xmpp_client.process(forever=False))

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
