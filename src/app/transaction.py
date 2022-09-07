from pydantic import BaseModel
from src.app.product import Product
from src.app.utilities import COIN_DENOMINATIONS


class Transaction(BaseModel):
	""" Defines a representation of a on going transaction with the vending machine.

    Keyword arguments:
	product -- the product object for which a particular transaction is being executed by the vending machine (required)
    deposited_coins -- the balance of coins per denomination deposited by the user (default: set all denomination quantities to 0)
    """

	product: Product
	deposited_coins: dict = { d: 0 for d in COIN_DENOMINATIONS } # { denomination_value : quantity }