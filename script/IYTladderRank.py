import sys
from bs4 import BeautifulSoup
import pickle
import math

#
# TODO
#
# * handle pickle retrieve/store exceptions!!!
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
% python IYTladderRank.py 

# use alphanumeric ID for input (html) and output (dat) filenames, in
# this case i000.html is expected as input and output is sent to p000.dat
% python IYTladderRank.py 000
# same, with i0001.html and p001.html
% python IYTladderRank.py 001

# sum 2 dat files (p000.dat, p001.dat) and store result in pickle.dat
% python IYTladderRank.py 000 001

# view 1 dat file, using special 2nd id '-' meaning none
% python IYTladderRank.py 000 -

'''
class IYTladderRank :


  def __init__( self, psId = None ) :

    self.mBeautifulSoup = None
    self.msFilename = None
    self.msId = psId

    self.initObjects()


  def initObjects( self ) :

    if self.msId == None :
      self.msFilename = 'iytLadderTop50.html'
      self.msPickleFile = 'pickle.dat'
    else :
      self.msFilename = 'i' + self.msId + '.html'
      self.msPickleFile = 'p' + self.msId + '.dat'
    print 'input:%s - output:%s' % ( self.msFilename, self.msPickleFile )


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



  def parseHtmlRanking( self ) :

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
                  if not lA == None :
                    for ls in lA.strings : # 'ISO-8859-1'
                      try :
                        lsPlayer = str( ls ) # get last one, avoid optional 'member' symbol
                      except :
                        lsPlayer = '--utf--'
                      print lsPlayer
                    print "ranking:", lsRanking
                    print "player:", lsPlayer
                    try :
                      liRanking = int( lsRanking )
                    except :
                      print "not a number, not a valid ranking"
                      continue

                    liPointsNegexp = IYTladderRank.pointsNegexp( liRanking )
                    liPointsLinear = IYTladderRank.pointsLinear( liRanking )

                    # store
                    # 1 is number of appearences, will be used for the sum
                    lTuple = ( liRanking, 1, liPointsNegexp, liPointsLinear, lsPlayer )
                    lDictRanking[ lsUserId ] = lTuple

                else :
                  print "ERROR, no TD with link found"
            print '--'

    if len( lDictRanking ) < 2 :
      print "not enough entries, return None"
      lDictRanking = None
    return lDictRanking



  # depending on the value of sDisplayMode :
  # - None : sorts by player id
  # - '-'  : sorts by average ranking
  # - 'e'  : sorts by exponential points
  # - 'l'  : sorts by linear points
  def displayDict( self, sDisplayMode ) :

    print 'ranked players =', len( self.mDictRanking )
    # TODO : use pretty
    lList = self.mDictRanking.keys()
    if sDisplayMode == None :
      lList.sort()
      for lKey in lList :
        print lKey, self.mDictRanking[ lKey ]
    else : # sort by some mode
      if sDisplayMode == '-' :
        liSortKey = 0 # tuple pos of average ranking
        lbReverse = False
      if sDisplayMode == 'e' :
        liSortKey = 2 # tuple pos of exponential points
        lbReverse = True
      if sDisplayMode == 'l' :
        liSortKey = 3 # tuple pos of linear points
        lbReverse = True

      lList1 = []
      for lKey in lList :
        lTuple = self.mDictRanking[ lKey ]
        lList1.append( lTuple )
      # print lList1
      print '============'
      lListSorted = sorted( lList1, key = lambda tup : tup[ liSortKey ], reverse = lbReverse )
      for lPlayerTuple in lListSorted :
        IYTladderRank.displayPlayer( lPlayerTuple )




  def fpick_retrieve( self ) :

    liRet = 0 # OK
    try :
      lFile = open( self.msPickleFile )
      try :
        lDict = pickle.load( lFile )
        self.mDictRanking = lDict # to prevent errors while reading
      except :
        print 'fpick_retrieve.read(), corrupted file ' + self.msPickleFile
      lFile.close()

    except IOError :
      liRet = 1 # error
      print 'FATAL: fpick_retrieve.read(), could not read file ' + self.msPickleFile
      raise # while not implemented exception / return code handling

    return liRet



  def fpick_store( self ) :

    liRet = 0 # OK
    try :

      lFile = open( self.msPickleFile, 'w' )
      pickle.dump( self.mDictRanking, lFile )

      lFile.close()

    except IOError :
      liRet = 1 # error
      print 'fpick_store(), corrupted file ' + self.msPickleFile

    return liRet



  @staticmethod
  def sumDictRanking( pDict1, pDict2 ) :

    # lists
    lKeys1 = pDict1.keys()
    lKeys2 = pDict2.keys()

    lKeys = list( lKeys1 ) # duplicate, not a pointer
    lKeys.extend( lKeys2 ) # still a list
    lSetKeys = set( lKeys ) # removes duplicates
    print 'keys: %d, %d : %d' % ( len( lKeys1 ), len( lKeys2 ), len( lSetKeys ) )

    lDictSum = {}
    for liKey in lSetKeys :
      try :
        lD1 = pDict1[ liKey ]
        liRank1  = lD1[ 0 ]
        liTimes1 = lD1[ 1 ]
        liPexp1  = lD1[ 2 ]
        liPlin1  = lD1[ 3 ]
        lsName1  = lD1[ 4 ]
      except :
        liRank1  = 0
        liTimes1 = 0
        liPexp1  = 0
        liPlin1  = 0
        lsName1  = '-'
      try :
        lD2 = pDict2[ liKey ]
        liRank2  = lD2[ 0 ]
        liTimes2 = lD2[ 1 ]
        liPexp2  = lD2[ 2 ]
        liPlin2  = lD2[ 3 ]
        lsName2  = lD2[ 4 ]
      except :
        liRank2  = 0
        liTimes2 = 0
        liPexp2  = 0
        liPlin2  = 0
        lsName2  = '-'
      print '%s : %d + %d, %d + %d, %s / %s ' % ( liKey, liRank1, liRank2 , liTimes1, liTimes2 , lsName1, lsName2 )
      liSumRank  = liRank1 + liRank2
      liSumTimes = liTimes1 + liTimes2
      lsSumName  = lsName2 if not lsName2 == '-' else lsName1
      liSumPexp = liPexp1 + liPexp2
      liSumPlin = liPlin1 + liPlin2
      lTuple = ( liSumRank, liSumTimes, liSumPexp, liSumPlin, lsSumName )
      IYTladderRank.displayPlayer( lTuple )

      lDictSum[ liKey ] = lTuple

    # return None if error ...
    return lDictSum



  @staticmethod
  def displayPlayer( pPlayerTuple ) :
    if len( pPlayerTuple ) == 5 :
      print '#%03d (%02d) = %4d - %4d %s' % pPlayerTuple
    else :
      print 'N/A'



  # note: at least 2 guaranteed (script syntax) => need not check len
  # if 2nd is '-' will just read and display the 1st
  @staticmethod
  def readSum( pListIds ) :

    lIYTladderRankSum = IYTladderRank()

    lsId1 = pListIds[ 0 ]
    lIYTladderRank1 = IYTladderRank( lsId1 )
    lIYTladderRank1.fpick_retrieve()

    lsId = pListIds[ 1 ]
    if lsId[ 0 ] == '-' :
      lsDisplayMode = None if len( lsId ) == 1 else lsId[ 1 ]
      lIYTladderRank1.displayDict( lsDisplayMode )
    else :
      for lsId in pListIds[ 1 : ] :
        lIYTladderRank2 = IYTladderRank( lsId )
        lIYTladderRank2.fpick_retrieve()

        lDict1 = lIYTladderRank1.mDictRanking
        lDict2 = lIYTladderRank2.mDictRanking

        lDict = IYTladderRank.sumDictRanking( lDict1, lDict2 )
        if not lDict == None :
          lIYTladderRank1.mDictRanking = lDict

      lIYTladderRankSum.mDictRanking = lIYTladderRank1.mDictRanking
      # average
      liNum = len( pListIds )
      for lKey in lIYTladderRankSum.mDictRanking.keys() :
        lPlayer = lIYTladderRankSum.mDictRanking[ lKey ]
        lPlayer2 = (
          lPlayer[ 0 ] / lPlayer[ 1 ],
          lPlayer[ 1 ],
          lPlayer[ 2 ] / liNum,
          lPlayer[ 3 ] / liNum,
          lPlayer[ 4 ],
        )
        lIYTladderRankSum.mDictRanking[ lKey ] = lPlayer2

      lIYTladderRankSum.fpick_store()



  # negative exponential function
  # yields :
  # * 100 for 1
  # * 1 for 50
  # * 0 for 51
  @staticmethod
  def pointsNegexp( iRank ) :
    lfMagnifier = 1.0
    lfMagicConstant = 10.640215
    lfExp = ( 1 - iRank ) * lfMagnifier / lfMagicConstant
    #print 'exp =', lfExp
    lfBase = ( math.e ** lfExp )
    lfPoints = 100*lfBase
    liPoints = int( lfPoints )
    print lfPoints, liPoints
    return liPoints


  # negative exponential function
  # yields :
  # * 100 for 1
  # * 1 for 50
  # * 0 for 51
  @staticmethod
  def pointsLinear( iRank ) :
    liPoints = 100 - 2 * ( iRank - 1 )
    print liPoints
    return liPoints


  def process( self ) :

    self.mBeautifulSoup = self.initParse()
    if not self.mBeautifulSoup == None :
      self.mDictRanking = self.parseHtmlRanking()
      if not self.mDictRanking == None :
        self.fpick_store()
        self.mDictRanking = None
        self.fpick_retrieve()
        print self.mDictRanking




if __name__ == "__main__":

  
  '''
  # exp test
  IYTladderRank.pointsNegexp( int( sys.argv[ 1 ] ) )
  # linear test
  IYTladderRank.pointsLinear( int( sys.argv[ 1 ] ) )
  sys.exit(0)
  '''

  if len( sys.argv ) > 2 :
    # 1 : may change when getopt is used
    IYTladderRank.readSum( sys.argv[ 1 : ] )
  else :
    if len( sys.argv ) == 1 :
      lIYTladderRank = IYTladderRank()
    else :
      lIYTladderRank = IYTladderRank( sys.argv[ 1 ] )
    lIYTladderRank.process()


