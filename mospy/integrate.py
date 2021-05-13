def integrate(sim, astroInputs, rebInputs, simResults, energy, plotTypes):
    # Import packages and methods from other classes
    import numpy as np
    import rebound
    #import matplotlib.pyplot as plt
    import math
    from .Energy import Energy
    from .rotTransform import rotTransform
    from .archive import Archive

    # Assign the sim particles to variable p.
    p = sim.particles
    #fresult=simResults.SimResults_new
    # The amount of steps in the simulation.
    Noutputs = int(rebInputs.outputPoints*rebInputs.orbits)
    # The length of the simulation in seconds.
    simlength = rebInputs.orbits*simResults.torbMirror
    # Creates all the time steps of the simulation. Used mainly for plotting in plotSims.py.
    times = np.linspace(0, simlength, Noutputs + 1) # Fixed bug here, used to not have + 1
    # Record at what point the simulation ends. Also, records the timestamp for each
    # integration loop.
    integrateEndTime=0
    # Record the timesteps of the simulation to properly index the recorded data
    # in simResults.py.
    ts = 0
    megno=-1
    #quick test of
    #sim.N_active=2

    # Define a minimum distance for collision. Used for collision detection.
    minDist = astroInputs.planetRadius + astroInputs.atmos
    sim.exit_min_distance = minDist
    # Creates a loop that iterates Noutputs + 1's amount for integrating.
    print('last input time : ',times[-1])
    sim.status()
    
    arxiv = Archive()
    
    for i,time in enumerate(times):

        #if (True): # Uncomment to remove crash detection
        # Do the integration. Uses exactFinishTime parameter specified in
        # the infile.
        try:
           sim.integrate( time, exact_finish_time = rebInputs.exactFinishTime )
        except rebound.Encounter as error:
           print("ENCOUNTER OCCURS")
           print(error)

        integrateEndTime=sim.t # Update integration time.

        if rebInputs.outputMegno:
            megno=sim.calculate_megno()

        simResults.newResults.append(p,sim.dt,sim.t,time,megno)
        if astroInputs.starType == None: # If there is no star, update only mirror and planet coord & vel
            coordTempPlanet = [p[0].x,  p[0].y,  p[0].z]
            velTempPlanet   = [p[0].vx, p[0].vy, p[0].vz]
            accelTempPlanet = [p[0].ax, p[0].ay, p[0].az]

            # Need both if statements because we created a dummy particle
            # thus the indexes are off.
            # TODO Perhaps add the dummy particle first so we can
            # keep the indexes the same and we just need one if statement
            # adding the star and then outside the if statement we
            # add the planet and mirror coordinates because the indexes
            # will be the same regardless of if there is a star or not.
            coordTempMirror = [p[2].x,  p[2].y,  p[2].z]
            velTempMirror   = [p[2].vx, p[2].vy, p[2].vz]
            accelTempMirror = [p[2].ax, p[2].ay, p[2].az]

        if astroInputs.starType != None: # If there is a star, update all three particles.
            coordTempStar   = [p[0].x,  p[0].y,  p[0].z]
            velTempStar     = [p[0].vx, p[0].vy, p[0].vz]
            accelTempStar   = [p[0].ax, p[0].ay, p[0].az]

            coordTempPlanet = [p[1].x,  p[1].y,  p[1].z]
            velTempPlanet   = [p[1].vx, p[1].vy, p[1].vz]
            accelTempPlanet = [p[1].ax, p[1].ay, p[1].az]

            coordTempMirror = [p[2].x,  p[2].y,  p[2].z]
            velTempMirror   = [p[2].vx, p[2].vy, p[2].vz]
            accelTempMirror = [p[2].ax, p[2].ay, p[2].az]

        # Calculate and save the current simulation energy.
        energyTemp = sim.calculate_energy()
        energy.saveEnergy(energyTemp)

        # Update the number of timesteps.
        ts = ts + 1

        # Saves particle conditions
        if astroInputs.starType == None: # If there is no star, only record the planet/mirror info
            simResults.saveData(None, None, None,
                                coordTempPlanet, velTempPlanet, accelTempPlanet,
                                coordTempMirror, velTempMirror, accelTempMirror,
                                time,integrateEndTime, sim.dt)
        if astroInputs.starType != None: # If there is a star, record the star info too.
            simResults.saveData(coordTempStar, velTempStar, accelTempStar,
                                coordTempPlanet, velTempPlanet, accelTempPlanet,
                                coordTempMirror, velTempMirror, accelTempMirror,
                                time,integrateEndTime, sim.dt)
        if astroInputs.starType != None:
            dist = math.sqrt((p[2].x-p[1].x)**2 + (p[2].y-p[1].y)**2 + (p[2].z-p[1].z)**2)
            mirrorVel = math.sqrt((p[2].vx-p[1].vx)**2 + (p[2].vy-p[1].vy)**2 + (p[2].vz-p[1].vz)**2)
        if astroInputs.starType == None:
            dist = math.sqrt((p[2].x-p[0].x)**2 + (p[2].y-p[0].y)**2 + (p[2].z-p[0].z)**2)
            mirrorVel = math.sqrt((p[2].vx-p[0].vx)**2 + (p[2].vy-p[0].vy)**2 + (p[2].vz-p[0].vz)**2)
        # Calculate the mirror's escape velocty
        escVel = math.sqrt((2*sim.G*astroInputs.planetMass)/dist)

        # If the mirror crashed or escaped orbit, stop the simulation.
        # Considered a collision if within a certain distance of planet surface
        if (dist < minDist or mirrorVel > escVel):
            if (dist <= astroInputs.planetRadius + astroInputs.atmos):
                print("Collision with planet.")
            if (mirrorVel >= escVel):
                print("Mirror reached escape velocity.")
            # If the simulation stopped for any other reason, tell the user
            # the current stats.
            print("Sim stopped before specified orbit.")
            print("Distance from planet (m) - Planet Radius + Atmosphere (m): ")
            print("    ", dist, " - ", astroInputs.planetRadius + astroInputs.atmos)
            print("Mirror Vel (m/s) - Mirror Escape Vel (m/s): ")
            print("    ", mirrorVel, " - ", escVel)
            # Breaks the integration.
            break
    print ('simulation end time - ',sim.t)
    # ---Transform the Coordinates to a Rotating Reference Frame--- 
    # Create arrays for new rotating reference fram coordinates.
    planetRRFx = np.zeros(Noutputs + 1)
    planetRRFy = np.zeros(Noutputs + 1)
    mirrorRRFx = np.zeros(Noutputs + 1)
    mirrorRRFy = np.zeros(Noutputs + 1)
    # Finding XY coordinates. Don't need Z because the planet orbits in the XY plane.
    pX = np.array([x[0] for x in simResults.coordPlanet])
    pY = np.array([y[1] for y in simResults.coordPlanet])
    pZ = np.array([z[2] for z in simResults.coordPlanet])  #added z info
    mX = np.array([x[0] for x in simResults.coordMirror])
    mY = np.array([y[1] for y in simResults.coordMirror])
    mZ = np.array([z[2] for z in simResults.coordMirror])  #added z info
    if astroInputs.starType != None: # If there is a star, calculate the star coordinated too.
        sX = np.array([x[0] for x in simResults.coordStar])
        sY = np.array([y[1] for y in simResults.coordStar])
        sZ = np.array([z[2] for z in simResults.coordStar])  #added z info
        # Finding theta (angle of Earth in its orbit).
        theta = np.arctan2(pY-sY,pX-sX) # Translate the planet because the star may move.
        for t in range(0,ts):
            # Do the transformation and save the rotating reference frame (RRF) coord.
            planetxRRFy = rotTransform(pX[t]-sX[t],pY[t]-sY[t], theta[t])
            planetRRFx[t] = planetxRRFy[0]
            planetRRFy[t] = planetxRRFy[1]
            mirrorxRRFy = rotTransform(mX[t]-sX[t],mY[t]-sY[t],theta[t])
            mirrorRRFx[t] = mirrorxRRFy[0]
            mirrorRRFy[t] = mirrorxRRFy[1]
            coordRRFTempPlanet = [planetRRFx[t], planetRRFy[t], pZ[t]-sZ[t]]
            coordRRFTempMirror = [mirrorRRFx[t], mirrorRRFy[t], mZ[t]-sZ[t]]
#            coordRRFTempPlanet = [planetRRFx[t], planetRRFy[t], 0]
#            coordRRFTempMirror = [mirrorRRFx[t], mirrorRRFy[t], 0]
            coordRRFTempStar = [0, 0, 0] # 14 June 2018 changed x,y from None to 0.
            # Save the transformed coordinates to the simResults object to be used
            # in plotSim.py for graphing.
            simResults.saveTransform(coordRRFTempStar, coordRRFTempPlanet, coordRRFTempMirror)
    else:
        theta = np.arctan2(pY,pX) # No need to translate the planet if it's at the origin
        for t in range(0,ts):
                # Do the transformation and save the rotating reference frame (RRF) coord.
                planetxRRFy = rotTransform(pX[t],pY[t], theta[t])
                planetRRFx[t] = planetxRRFy[0]
                planetRRFy[t] = planetxRRFy[1]
                mirrorxRRFy = rotTransform(mX[t],mY[t],theta[t])
                mirrorRRFx[t] = mirrorxRRFy[0]
                mirrorRRFy[t] = mirrorxRRFy[1]
                coordRRFTempPlanet = [planetRRFx[t], planetRRFy[t], 0]
                coordRRFTempMirror = [mirrorRRFx[t], mirrorRRFy[t], 0]
                coordRRFTempStar = [0, 0, 0] # 14 June 2018 changed x,y from None to 0.
                # Save the transformed coordinates to the simResults object to be used
                # in plotSim.py for graphing.
                simResults.saveTransform(coordRRFTempStar, coordRRFTempPlanet, coordRRFTempMirror)


    if 'energy' in plotTypes: # If we care about energy, return it.
        return [energy, ts]
    else: # If we don't care about energy, just return the number of timesteps.
        return ts

