import argparse
import cmd
from typing import Counter

from src.app.vending_machine import VendingMachine
from src.app.fsm import State
from src.app.utilities import COIN_DENOMINATIONS
from src.app.logging import log_to_file


class REPL(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.machine = VendingMachine()
		self.parser = argparse.ArgumentParser(description='API for vending machine')
		
		for denomination in COIN_DENOMINATIONS:
			self.parser.add_argument(f"--{denomination}p", type=int, default=0)
		
		self.parser.add_argument(f"--product", type=str)

	
	def do_init(self, line):
		try:
			if self.machine._state != State.IDLE:
				raise Exception('Machine has already been initialized!')
			args = self.parser.parse_args(line.split())
			args = vars(args)
			for key in args:
				if key.endswith('p'):
					self.machine.balances[int(key[:-1])] =  int(args[key])
			print('Balances updated!')
		
		except Exception as e:
			print(f'Failed to initialize balances.')
			log_to_file('init failure', e)


	def do_display_balances(self, line):
		print('Displaying coin balances in the vending machine...')
		print({ f'{c}p' : v for c, v in self.machine.balances.items() })

	
	def do_select_product(self, line):
		args = self.parser.parse_args(line.split())
		args = vars(args)

		try:
			self.machine.select_product(args['product'])
			print(f"{args['product']} successfully selected.")
		except Exception as e:
			print(f'Please select another product as f{args["product"]} not in machine.')
			log_to_file('select_product failure', e)

	
	def do_cancel_tx(self, line):
		print('Cancelling transaction...')
		try:
			self.machine.cancel_tx()
			print('Transaction cancelled.')
		except Exception as e:
			print(f'Could not cancel the transaction. Please contact an administrator.')
			log_to_file('cancel_tx failure', e)

	
	def do_insert_coins(self, line):
		try:
			args = self.parser.parse_args(line.split())
			args = vars(args)

			for key in args:
				if key.endswith('p'):
					c = int(key[:-1])
					q = int(args[key])
					self.machine.insert_coins(denomination=c, quantity=q)

			print(f'Coins succesfully updated. Your current balance: {self.machine._inserted_coin_balance()}')
			
		except Exception as e:
			print(f'Could not insert coins. Please contact an administrator - {e}.')
			log_to_file('insert_coins failure', e)


	def do_get_change(self, line):
		print(f'You will receive total change of {self.machine._calculate_change_required()}p')

		change = self.machine.return_change()
		print('This will consist of:')
		counter = Counter(change)
		for c in counter:
			print(f'{counter[c]} x {c}p')


def cli():
	repl = REPL()
	repl.prompt = '> '
	repl.cmdloop()


if __name__ == "__main__":
	cli()
