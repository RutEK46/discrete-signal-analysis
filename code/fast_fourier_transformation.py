from numpy import pi, exp


class FastFourierTransformationError(Exception):
    pass


def is_power_of_two(n):
    return (n > 0) and not (n & (n - 1))


def fast_fourier_transformation(signal):
    if not is_power_of_two(len(signal)):
        raise FastFourierTransformationError(
            f"Length of the signal must be the power of two! Given length of the signal: {len(signal)}"
        )
        
    if len(signal) == 1:
        return signal
    else:
        signal = fast_fourier_transformation(signal[0::2]) + fast_fourier_transformation(signal[1::2])
        y1, y2 = [], []
        n = len(signal)
        for k, x in enumerate(signal[:int(n/2)]):
            ex = -2j * pi * k / n
            y1.append(x + exp(ex) * signal[k + int(n/2)])
            y2.append(x - exp(ex) * signal[k + int(n/2)])
        return y1 + y2
