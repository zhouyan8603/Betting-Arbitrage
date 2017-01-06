def ConvertUS(americanOdds): # CONVERTS US ODDS TO DECIMAL ODDS
    if americanOdds >= 0:
        decimalOdds = "{:10.3f}".format(americanOdds / 100 +1)
    else:
        decimalOdds = "{:10.3f}".format(100 / (americanOdds * -1) + 1)
    return float(decimalOdds)

