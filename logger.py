import logging

class Logger:
    def __init__(self, log_file='app.log'):
        logging.basicConfig(filename=log_file, level=logging.INFO)

    def log_action(self, action):
        logging.info(action)
