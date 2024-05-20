# import bluetooth
# _ble = bluetooth.BLE()
# _ble.active(True)
# print(dir(_ble))
#
#
# _IRQ_CENTRAL_CONNECT = 1
# _IRQ_CENTRAL_DISCONNECT = 2
# _IRQ_GATTS_WRITE = 9
#
# _connections = set()
#
#
# def _irq(self, event, data):
#     if event == _IRQ_CENTRAL_CONNECT:
#         conn_handle, _, _ = data
#         _connections.add(conn_handle)
#     elif event == _IRQ_CENTRAL_DISCONNECT:
#         conn_handle, _, _ = data
#         _connections.remove(conn_handle)
#         _advertise()
#     elif event == _IRQ_GATTS_WRITE:
#         conn_handle, value_handle = data
#         received_data = _ble.gatts_read(value_handle)
#         print("Received data:", received_data.decode())
#
#
# def _advertise():
#     pass
#
#
# _ble.irq(_irq)
import aioble  # wrapper for bluetooth, needed to be installed with thonny
print(dir(aioble))


async def scan():
    async with aioble.scan(duration_ms=5000) as scanner:
        async for result in scanner:
            print(result, result.name(), result.rssi, result.services())

scan()
# while True:
#     pass
