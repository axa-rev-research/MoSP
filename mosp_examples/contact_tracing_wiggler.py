#!/bin/env python

"""Infection simulation with digital contact tracing 
    - random movement
    - infection event
    - quarantine when symptoms revealed or notified by app
    - visualization in separate viewer, executed as child process
"""

import sys
sys.path.append("..") 

from mosp.core import Simulation, Person, action, start_action
from mosp.geo import osm
from mosp.impl import movement
from mosp.monitors import SocketPlayerMonitor, EmptyMonitor
import pickle

__author__ = "Boris Ruf"
__contact__ = "boris.ruf@axa.com"
__copyright__ = "(c) 2020, REV Research, AXA, Paris, France"
__license__ = "GPLv3"

try:
    infection_times = pickle.load(open("infection_times.p", "rb"))
except (OSError, IOError) as e:
    infection_times = {}


adoption_rate = 10     # The installation rate of the app in percent


class ContactTracingWiggler(Person):
    """Models one person who can get infected and may or may not use the app 
    """
    def __init__(self, *args, **kwargs):
        super(ContactTracingWiggler, self).__init__(*args, **kwargs)
        self.p_infected = False                               # infected?
        self.p_appInstalled = False                           # uses the tracing app?
        self.pplInRange = {}                                  # stores infecting people in range
        self.p_othersInfected = []
        if 'appInstalled' in kwargs:
            self.p_appInstalled = True
            self.p_color = 3                                  
            self.p_color_rgba = (0,0.8,0,1.0)                 # green
        if 'infected' in kwargs:
            self.p_color = 1                                  
            self.p_color_rgba = (0.9,0.1,0.1,1.0)             #: red
            self.p_infected = True
            self.p_infectionTime = self.sim.now()
            self.p_infectionPlace = self.current_coords()     #: coordinates of infection
            print self.p_infectionTime, self.p_infectionPlace[0], self.p_infectionPlace[1], self.name, self.name
            infection_times[str(adoption_rate)] = []
            infection_times[str(adoption_rate)].append(self.p_infectionTime)
            start_action(self.infect_other)
        if 'infectionTime' in kwargs:
            self.p_infectionTime = kwargs['infectionTime']
            
    next_target = movement.person_next_target_random
    
    def tryinfect(self, infecting_one):
        """The infection routine
        """
        now = self.sim.now()
        if infecting_one not in self.pplInRange:                        # new contact
            new = { infecting_one : [1, now]}                           
            self.pplInRange.update(new)                                 
        else:                                                           # close by for some time
            old = self.pplInRange[infecting_one]                        
            if old[1] < self.sim.now()-1:                               # contact was interrupted
                new = { infecting_one : [1, now] }                      # reset
                self.pplInRange.update(new)                             
            else:                                                       # continous contact
                new = { infecting_one : [old[0]+1, now] }               # increase duration
                self.pplInRange.update(new)                             
            if self.pplInRange[infecting_one][0] >= 5:                  # infection time is reached
                self.p_color = 3
                self.p_color_rgba = (0.5,0.0,0.5,1.0)                   # purple: infected but not infectious
                self.p_infected = True                                  # person is infected now, infectious in 100 ticks
                self.p_infectionTime = now                                
                self.p_infectionPlace = self.current_coords()             
                print self.p_infectionTime, self.p_infectionPlace[0], self.p_infectionPlace[1], self.name, infecting_one.name
                infection_times[str(adoption_rate)].append(self.p_infectionTime)
                infecting_one.p_othersInfected.append(self)
                start_action(self.infect_other, delay=100)              # start being infectious after 100 ticks

    @action(1, start=False)
    def infect_other(self):
        """The infection action
        
        This action is called every tick looking for people close by (in a random range of 10-20 meters). It calls the tryinfect() 
        routine for any identified person."""
        if self.p_infected == True and self.passivate == False:         # if I'm infectious and not in quarantine
            if self.p_color == 3: 
                self.p_color = 1 
                self.p_color_rgba = (0.9,0.1,0.1,1.0)                   # red: infected and infectious
            self.get_near(self._random.randint(10,20), self_included=False).filter(p_infected=False).call(delay=0).tryinfect(self)

            if self.sim.now() - self.p_infectionTime > 300:   # symptoms reveal infection, person is quarantined
                self.passivate = True
                self.p_color = 4 
                self.p_color_rgba = (1.0,1.0,1.0,1.0)                   # white: infectious but quarantined
                for p in self.p_othersInfected: 
                    if p.p_appInstalled == True:                        # quarantine all contacts who used the app
                        p.passivate = True
                        p.p_color = 4 
                        p.p_color_rgba = (1.0,1.0,1.0,1.0)              # white: infectious but quarantined


def main():
    """The infection simulation with digital contact tracing.
    
    map: paris8.osm, output to socketPlayer, 
    1 infected person, 500 healthy people. Modify adoption_rate to vary app installation rate."""

    duration = 4000

    s = Simulation(geo=osm.OSMModel('../data/paris8.osm'), rel_speed=120, seed=299)
    
    m = s.add_monitor(SocketPlayerMonitor, 2)
    
    s.add_persons(ContactTracingWiggler, 1, monitor=m, args={"infected":True, "infectionTime":-51})
    s.add_persons(ContactTracingWiggler, (100-adoption_rate)*5, monitor=m)
    s.add_persons(ContactTracingWiggler, adoption_rate*5, monitor=m, args={"appInstalled":True})
    
    s.run(until=duration, real_time=True, monitor=True)   
    
    pickle.dump( infection_times, open( "infection_times.p", "wb" ) )


if __name__ == '__main__':
    main()