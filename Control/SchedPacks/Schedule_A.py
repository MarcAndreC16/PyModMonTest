def schedule_A():

    sched = {
    1: {'Action' :0, 'P' : 28.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' : 1 * 60 },	    # Charge to SOCmax=100%	
    2: {'Action' :0, 'P' : 10.0, 'Q' :0, 'maxSOC' :100, 'minSOC':0, 'Duration' :1 * 60 },     # Wait for 10 minutes
    3: {'Action' :1, 'P' : 30.0, 'Q' :0, 'maxSOC' :96, 'minSOC':0, 'Duration' :2 * 60 },     # Wait for 10 minutes
    }	

    return(sched)	