def calculate_pe_ratio(price, eps) -> float:
    """Calculate the price to earnings (PE) ratio.
    Formula: price / EPS

    >>> calculate_pe_ratio(400, 20)
    20.0
    """
    if eps <= 0:
        return 0.0
    return round(price / eps, 1)


def calculate_peg_ratio(pe_ratio, eps_growth) -> float:
    """calcalate the PEG ratio.
    Formula: PE ratio / growth rate

    growth rate: yafoo finance analysis -> growth estimates -> next year column
    >>> calculate_peg_ratio(25, 15)
    1.67
    """
    if eps_growth <= 0:
        return 0.0
    return round(pe_ratio / eps_growth, 2)

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)