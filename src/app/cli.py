import argparse
import cmd
from typing import Counter

from src.app.vending_machine import VendingMachine
from src.app.fsm import State
from src.app.utilities import COIN_DENOMINATIONS, InvalidStateException, InsufficientBalanceException
from src.app.logging import log_to_file


class REPL(cmd.Cmd):
	""" Defines a basic REPL-like interface for the CLI. This provides the API the user interacts with."""

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.machine = VendingMachine()
		self.parser = argparse.ArgumentParser(description='API for vending machine')
		for denomination in COIN_DENOMINATIONS:
			self.parser.add_argument(f"--{denomination}p", type=int, default=0)
		self.parser.add_argument(f"--product", type=str)

	
	def do_init(self, line):
		"""Initialize the machine with a provided set of balances."""

		try:
			if self.machine.state != State.IDLE:
				raise InvalidStateException('Machine has already been initialized!')
			args = self.parser.parse_args(line.split())
			args = vars(args)
			for key in args:
				if key.endswith('p'):
					self.machine.balances[int(key[:-1])] =  int(args[key])
			print('Balances updated!')
		
		except InvalidStateException as e:
			print('That action is not allowed. Please try one of the following:')
			print('- display_balances')
			print('- select_product')

			log_to_file('init failure', e)

		except Exception as e:
			print(f'Failed to initialize balances.')
			log_to_file('init failure', e)


	def do_display_balances(self, line):
		"""Displays the vending machine balance. Exists mostly to allow machine admin to view balances."""

		print('Displaying coin balances in the vending machine...')
		print({ f'{c}p' : v for c, v in self.machine.balances.items() })

	
	def do_select_product(self, line):
		"""Selects a product and initiates a new transaction between the user and machine."""

		args = self.parser.parse_args(line.split())
		args = vars(args)

		try:
			self.machine.select_product(args['product'])
			print(f"{args['product']} successfully selected.")
		
		except InvalidStateException as e:
			print('That action is not allowed. Please try one of the following:')
			print('- display_balances')
			print('- cancel_tx')
			log_to_file('select_product failure', e)
		
		except Exception as e:
			print(f'Please select another product as {args["product"]} not in machine.')
			log_to_file('select_product failure', e)

	
	def do_cancel_tx(self, line):
		"""Cancels the current transaction and returns the machine to the IDLE state."""
		
		try:
			if self.machine.current_transaction is None:
				raise InvalidStateException('Cannot cancel tx - there is none. First select a product.')

			print('Cancelling transaction...')
			self.machine.cancel_tx()
			print('Transaction cancelled.')
		
		except InvalidStateException as e:
			print('That action is not allowed. Please try one of the following:')
			print('- display_balances')
			print('- select_product')
			log_to_file('cancel_tx failure', e)
		
		except Exception as e:
			print(f'Could not cancel the transaction. Please contact an administrator.')
			log_to_file('cancel_tx failure', e)

	
	def do_insert_coins(self, line):
		"""Allows the user to insert coins into the machine or a given transaction."""

		try:
			args = self.parser.parse_args(line.split())
			args = vars(args)

			for key in args:
				if key.endswith('p'):
					c = int(key[:-1])
					q = int(args[key])
					self.machine.insert_coins(denomination=c, quantity=q)

			print(f'Coins succesfully updated. Your current balance: {self.machine._inserted_coin_balance()}')
			
		except InvalidStateException as e:
			print('That action is not allowed. Please try one of the following:')
			print('- display_balances')
			print('- cancel_tx')
			log_to_file('insert_coins failure', e)

		except Exception as e:
			print(f'Could not insert coins. Please contact an administrator - {e}.')
			log_to_file('insert_coins failure', e)


	def do_get_change(self, line):
		"""Allows the user to receive their change, while updating the machine's coin balances."""

		try:
			change = self.machine.return_change()
			print(f'You will receive total change of {self.machine._calculate_change_required()}p')
			print('This will consist of:')
			counter = Counter(change)
			for c in counter:
				print(f'{counter[c]} x {c}p')
		

		except InvalidStateException as e:
			print('That action is not allowed. Please try one of the following:')
			print('- display_balances')
			print('- cancel_tx')
			log_to_file('get_change failure', e)


		except InsufficientBalanceException as e:
			print(f'Machine has run out of coins. Please contact an administrator - {e}')
			print(f'Your coins are being returned now:')
			coins = self.machine.return_inserted_coins()
			for c in coins:
				print(f'{coins[c]} x {c}p')
			log_to_file('get_change failure', e)


		except Exception as e:
			print(f'Could not get your change. Please contact an administrator - {e}.')
			log_to_file('get_change failure', e)


def cli():
	repl = REPL()
	repl.prompt = '> '
	repl.cmdloop()


if __name__ == "__main__":
	cli()
