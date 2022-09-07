from typing import Optional

from src.app.product import ProductFactory
from src.app.transaction import Transaction
from src.app.fsm import FiniteStateMachine, State
from src.app.utilities import COIN_DENOMINATIONS

class VendingMachine(FiniteStateMachine):
	
	transition_graph = {
		State.IDLE: [ State.PRODUCT_SELECTED ],
		State.PRODUCT_SELECTED: [ State.TRANSACTION_IN_PROGRESS, State.TRANSACTION_READY, State.IDLE ],
		State.TRANSACTION_IN_PROGRESS: [ State.TRANSACTION_IN_PROGRESS, State.TRANSACTION_READY, State.IDLE ],
		State.TRANSACTION_READY: [ State.TRANSACTION_READY, State.TRANSACTION_COMPLETED, State.IDLE ],
	}

	
	def __init__(self, balances = { d: 0 for d in COIN_DENOMINATIONS }) -> None:
		self._state = State.IDLE
		self._balances = balances
		self._current_transaction = None
		

	@property
	def balances(self):
		return self._balances

	def _transition_state(self, dest: State) -> None:
		"""Handles transitioning from current state to `dest`."""

		if dest not in VendingMachine.transition_graph[self._state]:
			raise ValueError(f'Invalid state transition attempted from {self._state} to {dest}.')
		
		self._state = dest


	def cancel_tx(self) -> None:
		"""Cancels the current transaction and returns the vending machine to an `IDLE` state."""
	
		self._transition_state(State.IDLE)
		self._current_transaction = None
		
		
	def select_product(self, product_id) -> None:
		"""Select a product in the vending machine. Transitions state to `PRODUCT_SELECTED`."""

		product = ProductFactory.create_product(product_id)
		tx = Transaction(product=product)

		self._transition_state(State.PRODUCT_SELECTED)
		self._current_transaction = tx

	
	def insert_coins(self, denomination: int, quantity) -> None:
		"""Insert coins to pay for the current transaction."""

		if denomination not in COIN_DENOMINATIONS:
			raise ValueError(f'Invalid coin denomination of `{denomination}p`.')

		if quantity < 0:
			raise ValueError(f'Invalid coin quantity of `{quantity}`.')

		if self._current_transaction is None:
			raise ValueError(f'Current transaction must be set first.')

		if self._inserted_coin_balance() + denomination * quantity >= self._current_transaction.product.price:
			self._transition_state(State.TRANSACTION_READY)

		else:
			self._transition_state(State.TRANSACTION_IN_PROGRESS)
		
		self._current_transaction.deposited_coins[denomination] += quantity
		

	def _inserted_coin_balance(self) -> int:
		"""Checks the balance of the inserted coins and returns the total."""
		
		total = 0
		for c in COIN_DENOMINATIONS:
			quantity = self._current_transaction.deposited_coins.get(c, 0)
			total += c * quantity
		return total


	def _calculate_change_required(self) -> int:
		"""Calculates the change amount that needs to be returned to the user. 
		If the user balance is too low to cover the product, return 0.
		"""
		
		return max(0, self._inserted_coin_balance() - self._current_transaction.product.price)

	def _construct_change(self) -> list:
		"""This function returns the minimum number of coins that can be used from the existing
		balances to construct the change for the user.

		The minimum number is used so as to prolong the total coins in the vending machine.

		Returns a list containing the coins.
		"""

		def inner(coins: dict, amount: int) -> Optional[list]:
			dp = [amount + 1] * (amount + 1)
			lst = [None] * (amount + 1)
			
			dp[0] = 0
			lst[0] = []

			for c in coins:
				for _ in range(coins[c]):
					for a in range(amount, -1, -1):
						if a - c < 0:
							break

						if a - c >= 0:
							if 1 + dp[a - c] < dp[a]:
								dp[a] = 1 + dp[a - c]
								lst[a] = [c] + lst[a-c]
									
								
			return lst[amount] if dp[amount] != amount + 1 else None
		
		# calculate the target amount we are aiming for
		amount = self._calculate_change_required()
		
		# sort the existing vending machine coin balances by denomination
		existing_coins = { k: v for k, v in sorted(self.balances.items()) }

		return inner(existing_coins, amount)

	
	def return_change(self) -> dict:
		"""Reduces the vending machine balance based on how the change is constructed.
		Returns a dictionary containing the denominations and their respective quantities.
		"""

		change_required = self._construct_change()

		if change_required is None:
			raise Exception('Cannot construct correct change. Please cancel transaction.')

		for c in change_required:
			self.balances[c] -= 1

		return change_required
	
