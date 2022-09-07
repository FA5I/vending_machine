COIN_DENOMINATIONS = [1, 2, 5, 10, 20, 50, 100, 200]

class InvalidStateException(Exception):
	pass

class InsufficientBalanceException(Exception):
	pass