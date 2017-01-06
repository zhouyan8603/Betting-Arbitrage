from __future__ import division
import time
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
from dateutil.parser import parse
import datetime
import string
import requests
import pytz
import pandas.io.sql as pd_sql
import numpy as np
import pincalc
from dateutil.tz import tzlocal

# To convert US odds, use pincalc

myTimeZone = pytz.timezone('Europe/Dublin') # YOUR TIME ZONE
eastern = pytz.timezone('US/Eastern')
gmt = pytz.timezone('GMT')


def UpdateFeed():
    url = 'http://xml.pinnaclesports.com/pinnacleFeed.aspx?'
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    events = soup.findAll('event')
    return events, datetime.datetime.now()

def FixNames(input_str):
    nkfd = unicodedata.normalize('NFKD', input_str)
    ascii = nkfd.encode('ASCII', 'ignore')
    return ascii.replace('amp;','')

def Unpacker(event):
  playerOne = event.findAll('participant')[0].participant_name.string
  playerOneVisitHome = event.findAll('participant')[0].visiting_home_draw.string
  playerTwo = event.findAll('participant')[1].participant_name.string
  playerTwoVisitHome = event.findAll('participant')[1].visiting_home_draw.string
  if playerOneVisitHome == 'Visiting':
    mlPlayerOne = event.moneyline_visiting.string
    mlPlayerTwo = event.moneyline_home.string
  elif playerOneVisitHome == 'Home':
    mlPlayerOne = event.moneyline_home.string
    mlPlayerTwo = event.moneyline_visiting.string
  else:
    print 'Couldnt work out if players were visiting or home for pinnacle for ' + event
  return playerOne, playerOneVisitHome, mlPlayerOne, playerTwo, playerTwoVisitHome, mlPlayerTwo

def sortType(event,sport,gametype):
  if event.sporttype.string == sport:
    try:
      if event.period_description.string == gametype:
        return Unpacker(event)
      else:
        pass
    except AttributeError:
      pass
  else:
    pass



