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

  lDictRanking = {}
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
                lsUrl = lA[ 'href' ]
                print lsUrl
                liPos = lsUrl.find( 'userid=' )
                if liPos >= 0 :
                  lsUserId = lsUrl[ liPos + 7 : ].split( '&' )[ 0 ]
                  print lsUserId
                  if len( lsUserId ) < 5 : continue
                else : continue
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

                  # this should be on the wrapper
                  liPoints = 100 - liRanking

                  # store
                  lDictRanking[ lsUserId ] = ( liRanking, lsPlayer )

              else :
                print "ERROR, no TD with link found"
          print '--'

  return lDictRanking



initObjects()
initParse()
# prettyprint()

tryThings()



