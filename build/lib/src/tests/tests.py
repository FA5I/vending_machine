from typing import Counter
import pytest


from src.app.vending_machine import VendingMachine, State
from src.app.product import Product, ProductFactory
from src.app.transaction import Transaction
from src.app.utilities import COIN_DENOMINATIONS


def test_invalid_product_name():
	with pytest.raises(Exception):
		ProductFactory.create_product('XX')
		

def test_valid_product_name():
	try:
		ProductFactory.create_product('A1')
	except Exception as e:
		pytest.fail(f"Unexpected error - {e}.")
		

def test_transaction():
	product = ProductFactory.create_product('A1')
	tx = Transaction(product=product)
	assert tx.product.name == 'A1'
	assert tx.product.price == 100


def test_invalid_load_balance():
	vm = VendingMachine()
	with pytest.raises(Exception):
		vm.load_balances({})


def test_vending_machine_select_product():
	vm = VendingMachine()
	assert vm._state == State.IDLE
	vm.select_product('A1')
	assert vm._state == State.PRODUCT_SELECTED
	assert vm._current_transaction.product.name == 'A1'


def test_vending_machine_invalid_transition():
	vm = VendingMachine()
	assert vm._state == State.IDLE
	with pytest.raises(Exception):
		vm.insert_coins(denomination=1, quantity=11)


def test_vending_machine_cancel_transaction():
	vm = VendingMachine()
	vm.select_product('A1')
	vm.cancel_tx()
	assert vm._current_transaction is None


def test_vending_machine_insert_coins():
	vm = VendingMachine()
	vm.select_product('A1')
	with pytest.raises(Exception):
		vm.insert_coins(denomination=1, quantity=-11)
	with pytest.raises(Exception):
		vm.insert_coins(denomination=11, quantity=1)
	vm.insert_coins(denomination=1, quantity=130)
	assert vm._current_transaction.deposited_coins[1] == 130


def test_vending_machine_insert_coins():
	vm = VendingMachine()
	vm.select_product('A1')
	vm.insert_coins(denomination=1, quantity=130)
	vm.insert_coins(denomination=10, quantity=1)
	assert vm._inserted_coin_balance() == 140


def test_vending_machine_calc_change_required():
	vm = VendingMachine()
	vm.select_product('A1')
	# for a new transaction added to the vending machine, all quantities should be 0
	assert vm._inserted_coin_balance() == 0
	# simulate user adding 100 1p coins into the machine
	vm.insert_coins(denomination=1, quantity=130)
	# check the balance has been updated correctly
	assert vm._inserted_coin_balance() == 130
	assert vm._current_transaction.deposited_coins.get(1) == 130
	# check the change required is calculated correctly
	assert vm._calculate_change_required() == 30


def test_vending_machine_construct_change():
	test_balances = {
		1: 1000,
		2: 0,
		5: 0,
		10: 0,
		20: 0,
		50: 0,
		100: 0,
		200: 0
	}

	vm = VendingMachine(test_balances)
	vm.select_product('A1')
	vm.insert_coins(denomination=1, quantity=130)
	vm.insert_coins(denomination=10, quantity=13)
	assert vm._calculate_change_required() == 160
	counts = Counter(vm._construct_change())
	assert sum([k*v for k, v in counts.items()]) == vm._calculate_change_required()


def test_vending_machine_construct_change_nil():
	test_balances = {
		1: 0,
		2: 0,
		5: 0,
		10: 0,
		20: 0,
		50: 0,
		100: 0,
		200: 0
	}

	vm = VendingMachine(test_balances)
	vm.select_product('A1')
	assert vm.return_change() == []



def test_vending_machine_construct_change_fail():
	"""scenario where change required > vending machine balances"""

	test_balances = {
		1: 0,
		2: 0,
		5: 0,
		10: 0,
		20: 0,
		50: 0,
		100: 0,
		200: 0
	}

	# create a vending machine with 0 balance
	vm = VendingMachine(test_balances)
	vm.select_product('A1')
	
	# add 200 worth of 10p coins
	vm.insert_coins(denomination=10, quantity=20)
	
	# should raise an exception as vending machine balance is insufficient
	with pytest.raises(Exception):
		vm.return_change()



def test_vending_machine_construct_change_success():
	"""Scenario where we have sufficient vending machine balances to create change"""

	test_balances = {
		1: 0,
		2: 0,
		5: 10,
		10: 16,
		20: 10,
		50: 10,
		100: 10,
		200: 10
	}

	vm = VendingMachine(test_balances)
	vm.select_product('A1')
	vm.insert_coins(denomination=1, quantity=130)
	vm.insert_coins(denomination=10, quantity=13)
	

	initial_balance = vm.balances.copy()
	change = vm.return_change()
	final_balance = vm.balances.copy()

	counter = Counter(change)

	for k in counter:
		assert counter[k] == initial_balance[k] - final_balance[k]
		

	