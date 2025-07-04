import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Change to DEBUG for more detail
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
