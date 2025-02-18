import unittest
import math

# Import the functions to be tested.
# Adjust the import statement if your module name is different.
from blackjack_ui import calculate_hand_value, update_count, calculate_true_count

class TestBlackjackFunctions(unittest.TestCase):
    # Tests for calculate_hand_value
    def test_calculate_hand_value_no_ace(self):
        print("Test: calculate_hand_value with no Ace. Expect hand total of 15 (5 + K).")
        # A hand with no aces: 5 + K (10) = 15.
        hand = [('5', 'Hearts', 5), ('K', 'Spades', 10)]
        self.assertEqual(calculate_hand_value(hand), 15)

    def test_calculate_hand_value_with_one_ace_no_adjustment(self):
        print("Test: calculate_hand_value with one Ace that does not require adjustment. Expect hand total of 16 (Ace + 5).")
        # A hand with one ace where 11 doesn't bust: Ace + 5 = 16.
        hand = [('A', 'Diamonds', 11), ('5', 'Clubs', 5)]
        self.assertEqual(calculate_hand_value(hand), 16)

    def test_calculate_hand_value_with_one_ace_adjustment(self):
        print("Test: calculate_hand_value with one Ace needing adjustment. Expect hand total of 13 (Ace adjusted from 11 to 1 with 9 and 3).")
        # A hand where ace must be adjusted: Ace (11) + 9 + 3 = 23 initially,
        # then ace becomes 1 so total is 13.
        hand = [('A', 'Hearts', 11), ('9', 'Diamonds', 9), ('3', 'Clubs', 3)]
        self.assertEqual(calculate_hand_value(hand), 13)

    def test_calculate_hand_value_multiple_aces(self):
        print("Test: calculate_hand_value with multiple Aces. Expect hand total of 12 (one Ace adjusted from 11 to 1).")
        # Two aces: initially 11 + 11 = 22 but one ace must be reduced so total becomes 12.
        hand = [('A', 'Hearts', 11), ('A', 'Spades', 11)]
        self.assertEqual(calculate_hand_value(hand), 12)

    # Tests for update_count
    def test_update_count_increase(self):
        print("Test: update_count with a low card (5). Expect count to increase by 1.")
        # Cards 2-6 should increase the count by one.
        card = ('5', 'Hearts', 5)
        self.assertEqual(update_count(card, 0), 1)
    
    def test_update_count_decrease_ten(self):
        print("Test: update_count with a high card (K, value 10). Expect count to decrease by 1.")
        # Cards with value 10 decrease the count by one.
        card = ('K', 'Spades', 10)
        self.assertEqual(update_count(card, 0), -1)
    
    def test_update_count_decrease_eleven(self):
        print("Test: update_count with an Ace (value 11). Expect count to decrease by 1.")
        # Ace is represented as 11, so should decrease the count.
        card = ('A', 'Diamonds', 11)
        self.assertEqual(update_count(card, 5), 4)
    
    def test_update_count_no_change(self):
        print("Test: update_count with a neutral card (8). Expect no change in count.")
        # Cards with values not in [2,3,4,5,6] or [10, 11] (e.g., 7, 8, 9) should leave the count unchanged.
        card = ('8', 'Clubs', 8)
        self.assertEqual(update_count(card, 2), 2)

    # Tests for calculate_true_count
    def test_calculate_true_count_multiple_decks(self):
        print("Test: calculate_true_count with 2 full decks (104 cards) and running count 4. Expect true count of 2.0.")
        # Simulate a shoe with 104 cards (2 full decks).
        shoe = [("dummy", "dummy", 0)] * 104
        # For a running count of 4, the true count should be 4 / 2 = 2.0.
        self.assertAlmostEqual(calculate_true_count(4, shoe), 2.0)
    
    def test_calculate_true_count_less_than_one_deck(self):
        print("Test: calculate_true_count with less than a full deck (26 cards) and running count 4. Expect true count of 4.0.")
        # Simulate a shoe with 26 cards (less than one full deck, but math.ceil(26/52) = 1).
        shoe = [("dummy", "dummy", 0)] * 26
        self.assertAlmostEqual(calculate_true_count(4, shoe), 4.0)
    
    def test_calculate_true_count_empty_shoe(self):
        print("Test: calculate_true_count with an empty shoe and running count 4. Expect true count equal to running count (4).")
        # If the shoe is empty, math.ceil(0) = 0 and the function should return the running count.
        shoe = []
        self.assertEqual(calculate_true_count(4, shoe), 4)

if __name__ == '__main__':
    unittest.main()
