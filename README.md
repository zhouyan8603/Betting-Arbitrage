Sports Arbitrage
================


This is a basic python alert service for Sports Arbitrage. It scans odds across:
* Betfair 
* Pinnacle
* William Hill
* bet365
* Bookmaker
* BetOnline
* The Greek Sportsbook 
* JustBet
* SportsInteraction 
* WagerWeb 
* 5Dimes
though it can easily be modified to include:
* Bodog
* Sportsbetting
* SBR Sportsbook
* Sportbet
* IslandCasino
* Diamond Sportsbook
* Intertops
* betcris
* Heritage
* YouWager
* JazzSports
* ABCislands
* LooseLines
* BetUs
* matchbook
* Bovada
* GtBets
* Mybookie.ag

Work is underway to MarathonBet and Ladbrokes in the near future.


What is Arbitrage?
------------------





Getting a betfair API key
-------------------------

In order to use the Betting & Accounts API, you need to have an Application Key. The Application Key identifies your API client.  Two App Keys are assigned to a single Betfair account, one live App Key and one delayed App Key for testing.
The delayed API key will give a delay on all odds feeds from the listMarketBook operation. This script can be used using only the delayed API key, however red herrings's may appear, and arbs may be missede due to the delay in the feeds.

To obtain a betfair API key, you must first create an account on [Betfair](https://www.betfair.com/exchange/). 
Once this is done:
* Log in to your Betfair exchange account (make sure to do this first).
* Go to the [Accounts API Visualiser](https://developers.betfair.com/visualisers/api-ng-account-operations/) and ensure the the Endpoint "UK" is selected.  
* Select the **createDeveloperAppKeys** operation from the list of Operations on the top left hand side of the visualiser.
* Enter your **Application Name** (this must be unique) in the 'Request' column.  The Application Name can be any name of your choice, but like your Betfair username, must be unique.
* Press Execute at the bottom of the 'Request' column.
* Two Application Keys will then be created and displayed in the **Developer Apps** column of the demo tool.

You will only need to create an application key once. See [here](http://docs.developer.betfair.com/docs/display/1smk3cen4v3lu3yomq5qye0ni/Application+Keys) learn more, and to find out about activating the live API key


How to use the script?
----------------------

Dependencies:
* urllib
* urllib2
* json
* requests
* BeautifulSoup
* Pandas
* unicodedata
* numpy
* pytz
* sqlite3

To use the script, you will first have to fill out the betfair/userinfo.py file. It should contain your Betfair username, password, and API key from above.
Provided this is done and all dependencies are installed, the bot should run infinitely (until stopped) by simply running  `python master.py`.

It will return arbitrage opportunities in the form of:
`We will get 5% ROI if we bet 70% on N Djokovic at 1.5 and 30% on R Nadal at 3.5`

(Info as to which book each odds are available at will be in the next commit)

This means that if you are betting €/$/£500, you should bet 350 on N Djokovic and 150 on Nadal, to get a guaranteed profit of €/$/£25.

Disclaimer
----------
This is intended purely as an experiment and it is not recommended that anyone pursue the alerts provided by this script with their real money. I will not be devoting any time to maintaining this bot, and as such bugs can creep in which can challenge the authenticity of an arb. Combined with this, arbitrage is a risky endeavour even with a perfect alert service. I repeat the earlier mantra: do not practice this with money.

This work is completely open sourced for anyone to use for any purpose they see fit. I greatly welcome any contributions to the project. If implementing my work somewhere else I simply ask that you accredit me, though please note that not all work included here is mine (see below).

The code here contains pieces taken from the repositories below:
* [Betfair](https://github.com/betfair) - Used for calls to the Betfair API
* [SharpChiCity](https://github.com/SharpChiCity) - Modified version of this was used to scrape Sportsbookreview's odds feed.



