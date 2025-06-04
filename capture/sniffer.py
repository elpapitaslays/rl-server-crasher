from scapy.all import sniff, UDP, IP
from utils.logger import logger

class ServerSniffer:
    def __init__(self, port_range=(7000, 8000), threshold=10):
        self.port_min, self.port_max = port_range
        self.threshold = threshold
        self.packet_counter = {}
        self.detected_server = None

    def _packet_filter(self, pkt):
        if IP in pkt and UDP in pkt:
            ip = pkt[IP].dst
            port = pkt[UDP].dport

            if self.port_min <= port <= self.port_max:
                key = (ip, port)
                self.packet_counter[key] = self.packet_counter.get(key, 0) + 1

                logger.debug(f"Traffic to {ip}:{port} ({self.packet_counter[key]} packets)")

                if self.packet_counter[key] >= self.threshold:
                    self.detected_server = key
                    logger.info(f"Server detected: {ip}:{port}")
                    return True
        return False

    def start_sniffing(self):
        logger.info("Starting packet capture. Waiting for Rocket League traffic...")
        sniff(filter="udp", prn=self._packet_filter, store=0,
              stop_filter=lambda x: self.detected_server is not None)
        return self.detected_server if self.detected_server else (None, None)