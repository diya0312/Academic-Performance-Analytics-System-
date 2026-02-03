import logging

logging.basicConfig(
    filename="apas.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_event(msg):
    logging.info(msg)
