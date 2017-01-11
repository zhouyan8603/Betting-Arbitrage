#! python3

# calculator.py - Contains calculators needed


from __future__ import division
import math

"""
Function which turns Fractional odds into decimal odds
"""
def fractionToDecimal(fractional_odds):
	return 1.+ eval(fractional_odds)

"""
Function which turns US odds to decimal
"""

def USToDecimal(us_odds):
    if '+' in us_odds:
      return ((float(us_odds.replace('+','').replace('-','')))/100.) +1.
    else:
      return ((100./float(us_odds.replace('+','').replace('-','')))) +1.


"""
Function which turns Lay odds into back odds
http://www.bettingtools.co.uk/back-lay-equivs
"""

def layToBack(layOdds):
	return (1./float(layOdds)-1.)+1.



"""
Arb Calculator (Back-Back). Works out if an arb exists when given odds of two mutually exclusive events. Gives ROI for arb
"""

def BackBack(stake,underdog,favourite):
    underdog_amount = (float(stake)*float(favourite))/(float(underdog)+float(favourite))
    favourite_amount = (float(stake)*float(underdog))/(float(underdog)+float(favourite))
    profit = (float(stake)*float(underdog)*float(favourite))/(float(underdog)+float(favourite))-float(stake)
    return underdog_amount, favourite_amount,profit

"""
Arb Calculator (Lay-Back). Works out if an arb exists for both backing and laying an event. Gives ROI.
"""
def LayBack(stake,layOdds,backOdds):
	return BackBack(stake,layToBack(layOdds),backOdds)

"""
Arb Calculator (Lay-Lay). Works out if an arb exists for laying 2 mutually exclusing events at different exchanges
"""

def LayLay(stake,underdog,favourite):
	return BackBack(stake,layToBack(underdog),layToBack(favourite))

"""
Arb Calculator (3-way)
"""

"""
Middle Calculator (asian handicap)
"""






