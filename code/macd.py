from pandas import DataFrame


def macd(y, EMA1=12, EMA2=26, SIGNAL_EMA=9):
    y = DataFrame(y)
    macd_ = y.ewm(span=EMA1, adjust=False).mean() - y.ewm(span=EMA2, adjust=False).mean()
    signal = macd_.ewm(span=SIGNAL_EMA, adjust=False).mean()
    return [list(macd_[0]), list(signal[0])]
