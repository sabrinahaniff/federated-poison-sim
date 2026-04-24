# Federated Learning Poisoning Attack Simulator

I built this to understand how poisoning attacks actually work in federated 
learning and whether the trimmed mean defense holds up under pressure. 
Motivated by reading about proactive defense mechanisms in distributed AI 
systems.

## The Core Idea

In federated learning, clients train locally and send updates to a central 
server. If some clients are malicious they can send poisoned updates to 
corrupt the global model. This is called a poisoning attack.

I simplified this down to the math to understand it clearly:
- Honest clients report a true value with some natural noise
- Malicious clients send manipulated values (flipped labels or random garbage)
- The server tries to recover the true value using two strategies:
- FedAvg: plain average, fast, works when everyone is honest
- Trimmed Mean: cuts extreme values before averaging, more robust

## What I Found

![Results Chart](results.png)

- At 10-20% malicious clients, trimmed mean cuts error by over 90%. The defense works really well here.
- At 30% malicious clients, improvement drops to around 38%. Poisoned votes are starting to survive the trim.
- At 50% malicious clients, trimmed mean stops helping entirely.
- Beyond 50%, trimmed mean actually makes things worse because it starts cutting honest votes instead of malicious ones.

The 20% trim parameter is basically a hard limit. Once malicious clients 
exceed it the defense collapses. This is a known limitation and part of 
what motivates more adaptive approaches like the RECESS vaccine.

## Files

```
clients.py      -- honest clients with gaussian noise, malicious clients 
                   with label flipping and random poisoning
aggregator.py   -- FedAvg and trimmed mean implementations
simulation.py   -- runs 100 rounds per configuration
main.py         -- varies malicious ratio from 10% to 80% and plots results
```

## Attack Types

**Label flipping** -- malicious client reports the exact opposite of the 
true value. In a real system this maps to flipping training labels.

**Random poisoning** -- malicious client sends a random value between -10 
and 10. Models a disruptive attacker who just wants to break things.

## How the Defense Works

Trimmed mean with trim=0.2:
1. Sort all client updates
2. Cut the bottom 20% and top 20%
3. Average what's left

Works great until malicious clients outnumber the trim buffer. After that 
point you need something smarter, like tracking client behavior across 
multiple rounds instead of just looking at one round at a time.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy matplotlib
python main.py
```
