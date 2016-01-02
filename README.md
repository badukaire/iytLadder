# iytLadder
A python script to compute stats from an IYT ladder (IYT: itsyourturn.com)

Takes as input a set of html files containing the first 50 players on a IYT
the html is parsed using the BeautifulSoup, extracts players data, basically
the rank. The rank is used to award points. These points are given in 2 
different ways: linear and exponential-negative (not sure which one is more
representative and fair).

After extracting the data, it is time to calculate for that period of time
(corresponding to the html files) the players average rating, based on the
points awarded from the rank.

For usage examples see the embedded help on IYTladder.py

