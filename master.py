from tools import calculator as calc
from tools import sqlitecommands as sq
from sbr import sbrscraper as sbr
#from betfair import bfairapi as b
from pinnacle import pinnaclexml as pin
from datetime import date
# import socket
# import socks

"""
def connectTor():
## Connect to Tor for privacy purposes
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9150, True)
    socket.socket = socks.socksocket
    print("connected to Tor!")
"""

# Create sql connection
con = sq.conn


# Write SBR dataframe to sql
def writeSBR():
  todays_date = str(date.today()).replace('-','')
  soup, time_ml = sbr.soup_url('ML', todays_date)
  df = sbr.parse_and_write_data(soup,todays_date,time_ml) # Getting dataframe of SBR odds
  df.to_sql('tennis',con,schema=None,if_exists='replace',index=True,index_label=True,chunksize=None,dtype=None) # Writing dataframe to master.db-tennis. if_exist='replace means that if the table is already there, it will be deleted and replaced.

# Add names from pinnacle

# Update pinnacle odds
def writePinnacle():
  fullListing = pin.UpdateFeed()[0]
  for event in fullListing:
    try:
      playerOne = pin.sortType(event,'Tennis','Match')[0].lower().replace("'","")
      playerOneOdds = pin.sortType(event,'Tennis','Match')[2]
      playerTwo = pin.sortType(event,'Tennis','Match')[3].lower().replace("'","")
      playerTwoOdds = pin.sortType(event,'Tennis','Match')[5]
      print playerOne, playerOneOdds, playerTwo, playerTwoOdds
      #sq.dynamic_data_entry('Pinnacle',playerOne)
      sq.update(playerOne,'Pinnacle',playerOneOdds)
      sq.update(playerTwo,'Pinnacle',playerTwoOdds)
    except TypeError:
      pass
  con.commit()

# Add names from betfair
# Update betfair odds
#writeBetfair():

# Add names from marathonbet
# Update marathonbet odds

# Make dictionary of competitors {playerOne: playerTwo}

# Function saying if there is an arb


# Iterate through database (dictionary) looking for arbs


