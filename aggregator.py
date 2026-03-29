import numpy as np

def fedavg(votes):
    # The original Google FedAvg algorithm in its simplest form
    # Just a plain mean, fast and works perfectly when all clients are honest
    # Vulnerability: one malicious client with an extreme value pulls the mean toward them
    # With 7 honest votes near 1.0 and 3 flippers at -1.0:
    # mean = (7*1.0 + 3*-1.0) / 10 = 0.4 is significantly corrupted
    return np.mean(votes)

def trimmed_mean(votes, trim=0.2):
    # Robust aggregation defense is to TRIM extreme values before averaging
    # trim=0.2 means cut the bottom 20% and top 20% of votes
    # With 10 clients that's cutting 2 from each end = 4 votes removed total
    # Malicious clients sending -1.0 or random extremes get trimmed out
    # What remains is dominated by the honest clients near 1.0
    votes = sorted(votes)
    cut = int(len(votes) * trim)
    # If cut=2 and votes has 10 elements:
    # votes[2:8], keep only the middle 6 votes
    trimmed = votes[cut: len(votes) - cut]
    return np.mean(trimmed)