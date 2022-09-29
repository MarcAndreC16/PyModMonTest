 #  SCHEDULE FOR MEASUREMENTS
    # 
    #  Action : 0: as_given  (pause of value Duration)
    #        	1: charge/discharge to given maxSOC
    #        	(2: charge (to defined maxSOC with given P)
    #        	(3: discharge (to defined maxSOC with given P)
    #        	(4: standby)
    #        	(5: default)
    #  Duration : 0 = do not wait
    #             >0 = wait in sec
	#  If Value== 0.0: not used value

def schedule_A():

    sched = {
        1: { 'Action' :0, 'P' :0.0, 'Q' :0.0, 'maxSOC' :100, 'minSOC' :0.0, 'Duration' :10 }, # Pause for 5 minutes (not mandatory)
		
		#--------Start of Battery-Test------------
		#---Conditioning---		
		2: { 'Action' :1, 'P' : 100, 'Q' :0.0, 'maxSOC' :100, 'minSOC':0.0, 'Duration' : 0.0 * 60 },	#Charge to SOCmax=100%	
		3: { 'Action' :0, 'P' :   0.0, 'Q' :0.0, 'maxSOC' :100, 'minSOC':0.0, 'Duration' :10 }, # Pause for 10 minutes
		
		#---Discharging/Charging with 100% nom. Power	(1of3)---
		4: { 'Action' :3, 'P' : 100.0, 'Q' :0, 'maxSOC' :  0, 'minSOC':0.0, 'Duration' : 0.0 * 60 },	#Discharging
		5: { 'Action' :0, 'P' :   0.0, 'Q' :0.0, 'maxSOC' :100, 'minSOC':0.0, 'Duration' : 5  }, # Pause for 5 minutes (not mandatory)
		6: { 'Action' :2, 'P' : 100.0, 'Q' :0.0, 'maxSOC' :100, 'minSOC':0.0, 'Duration' : 0.0 * 60 }, #Charging
		7: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 }, # Pause for 5 minutes (not mandatory)
		# #---Discharging/Charging with 100% nom. Power	(2of3)---
		# 8: { 'Action' :1, 'P' : 100.0, 'Q' :0, 'maxSOC' :  0, 'minSOC':0, 'Duration' : 0 * 60 },	#Discharging
		# 9: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		# 10: { 'Action' :1, 'P' : 100.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 0 * 60 }, #Charging
		# 11: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		# #---Discharging/Charging with 100% nom. Power	(3of3)---
		# 12: { 'Action' :1, 'P' : 100.0, 'Q' :0, 'maxSOC' :  0, 'minSOC':0, 'Duration' : 0 * 60 },	#Discharging
		# 13: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		# 14: { 'Action' :1, 'P' : 100.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 0 * 60 }, #Charging
		# 15: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		
		# #{ 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		
    }	

    return(sched)	

def schedule_B():

    sched = {

		1: { 'Action' :0, 'P' :0.0, 'Q' :0.0, 'maxSOC' :100, 'minSOC' :0.0, 'Duration' :10 }, # Pause for 5 minutes (not mandatory)
		
		#--------Start of Battery-Test------------
		#---Conditioning---		
		2: { 'Action' :1, 'P' : 100, 'Q' :0.0, 'maxSOC' :100, 'minSOC':0.0, 'Duration' : 0.0 * 60 },	#Charge to SOCmax=100%	
		3: { 'Action' :0, 'P' :   0.0, 'Q' :0.0, 'maxSOC' :100, 'minSOC':0.0, 'Duration' :10 }, # Pause for 10 minutes

		#---Discharging/Charging with 50% nom. Power	(1of3)---
		4: { 'Action' :1, 'P' :  50.0, 'Q' :0, 'maxSOC' :  0, 'minSOC':0, 'Duration' : 0 * 60 },	#Discharging
		5: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		6: { 'Action' :1, 'P' : -50.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 0 * 60 }, #Charging
		7: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		#---Discharging/Charging with 50% nom. Power	(2of3)---
		8: { 'Action' :1, 'P' :  50.0, 'Q' :0, 'maxSOC' :  0, 'minSOC':0, 'Duration' : 0 * 60 },	#Discharging
		9: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		10: { 'Action' :1, 'P' : -50.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 0 * 60 }, #Charging
		11: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		#---Discharging/Charging with 50% nom. Power	(2of3)---
		12: { 'Action' :1, 'P' :  50.0, 'Q' :0, 'maxSOC' :  0, 'minSOC':0, 'Duration' : 0 * 60 },	#Discharging
		13: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		14: { 'Action' :1, 'P' : -50.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 0 * 60 }, #Charging
		15: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		
		#{ 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
    }	

    return(sched)	


def schedule_C():
	
	sched = {
    	1: { 'Action' :0, 'P' :0.0, 'Q' :0.0, 'maxSOC' :100, 'minSOC' :0.0, 'Duration' :10 }, # Pause for 5 minutes (not mandatory)
		
		#--------Start of Battery-Test------------
		#---Conditioning---		
		2: { 'Action' :1, 'P' : 100, 'Q' :0.0, 'maxSOC' :100, 'minSOC':0.0, 'Duration' : 0.0 * 60 },	#Charge to SOCmax=100%	
		3: { 'Action' :0, 'P' :   0.0, 'Q' :0.0, 'maxSOC' :100, 'minSOC':0.0, 'Duration' :10 }, # Pause for 10 minutes

		#---Discharging/Charging with 25% nom. Power	(1of3)---
		4: { 'Action' :1, 'P' :  25.0, 'Q' :0, 'maxSOC' :  0, 'minSOC':0, 'Duration' : 0 * 60 },	#Discharging
		5: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		6: { 'Action' :1, 'P' :  25.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 0 * 60 }, #Charging
		7: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		#---Discharging/Charging with 25% nom. Power	(2of3)---
		8: { 'Action' :1, 'P' :  25.0, 'Q' :0, 'maxSOC' :  0, 'minSOC':0, 'Duration' : 0 * 60 },	#Discharging
		9: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		10: { 'Action' :1, 'P' :  25.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 0 * 60 }, #Charging
		11: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		#---Discharging/Charging with 25% nom. Power	(3of3)---
		12: { 'Action' :1, 'P' :  25.0, 'Q' :0, 'maxSOC' :  0, 'minSOC':0, 'Duration' : 0 * 60 },	#Discharging
		13: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		14: { 'Action' :1, 'P' :  25.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 0 * 60 }, #Charging
		15: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		
		16: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 5 * 60 }, # Pause for 5 minutes (not mandatory)
		
		#--------End of Battery-Test------------
		
		17: { 'Action' :0, 'P' :   0.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 0 * 60 }, # OFF     # Wait for 10 minutes
	}
	return(sched)	
