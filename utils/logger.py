import logging

logger = logging.getLogger("RocketTool")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s", "%H:%M:%S")
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)