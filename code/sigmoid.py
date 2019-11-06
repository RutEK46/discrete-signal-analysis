from collections.abc import Iterable
from numpy import exp


def sigmoid(signal):
    if isinstance(signal, Iterable):
        return (sigmoid(y) for y in signal)
    else:
        return 1 / (1 + exp(-signal))
