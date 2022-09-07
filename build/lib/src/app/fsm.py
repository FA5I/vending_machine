from abc import ABC
from enum import Enum, auto



class State(Enum):
	IDLE = auto()
	PRODUCT_SELECTED = auto()
	TRANSACTION_IN_PROGRESS = auto()
	TRANSACTION_READY = auto()
	TRANSACTION_FAILED = auto()
	TRANSACTION_COMPLETED = auto()


class FiniteStateMachine(ABC):
	""" Defines a basic interface for a finite state machine.

    Properties:
	transition_graph -- A state graph (adjacency list) describing valid state transitions.

	Methods:
	_transition_state -- An internal method that determines whether the keyword arugment `dest` can be reached from the current state.
    """

	@property
	def transition_graph(self):
		raise NotImplementedError

	def _transition_state(self, dest: State) -> None:
		raise NotImplementedError