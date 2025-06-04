import socket
from utils.logger import logger

class PacketSender:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send_packets(self, count=1000, payload=b"RocketTest"):
        logger.info(f"Sending {count} UDP packets to {self.ip}:{self.port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(count):
            sock.sendto(payload, (self.ip, self.port))
            logger.debug(f"Sent packet {i+1}/{count}")
        sock.close()
        logger.info("Packet sending complete.")