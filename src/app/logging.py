import logging
import datetime

logger = logging.getLogger('vending_machine_app')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('vending_machine.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def log_to_file(msg, exception):
	"""Logs a message and exception to file."""

	logger.error(f'{datetime.datetime.now().isoformat()} - {msg} - exception: {exception}')
		