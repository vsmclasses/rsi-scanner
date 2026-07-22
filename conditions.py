def condition_1(current_rsi):

    return current_rsi > 50


def condition_2(previous_rsi):

    return previous_rsi < 50


def condition_3(weekly_rsi):

    return weekly_rsi > 60


def condition_4(monthly_rsi):

    return monthly_rsi > 60
