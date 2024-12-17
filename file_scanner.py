import os

class FileScanner:
    def __init__(self):
        self.temp_files = []
        self.log_files = []

    def scan_temp_files(self):
        temp_dirs = ['/tmp', '/var/tmp']
        for directory in temp_dirs:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    self.temp_files.append(os.path.join(root, file))

    def scan_log_files(self):
        log_dirs = ['/var/log']
        for directory in log_dirs:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    self.log_files.append(os.path.join(root, file))
