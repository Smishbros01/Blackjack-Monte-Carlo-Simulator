import random
import json

#load assumptions from the config
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

class Deck:
    def __init__(self):
        self.num_decks = CONFIG['table_rules']['num_decks']
        self.cards = []
        self.build()
        self.shuffle()
        self.running_count = 0

    #create full deck of cards
    def build(self):
        single = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        self.cards = single * self.num_decks

    #shuffle deck to simulate real life shuffling
    def shuffle(self):
        random.shuffle(self.cards)
        self.running_count = 0

    #check if there are cards create full deck if not then use pop to 
    #simulate drawing from top of deck
    def draw(self):
        if not self.cards:
            self.build()
            self.shuffle()
        card = self.cards.pop()

        #card counting rules
        if card in [2, 3, 4, 5, 6]:
            self.running_count += 1
        elif card in [10, 11]:
            self.running_count -= 1
        return card

    #true count is disrupted by the number of decks so true_count standardizes it
    @property
    def true_count(self):
        decks_remaining = max(len(self.cards) / 52, 1)
        return self.running_count / decks_remaining

#calulcate total and account for ace switches
def score(hand):
    total = sum(hand)
    aces = hand.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

#play a game
def play_hand(deck, strategy, split_logic, double_logic):
    rules = CONFIG['table_rules']
    p_card1, p_card2 = deck.draw(), deck.draw()
    dealer = [deck.draw(), deck.draw()]

    #nested lists make it easier when we split decks
    player_hands = [[[p_card1, p_card2], 1]]
    
    #check if we allow splitting and then see if we meet the reqs for splitting
    if rules['allow_split'] and p_card1 == p_card2 and split_logic(p_card1, dealer[0]):
        player_hands = [[[p_card1, deck.draw()], 1], [[p_card2, deck.draw()], 1]]

    #natural check for dealer
    if score(dealer) == 21:
        return sum(0 if score(h[0]) == 21 else -h[1] for h in player_hands)

    total_payout = 0

    #iterate through multiple hands
    for hand_data in player_hands:
        hand, bet = hand_data[0], hand_data[1]
        
        #natural check for first hand ONLY
        if score(hand) == 21 and len(player_hands) == 1:
            total_payout += rules['blackjack_payout']
            continue
            
        #check for double down
        if rules['allow_double'] and double_logic(hand, dealer[0]):
            hand_data[1] = bet * 2
            bet = hand_data[1]
            hand.append(deck.draw())
            if score(hand) > 21:
                total_payout -= bet
                continue

        #play normal round using strategy
        else:
            while strategy(hand, dealer[0]):
                hand.append(deck.draw())
                if score(hand) > 21: break
            if score(hand) > 21:
                total_payout -= bet
                continue

    #dealer plays turn (always hits on <17 so hardcode)
    while score(dealer) < 17:
        dealer.append(deck.draw())
    d_final = score(dealer)

    #compare hands
    for hand, bet in player_hands:
        p_final = score(hand)
        if p_final > 21: continue
        if d_final > 21 or p_final > d_final: total_payout += bet
        elif p_final < d_final: total_payout -= bet
            
    return total_payout