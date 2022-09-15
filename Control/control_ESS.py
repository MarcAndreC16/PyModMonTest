#!/usr/bin/env python

"""
Created on Thu May  06 07:00:00 2020

@author: JosefMeiers
"""
# Imports from Python standard library
import sys
import csv
import os
import time
import pprint
import copy
from datetime import datetime

# Imports from external libraries
#pymodbus
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

#influxdb
from influxdb import InfluxDBClient

#json
import json


#Battery Schedules
#https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder/20753073#20753073
#from SchedPacks.scheduleA import schedule_A, schedule_B
from SchedPacks.scheds.scheduleA import schedule_A, schedule_B
from SchedPacks.RunSchedule import RunSchedule

def read_input_states(client):
    """Parse non-dummy values from client as dictionary."""

    #dt = datetime.utcnow()  # is "now" right before or after reading the registers?

    # Get holding_registers
    #try:
        #client.connect()
        #holdingRegs5050 = client.read_holding_registers(5050, 16)
        #holdingRegs5080 = client.read_holding_registers(5080, 101)
        #holdingRegs5190 = client.read_holding_registers(5190, 76)
    holdingRegs5146 = client.read_holding_registers(5146, 20)
    '''
    except Exception as e:
        raise SystemExit(e)
    finally:
        client.close()
    '''

    #result5050 = holdingRegs5050.registers
    #result5080 = holdingRegs5080.registers
    #result5190 = holdingRegs5190.registers
    result5146 = holdingRegs5146.registers

    #decoder5050 = BinaryPayloadDecoder.fromRegisters(result5050, Endian.Big, wordorder=Endian.Little)
    #decoder5080 = BinaryPayloadDecoder.fromRegisters(result5080, Endian.Big, wordorder=Endian.Little)
    #decoder5190 = BinaryPayloadDecoder.fromRegisters(result5190, Endian.Big, wordorder=Endian.Little)
    decoder5146 = BinaryPayloadDecoder.fromRegisters(result5146, Endian.Big, wordorder=Endian.Little)

    '''
    HORST_ESS_data5050 = {
        "UTC_datetime": str(dt),
        "UTC_Timestamp": dt.timestamp(),
        "State": decoder5050.decode_16bit_uint(),                               # 5050
        "ControlPlace": decoder5050.decode_16bit_uint(),                        # 5051
        "ControlStatusWord": decoder5050.decode_16bit_uint(),                   # 5051
        "ActiveDesiredConverterMode": decoder5050.decode_16bit_uint(),          # 5052
        "P_Setpoint": round(decoder5050.decode_32bit_float(), 3),               # 5053
        "Q_Setpoint": round(decoder5050.decode_32bit_float(), 3),               # 5055
        "ActiveMinSOC_Setpoint": round(decoder5050.decode_32bit_float(), 3),    # 5057
        "ActiveMaxSOC_Setpoint": round(decoder5050.decode_32bit_float(), 3),    # 5059
        "ActiveDesiredFreqAdjust": round(decoder5050.decode_32bit_float(), 3),  # 5061
        "LifeCounter": decoder5050.decode_16bit_uint()                          # 5063
    }
    '''

    '''
    HORST_ESS_data5080 = {
             "ConnectedBatteryRacks": decoder5080.decode_16bit_uint(),               # 5080 
        "CommunicatingBatteryRacks": decoder5080.decode_16bit_uint(),           # 5081
        "dummy": decoder5080.decode_16bit_uint(),                               # 5082
        "FaultedSubComponents": decoder5080.decode_16bit_uint(),                # 5083
        "P_Total": round(decoder5080.decode_32bit_float(), 3),                  # 5084
        "Q_Total": round(decoder5080.decode_32bit_float(), 3),                  # 5086
        "S_Total": round(decoder5080.decode_32bit_float(), 3),                  # 5088
        "BCU_PF": round(decoder5080.decode_32bit_float(), 3),                   # 5090
        "Grid_Frequency": round(decoder5080.decode_32bit_float(), 3),           # 5092
        "Grid_U_LL": round(decoder5080.decode_32bit_float(), 3),                # 5094
        "Grid_U_LN": round(decoder5080.decode_32bit_float(), 3),                # 5096
        "P_L1": round(decoder5080.decode_32bit_float(), 3),                     # 5098
        "P_L2": round(decoder5080.decode_32bit_float(), 3),                     # 5100
        "P_L3": round(decoder5080.decode_32bit_float(), 3),                     # 5102
        "Q_L1": round(decoder5080.decode_32bit_float(), 3),                     # 5104
        "Q_L2": round(decoder5080.decode_32bit_float(), 3),                     # 5106
        "Q_L3": round(decoder5080.decode_32bit_float(), 3),                     # 5108
        "S_L1": round(decoder5080.decode_32bit_float(), 3),                     # 5110
        "S_L2": round(decoder5080.decode_32bit_float(), 3),                     # 5112
        "S_L3": round(decoder5080.decode_32bit_float(), 3),                     # 5114
        "U_L1N": round(decoder5080.decode_32bit_float(), 3),                    # 5116
        "U_L2N": round(decoder5080.decode_32bit_float(), 3),                    # 5118
        "U_L3N": round(decoder5080.decode_32bit_float(), 3),                    # 5120
        "U_L1L2": round(decoder5080.decode_32bit_float(), 3),                   # 5122
        "U_L2L3": round(decoder5080.decode_32bit_float(), 3),                   # 5124
        "U_L3L1": round(decoder5080.decode_32bit_float(), 3),                   # 5126
        "I_Total": round(decoder5080.decode_32bit_float(), 3),                  # 5128
        "I_L1": round(decoder5080.decode_32bit_float(), 3),                     # 5130
        "I_L2": round(decoder5080.decode_32bit_float(), 3),                     # 5132
        "I_L3": round(decoder5080.decode_32bit_float(), 3),                     # 5134
        "Ea_generated": round(decoder5080.decode_32bit_float(), 3),             # 5136
        "Ea_consumed": round(decoder5080.decode_32bit_float(), 3),              # 5138
        "U_ACatFU": round(decoder5080.decode_32bit_float(), 3),                 # 5140
        "U_DCatFU": round(decoder5080.decode_32bit_float(), 3),                 # 5142
        "T_FU": round(decoder5080.decode_32bit_float(), 3),                     # 5144
        "SOC_Available": round(decoder5080.decode_32bit_float(), 3),            # 5146
        "SOC_Online": round(decoder5080.decode_32bit_float(), 3),               # 5148
        "SOH_Available": round(decoder5080.decode_32bit_float(), 3),            # 5150
        "SOH_Online": round(decoder5080.decode_32bit_float(), 3),               # 5152
        "SOE_Available": round(decoder5080.decode_32bit_float(), 3),            # 5154
        "SOE_Online": round(decoder5080.decode_32bit_float(), 3),               # 5156
        "P_DC_Battery": round(decoder5080.decode_32bit_float(), 3),             # 5158
        "E_Generating_Online": round(decoder5080.decode_32bit_float(), 3),      # 5160
        "E_Charging_Online": round(decoder5080.decode_32bit_float(), 3),        # 5162
        "E_Generating_Available": round(decoder5080.decode_32bit_float(), 3),   # 5164
        "E_Charging_Available": round(decoder5080.decode_32bit_float(), 3),     # 5166
        "P_GeneratingReserve": round(decoder5080.decode_32bit_float(), 3),      # 5168
        "P_ChargingReserve": round(decoder5080.decode_32bit_float(), 3),        # 5170
        "E_Nominal_Online": round(decoder5080.decode_32bit_float(), 3),         # 5172
        "E_Nominal_Available": round(decoder5080.decode_32bit_float(), 3),      # 5174
        "ActiveModeFU": decoder5080.decode_16bit_uint(),                        # 5176
        "P_Setpoint_Internal": round(decoder5080.decode_32bit_float(), 3),      # 5178
        "Q_Setpoint_Internal": round(decoder5080.decode_32bit_float(), 3),      # 5180
    }
    '''

    '''
    HORST_ESS_data5190 = {
        "BCUAlarmWord": decoder5190.decode_16bit_uint(),                        # 5190
        "TemperatureWarnings": decoder5190.decode_16bit_uint(),                 # 5191
        "TemperatureAlarms": decoder5190.decode_16bit_uint(),                   # 5192
        "EventSensors": decoder5190.decode_16bit_uint(),                        # 5193
        "BatteryWarningWord": decoder5190.decode_16bit_uint(),                  # 5194
        "BatteryTripWord": decoder5190.decode_16bit_uint(),                     # 5195
        "EmStopConditions": decoder5190.decode_16bit_uint(),                    # 5196
        "LimitConditions": decoder5190.decode_16bit_uint(),                     # 5197
        "InhibitConditions": decoder5190.decode_16bit_uint(),                   # 5198
        "ConverterAlarmWord": decoder5190.decode_16bit_uint(),                  # 5199
        "FailedRestartAttempts": decoder5190.decode_16bit_uint(),               # 5200
        "TotalRestartAttempts": decoder5190.decode_16bit_uint(),                # 5201
        "dummy": decoder5190.decode_16bit_uint(),                               # 5202
        "dummy": decoder5190.decode_16bit_uint(),                               # 5203
        "dummy": decoder5190.decode_16bit_uint(),                               # 5204
        "dummy": decoder5190.decode_16bit_uint(),                               # 5205
        "dummy": decoder5190.decode_16bit_uint(),                               # 5206
        "dummy": decoder5190.decode_16bit_uint(),                               # 5207
        "dummy": decoder5190.decode_16bit_uint(),                               # 5208
        "dummy": decoder5190.decode_16bit_uint(),                               # 5209
        "Temperature1": round(decoder5190.decode_32bit_float(), 3),             # 5210
        "Temperature2": round(decoder5190.decode_32bit_float(), 3),             # 5212
        "Temperature3": round(decoder5190.decode_32bit_float(), 3),             # 5214
        "Temperature4": round(decoder5190.decode_32bit_float(), 3),             # 5216
        "Temperature5": round(decoder5190.decode_32bit_float(), 3),             # 5218
        "Temperature6": round(decoder5190.decode_32bit_float(), 3),             # 5220
        "Temperature7": round(decoder5190.decode_32bit_float(), 3),             # 5222
        "Temperature8": round(decoder5190.decode_32bit_float(), 3),             # 5224
        "dummy": round(decoder5190.decode_32bit_float(), 3),                    # 5226
        "dummy": round(decoder5190.decode_32bit_float(), 3),                    # 5228
        "dummy": round(decoder5190.decode_32bit_float(), 3),                    # 5230
        "dummy": round(decoder5190.decode_32bit_float(), 3),                    # 5232
        "dummy": round(decoder5190.decode_32bit_float(), 3),                    # 5234
        "dummy": round(decoder5190.decode_32bit_float(), 3),                    # 5236
        "dummy": round(decoder5190.decode_32bit_float(), 3),                    # 5238
        "StandardDI": decoder5190.decode_16bit_uint(),                          # 5240
        "StandardDO": decoder5190.decode_16bit_uint(),                          # 5241
        "dummy": decoder5190.decode_16bit_uint(),                               # 5242
        "dummy": decoder5190.decode_16bit_uint(),                               # 5243
        "dummy": decoder5190.decode_16bit_uint(),                               # 5244
        "dummy": decoder5190.decode_16bit_uint(),                               # 5245
        "dummy": decoder5190.decode_16bit_uint(),                               # 5246
        "dummy": decoder5190.decode_16bit_uint(),                               # 5247
        "dummy": decoder5190.decode_16bit_uint(),                               # 5248
        "dummy": decoder5190.decode_16bit_uint(),                               # 5249
        "MaxCellVoltage_Connected": round(decoder5190.decode_32bit_float(), 3), # 5250
        "MinCellVoltage_Connected": round(decoder5190.decode_32bit_float(), 3), # 5252
        "MaxCellVoltage": round(decoder5190.decode_32bit_float(), 3),           # 5254
        "MinCellVoltage": round(decoder5190.decode_32bit_float(), 3),           # 5256
        "MaxBatteryTemperature": round(decoder5190.decode_32bit_float(), 3),    # 5258
        "MinBatteryTemperature": round(decoder5190.decode_32bit_float(), 3),    # 5260
        "BatteryBusVoltage": round(decoder5190.decode_32bit_float(), 3),        # 5252
        "BatteryCurrent": round(decoder5190.decode_32bit_float(), 3),           # 5254
    }
    '''
    HORST_ESS_data5146 = {
        "SOC_Available": round(decoder5146.decode_32bit_float(), 3),            # 5116
        "SOC_Online": round(decoder5146.decode_32bit_float(), 3),               # 5118
        "SOH_Available": round(decoder5146.decode_32bit_float(), 3),            # 5120
        "SOH_Online": round(decoder5146.decode_32bit_float(), 3),               # 5122
        "SOE_Available": round(decoder5146.decode_32bit_float(), 3),            # 5124
        "SOE_Online": round(decoder5146.decode_32bit_float(), 3),               # 5126
    }

    # Combine dictionaries
    HORST_ESS_data = {**HORST_ESS_data5146}

    # Remove placeholders
    if "dummy" in HORST_ESS_data:
        del HORST_ESS_data["dummy"]

    return (HORST_ESS_data)   


def write_outputs(builder, client):

    payload = builder.to_registers()
    '''
    print("-" * 60)
    print("Writing Registers")
    print("-" * 60)
    print(payload)
    print("\n")
    '''
    payload = builder.build()
    address = 5002
    # Write registers
    registers = builder.to_registers()
    rq = client.write_registers(address, registers)
    return (rq)

def main():

    '''
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers,byteorder=Endian.Big, wordorder=Endian.Little)
    decoded = {
            'string': decoder.decode_string(8),
            'float': decoder.decode_32bit_float(),
            '16uint': decoder.decode_16bit_uint(),
            'ignored': decoder.skip_bytes(2),
            '8int': decoder.decode_8bit_int(),
            'bits': decoder.decode_bits(),
        }
    
    arguments = {
        'read_address':    1,
        'read_count':      8,
        'write_address':   1,
        'write_registers': [20]*8,
        }
    '''
    ## Device 1 - SPS in storage system container
    HORST_ESS_IP = '192.168.161.230'
    HORST_ESS_PORT = 502
    client = ModbusTcpClient(host=HORST_ESS_IP, port=HORST_ESS_PORT)
    client.connect()

    sched_table={}
    sched_table[1] = schedule_A()
    sched_table[2] = schedule_B()
    pprint.pprint(sched_table)

    inner_states={'sched_table_no':None,
            'schedIdx': None,
            'schedTimestamp': None,
            'entryAction': None,
        }
        
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)  
    address = 5002
    
    while True:
        ## Read inputs and show
        input_states = read_input_states(client)
        pprint.pprint(input_states)

       
        ## Scheduler: Calculate output and prepare writing modbus register
        if inner_states['sched_table_no'] != 0:
            exitcode, inner_states, setpoints = RunSchedule(client, input_states, sched_table, inner_states)
            pprint.pprint(setpoints)
            pprint.pprint(inner_states)

            builder.add_32bit_float(setpoints['P_Setpoint_Internal'])    
            builder.add_32bit_float(setpoints['Q_Setpoint_Internal']) 
            builder.add_32bit_float(setpoints['ActiveMinSOC_Setpoint']) 
            builder.add_32bit_float(setpoints['ActiveMaxSOC_Setpoint'])  

        else:

            builder.add_32bit_float(0)    
            builder.add_32bit_float(0) 
            builder.add_32bit_float(0) 
            builder.add_32bit_float(100) 
        
        payload = builder.to_registers()
        #payload = builder.build()
        print("-" * 60)
        print("Writing Registers")
        print("-" * 60)
        print(payload)
        print("\n")
            
        #payload = builder.build()
        
        # Write registers
        registers = builder.to_registers()
        rq = client.write_registers(address, registers)


        ## 
        time.sleep(5)
    '''
    sched_table={}
    sched_table[1] = schedule_A()
    sched_table[2] = schedule_B()
    pprint.pprint(sched_table)

    #input_states = read_input_states(client)
    #pprint.pprint(input_states)

    for t in range(1,len(sched_table)+1):
    
        try:
            exitcode = ProcessSchedule(sched_table[t], client)
            print('Exitcode: {}'.format(exitcode))
        except:
            setpoints={}
            setpoints['P_Setpoint_Internal'] = 0
            setpoints['Q_Setpoint_Internal'] = 0
            setpoints['ActiveMaxSOC_Setpoint'] = 100
            setpoints['ActiveMinSOC_Setpoint'] = 0
            builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
        
            builder.add_32bit_float(setpoints['P_Setpoint_Internal'])    
            builder.add_32bit_float(setpoints['Q_Setpoint_Internal']) 
            builder.add_32bit_float(setpoints['ActiveMinSOC_Setpoint']) 
            builder.add_32bit_float(setpoints['ActiveMaxSOC_Setpoint'])     
            
            payload = builder.to_registers()
            print("-" * 60)
            print("Writing Registers")
            print("-" * 60)
            print(payload)
            print("\n")
            payload = builder.build()
            address = 5002
            # Write registers
            registers = builder.to_registers()
            rq = client.write_registers(address, registers)
        finally:
            client.close()

    #pprint.pprint(output_state)

    #rq = client.readwrite_registers(**arguments)
    #rr = client.read_input_registers(1,8)
    #dassert(rq, lambda r: r.registers == [20]*8)      # test the expected value
    #dassert(rr, lambda r: r.registers == [17]*8)      # test the expected value

    #rq = client.write_register(1, 10, unit=1)
    #rr = client.read_holding_registers(1, 1, unit=1)
    #assert(rq.function_code < 0x80)     # test that we are not an error
    #assert(rr.registers[0] == 10)       # test the expected value
'''


if __name__ == '__main__':
    sys.exit(main())
    #sys.exit(0)