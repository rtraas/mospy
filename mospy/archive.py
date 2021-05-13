import time

Class TimerError(Exception):
    """
    Exception for errors when using the Archive class
    
    """

Class Archive:
    """ 
    Class to manage archiving Simulation outputs 
    
    Parameters
    ----------
    interval : tuple, optional
        Time interval between successive archiving of simulation data (hours, minutes, seconds). Default: 5 min
    filename : str, optional
        The name of the output file to write to. Default: name of simulation input file
    backup : bool, optional
        If set to True, saves a backup copy of the archived output files. Default: True
    
    """
    
    def __init__(self, interval=(0, 0, 10), filename=None, backup=True):
        self.t0 = None
        self.dt = interval[0]*60*60 + interval[1]*60 + interval[2]
        self.filename = filename
        self.backup = backup
        self.interval_elapsed = False
    
    def start(self):
        if self.t0 is not None:
            raise TimerError("Timer already running")
        self.t0 = time.perf_counter()
    
    def stop(self):
        if self.t0 is None:
            raise TimerError("Time is not running")
        print(f"Elapsed Time: {time.perf_counter() -  self.t0} seconds")
        self.t0 = None
    
    def check_time(self):
        elapsed = int(time.perf_counter() - self.t0)
        hh, mm, ss = (elapsed//(60*24))%24, (elapsed//60)%60, elapsed
        if (hh, mm, ss) > self.interval:
            self.interval_elapsed = True
        self.interval_elapsed = False
    
    def save(self, data):
        with open(f"{self.filename}", "w") as out_file:
            out_file.write(data)
        if self.backup:
            if hasattr(self, "backup_filename"):
                with open(self.backup_filename, "w") as out_file:
                    out_file.write(data)
