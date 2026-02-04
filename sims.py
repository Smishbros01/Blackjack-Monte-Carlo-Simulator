import numpy as np
import json
from backend import Deck, play_hand, CONFIG
from strats import should_split, should_double

#goes through the strategy
def test_strategy(name, strategy, use_count=False):
    outcomes = []
    deck = Deck()
    games = CONFIG['simulation_params']['standard_ev_games']

    #run the strategy for a number of games
    for _ in range(games):

        #check deck length if its too small then reset deck
        if len(deck.cards) < CONFIG['table_rules']['min_cards_before_shuffle']:
            deck.shuffle()

        bet_multiplier = 10 if (use_count and deck.true_count > 2) else 1
        res = play_hand(deck, strategy, should_split, should_double)
        outcomes.append(res * bet_multiplier)

    avg_ev = np.mean(outcomes)
    std_dev = np.std(outcomes)
    sharpe = avg_ev / std_dev if std_dev != 0 else 0
    
    print(f"{name:20} | EV: {avg_ev:>7.4f} | SD: {std_dev:>7.4f} | Sharpe: {sharpe:>7.4f}")
    return name, avg_ev

#simulate player card counting strategy using a starting balance
def bankroll_simulation(strategy):
    s_params = CONFIG['simulation_params']
    b_params = CONFIG['betting_params']
    
    bankroll = s_params['starting_bankroll']
    history = [bankroll]
    deck = Deck()
    
    #each _ is a game p;ayed but before we run the game we must 
    #check whether or not the player has enough funds
    for _ in range(s_params['games_limit']):
        if bankroll <= 0: break
        
        #check player edge
        edge = (deck.true_count - b_params['count_threshold']) * 0.005

        #if edge positive we divide by 1.3 as a safety net 
        #multiply by kelly fraction to prevent small losing streaks 
        #from causing horrible drawdowns
        if edge > 0:
            fraction = (edge / 1.3) * b_params['kelly_fraction']
            bet_unit = max(b_params['min_bet'], bankroll * fraction)

        #if our edge is negative or 0 we wil just place our minimum bet
        else:
            bet_unit = b_params['min_bet']
            
        #if we cannot afford min bet use our bankroll, play game and edit bankroll
        #after game track how there bankroll has changed
        bet_unit = min(bet_unit, bankroll)
        result = play_hand(deck, strategy, should_split, should_double)
        bankroll += (result * bet_unit)
        history.append(bankroll)
        
        #check if min cards in deck if too small reset
        if len(deck.cards) < CONFIG['table_rules']['min_cards_before_shuffle']:
            deck.shuffle()

    return history, bankroll <= 0

#calculate risk of ruin (likelihood of losing entire bankroll)
def calculate_risk_of_ruin(strategy):
    
    #iterations are players
    iterations = CONFIG['simulation_params']['monte_carlo_iterations']
    ruin_count = 0
    all_paths = []

    #for each player run the bankroll simulation
    for _ in range(iterations):
        history, is_bust = bankroll_simulation(strategy)
        all_paths.append(history)

        #if they go below 0 then add them to ruin count
        if is_bust: ruin_count += 1
            
    ruin_probability = (ruin_count / iterations) * 100
    print(f"Solvency Report")
    print(f"Iterations: {iterations} | Ruin Prob: {ruin_probability:.2f}%")
    return all_paths, ruin_probability