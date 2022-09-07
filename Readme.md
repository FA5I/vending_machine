# Vending Machine

## Installation

Run the following commands from the root folder:

- `pipenv install`
- `pipenv install --editable .`
- `vending_machine`

Once you have done this, you should see a `>` prompt in the terminal. The CLI is now running.

## File Overview

### `src` directory

- The `app` folder contains most of the files that implement the CLI:
	- `cli.py`: contains code for the cli application a user interacts with.
	- `fsm.py`: contains the interface for the finite state machine.
	- `logging.py`: contains a custom logger that logs to the `vending_machine.log` file.
	- `product.py`: contains the class definition for a product, and also a product factory.
	- `transaction.py`: contains the class definition for a transaction.
	- `utilties.py`: contains ad hoc code used in multiple files (pretty bare at the moment).
	- `vending_machines.py`: contains the code for the vending machine that really drives the app.

### `src/tests` directory

- This contains all the unit tests.
- Unit tests can be run using the following command from the project root directory:
	- `pytest ./src/tests/tests.py`


### Other files of interest

- `.github/workflows/actions.yaml`: This is the file used for CI/CD on Github.
- `vending_machine.log`: a log file mostly for keeping log of errors (at the moment at least, but could be extended).
- `setup.py`: allows the code to be installed as a standalone package in the virtual env. Simply run:
	-  `pipenv install --editable .`
	- `vending_machine`


### Commands

The commands with an `=` sign in them are command line arguments that can be varied.

- Initialize the vending machine balances using:
	- `init --1p=100 --2p=100 --5p=100 --10p=100 --20p=100 --50p=100 --100p=100 --200p=100`

- The vending machine balances can be displayed using:
	- `display_balances`

- Select a product using:
	- `select_product --product=A1`

- Insert coins to pay for the items using:
	- `insert_coins --1p=100 --2p=1 --5p=1 --10p=1 --20p=1 --50p=1 --100p=1 --200p=1`
 
- Retrieve the change for a user using:
 - `get_change`


### Design Decisions & Areas of Improvement

- The goal of the project was getting a minimum viable product (MVP) up and running as quickly as possible. I tried to avoid pulling in unecessary dependencies.

- The CLI API was kept as simple as possible due to time constraints. Most of the API design was based on how a user may interact with a vending machine. As there were no databases used for persistence, objects with appropriate variables were used to maintain state.

- I avoided using web server with a REST API as that seemed like overkill for a vending machine. A CLI with a REPL-like behaviour seemed more appropriate.

- Errors and exception handling were used in places deemed logical. If given more time, there is definitely scope to increase the types of custom errors to be more explicit about the errors being thrown.

- I used a Finite State Machine (FSM) to model the vending  machine as it seemed like a good fit given the transitional nature of the interactions between user and machine. The FSM is a very barebones implementation, in reality something like [pytransitions](https://github.com/pytransitions/transitions) may be more robust.

- [pydantic](https://pydantic-docs.helpmanual.io/) is minimally used for data validation, although if the project grew in scope, using it would demonstrate its effectiveness a bit more.

- I usec [pytest](https://docs.pytest.org/en/7.1.x/) for unit testing as it's much more succint vs the `unnittest` library that ships with the standard lib in Python.

- The most challenging bit of code was the `VendingMachine._construct_change` function. I used a memoization approach to compute the minimum number of coins that could be returned to fulfill the change returned to the user. I wanted to return the minimum number of coins so as to keep the vending machine float filled for as long as possible.

- For CI/CD a simple Github workflow file is defined in `.github/workflows/actions.yaml`. I chose `Black` as the formatter for the code mainly as it it's opinionated and does a good job with minimal config.