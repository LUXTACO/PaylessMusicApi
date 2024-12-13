import logging

class RemovePyExtensionFilter(logging.Filter):
    def filter(self, record):
        record.filename = record.filename.replace('.py', '')
        return True