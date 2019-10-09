from pandas import DataFrame


def macd(x):
    x = DataFrame(x)
    macd_ = x.ewm(span=12, adjust=False).mean() - x.ewm(span=26, adjust=False).mean()
    signal = macd_.ewm(span=9, adjust=False).mean()
    return [list(macd_[0]), list(signal[0])]
