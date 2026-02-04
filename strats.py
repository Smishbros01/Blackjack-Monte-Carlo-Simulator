import random
from backend import score

#check if we should split
def should_split(card_value, dealer_upcard):

    #always split pair of aces and pair of 8s (pair of 8s is the worst hand)
    if card_value in [11, 8]:
        return True
    
    #10 pair is already 20, never split 5 pair is 10 so still good
    if card_value in [10, 5]:
        return False
    
    #depending on how weak dealer upcard is we split 2, 3, 7 pairs
    if card_value in [2, 3, 7] and dealer_upcard <= 7:
        return True
    
    #only split 6 pair if dealer upcard is super weak
    if card_value == 6 and dealer_upcard <= 6:
        return True
        
    #split 9 pair if dealer upcard is 7 (may have 17), 10/ace (may have 21 or >18)
    if card_value == 9 and dealer_upcard not in [7, 10, 11]:
        return True
    
    return False

#always hit less than 17
def conservative(hand, dealer_upcard):
    return score(hand) < 17

#always hit less than 19
def aggressive(hand, dealer_upcard):
    return score(hand) < 19

#50/50 chance of hitting (random)
def random_play(hand, dealer_upcard):
    return random.random() < 0.5

#base hitting on dealer upcard
def dealer_aware(hand, dealer_upcard):
    val = score(hand)
    
    #dealer has super weak upcard then stand on 12+ hope for bust
    if dealer_upcard <= 6:
        return val < 12
    
    #dealer is strong then must at least hit until 17
    else:
        return val < 17

#check if we should double down
def should_double(hand, dealer_upcard):
    val = score(hand)

    #only double on 9, 10, or 11 best odds
    if val == 11:
        return True
    if val == 10 and dealer_upcard <= 9:
        return True
    if val == 9 and dealer_upcard in [3, 4, 5, 6]:
        return True
        
    return False