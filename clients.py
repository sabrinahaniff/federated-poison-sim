import random

# The true value every honest client is trying to report
TRUE_VALUE = 1.0

def honest_client(true_value):
    # Gaussian noise simulates the natural variance in real local datasets
    # mean=0 means the noise is unbiased and honest clients aren't systematically wrong
    # std=0.1 means most honest votes land within 0.1 of the true value
    noise = random.gauss(0, 0.1)
    return true_value + noise

def malicious_label_flipper(true_value):
    # Very classic poisoning attack, reports the exact negation of truth
    # In real FL maps to flipping class labels in training data
    # If true is 1.0, this client always reports -1.0
    return -true_value

def malicious_random_poisoner():
    # More aggressive attack, sends random noise between -10 and 10
    # Goal is to maximally destabilize the aggregate regardless of direction
    return random.uniform(-10, 10)