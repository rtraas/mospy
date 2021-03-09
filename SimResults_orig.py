class SimResults:
    # Create the particle and its attributes. Default is none for everything.
    def __init__(self, coordStar = None, coordRRFStar = None, velStar = None, accelStar = None,
                 coordPlanet = None, coordRRFPlanet = None, velPlanet = None, accelPlanet = None,
                 coordMirror = None, coordRRFMirror = None, velMirror = None, accelMirror = None,
                 torbMirror = None,suggestedEndTime = None, actualEndTime = None,
                 currdt = None):
        # Initialize Star
        self.coordStar = coordStar
        self.coordRRFStar = coordRRFStar
        self.velStar = velStar
        self.accelStar = accelStar
        # Initialize Planet
        self.coordPlanet = coordPlanet
        self.coordRRFPlanet = coordRRFPlanet
        self.velPlanet = velPlanet
        self.accelPlanet = accelPlanet
        # Initialize Mirror
        self.coordMirror = coordMirror
        self.coordRRFMirror = coordRRFMirror
        self.velMirror = velMirror
        self.accelMirror = accelMirror
        self.torbMirror = torbMirror
        # Initialize times
        self.suggestedEndTime= suggestedEndTime
        self.actualEndTime= actualEndTime
        self.currdt = currdt
    # Set initial coordinates before integrating
    def setInitial(self):
        # Star
        self.coordStar = []
        self.coordRRFStar = []
        self.velStar = []
        self.accelStar = []
        # Planet
        self.coordPlanet = []
        self.coordRRFPlanet = []
        self.velPlanet = []
        self.accelPlanet = []
        # Mirror
        self.coordMirror = []
        self.coordRRFMirror = []
        self.velMirror = []
        self.accelMirror = []
        self.torbMirror = self.torbMirror
        # Times
        self.suggestedEndTime= []
        self.actualEndTime= []
        self.currdt = []
    # Save the data at each timestep of the integrator (not every integration step)
    def saveData(self, coordTempStar, velTempStar, accelTempStar,
                 coordTempPlanet, velTempPlanet, accelTempPlanet,
                 coordTempMirror, velTempMirror, accelTempMirror,
                 suggestedEndTime, actualEndTime, currdt):
        # Lists have Noutputs + Initial coordinates entries, each entry is
        # the X, Y, Z coordinates of the attribute
        # EX) self.coord = [[x,y,z],...,[xn,yn,zn]]
        # Star
        self.coordStar.append(coordTempStar)
        self.velStar.append(velTempStar)
        self.accelStar.append(accelTempStar)
        # Planet
        self.coordPlanet.append(coordTempPlanet)
        self.velPlanet.append(velTempPlanet)
        self.accelPlanet.append(accelTempPlanet)
        # Mirror
        self.coordMirror.append(coordTempMirror)
        self.velMirror.append(velTempMirror)
        self.accelMirror.append(accelTempMirror)
        # Times
        self.suggestedEndTime.append(suggestedEndTime)
        self.actualEndTime.append(actualEndTime)
        self.currdt.append(currdt)


   # Lists have Noutputs + Initial coordinates entries, each entry is
   # the X, Y, Z coordinates of the attribute
   # EX) self.coord = [[RRFx,RRFy,RRFz],...,[RRFxn,RRFyn,RRFzn]]
    def saveTransform(self, coordRRFTempStar, coordRRFTempPlanet, coordRRFTempMirror):
        self.coordRRFStar.append(coordRRFTempStar)
        self.coordRRFPlanet.append(coordRRFTempPlanet)
        self.coordRRFMirror.append(coordRRFTempMirror)

