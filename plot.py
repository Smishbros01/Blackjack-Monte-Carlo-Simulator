import matplotlib.pyplot as plt
from backend import CONFIG
import os

#for ev bar graph
def plot_results(results):
    names = [r[0] for r in results]
    evs = [r[1] for r in results]

    #green for pos ev, red for neg ev
    colors = ['#2ecc71' if ev > 0 else '#e74c3c' for ev in evs]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, evs, color=colors, edgecolor='black', alpha=0.8)
    
    #for baseline
    plt.axhline(0, color='black', linewidth=0.8)

    plt.ylabel("Expected Value (EV)", fontsize=12)
    plt.title("Blackjack Strategy: Profitability Comparison", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    #rotate names if they overlap
    plt.xticks(rotation=15)
    
    #auto adjust format
    plt.tight_layout()

    if not os.environ.get('GITHUB_ACTIONS'):
        plt.show()

#for monte carlo line graph
def plot_bankroll_paths(paths, title):
    plt.figure(figsize=(10, 5))

    #plot each players cycle
    for path in paths[:CONFIG['simulation_params']['monte_carlo_iterations_graph_paths']]: 
        plt.plot(path, linewidth=1, alpha=0.5)

    #ruin line
    plt.axhline(0, color='red', linestyle='--', label='Bankruptcy')

    #start line
    plt.axhline(CONFIG['simulation_params']['starting_bankroll'], color='black', label='Starting')
    
    plt.title(title)
    plt.xlabel('Hands Played')
    plt.ylabel('Bankroll ($)')
    plt.legend()
    if not os.environ.get('GITHUB_ACTIONS'):
        plt.show()