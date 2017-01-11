#!/usr/bin/env python

import urllib
import urllib2
import json
import datetime
import sys
import userinfo

def getSESSIONToken(username, password):

        login_data = urllib.urlencode({
                                        'username' : username,
                                        'password' : password,
                                        'product' : 'exchange',
                                        'url' : 'https://www.betfair.com/Fexchange/login/success/rurl/https://www.betfair.com/Fexchange'
                                        })
        url = "https://identitysso.betfair.com/api/login"
        req = urllib2.Request(url, login_data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        cookie = response.info()['set-cookie']
        idx = cookie.find("ssoid=")+6
        SESSION_TOKEN = cookie[idx:].split(";")[0]

        return SESSION_TOKEN

"""
make a call API-NG
"""

def callAping(jsonrpc_req):
    try:
        req = urllib2.Request(url, jsonrpc_req, headers)
        response = urllib2.urlopen(req)
        jsonResponse = response.read()
        return jsonResponse
    except urllib2.URLError:
        print 'Oops no service available at ' + str(url)
        exit()
    except urllib2.HTTPError:
        print 'Oops not a valid operation from the service ' + str(url)
        exit()


"""
calling getEventTypes operation
"""

def getEventTypes():
    event_type_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
    #print 'Calling listEventTypes to get event Type ID'
    eventTypesResponse = callAping(event_type_req)
    eventTypeLoads = json.loads(eventTypesResponse)
    """
    print eventTypeLoads
    """

    try:
        eventTypeResults = eventTypeLoads['result']
        return eventTypeResults
    except:
        print 'Exception from API-NG' + str(eventTypeLoads['error'])
        exit()


"""
Extraction eventypeId for eventTypeName from evetypeResults
"""

def getEventTypeIDForEventTypeName(eventTypesResult, requestedEventTypeName):
    if(eventTypesResult is not None):
        for event in eventTypesResult:
            eventTypeName = event['eventType']['name']
            if( eventTypeName == requestedEventTypeName):
                return  event['eventType']['id']
    else:
        print 'Oops there is an issue with the input'
        exit()


"""
Calling marketCatalouge to get marketDetails
"""

def getMarketCatalogue(eventTypeID):
    if (eventTypeID is not None):
        #print 'Calling listMarketCatalouge Operation to get MarketID and selectionId'
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        market_catalogue_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventTypeIds":["' + eventTypeID + '"],"marketBettingTypes":["ODDS"],"marketTypeCodes":["MATCH_ODDS"],'\
                                                                                                                                                             '"marketStartTime":{"from":"' + now + '"}},"sort":"FIRST_TO_START","maxResults":"200","marketProjection":["RUNNER_METADATA"]}}'

       # print  market_catalogue_req

        market_catalogue_response = callAping(market_catalogue_req)

        #print market_catalogue_response

        market_catalouge_loads = json.loads(market_catalogue_response)
        try:
            market_catalouge_results = market_catalouge_loads['result']
            return market_catalouge_results
        except:
            print  'Exception from API-NG' + str(market_catalouge_loads['error'])
            exit()


def getMarketId(marketCatalogueResult):
    if( marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            return market['marketId']


def getSelectionId(marketCatalogueResult):
    if(marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            return market['runners'][0]['selectionId']


def getMarketBookBestOffers(marketId):
    #print 'Calling listMarketBook to read prices for the Market with ID :' + marketId
    market_book_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": {"marketIds":["' + marketId + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS"]}}}'
    """
    print  market_book_req
    """
    market_book_response = callAping(market_book_req)
    """
    print market_book_response
    """
    market_book_loads = json.loads(market_book_response)
    try:
        market_book_result = market_book_loads['result']
        return market_book_result
    except:
        print  'Exception from API-NG' + str(market_book_result['error'])
        exit()


def printPriceInfo(market_book_result):
    if(market_book_result is not None):
        print 'Please find Best three available prices for the runners'
        for marketBook in market_book_result:
            runners = marketBook['runners']
            for runner in runners:
                print 'Selection id is ' + str(runner['selectionId'])
                if (runner['status'] == 'ACTIVE'):
                    print 'Available to back price :' + str(runner['ex']['availableToBack'])
                    print 'Available to lay price :' + str(runner['ex']['availableToLay'])
                else:
                    print 'This runner is not active'


def placeFailingBet(marketId, selectionId):
    if( marketId is not None and selectionId is not None):
        print 'Calling placeOrder for marketId :' + marketId + ' with selection id :' + str(selectionId)
        place_order_Req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/placeOrders", "params": {"marketId":"' + marketId + '","instructions":'\
                                                                                                                              '[{"selectionId":"' + str(
            selectionId) + '","handicap":"0","side":"BACK","orderType":"LIMIT","limitOrder":{"size":"0.01","price":"1.50","persistenceType":"LAPSE"}}],"customerRef":"test12121212121"}, "id": 1}'
        """
        print place_order_Req
        """
        place_order_Response = callAping(place_order_Req)
        place_order_load = json.loads(place_order_Response)
        try:
            place_order_result = place_order_load['result']
            print 'Place order status is ' + place_order_result['status']
            """
            print 'Place order error status is ' + place_order_result['errorCode']
            """
            print 'Reason for Place order failure is ' + place_order_result['instructionReports'][0]['errorCode']
        except:
            print  'Exception from API-NG' + str(place_order_load['error'])
        """
        print place_order_Response
        """


url = "https://api.betfair.com/exchange/betting/json-rpc/v1"



headers = { 'X-Application' : 'xxxxxx', 'X-Authentication' : 'xxxxx' ,'content-type' : 'application/json' }


appKey = userinfo.appKey
sessionToken = getSESSIONToken(userinfo.username, userinfo.password)
headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}


def playerOdds(marketId,playerNumber,BackOrLay): #Need to write 'Back' or 'Lay' in argument (with inverted commas)
	return getMarketBookBestOffers(marketId)[0]['runners'][playerNumber]['ex']['availableTo'+BackOrLay][0]['price']


def bfairRenamer(string):
	if '/' in string:
		cutString = string.split('/')
		cutString.sort()
		return  cutString[0]+ ' ' + cutString[1]
	else:
		return string.split()[0][0] + ' ' + string.split()[1]

market_catalogue = getMarketCatalogue('2')

playerOne = []
playerTwo = []
backOddsOne = []
backOddsTwo = []

for i in range(len(market_catalogue)):
	playerOne.append(bfairRenamer(market_catalogue[i]['runners'][0]['runnerName']))
	playerTwo.append(bfairRenamer(market_catalogue[i]['runners'][1]['runnerName']))
	backOddsOne.append(playerOdds(market_catalogue[i]['marketId'],0,'Back'))
	backOddsTwo.append(playerOdds(market_catalogue[i]['marketId'],1,'Back'))




