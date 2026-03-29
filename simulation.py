import random
import numpy as np
from clients import honest_client, malicious_label_flipper, malicious_random_poisoner
from aggregator import fedavg, trimmed_mean

def run(n_clients=10, n_malicious=3, rounds=100):
    # true_value is what every honest client is trying to report
    # the "correct answer" the federation should converge to
    true_value = 1.0
    
    results = {
        "no_defense": [],
        "with_defense": [],
        "n_malicious": n_malicious,
        "n_clients": n_clients
    }

    for _ in range(rounds):
        # honest clients report true value with natural noise
        votes = [honest_client(true_value) 
                for _ in range(n_clients - n_malicious)]
        
        # malicious clients report poisoned values
        votes += [malicious_label_flipper(true_value) 
                 for _ in range(n_malicious)]
        
        # shuffle so aggregator can't identify malicious by position
        random.shuffle(votes)
        
        # record both aggregation strategies
        results["no_defense"].append(fedavg(votes))
        results["with_defense"].append(trimmed_mean(votes))

    return results