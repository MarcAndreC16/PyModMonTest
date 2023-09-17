import pprint
import time

import pandas as pd 
import numpy as np

from Control.SchedPacks.ScheduleA import schedule_A
from Control.SchedPacks.ScheduleA import schedule_B
from Control.SchedPacks.ScheduleA import schedule_C

#we have called ProcessSchedule in RunSchedule after defenided the schedule table
#def ProcessSchedule(scheduleTable, client, input_states, inner_states):
def ProcessSchedule(scheduleTable, input_states, inner_states): #we first don't use modbus
    """
    Execute a part of the schedule of test  
    Parameters:
        input_states : machine state we want to study
        sched_table  : part of the table that describe the test we want to perform
        inner_states : function parameters used to follow the test described in sched_table
    Returns:
        exitcode     : 1 if the test is perform correctly
        inner_states : 
        setpoints    : setpoints value that will be send to physical system 
        
    """

    def select():
        # prepare ESS to defined SOC
        # charge/discharge to given maxSOC
        if (SOC < entry['maxSOC']):
            #entry['Action'] = 2 # charge
            #print('Charge Battery (Action=2)')
            entry['Action']=2
            res=state(entry['Action'])
        
        # elif (SOC > entry['maxSOC']):
        #     #entry['Action'] = 3 # discharge        
        #     #print('Discharge Battery (Action=3)')
        #     entry['Action']=3
        #     res=state(entry['Action'])

        else: #we can suppose maxSOC=100%
            #entry['Action'] = 4 # target reached --> set standby values and go to next table entry
            #print('Table entry {} finished (Action=4)'.format(schedIdx))
            entry['Action']=4
            res=state(entry['Action'])
        #print('STATE: select: Action: {}'.format(entry['Action']))
        return(res)
    
    #charge to given finalSOC
    def charge():
        
        print('STATE: charge')
        #pprint.pprint(SetPoints)
        print('SOC: {}% -->{}%'.format(SOC,entry['maxSOC']))
        if (SOC >= entry['maxSOC']):
            entry['Action'] = 4
            SetPoints=state(entry['Action']) 
        else:
            SetPoints={}
            SetPoints['P_Setpoint_Internal'] = +1*abs(entry['P'])
            SetPoints['Q_Setpoint_Internal'] = +1*abs(entry['Q'])
            SetPoints['ActiveMaxSOC_Setpoint'] = entry['maxSOC']
            SetPoints['ActiveMinSOC_Setpoint'] = entry['minSOC']
        return(SetPoints)

    #discharge to given finalSOC
    def discharge():
        
        print('STATE: discharge')
        #pprint.pprint(SetPoints)
        print('SOC: {}% -->{}%'.format(SOC,entry['maxSOC']))
        if (SOC <= entry['maxSOC']):
            entry['Action'] = 4     
            SetPoints=state(entry['Action'])  
        else:
            SetPoints={}
            SetPoints['P_Setpoint_Internal'] = -1*abs(entry['P'])
            SetPoints['Q_Setpoint_Internal'] = -1*abs(entry['Q'])
            SetPoints['ActiveMaxSOC_Setpoint'] = entry['maxSOC']
            SetPoints['ActiveMinSOC_Setpoint'] = entry['minSOC']
        return(SetPoints)

    def as_given():
        
        print('STATE: as_given')
        #pprint.pprint(SetPoints)
        #print('SOC: {}'.format(SOC))
        d_t = abs(time.time() - schedTimestamp)
        if d_t >= entry['Duration'] :
            print('countdown finished: {}'.format(entry['Duration']-d_t))
            entry['Action'] = 4       
            SetPoints=state(entry['Action'])
            return(SetPoints)
        else:
            print('countdown running: {}'.format(entry['Duration']-d_t))
            #entry['Action']=0
            SetPoints={}
            SetPoints['P_Setpoint_Internal'] = entry['P']
            SetPoints['Q_Setpoint_Internal'] = entry['Q']
            SetPoints['ActiveMaxSOC_Setpoint'] = entry['maxSOC']
            SetPoints['ActiveMinSOC_Setpoint'] = entry['minSOC']
            return(SetPoints)

    #target reached  --> set standby values and go to next table entry
    def standby():
        SetPoints={}
        SetPoints['P_Setpoint_Internal'] = 0
        SetPoints['Q_Setpoint_Internal'] = 0
        SetPoints['ActiveMaxSOC_Setpoint'] = entry['maxSOC']
        SetPoints['ActiveMinSOC_Setpoint'] = entry['minSOC']
        print('STATE: standby')
        print('SOC: {}'.format(SOC))
        #pprint.pprint(SetPoints)
        return(SetPoints)

    def default():
        SetPoints=standby()
        return(SetPoints)

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
        ''' '''
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
        inner_states['SOC']=input_states['SOC_Online']

        inner_states['entryAction'] = entry['Action']
        setPoints = state(entry['Action']) 
        # print(inner_states)

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
        print("an error occured")
        exitcode=0
        setPoints=None
        inner_states = None

    return (exitcode, inner_states, setPoints)


#coming (normally) from control_ESS where config mobdbus where defined
#we have called RunSchedule 
# def RunSchedule(client,input_states,sched_table, inner_states): => no modbus so no client
def RunSchedule(input_states,sched_table, inner_states):
    """
    Check where we are in the execution of the schedule
    Parameters:
        input_states : machine state we want to study
        sched_table  : table that describe the test we want to perform
        inner_states : function parameters used to follow the test described in sched_table
    Returns:
        exitcode     : 1 if the test is perform correctly
        inner_states : 
        setpoints    : setpoints value that will be send to physical system
        
    """
    pprint.pprint(inner_states)
    
    # for t in range(1,len(sched_table)+1):
    if inner_states['sched_table_no'] is None:
        t = 1
        inner_states['sched_table_no'] = t
    else:
        t = inner_states['sched_table_no']
    
    # exitcode, inner_states, setpoints = ProcessSchedule(sched_table[t], client, input_states, inner_states)
    exitcode, inner_states, setpoints = ProcessSchedule(sched_table[t], input_states, inner_states)
    print('Exitcode: {}'.format(exitcode))
    # print(inner_states)
    if inner_states['schedIdx'] == 0:
        if inner_states['sched_table_no'] < len(sched_table):
            inner_states['sched_table_no'] += 1
            inner_states['schedIdx'] = None
        else:
            inner_states['sched_table_no'] = 0
        
    
    return(exitcode, inner_states, setpoints)

#main function of the control_ESS script without modbus communication
def main(ArgumentA,ArgumentB,ArgumentC,P):
    """
    Launching the desired programm of test (and will do modbus connection) 
    Parameters:
        Argument: type of test we want to do (to redefined)
    Returns:
        None
    """
    Argument_A = ArgumentA.get()
    Argument_B = ArgumentB.get()
    Argument_C = ArgumentC.get()

    # we defined the schedule table accordingly to witch test we want to proceed
    sched_table = {}
    if Argument_A==1 and Argument_B==0 and Argument_C==0:
        sched_table[1] = schedule_A() 
    elif Argument_A==0 and Argument_B==1 and Argument_C==0:
        sched_table[1] = schedule_B()
    elif Argument_A==0 and Argument_B==0 and Argument_C==1:
        sched_table[1] = schedule_C()
    elif Argument_A==1 and Argument_B==1 and Argument_C==0:
        sched_table[1] = schedule_A()
        sched_table[2] = schedule_B()
    elif Argument_A==1 and Argument_B==0 and Argument_C==1:
        sched_table[1] = schedule_A()
        sched_table[2] = schedule_C()
    elif Argument_A==0 and Argument_B==1 and Argument_C==1:
        sched_table[1] = schedule_B()
        sched_table[2] = schedule_C()
    else:
        sched_table[1] = schedule_A()
        sched_table[2] = schedule_B()
        sched_table[3] = schedule_C()
        
    pprint.pprint(sched_table)


    inner_states={'sched_table_no':None,
            'schedIdx':None,
            'schedTimestamp':None,
            'entryAction':None,
            'SOC':None
        }
        
    E_bat = 0
    n=0
    Tkmin1 = 0
    # results = np.asarray([['Time','Idx','Soc','E_bat','P']])
    results = np.zeros([1,5])

    while True:
        ## Read inputs and show
        # input_states = read_input_states(client) => first we don't use modbus so we'll start with default input state defined arbitrary
        input_states = {
            "SOC_Online": 0, #completly decharge
        }
        # pprint.pprint(input_states)

        # we don't use modbus so we simulate change of soc
        if inner_states['sched_table_no'] != None:
            input_states["SOC_Online"] = inner_states['SOC']
        
        # Scheduler: Calculate output (not in this part =>and prepare writing modbus register)
        if inner_states['sched_table_no'] != 0:
            # exitcode, inner_states, setpoints = RunSchedule(client, input_states, sched_table, inner_states) 
            exitcode, inner_states, setpoints = RunSchedule(input_states, sched_table, inner_states) #no modbus yet

            # pprint.pprint(setpoints)
            # pprint.pprint(inner_states)

            #Use Tkmin1 to calculate dt
            if inner_states['schedTimestamp'] == None:
                Tkmin1=0

            #calculate the new value
            if inner_states['schedTimestamp'] != None:
                Tkplus1 = abs(time.time() - inner_states['schedTimestamp'])
                dt = Tkplus1-Tkmin1
                Tkmin1 = Tkplus1
                E_bat += P*setpoints['P_Setpoint_Internal']*dt/3600
                inner_states['SOC'] = E_bat/5 

                #add value to results array
                row = []
                row.append(Tkplus1)
                row.append(inner_states['schedIdx'])
                row.append(inner_states['SOC'])
                row.append(E_bat)
                row.append(setpoints['P_Setpoint_Internal'])
                results = np.vstack([results,row])
                # print(results)

            # if n>3:
            #     np.savetxt('RESULTS.csv', results, fmt="%s", delimiter=",")
            #     print("see csv")
            # else:
            #     n+=1
        
        else:
            np.savetxt('RESULTS.csv', results,fmt="%s", delimiter=",")
            print("End: the schedule has been completed")
            break #we have done all the schedule

        time.sleep(5)
        

if __name__ == '__main__':
    sys.exit(main())
    #sys.exit(0)