from simulation import run
import numpy as np
import matplotlib.pyplot as plt

def print_results(results):
    true_value = 1.0
    no_def_avg = np.mean(results["no_defense"])
    with_def_avg = np.mean(results["with_defense"])
    no_def_error = abs(true_value - no_def_avg)
    with_def_error = abs(true_value - with_def_avg)
    improvement = ((no_def_error - with_def_error) / no_def_error * 100)

    print(f"{results['n_malicious']}/{results['n_clients']} malicious | "
          f"fedavg error: {no_def_error:.4f} | "
          f"trimmed mean error: {with_def_error:.4f} | "
          f"improvement: {improvement:.1f}%")

def plot_results(all_results):
    ratios = [r["n_malicious"] / r["n_clients"] for r in all_results]
    no_def = [abs(1.0 - np.mean(r["no_defense"])) for r in all_results]
    with_def = [abs(1.0 - np.mean(r["with_defense"])) for r in all_results]

    plt.figure(figsize=(10, 6))
    plt.plot(ratios, no_def, 'r-o', label='FedAvg (no defense)')
    plt.plot(ratios, with_def, 'g-o', label='Trimmed Mean (with defense)')
    
    # trimmed mean starts breaking down past this point
    plt.axvline(x=0.2, color='gray', linestyle='--', alpha=0.7,
                label='trim threshold (20%)')
    
    plt.xlabel('fraction of malicious clients')
    plt.ylabel('error from true value')
    plt.title('federated learning poisoning — fedavg vs trimmed mean')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('results.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("saved to results.png")

if __name__ == "__main__":
    print("running poisoning experiments across different malicious client ratios...\n")
    
    all_results = []
    for n_malicious in range(1, 9):
        results = run(n_clients=10, n_malicious=n_malicious, rounds=100)
        print_results(results)
        all_results.append(results)

    print("\nplotting results...")
    plot_results(all_results)