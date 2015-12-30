import sys
from bs4 import BeautifulSoup

def initObjects() :

  global gBeautifulSoup
  global gsFilename

  gBeautifulSoup = None
  gsFilename = 'iytLadderTop50.html'


def initParse() :

  global gBeautifulSoup
  global gsFilename
  try :
    # this may be sys.stdin if no filename ...
    lFile = open( gsFilename )

  except :
    print "FATAL, could not open file", lsFilename

  try :
    gBeautifulSoup = BeautifulSoup( lFile, 'html.parser' )

  except :
    print "FATAL exception during beautifulsoup constructor"

  lFile.close()


def prettyprint() :

  global gBeautifulSoup
  try :
    lsPretty = gBeautifulSoup.prettify()

  except :
    print "FATAL, during prettify ..."

  try :
    print lsPretty

  except UnicodeEncodeError :
    print "FATAL, UnicodeEncodeError printing prettify ..."
    raise


def tryThings() :

  lRanking = []
  global gBeautifulSoup
  for lSeekCaption in gBeautifulSoup.find_all( "caption" ) :
    print lSeekCaption
    print lSeekCaption.b
    for ls in lSeekCaption.strings :
      print ls
      if ls.find( "Ranking of players" ) >= 0 :
        print "found the ranking table!"
        lTable = lSeekCaption.parent
        for lTR in lTable.find_all( "tr" ) :
          print 'TR'
          lListTD = lTR.find_all( "td" )
          if len( lListTD ) < 2 :
            print "TR with less than 2 TDs, discard"
          else :
            lTDrank = lListTD[ 0 ]
            lB = lTDrank.b
            if not lB == None :
              lsRanking = lB.string
              #print "lB.string:", lsRanking
              lTDname = lListTD[ 1 ]
              lA = lTDname.a
              if not lA == None :
                #print lA
                lBA = lA.b
                if not lBA == None :
                  #print lBA
                  for ls in lBA.strings :
                    lsPlayer = ls # get last one, avoid optional 'member' symbol
                  print "ranking:", lsRanking
                  print "player:", lsPlayer
                  try :
                    liRanking = int( lsRanking )
                  except :
                    print "not a number, not a valid ranking"
                    continue
                  liPoints = 100 - liRanking
                  lRanking.append( ( lsPlayer, liRanking ) )


              else :
                print "ERROR, no TD with link found"
          print '--'

  print lRanking


initObjects()
initParse()
# prettyprint()

tryThings()



