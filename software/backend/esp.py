import time

import serial


PORT = "/dev/ttyUSB0"
BAUDRATE = 115200
MAX_MESSAGE_BYTES = 63
_connection = None


def open_connection() -> None:
    """Open the USB port once and wait for ESP32 to boot."""
    global _connection

    if _connection is None:
        _connection = serial.Serial(port=None, baudrate=BAUDRATE, timeout=1, write_timeout=1)
        try:
            # Keep control lines inactive; opening some USB adapters still resets ESP32.
            _connection.dtr = False
            _connection.rts = False
            _connection.port = PORT
            _connection.open()
            time.sleep(2)  # Allow the board to boot after USB connection.
            _connection.reset_input_buffer()
        except BaseException:
            close_connection()
            raise


def send_message(message: str) -> None:
    """Send one UTF-8 line, opening the connection if needed."""
    payload = message.encode("utf-8")
    if not message.strip() or any(char in message for char in "\r\n\0"):
        raise ValueError("Message must be nonempty and contain no CR, LF or NUL")
    if len(payload) > MAX_MESSAGE_BYTES:
        raise ValueError(f"Message must not exceed {MAX_MESSAGE_BYTES} UTF-8 bytes")

    open_connection()
    _connection.write(payload + b"\n")


def read_message() -> str | None:
    """Read one ESP32 line; return None if disconnected or no reply arrives in 1 second."""
    if _connection is None:
        return None
    response = _connection.readline(MAX_MESSAGE_BYTES + 3)
    if not response:
        return None
    payload = response.removesuffix(b"\n").removesuffix(b"\r")
    if not response.endswith(b"\n") or len(payload) > MAX_MESSAGE_BYTES:
        raise ValueError("ESP32 sent an incomplete or oversized line")
    return payload.decode("utf-8")


def close_connection() -> None:
    """Close the USB port if connected."""
    global _connection

    if _connection is not None:
        _connection.close()
        _connection = None
