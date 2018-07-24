from random import shuffle
from typing import *

"""
Miscellaneous utility functions.
"""

T = TypeVar("T")


def shuffle_data(items: Sequence[T]) -> Sequence[T]:
    """
    Randomly shuffles the data.
    """
    ran = list(range(len(items)))
    shuffle(ran)
    return [items[i] for i in ran]


def get_num_params(vocab_size, num_layers, num_neurons):
    """Returns the number of trainable parameters of an LSTM.

    Args:
        vocab_size (int): The vocabulary size
        num_layers (int): The number of layers in the LSTM
        num_neurons (int): The number of neurons / units per layer

    Returns:
        int: The number of trainable parameters
    """
    num_first_layer = 4 * (num_neurons * (vocab_size + num_neurons) + num_neurons)
    num_other_layer = 4 * (num_neurons * 2 * num_neurons + num_neurons)
    num_softmax = vocab_size * num_neurons + vocab_size

    return num_first_layer + (num_layers - 1) * num_other_layer + num_softmax
