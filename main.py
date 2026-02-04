from sims import test_strategy, calculate_risk_of_ruin
from strats import random_play, conservative, aggressive, dealer_aware
from plot import plot_results, plot_bankroll_paths
from backend import CONFIG
import matplotlib.pyplot as plt


def print_simulation_summary(paths, starting_bankroll):

    #Get the final bankroll from every iteration
    final_values = [p[-1] for p in paths]
    total_iters = len(final_values)

    #Categorize the results
    busts = [v for v in final_values if v <= 0]
    losers = [v for v in final_values if 0 < v < starting_bankroll]
    break_even = [v for v in final_values if v == starting_bankroll]
    winners = [v for v in final_values if v > starting_bankroll]

    #Calculate Percentages
    prob_bust = (len(busts) / total_iters) * 100
    prob_loss = (len(losers) / total_iters) * 100
    prob_be = (len(break_even) / total_iters) * 100
    prob_win = (len(winners) / total_iters) * 100

    #Printout
    print("\n Simulation End State Summary")
    print(f"Total Iterations: {total_iters}")
    print(f"Starting Capital:   ${starting_bankroll:,}")
    print(f"Profitable:    {prob_win:>6.2f}% ({len(winners)} paths)")
    print(f"Break Even:    {prob_be:>6.2f}% ({len(break_even)} paths)")
    print(f"Net Loss:      {prob_loss:>6.2f}% ({len(losers)} paths)")
    print(f"Total Ruin:    {prob_bust:>6.2f}% ({len(busts)} paths)")

    #Calculate average
    avg_final = sum(final_values) / total_iters
    print(f"Expected Final Wealth: ${avg_final:,.2f}")

def main():
    print(" Running Strategy Comparison...")
    results = []
    
    #Run strategies and store results in a list of tuples for the bar chart
    results.append(test_strategy("Random", random_play))
    results.append(test_strategy("Conservative", conservative))
    results.append(test_strategy("Aggressive", aggressive))
    results.append(test_strategy("Dealer Aware", dealer_aware))
    results.append(test_strategy("Count + Aware", dealer_aware, use_count=True))

    print("\n Starting Solvency Analysis for Card Counting...")
    paths, ruin_prob = calculate_risk_of_ruin(dealer_aware)

    #print out the simulation summary
    print_simulation_summary(paths, CONFIG['simulation_params']['starting_bankroll'])

    print("\n Generating Graphs...")
    
    #Plot EVs for all strategies side by side
    plot_results(results) 
    
    #shows how iterations won or lose overtime
    plot_bankroll_paths(paths, "Monte Carlo: Bankroll Volatility (Card Counting)")

if __name__ == "__main__":
    main()