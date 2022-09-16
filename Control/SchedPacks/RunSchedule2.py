import pprint
import time

from Control.SchedPacks.ScheduleA import schedule_A
from Control.SchedPacks.ScheduleB import schedule_B

#coming (normally) from control_ESS where config mobdbus where defined
#we have called RunSchedule 
# def RunSchedule(client,input_states,sched_table, inner_states): => no modbus so no client
# def RunSchedule(input_states,sched_table, inner_states):
#     pprint.pprint(inner_states)
    
#     #for t in range(1,len(sched_table)+1):
#     if inner_states['sched_table_no'] is None:
#         t = 1
#         inner_states['sched_table_no'] = t
#     else:
#         t = inner_states['sched_table_no']
    
#     exitcode, inner_states, setpoints = ProcessSchedule(sched_table[t], client, input_states, inner_states)
#     print('Exitcode: {}'.format(exitcode))
    
#     if inner_states['schedIdx'] == 0:
#         if inner_states['sched_table_no'] < len(sched_table):
#             inner_states['sched_table_no'] += 1
#             inner_states['schedIdx'] = None
#         else:
#             inner_states['sched_table_no'] = 0
        
    
#     return(exitcode, inner_states, setpoints)

#main function of the control_ESS script without modbus communication
def main(Argument):

    def schedule_all():
        ''' Merge all schedule table to do a complete test of the system'''
        schedule_table={}
        schedule_table[1] = schedule_A()
        schedule_table[2] = schedule_B()

        return schedule_table

    # #we can choose wich test we are doing
    # def ScheduleChoice(argument):
    #     switcher = {
    #         0: schedule_B, #Power conversion system
    #         1: schedule_A, #Battery
    #         2: schedule_all #Complete test
    #     }
    #     # Get the function from switcher dictionary
    #     func = switcher.get(argument)
        
    #     # Execute the function
    #     return(func())
    
    # we defined the schedule table accordingly to witch test we want to proceed
    sched_table = {}
    if Argument==0:
        sched_table[1] = schedule_A()
        sched_table[2] = {}
    elif Argument==1:
        sched_table[1] = schedule_B()
        sched_table[2] = {}
    else:
        sched_table[1] = schedule_A()
        sched_table[2] = schedule_B()
        
    pprint.pprint(sched_table)

    inner_states={'sched_table_no':None,
            'schedIdx': None,
            'schedTimestamp': None,
            'entryAction': None,
        }
        
    
    while True:
        ## Read inputs and show
        # input_states = read_input_states(client) => first we don't use modbus so we'll start with default input state defined arbitrary
        input_states = {
            "SOC": 0, #completly decharge
        }
        pprint.pprint(input_states)
        
        ## Scheduler: Calculate output (not in this part =>and prepare writing modbus register)
        # if inner_states['sched_table_no'] != 0:
        #     exitcode, inner_states, setpoints = RunSchedule(client, input_states, sched_table, inner_states)
        #     pprint.pprint(setpoints)
        #     pprint.pprint(inner_states)
        
        time.sleep(5)
        break #to test only one loop
        

if __name__ == '__main__':
    sys.exit(main())
    #sys.exit(0)