#!/usr/bin/env python

"""
Created on Fry May  15 16:25:00 2020

@author: JosefMeiers
"""
#Battery Schedules
#https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder/20753073#20753073

import pprint
import time
import numpy as np


def ProcessSchedule(scheduleTable, client, input_states, inner_states):


# SCHEDULE FOR MEASUREMENTS
#
# Action :  0 = process schedule
#           1 = charge/discharge to maxSOC with given P
# Duration :0 = do not wait
#           >0 = wait in sec    
    def select():
        # prepare ESS to defined SOC
        # charge/discharge to given maxSOC
        if (SOC < entry['maxSOC']):
            #entry['Action'] = 2 # charge
            #print('Charge Battery (Action=2)')
            entry['Action']=2
            res=state(entry['Action'])
        
        elif (SOC > entry['maxSOC']):
            #entry['Action'] = 3 # discharge        
            #print('Discharge Battery (Action=3)')
            entry['Action']=3
            res=state(entry['Action'])
        else:
            #entry['Action'] = 4 # target reached --> set standby values and go to next table entry
            #print('Table entry {} finished (Action=4)'.format(schedIdx))
            entry['Action']=4
            res=state(entry['Action'])
        #print('STATE: select: Action: {}'.format(entry['Action']))
        return(res)
    
    #charge to given finalSOC
    def charge():
        
        print('STATE: charge')
        #pprint.pprint(setPoints)
        print('SOC: {}% -->{}%'.format(SOC,entry['maxSOC']))
        if (SOC >= entry['maxSOC']):
            entry['Action'] = 4
            setPoints=state(entry['Action']) 
        else:
            setPoints={}
            setPoints['P_Setpoint_Internal'] = -1*abs(entry['P'])
            setPoints['Q_Setpoint_Internal'] = -1*abs(entry['Q'])
            setPoints['ActiveMaxSOC_Setpoint'] = entry['maxSOC']
            setPoints['ActiveMinSOC_Setpoint'] = entry['minSOC']
        return(setPoints)

    #discharge to given finalSOC
    def discharge():
        
        print('STATE: discharge')
        #pprint.pprint(setPoints)
        print('SOC: {}% -->{}%'.format(SOC,entry['maxSOC']))
        if (SOC <= entry['maxSOC']):
            entry['Action'] = 4     
            setPoints=state(entry['Action'])  
        else:
            setPoints={}
            setPoints['P_Setpoint_Internal'] = +1*abs(entry['P'])
            setPoints['Q_Setpoint_Internal'] = +1*abs(entry['Q'])
            setPoints['ActiveMaxSOC_Setpoint'] = entry['maxSOC']
            setPoints['ActiveMinSOC_Setpoint'] = entry['minSOC']
        return(setPoints)

    def as_given():
        
        print('STATE: as_given')
        #pprint.pprint(setPoints)
        #print('SOC: {}'.format(SOC))
        d_t = abs(time.time() - schedTimestamp)
        if d_t >= entry['Duration'] :
            print('countdown finished: {}'.format(entry['Duration']-d_t))
            entry['Action'] = 4       
            setPoints=state(entry['Action'])
            return(setPoints)
        else:
            print('countdown running: {}'.format(entry['Duration']-d_t))
            #entry['Action']=0
            setPoints={}
            setPoints['P_Setpoint_Internal'] = entry['P']
            setPoints['Q_Setpoint_Internal'] = entry['Q']
            setPoints['ActiveMaxSOC_Setpoint'] = entry['maxSOC']
            setPoints['ActiveMinSOC_Setpoint'] = entry['minSOC']
            return(setPoints)

    #target reached  --> set standby values and go to next table entry
    def standby():
        setPoints={}
        setPoints['P_Setpoint_Internal'] = 0
        setPoints['Q_Setpoint_Internal'] = 0
        setPoints['ActiveMaxSOC_Setpoint'] = entry['maxSOC']
        setPoints['ActiveMinSOC_Setpoint'] = entry['minSOC']
        print('STATE: standby')
        print('SOC: {}'.format(SOC))
        #pprint.pprint(setPoints)
        return(setPoints)

    def default():
        setPoints=standby()
        return(setPoints)

    def state(argument):
        switcher = {
            0: as_given,
            1: select,
            2: charge,
            3: discharge,
            4: standby,
            5: default,
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument,default)
                # Execute the function
        
        return(func())
    
    def performance(data_useful_to_that):
        table_n29 = np.zeros(12,13)
        # table_n29 = ...

        return table_n29

    try:
        # schedIdx loop
        exitcode=1
        if inner_states['schedIdx'] is None:
           schedIdx = 1
           inner_states['schedIdx'] = schedIdx
        else: 
            schedIdx = inner_states['schedIdx']
        if inner_states['schedTimestamp'] is None:     
            schedTimestamp = time.time()
            inner_states['schedTimestamp'] = schedTimestamp
        else:
            schedTimestamp = inner_states['schedTimestamp']
        
        entry = scheduleTable[schedIdx]
        if inner_states['entryAction'] is None:
            pass
        else:
            entry['Action'] = inner_states['entryAction']
        
        SOC = input_states['SOC_Online']

        inner_states['entryAction'] = entry['Action']
        setpoints = state(entry['Action']) 

        if (entry['Action'] == 4) :
            if schedIdx < len(scheduleTable): 
                schedIdx += 1
                inner_states['schedIdx'] = schedIdx
                inner_states['schedTimestamp'] = None
                inner_states['entryAction'] = None
            else:
                schedIdx = 0
                inner_states['schedIdx'] = schedIdx
                inner_states['schedTimestamp'] = None
                inner_states['entryAction'] = None
 
    except:
        exitcode=0
        setpoints=None
        inner_states = None

    return (exitcode, inner_states, setpoints)
    #if (schedIdx >= len(scheduleTable)):
                #return() # nothing to do            

def RunSchedule(client,input_states,sched_table, inner_states):
    pprint.pprint(inner_states)
    #sched_table={}
    #sched_table[1] = schedule_A()
    #sched_table[2] = schedule_B()
    #pprint.pprint(sched_table)

    #input_states = read_input_states(client)
    #pprint.pprint(input_states)

    #for t in range(1,len(sched_table)+1):
    if inner_states['sched_table_no'] is None:
        t = 1
        inner_states['sched_table_no'] = t
    else:
        t = inner_states['sched_table_no']
    
    exitcode, inner_states, setpoints = ProcessSchedule(sched_table[t], client, input_states, inner_states)
    print('Exitcode: {}'.format(exitcode))
    
    if inner_states['schedIdx'] == 0:
        if inner_states['sched_table_no'] < len(sched_table):
            inner_states['sched_table_no'] += 1
            inner_states['schedIdx'] = None
        else:
            inner_states['sched_table_no'] = 0
        
    
    return(exitcode, inner_states, setpoints)
        