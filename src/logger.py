import logging
import os
from datetime import datetime

def setup_logging(prefix="app"):
    log_file = f"{prefix}_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, log_file)

    file_handler = logging.FileHandler(log_path)
    formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler]
    )

    logging.info(f"Logging started: {log_path}")
