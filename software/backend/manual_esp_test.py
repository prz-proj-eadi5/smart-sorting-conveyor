"""Manually test ESP32 USB communication without a camera or neural network."""

import serial

from esp import PORT, close_connection, read_message, send_message


def main() -> None:
    print("Enter a color to send to ESP32. Type exit to quit.")
    try:
        while True:
            color = input("Color: ").strip()
            if color.lower() == "exit":
                break
            if not color:
                continue
            try:
                send_message(color)
                response = read_message()
                print(f"ESP32: {response}" if response is not None else "ESP32: no response")
            except ValueError as error:
                print(f"Error: {error}")
    except (KeyboardInterrupt, EOFError):
        pass
    except serial.SerialException as error:
        if error.errno == 16:
            raise SystemExit(
                f"Port {PORT} is busy. Close Arduino Serial Monitor and other programs using it."
            ) from error
        raise SystemExit(f"USB port error ({PORT}): {error}") from error
    finally:
        close_connection()


if __name__ == "__main__":
    main()
