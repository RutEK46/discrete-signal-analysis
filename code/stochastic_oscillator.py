from base_operations import sma, standard_deviation


def stochastic_oscillator(y):
    min_price = min(y)
    max_price = max(y)
    line_k = [(100 * ((price - min_price)/(max_price - min_price))) for price in y]
    line_d = sma(line_k, span=3)
    return [line_k, line_d]

