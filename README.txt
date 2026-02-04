#Blackjack Monte Carlo: Strategy & Solvency Simulator

Welcome to the Blackjack Strategy Simulator! This project is a tool designed to simulate thousands of Blackjack games to analyze the mathematical Expected Value (EV) of various strategies and the long-term "Risk of Ruin" for card counters.

Intended Use
- Strategy Benchmarking: Compare standard strategies (Conservative, Aggressive, Dealer-Aware) against a random baseline.
- Risk Analysis: Use Monte Carlo simulations to see how a fixed bankroll changes over time using the Kelly Criterion for bet sizing.
- Card Counting Evaluation: Quantify the actual advantage gained by standardized card counting.
- Visual Reporting: Generate distribution charts and "Random Walk" bankroll paths to visualize variance.

How to Install Dependencies
1. Ensure you have Python 3.8+ installed.
2. It is recommended to use a virtual environment:
	In terminal type
		python -m venv venv
		source venv/bin/activate  # On Windows: venv\Scripts\activate

Install the required libraries:
1. In terminal type
	pip install -r requirements.txt

How to Run the Simulator
1. Open your Terminal or Command Line.
2. Navigate to the project directory.
3. Run the main simulation:
	In terminal type
		python main.py

How to Customize the Simulation
	All parameters are within in config.json.
	You can modify:
		Table Rules: Number of decks, blackjack payout (e.g., 1.5 for 3:2) and shuffle points.
		Simulation Params: Starting bankroll, the number of hands to play and how many iterations to run.
		Betting Params: Minimum bets and the "Kelly Fraction" (how aggressive the card counter should be).

What Outputs to Expect
	- Statistical Table: A console output showing EV, Standard Deviation, and the Sharpe Ratio for 5 different strategies.
	- Solvency Report: A percentage breakdown of how many players ended the simulation profitable, at break-even, or totally bankrupt (Ruin).
	- Profitability Comparison: A bar chart color-coded by performance (Green for profit, Red for loss).
	- Volatility Visualization: A line graph showing the "Random Walk" of various bankrolls over multiple hands.

Limitations
	- Splitting Complexity: The current code only supports a single split, it does not currently support splitting multiple times.
	- Fixed Dealer Rules: The dealer is hardcoded to stand on all 17s.
	- Memory Usage: Running more than 10,000 iterations with high games_limit may consume significant RAM due to path tracking.