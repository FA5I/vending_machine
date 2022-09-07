from pydantic import BaseModel, validator

class Product(BaseModel):
	""" Defines a representation of a vending machine product.

    Keyword arguments:
	name -- the name or id of the product (what a user will type in on the numberpad to select) (required)
    price -- the price of the product in pence (required)
    """

	name: str
	price: int

	@validator('price')
	def validate_price(cls, v):
		assert v >= 0, 'Price must be non-negative.'
		return v


class ProductFactory:
	"""Factory class for generating products.

    class variables:
	_PRICE_MAP -- a class variable that defines valid product ids and their respective prices in pence
    """

	_PRICE_MAP = {
		'A1': 100,
		'A2': 150,
		'A3': 135,
	}

	@classmethod
	def create_product(cls, name) -> Product:
		"""Generate a product based on the name argument"""

		if name not in cls._PRICE_MAP:
			raise ValueError('Incorrect product name. There is no such product in the vending machine.')
		return Product(name=name, price=cls._PRICE_MAP[name])