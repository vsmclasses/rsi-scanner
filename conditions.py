from conditions import *

def condition_1(current_rsi):

    return current_rsi > 50


def condition_2(previous_rsi):

    return previous_rsi < 50


def condition_3(weekly_rsi):

    return weekly_rsi > 60


def condition_4(monthly_rsi):

    return monthly_rsi > 60


print()

print("Condition 1 :", condition_1(last["RSI"]))

print("Condition 2 :", condition_2(prev["RSI"]))

print("Condition 3 :", condition_3(weekly_last["RSI"]))

print("Condition 4 :", condition_4(monthly_last["RSI"]))
