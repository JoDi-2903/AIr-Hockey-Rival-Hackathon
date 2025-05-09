"""
Interface for controlling the motor axes.

Uses a UDP-based protocol for controlling and monitoring a 2-axis gantry. Communication is
performed over a broadcast-capable Ethernet network using designated UDP ports on both ends.
"""

import socket
import struct
import threading
import time
from typing import Tuple


def _receive_loop(this) -> None:
    msglen = 32
    while True:
        try:
            # Read until we have 32 bytes (might happen in multiple chunks in high network load)
            chunks = []
            bytes_recd = 0
            while bytes_recd < msglen:
                # blocking (this is why we are in an extra thread)
                chunk = this.receive_socket.recv(msglen - bytes_recd)
                if chunk == b'':
                    raise RuntimeError("socket connection broken")
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
            this.data = b''.join(chunks)
        except Exception as e:
            print(f"Error receiving update: {e}")

class MotorControlSystem:
    def __init__(
        self,
        # app,
        ip_address: str = "192.168.4.201",
        broadcast_address: str = "192.168.255.255",
        subnet_mask: str = "255.255.0.0",
        port_send: int = 3001,
        port_receive: int = 3000,
    ):
        """
        Initialize the motor control system with the given parameters.

        :param ip_address: The IP address of the motor control system.
        :param subnet_mask: The subnet mask for the network.
        :param port_send: The port number for the send.
        :param port_receive: The port number for the receive.
        """
        # self.app = app
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.port_send = port_send
        self.port_receive = port_receive
        self.broadcast_address = broadcast_address

        # Define the axes safety limits
        safety_limit_size = 20
        self.x_min = -5 + safety_limit_size
        self.x_max = 450 - safety_limit_size
        self.y_min = -5 + safety_limit_size
        self.y_max = 390 - safety_limit_size

        # Status flags and position data
        self.ready = False
        self.enabled = False
        self.error = False
        self.current_position = (0, 0)
        self.current_velocity = 0

        # Communication sockets
        self.send_socket = None
        self.receive_socket = None
        self.receive_thread = None
        self.data = None

    def is_running(self):
        # return app.running
        return True

    def connect(self) -> None:
        """
        Connect to the Festo motor control system and enable it.

        :raises: ConnectionError if the `ready` and `enabled` status are not True.
        """
        # Create UDP sockets for sending and receiving
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the receive port
        self.receive_socket.bind(('0.0.0.0', self.port_receive))

        # Start thread to read from receive_socket
        self.receive_thread = threading.Thread(target=_receive_loop, args=(self,), daemon=True).start()

        # Send enable command
        self._send_setpoint(enable=self.is_running(), acknowledge=False, velocity=0, acceleration=0, x=0, y=0)

        # Wait for system to be ready and enabled
        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            self._update_status()
            if self.ready and self.enabled:
                return
            time.sleep(0.5)
            attempt += 1

        # If we get here, connection failed
        raise ConnectionError("Failed to connect: System not ready or not enabled")

    def set_position(self, x: float, y: float, velocity: float, acceleration: float = 0.0) -> None:
        """
        Set the position of the motor axes.

        :param x: Target X position in mm
        :param y: Target Y position in mm
        :param velocity: Desired velocity as float between 0.0 and 1.0 (0.0 for maximum velocity)
        :param acceleration: Desired acceleration as float between 0.0 and 1.0 (0.0 for maximum acceleration)
        :raises: ValueError if the error flag is set to True or if velocity/acceleration values are invalid.
        """
        # Validate velocity and acceleration ranges
        if not 0.0 <= velocity <= 1.0:
            raise ValueError("Velocity must be between 0.0 and 1.0")
        if not 0.0 <= acceleration <= 1.0:
            raise ValueError("Acceleration must be between 0.0 and 1.0")

        # Check if the safety area is exceeded
        if x < self.x_min or x > self.x_max:
            raise ValueError(f"X position {x} is out of bounds ({self.x_min}, {self.x_max})")
        if y < self.y_min or y > self.y_max:
            raise ValueError(f"Y position {y} is out of bounds ({self.y_min}, {self.y_max})")

        # Check for errors first
        self._update_status()
        if self.error:
            raise ValueError("Cannot set position while error flag is active")

        # Send the position command
        self._send_setpoint(enable=self.is_running(), acknowledge=False,
                            velocity=velocity, acceleration=acceleration,
                            x=x, y=y)

    @property
    def get_position(self) -> Tuple[float, float]:
        """
        Get the current position of the motor axes.

        :return: current position as tuple (x, y) in mm
        """
        self._update_status()
        return self.current_position

    @property
    def get_velocity(self) -> float:
        """
        Get the current velocity of the motor axes.

        :return: current velocity as float between 0.0 and 1.0
        """
        self._update_status() # FEATURE: don't updated twice
        return self.current_velocity

    def acknowledge_error(self) -> None:
        """
        Acknowledge the error and reset the error flag.

        If error is true in `ActualValues`, the gantry awaits `acknowledge = true` in
        `SetpointValues` to reset. Motion commands are ignored during an error state until reset.
        """
        self._send_setpoint(
            enable=self.is_running(),
            acknowledge=True,
            velocity=0,
            acceleration=0,
            x=self.current_position[0],
            y=self.current_position[1],
        )

        # Wait for error flag to clear
        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            self._update_status()
            if not self.error:
                return
            time.sleep(0.1)
            attempt += 1

        raise ValueError("Failed to acknowledge error")

    def close(self) -> None:
        """
        Close the connection to the motor controller.
        """
        # Disable the system
        try:
            self._send_setpoint(
                enable=False,
                acknowledge=False,
                velocity=0,
                acceleration=0,
                x=self.current_position[0],
                y=self.current_position[1],
            )
        except:
            pass

        # Close sockets
        if self.send_socket:
            self.send_socket.close()
        if self.receive_socket:
            self.receive_socket.close()

    def _receive_loop(self) -> None:
        print("here")
        msglen = 32
        while True:
            try:
                # Read until we have 32 bytes (might happen in multiple chunks in high network load)
                chunks = []
                bytes_recd = 0
                while bytes_recd < msglen:
                    # blocking (this is why we are in an extra thread)
                    chunk = self.receive_socket.recv(msglen - bytes_recd)
                    if chunk == b'':
                        raise RuntimeError("socket connection broken")
                    chunks.append(chunk)
                    bytes_recd = bytes_recd + len(chunk)
                self.data = b''.join(chunks)
                print("saved data")
            except Exception as e:
                print(f"Error receiving update: {e}")

    def _update_status(self) -> None:
        """
        Update the status by receiving and processing the latest message from the controller.

        On-demand update instead of a threaded approach.
        """
        if not self.data:
            print("Error: no data to parse")
            self.error = True
            return
        # print(f"Converting raw data: ({len(data)} bytes): {data}")

        # Format: 3 Booleans, 5 Bytes Padding, 3 doubles
        ready, enabled, error, velocity, x, y = struct.unpack('<BBB5xddd', self.data)
        self.ready = bool(ready)
        self.enabled = bool(enabled)
        self.error = bool(error)
        self.current_velocity = float(velocity)
        self.current_position = (float(x), float(y))

    def _send_setpoint(self, enable: bool, acknowledge: bool,
                       velocity: float, acceleration: float,
                       x: float, y: float, use_broadcast: bool = False) -> None:
        """
        Pack and send setpoint values to the motor controller.

        :param enable: Enable/disable the system
        :param acknowledge: Acknowledge errors
        :param velocity: Desired velocity as float between 0.0 and 1.0
        :param acceleration: Desired acceleration as float between 0.0 and 1.0
        :param x: Target X position in mm
        :param y: Target Y position in mm
        :param use_broadcast: Whether to use broadcast instead of unicast
        """
        # Pack data according to the specification
        # Format: 1 byte bool, 1 byte bool, 6 bytes padding, 4 doubles (8 bytes each)
        data = struct.pack(
            '<BB6xdddd',
            1 if enable else 0,
            1 if acknowledge else 0,
            float(velocity),
            float(acceleration),
            float(x),
            float(y)
        )
        # print(f"Raw data to send ({len(data)} bytes): {data}")

        # Send to the PLC - either unicast or broadcast
        target_address = self.broadcast_address if use_broadcast else self.ip_address
        self.send_socket.sendto(data, (target_address, self.port_send))
