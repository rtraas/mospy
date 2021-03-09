def doPlot(sim, mirrorOrbit, astroInputs, rebInputs, simResults, Energy, times, file_dir,
           plotOutput, plotTypes, totalEnergyREB, infile): #TODO Delete totalEnergyREB here and in energies

# Do the necessary imports
    from .plotSim import forcetime, overview, stationary, energy, plancen, rrf3d
    from .energies import energies
    from .outputSim import outputSim

# Deal with the matplotlib setup
    import os
    import matplotlib
    if plotOutput == 1:
       matplotlib.use('Agg')
       print("Saving Fig Files")
    if plotOutput != 1 and plotOutput != 4:
       if  os.environ.get('DISPLAY','') == '':
           print('No display found. Using non-interactive Agg backend.')
           matplotlib.use('Agg')
           if plotOutput == 2: print("No plots will be displayed or output")
           if plotOutput == 3: print("Will save figs but not plot to screen")
       else:
           matplotlib.use('TkAgg')
           if plotOutput == 2: print("Printing Fig Files to Screen Only")
           if plotOutput == 3: print("Saving Fig Files & Plotting to Screen")
    import matplotlib.pyplot as plt # 12/09/2019 need this in addition to in plotSim.py
if plotOutput == 1:
        if 'force' in plotTypes:
            forcetime(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'energy' in plotTypes:
            # Runs energies from energies.py to get the mirror and system energies
            # commented out energies 4 Oct 2019
            #energies(sim, astroInputs, simResults, energy)
            energy(sim, astroInputs, rebInputs, simResults, Energy, times, file_dir, totalEnergyREB, plotOutput)
        if 'overview' in plotTypes:
            overview(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'stationary' in plotTypes:
            stationary(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'plancen' in plotTypes:
            plancen(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'rrf3d' in plotTypes:
            rrf3d(mirrorOrbit, astroInputs, rebInputs, simResults, times, file_dir, plotOutput)

    if plotOutput == 2:
        if 'force' in plotTypes:
            forcetime(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'energy' in plotTypes:
            # Runs energies from energies.py to get the mirror and system energies
            #energies(sim, astroInputs, simResults, energy)
            energy(sim, astroInputs, rebInputs, simResults, Energy, times, file_dir, totalEnergyREB, plotOutput)
        if 'overview' in plotTypes:
            overview(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'stationary' in plotTypes:
            stationary(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'plancen' in plotTypes:
            plancen(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'rrf3d' in plotTypes:
            rrf3d(mirrorOrbit,astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        plt.show() # Need to call plt.show() in doPlot()! plotSim.py is too deep.       

    if plotOutput == 3:
        if 'force' in plotTypes:
            forcetime(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'energy' in plotTypes:
            # Runs energies from energies.py to get the mirror and system energies
            #energies(sim, astroInputs, simResults, energy)
            energy(sim, astroInputs, rebInputs, simResults, Energy, times, file_dir, totalEnergyREB, plotOutput)
        if 'overview' in plotTypes:
            overview(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'stationary' in plotTypes:
            stationary(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'plancen' in plotTypes:
            plancen(astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        if 'rrf3d' in plotTypes:
            rrf3d(mirrorOrbit, astroInputs, rebInputs, simResults, times, file_dir, plotOutput)
        plt.show()

