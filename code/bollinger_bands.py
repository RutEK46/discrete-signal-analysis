from base_operations import sma, standard_deviation


def bollinger_bands(y, n=20, k=2):
    middle_band = list(sma(y, span=n))
    k_times_standard_deviation = [k*x for x in standard_deviation(y, span=n)]
    upper_band = [y + sd for y, sd in zip(middle_band, k_times_standard_deviation)]
    lower_band = [y - sd for y, sd in zip(middle_band, k_times_standard_deviation)]
    return [upper_band, middle_band, lower_band]

