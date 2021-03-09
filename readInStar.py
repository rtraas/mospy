def readInStar(astroInputs):
    # Read in the needed packages and methods
    import inspect, os
    import numpy as np
    from .isolateValue import isolateValue

    # Finds the file and opens it
    current_dir = str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    file_dir = current_dir + ('/starTypes/%s.txt' %(astroInputs.starType).upper())
    starFile = open(file_dir, 'r')

    # ---Store and Print the Variables---
    # Import function to issolate the values for parsing.
    # Looped using a list
    heading    = starFile.readline()
    starInfo = ['Mass', 'Radius', 'Lum', 'HZin', 'HZmid']
    units = ['Msun', 'Rsun', 'Lsun', 'AU', 'AU']
    for i in range(0,len(starInfo)):
        starInfo[i] = isolateValue(starFile.readline())
    starFile.close()

    # If no star information is given, assign stellar parameter to what's in the file
    # If it's specified, it's already assigned in runSim.py
    if astroInputs.starMass == None:
        astroInputs.starMass = starInfo[0]
    if astroInputs.starRadius == None:
        astroInputs.starRadius = starInfo[1]
    if astroInputs.starLum == None:
        astroInputs.starLum = starInfo[2]
    # If planetLoc is not a string, assume planet loc to be given in AU.
    if type(astroInputs.HZ) == str:
        if (astroInputs.HZ).upper() == 'HZIN':
            astroInputs.HZ = starInfo[3] # Planet loc in AU (HZin)
        elif (astroInputs.HZ).upper() == 'HZMID':
            astroInputs.HZ = starInfo[4] # Planet loc in AU (HZmid)

    # Print the read in star's information
    print("Star Mass (Msun): ", astroInputs.starMass)
    print("Star Radius (Rsun): ", astroInputs.starRadius)
    print("Star Luminosity (Lsun): ", astroInputs.starLum)
    print("Chosen HZ (AU): ", astroInputs.HZ)

