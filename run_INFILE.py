import time; import mospy


start= time.perf_counter()
mospy.doSim('INFILE');
end=time.perf_counter()
elapsed=end-start
print("elapsed time= {:.12f} seconds".format(elapsed))

