def sma(signal, span=None):
    if span is None:
        return sum(signal) / len(signal)
    else:
        return (sma(signal[i-span+1:i+1]) if i >= span else sma(signal[:i+1]) for i in range(len(signal)))


def variation(signal, span=None):
    u = sma(signal, span)
    if span is None:
        return sma([(y - u) ** 2 for y in signal])
    else:
        return sma([(y - ui) ** 2 for y, ui in zip(signal, u)], span)


def standard_deviation(signal, span=None):
    if span is None:
        return variation(signal) ** 0.5
    else:
        return (x ** 0.5 for x in variation(signal, span))


def energy(signal, span=None):
    if span is None:
        return sum(x**2 for x in signal)
    else:
        return (energy(signal[i-span+1:i+1]) if i >= span else energy(signal[:i+1]) for i in range(len(signal)))


def moment(signal, m, span=None):
    if span is None:
        return sum((i**m) * x for i, x in enumerate(signal))
    else:
        return (moment(signal[i-span+1:i+1], m) if i >= span else moment(signal[:i+1], m) for i in range(len(signal)))


def central_moment(signal, m, span=None):
    if span is None:
        moment_ = moment(signal, 1)
        return sum(((i - moment_)**m) * x for i, x in enumerate(signal))
    else:
        return (central_moment(signal[i-span+1:i+1], m) if i >= span else central_moment(signal[:i+1], m)
                for i in range(len(signal)))


def standardized_moment(signal, m, span=None):
    if span is None:
        return moment(signal, m) / sma(signal)
    else:
        return (standardized_moment(signal[i-span+1:i+1], m) if i >= span else standardized_moment(signal[:i+1], m)
                for i in range(len(signal)))


def standardized_central_moment(signal, m, span=None):
    if span is None:
        return central_moment(signal, m) / sma(signal)
    else:
        return (standardized_central_moment(signal[i-span+1:i+1], m) if i >= span else standardized_central_moment(signal[:i+1], m)
                for i in range(len(signal)))
