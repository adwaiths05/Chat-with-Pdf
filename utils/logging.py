from loguru import logger
import sys

# Configure loguru
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> | <level>{level}</level> | <cyan>{message}</cyan>")
logger.add("logs/app.log", rotation="1 MB", retention="7 days", compression="zip")

def get_logger():
    return logger
