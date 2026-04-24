import numpy as np

def fedavg(client_updates):
    # basic federated averaging which is just taking the mean of all client updates
    # works fine when everyone is honest but falls apart fast with bad actors
    # even a few malicious clients with extreme values can drag the mean way off
    return np.mean(client_updates)

def trimmed_mean(client_updates, trim=0.2):
    # defense against poisoning: trim the most extreme values before averaging
    # trim=0.2 cuts the bottom 20% and top 20% before taking the mean
    # so malicious clients sending garbage values just get ignored
    # works well when the number of bad actors is below the trim threshold
    # starts breaking down when malicious clients outnumber the trim buffer
    
    sorted_updates = sorted(client_updates)
    cut = int(len(sorted_updates) * trim)
    
    if cut == 0:
        return np.mean(sorted_updates)
    
    trimmed = sorted_updates[cut:-cut]
    return np.mean(trimmed)