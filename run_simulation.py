import time
import eSims
import sys

# Initialize variable
inputfile='INFILE'

# If only one sim is requested
if len(sys.argv) > 1:
    inputfile=sys.argv[1]

# for looping (ie multiple inputfiles on commandline)
# Initialize variable
inputlist=['INFILE']
if len(sys.argv)>1:
   inputlist=sys.argv[1:]
   for inputfile in inputlist:
      inputfile=inputfile.replace('.py','')
      start= time.perf_counter()
      eSims.doSim(inputfile)
      end=time.perf_counter()
      elapsed=end-start
      print("elapsed time= {:.12f} seconds".format(elapsed))

