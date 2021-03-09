def setUpSim(mirrorOrbit, astroInputs, rebInputs, simResults, energy):
    import rebound
    import math
    from .convertUnits import convertUnits
    from .addParticles import addParticles
    from .setUpAdditional import setUpAdditional

    # Create the simulation and sim settings
    sim = rebound.Simulation()
    # Default G = 1.0 (REBOUND Units)
    if rebInputs.units == "SI":
        sim.G = 6.67408e-11
        #sim.units=('m', 's', 'kg')
        #sim.G = rebound.units.G_SI


    # Convert all units to SI (INFILE Must have had correct units given by the comments)
    convertUnits(sim, mirrorOrbit, astroInputs, rebInputs)

    # Set up integrator
    sim.integrator = rebInputs.integrator
    if rebInputs=='whfast':
        if rebInputs.symCorr == None:# Default symplectic correcter is 0.
            rebInputs.symCorr = 0
        sim.ri_whfast.corrector = rebInputs.symCorr

    # Orbit Period = 2pi*sqrt(r^3/(GM))
    # Mirror orbit time in seconds
    # Radius is the resultant of mirror's init post
    if rebInputs.addUsingOrbitalElements == True:
        print("Orbital Elements Input")
    else:
        print("Cartesian Input")

    # Now that everything is set up and the units are consistent units, add them
    # to the simulation.
    addParticles(sim, mirrorOrbit, astroInputs, rebInputs)

    if rebInputs.addUsingOrbitalElements == True:
        radius = mirrorOrbit.a
    else:
        # If added with cartesian coordinates, calculate its orbit and use
        # semi-major axis a as radius
        radius = sim.particles[2].calculate_orbit(primary=sim.particles[1]).a

    simResults.torbMirror = 2.*math.pi*math.sqrt((radius**3)/(sim.G*astroInputs.planetMass))
    print("Mirror orbit time: ", simResults.torbMirror)
    simlength = rebInputs.orbits*simResults.torbMirror

    # "The optimum timestep for WHFast is roughly 0.1% of the shortest orbital period
    # Rein & Tamayo 2015 suggest dtfac = 0.001
    sim.dt = simResults.torbMirror*rebInputs.dtfac
    if rebInputs.outputMegno:
        sim.init_megno()
        #move the particles to near the mirror
        p=sim.particles
        for mp in p[sim.N_real:sim.N_var+sim.N_var]:
            mp.x=p[sim.N_real-1].x+mp.x
            mp.y=p[sim.N_real-1].y+mp.y
            mp.z=p[sim.N_real-1].z+mp.z

        print ('\n'.join([str(mp) for mp in p[sim.N_real:sim.N_var+sim.N_var]]))

    if rebInputs.heartbeat is not None:
        rebInputs.heartbeat.orbitperiod=simResults.torbMirror
        if rebInputs.heartbeat.stdout or rebInputs.heartbeat.fileout:
            sim.heartbeat=rebInputs.heartbeat.heartbeat

    # Create initial conditions for energy to be used in calculating the change
    # in energy. This is the total energy of the particles.
    simResults.setInitial()
    energy.setInitialEnergy()

    if rebInputs.addForce != None: # If there are additional units specified, add them
        setUpAdditional(sim, astroInputs, rebInputs, mirrorOrbit, simResults)

    return sim

