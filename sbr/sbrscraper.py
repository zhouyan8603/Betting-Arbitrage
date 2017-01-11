import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import time

def soup_url(type_of_line, tdate):
## get html code for odds based on desired line type and date
    web_url = dict()
    web_url['ML'] = ''
    url_addon = web_url[type_of_line]
    url = 'http://www.sportsbookreview.com/betting-odds/tennis/' + url_addon + '?date=' + tdate
    raw_data = requests.get(url)
    soup= BeautifulSoup(raw_data.text, 'html.parser')
    timestamp = time.strftime("%H:%M:%S")
    return soup, timestamp

    '''
    BookID  BookName
	238 Pinnacle Sports
	349 Will Hill
	43 bet365
	93 Bookmaker
	1096 BetOnline
	227 The Greek Sportsbook
	1275 JustBet
	300 SportsInteraction
	999993 WagerWeb
	19 5Dimes
	92 Bodog
	999991 Sportsbetting
	999998 SBR Sportsbook
	1537 Sportbet
	442 IslandCasino
	123 Diamond Sportsbook
	180 Intertops
	118 betcris
	169 Heritage
	139 YouWager
	186 JazzSports
	23 ABCislands
	423 LooseLines
	83 BetUs
	626 matchbook
	999996 Bovada
	1602 GtBets
	1680 Mybookie.ag
    '''


def replace_unicode(string):
    return string.replace(u'\xa0',' ').replace(u'\xbd','.5')

def parse_and_write_data(soup, date, time):
## Parse HTML to gather line data by book
    def book_line(book_id, line_id, homeaway):
        ## Get Line info from book ID
        line = soup.find_all('div', attrs = {'class':'el-div eventLine-book', 'rel':book_id})[line_id].find_all('div')[homeaway].get_text().strip()
        return line
    if True:
        df = DataFrame(
                columns=(
     'player','Pinnacle','Will Hill','bet365','Bookmaker','BetOnline','The Greek Sportsbook','JustBet','SportsInteraction','WagerWeb','FiveDimes'))

    counter = 0
    number_of_games = len(soup.find_all('div', attrs = {'class':'el-div eventLine-rotation'})) #correct
    players = soup.find_all('div', attrs = {'class':'el-div eventLine-team'})
    for i in range(0, number_of_games):
        A = []
        H = []
        ## get line/odds info for unique book. Need error handling to account for blank data
        def try_except_book_line(id, i , x):
            try:
                return book_line(id, i, x)
            except IndexError:
                return ''
        player_A = players[i].find_all('div')[0].get_text().strip()
        pinnacle_A = 0 #try_except_book_line('238',i, 0)
        willhill_A = try_except_book_line('349',i, 0)
        betThreeSixFive_A = try_except_book_line('43',i, 0)
        bookmaker_A = try_except_book_line('93',i, 0)
        betonline_A = try_except_book_line('1096', i, 0)
        thegreeksportsbook_A = try_except_book_line('227',i, 0)
        justbet_A = try_except_book_line('1275',i, 0)
        sportsinteraction_A = try_except_book_line('300',i, 0)
        wagerweb_A = try_except_book_line('999993',i, 0)
        fivedimes_A = try_except_book_line('19',i, 0)

        player_H = players[i].find_all('div')[1].get_text().strip()

        pinnacle_H = 0 #try_except_book_line('238',i, 1)
        willhill_H = try_except_book_line('349',i, 1)
        betThreeSixFive_H = try_except_book_line('43',i, 1)
        bookmaker_H = try_except_book_line('93',i, 1)
        betonline_H = try_except_book_line('1096', i, 1)
        thegreeksportsbook_H = try_except_book_line('227',i, 1)
        justbet_H = try_except_book_line('1275',i, 1)
        sportsinteraction_H = try_except_book_line('300',i, 1)
        wagerweb_H = try_except_book_line('999993',i, 1)
        fivedimes_H = try_except_book_line('19',i, 1)

        if ") " in replace_unicode(player_A):
          A.append(str(replace_unicode(player_A)).lower().split(") ")[1])
        else:
          A.append(str(replace_unicode(player_A)).lower())
        A.append(str(pinnacle_A))
        A.append(str(willhill_A))
        A.append(str(betThreeSixFive_A))
        A.append(str(bookmaker_A))
        A.append(str(betonline_A))
        A.append(str(thegreeksportsbook_A))
        A.append(str(justbet_A))
        A.append(str(sportsinteraction_A))
        A.append(str(wagerweb_A))
        A.append(str(fivedimes_A))

        if ") " in replace_unicode(player_H):
          H.append(str(replace_unicode(player_H)).lower().split(") ")[1])
        else:
          H.append(str(replace_unicode(player_H)).lower())
        H.append(str(pinnacle_H))
        H.append(str(willhill_H))
        H.append(str(betThreeSixFive_H))
        H.append(str(bookmaker_H))
        H.append(str(betonline_H))
        H.append(str(thegreeksportsbook_H))
        H.append(str(justbet_H))
        H.append(str(sportsinteraction_H))
        H.append(str(wagerweb_H))
        H.append(str(fivedimes_H))
        ## Take data from A and H (lists) and put them into DataFrame
        df.loc[counter]   = ([A[j] for j in range(len(A))])
        df.loc[counter+1] = ([H[j] for j in range(len(H))])
        counter += 2
    return df




