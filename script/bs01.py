import sys
from bs4 import BeautifulSoup
import pickle


#
# TODO sum a set of files, not just 2
#
'''
parses the html file resulting from a query of the first 50 players
on a IYT ladder, with a URL such as:
http://www.itsyourturn.com/iyt.dll?ldr?fn=103&id=353&st=1&end=50

it has 2 typical usage modes:
- parse an IYT-ladder html file, store result in a file, use 0 or 1 params
- sum 2 result files, giving the ladder ranking over a given time

usage examples: 

# use default input and output file names: iytLadderTop50.html and pickle.dat
% python s.py 

# use alphanumeric suffix for input and output filenames: i000.html and p000.dat
% python s.py 000
# same, with i0001.html and p001.html
% python s.py 001

# sum 2 dat files (p000.dat, p001.dat) and store in pickle.dat
% python s.py 000 001

'''
class IYTladderRank :

  def __init__( self ) :
    self.mBeautifulSoup = None
    self.msFilename = None


  def initObjects( self, psFile = None ) :

    if psFile == None :
      self.msFilename = 'iytLadderTop50.html'
    else :
      self.msFilename = psFile


  def initParse( self ) :

    lBeautifulSoup = None
    try :
      # this may be sys.stdin if no filename ...
      lFile = open( self.msFilename )

    except :
      print "FATAL, could not open file", self.msFilename
      return lBeautifulSoup # returns None, file is not open

    try :
      self.mBeautifulSoup = BeautifulSoup( lFile, 'html.parser' )

    except :
      print "FATAL exception during beautifulsoup constructor"

    lFile.close()
    return self.mBeautifulSoup



  def parseRanking( self ) :

    lDictRanking = {}
    for lSeekCaption in self.mBeautifulSoup.find_all( "caption" ) :
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
                    # it could also be negative exponential
                    liPoints = 100 - liRanking

                    # store
                    lDictRanking[ lsUserId ] = ( liRanking, lsPlayer )

                else :
                  print "ERROR, no TD with link found"
            print '--'

    if len( lDictRanking ) < 2 :
      print "not enough entries, return None"
      lDictRanking = None
    return lDictRanking



  @staticmethod
  def sumDictRanking( pDict1, pDict2 ) :

    # lists
    lKeys1 = pDict1.keys()
    lKeys2 = pDict2.keys()

    lKeys = list( lKeys1 ) # duplicate, not a pointer
    lKeys.extend( lKeys2 ) # still a list
    lSetKeys = set( lKeys ) # removes duplicates

    lDictRanking[ lsUserId ] = ( liRanking, lsPlayer )



  def process( self, psFile = None ) :

    self.initObjects( psFile ) # may pass a file name here
    self.mBeautifulSoup = self.initParse()
    if not self.mBeautifulSoup == None :
      self.mDictRanking = self.parseRanking()


if __name__ == "__main__":

  lIYTladderRank = IYTladderRank()
  lIYTladderRank.process()


