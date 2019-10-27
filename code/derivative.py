def derivative(x, signal):
    def derivative_func(i1, i2):
        return (signal[i2] - signal[i1]) / (x[i2] - x[i1])

    left = derivative_func(0, 1)
    right = derivative_func(-2, -1)
    return [left] + [derivative_func(i, i+2) for i, _ in enumerate(signal[1:-1])] + [right]
