import pygame
import random
import math

# ================ #
#  CARD & SHOE     #
# ================ #

# Define the four suits used in a standard deck.
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Define the card ranks and their corresponding values.
# Note: The Ace initially counts as 11; its value may be adjusted later.
ranks = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def create_deck():
    """
    Create a single deck of cards.
    Each card is represented as a tuple: (rank, suit, value).
    """
    return [(rank, suit, value) for suit in suits for rank, value in ranks.items()]

def create_shoe(num_decks=6):
    """
    Create a "shoe" which is a collection of multiple decks.
    By default, six decks are combined to form the shoe.
    After combining, the cards are shuffled.
    """
    shoe = []
    for _ in range(num_decks):
        shoe.extend(create_deck())
    random.shuffle(shoe)
    return shoe

def calculate_hand_value(hand):
    """
    Calculate the total value of a hand of cards.
    Initially, all Aces are counted as 11. If the total value exceeds 21,
    adjust the value of one or more Aces from 11 to 1 until the total is 21 or below.
    """
    total = sum(card[2] for card in hand)
    ace_count = sum(1 for card in hand if card[0] == 'A')
    while total > 21 and ace_count:
        total -= 10
        ace_count -= 1
    return total

def update_count(card, count):
    """
    Update the running count for card counting (Hi-Lo system).
    """
    if card[2] in [2, 3, 4, 5, 6]:
        count += 1
    elif card[2] in [10, 11]:
        count -= 1
    return count

def calculate_true_count(count, shoe):
    """
    Calculate the true count by adjusting the running count based on the number
    of decks remaining in the shoe.
    """
    decks_remaining = math.ceil(len(shoe) / 52)
    return count / decks_remaining if decks_remaining else count

def draw_card(shoe, count):
    """
    Draw a card from the shoe and update the running count.
    """
    if not shoe:
        print("Shoe is empty. Reshuffling...")
        shoe.extend(create_shoe())
        count = 0
        random.shuffle(shoe)
    card = shoe.pop()
    count = update_count(card, count)
    return card, count

# ================ #
#  PYGAME SETUP    #
# ================ #

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack Coach")

table_image = pygame.image.load("output.png")
table_image = pygame.transform.scale(table_image, (WIDTH, HEIGHT))

# Load card images for each suit.
suit_images = {
    "Clubs": pygame.image.load("Clubs.png"),
    "Diamonds": pygame.image.load("Diamonds.png"),
    "Hearts": pygame.image.load("Hearts.png"),
    "Spades": pygame.image.load("Spades.png")
}
card_back = pygame.image.load("Card-Back.png")
card_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def get_card_image(suit, rank):
    """
    Return the image for a specific card given its suit and rank.
    """
    index = card_ranks.index(rank)
    suit_image = suit_images[suit]
    CARD_WIDTH = suit_image.get_width() // 13
    CARD_HEIGHT = suit_image.get_height()
    return suit_image.subsurface((index * CARD_WIDTH, 0, CARD_WIDTH, CARD_HEIGHT))

# ─── NEW DRAWING FUNCTIONS ───────────────────────────────
def draw_dealer_hand(dealer_hand, hide_dealer=False):
    """
    Draw the dealer's hand (centered at the top).
    If hide_dealer is True, the dealer's second card is shown face down.
    """
    card_spacing = 80
    total_width = len(dealer_hand) * card_spacing
    start_x = (WIDTH - total_width) // 2
    y_dealer = 50
    for i, card in enumerate(dealer_hand):
        x = start_x + i * card_spacing
        if hide_dealer and i == 1:
            CARD_WIDTH = suit_images["Clubs"].get_width() // 13
            CARD_HEIGHT = suit_images["Clubs"].get_height()
            scaled_card_back = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT))
            screen.blit(scaled_card_back, (x, y_dealer))
        else:
            rank, suit, _ = card
            card_image = get_card_image(suit, rank)
            screen.blit(card_image, (x, y_dealer))

def draw_player_hand(hand, start_x, y, label=None):
    """
    Draw a single hand (list of cards) at the given x,y coordinates.
    Optionally, draw a label (e.g. "You" or "Computer Left") above the hand.
    """
    card_spacing = 70
    for i, card in enumerate(hand):
        rank, suit, _ = card
        card_image = get_card_image(suit, rank)
        screen.blit(card_image, (start_x + i * card_spacing, y))
    if label:
        font = pygame.font.Font(None, 28)
        text = font.render(label, True, (255, 255, 255))
        screen.blit(text, (start_x, y - 30))

def draw_all_players(user_hand, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=False):
    """
    Draw the table background, dealer's hand and all three player hands.
    The computer on the left is drawn at x = 300, the user at x = 535,
    and the computer on the right at x = 800 (all at y = 480).
    """
    screen.blit(table_image, (0, 0))
    draw_dealer_hand(dealer_hand, hide_dealer)
    y_players = 480
    draw_player_hand(comp_left_hand, 200, y_players, label="Computer Left")
    draw_player_hand(user_hand, 535, y_players, label="You")
    draw_player_hand(comp_right_hand, 900, y_players, label="Computer Right")

def draw_all_split_hands(user_hands, active_index, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=False):
    """
    When the user splits, draw the dealer's hand and the user's split hands.
    Then, also draw the computer players' hands.
    """
    # Use the existing split drawing function for the user hands.
    draw_split_hands(user_hands, active_index, dealer_hand, hide_dealer)
    # Draw the computer players.
    y_players = 480
    draw_player_hand(comp_left_hand, 100, y_players, label="Computer Left")
    draw_player_hand(comp_right_hand, 1000, y_players, label="Computer Right")

# ─── EXISTING SPLIT HAND DRAWING FUNCTION ───────────────
def draw_split_hands(player_hands, active_index, dealer_hand, hide_dealer=False):
    """
    When a player splits their hand, display the dealer's hand at the top and the
    player's split hands side-by-side.
    """
    screen.blit(table_image, (0, 0))
    # Draw dealer's hand.
    card_spacing = 80
    total_width = len(dealer_hand) * card_spacing
    start_x = (WIDTH - total_width) // 2
    y_dealer = 50
    for i, card in enumerate(dealer_hand):
        x = start_x + i * card_spacing
        if hide_dealer and i == 1:
            CARD_WIDTH = suit_images["Clubs"].get_width() // 13
            CARD_HEIGHT = suit_images["Clubs"].get_height()
            scaled_card_back = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT))
            screen.blit(scaled_card_back, (x, y_dealer))
        else:
            rank, suit, _ = card
            card_image = get_card_image(suit, rank)
            screen.blit(card_image, (x, y_dealer))
    
    # Draw user's split hands.
    y_player = 500              # Vertical position for split hands.
    start_x_player = 425        # Starting x-coordinate for the first hand.
    hand_gap = 250              # Gap between split hands.
    
    for i, hand in enumerate(player_hands):
        x_offset = start_x_player + i * hand_gap
        for j, card in enumerate(hand):
            rank, suit, _ = card
            card_image = get_card_image(suit, rank)
            x = x_offset + j * 80
            screen.blit(card_image, (x, y_player))
        # Draw label above each hand.
        font = pygame.font.Font(None, 28)
        label = font.render(f"Hand {i+1}", True, (255, 255, 255))
        screen.blit(label, (x_offset, y_player - 30))
        # Highlight the active hand.
        if i == active_index:
            if hand:
                card_image = get_card_image(hand[0][1], hand[0][0])
                card_width = card_image.get_width()
                card_height = card_image.get_height()
                rect = pygame.Rect(x_offset - 5, y_player - 5, len(hand) * 80, card_height + 10)
                pygame.draw.rect(screen, (255, 0, 0), rect, 2)

# ─── DRAW BUTTONS CENTERED ────────────────────────────────
def draw_buttons(split_available=False, split_mode=False):
    """
    Draw the action buttons (HIT, STAND, DOUBLE, and optionally SPLIT) at the bottom-center.
    """
    font = pygame.font.Font(None, 36)
    buttons = []
    if split_available and not split_mode:
        buttons.append("SPLIT")
    buttons.extend(["HIT", "STAND", "DOUBLE"])
    spacing = 20
    button_surfaces = {}
    total_width = 0
    for btn in buttons:
        surface = font.render(btn, True, (255, 255, 255))
        button_surfaces[btn] = surface
        total_width += surface.get_width()
    total_width += spacing * (len(buttons) - 1)
    
    start_x = (WIDTH - total_width) // 2
    y = (HEIGHT - font.get_height()) - 425
    button_rects = {}
    x = start_x
    for btn in buttons:
        surf = button_surfaces[btn]
        rect = surf.get_rect(topleft=(x, y))
        screen.blit(surf, (x, y))
        button_rects[btn] = rect
        x += surf.get_width() + spacing
    return button_rects

def draw_counts(count, true_count, funds):
    """
    Display the current running count, true count, and player's funds.
    """
    font = pygame.font.Font(None, 28)
    screen.blit(font.render(f"Running Count: {count}", True, (255, 255, 255)), (WIDTH - 200, 20))
    screen.blit(font.render(f"True Count: {true_count:.2f}", True, (255, 255, 255)), (WIDTH - 200, 50))
    screen.blit(font.render(f"Funds: ${funds}", True, (255, 255, 255)), (WIDTH - 200, 80))

def display_result(message):
    """
    Display a large result message in the center of the screen.
    """
    font = pygame.font.Font(None, 72)
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(1500)

def get_bet_input(funds, count, true_count):
    """
    Prompt the player to enter a bet.
    """
    font = pygame.font.Font(None, 48)
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    bet = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if bet.isdigit() and 20 <= int(bet) <= funds:
                            return int(bet)
                        else:
                            bet = ''
                    elif event.key == pygame.K_BACKSPACE:
                        bet = bet[:-1]
                    else:
                        if event.unicode.isdigit():
                            bet += event.unicode

        screen.fill((0, 100, 0))
        prompt_text = font.render(f"Enter your bet (Min $20, Max ${funds}):", True, (255, 255, 255))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 60))
        txt_surface = font.render(bet, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        count_font = pygame.font.Font(None, 36)
        running_count_text = count_font.render(f"Running Count: {count}", True, (255, 255, 255))
        true_count_text = count_font.render(f"True Count: {true_count:.2f}", True, (255, 255, 255))
        screen.blit(running_count_text, (WIDTH // 2 - running_count_text.get_width() // 2, HEIGHT // 2 + 70))
        screen.blit(true_count_text, (WIDTH // 2 - true_count_text.get_width() // 2, HEIGHT // 2 + 110))
        pygame.display.flip()

# ================ #
#  MAIN GAME LOOP  #
# ================ #

def play_blackjack():
    """
    Main function controlling the flow of the Blackjack game.
    Now includes three players: the human user (center), a computer player that plays before the user (right),
    and a computer player that plays after the user (left).
    """
    shoe = create_shoe()
    count = 0
    funds = 300
    running = True

    while running:
        bet = get_bet_input(funds, count, calculate_true_count(count, shoe))
        funds -= bet

        # --- Initial Deal ---
        # We now deal two cards each to: user, computer (right), computer (left) and dealer.
        user_hand = []
        comp_right_hand = []  # Computer player that plays BEFORE the user (displayed on the right)
        comp_left_hand = []   # Computer player that plays AFTER the user (displayed on the left)
        dealer_hand = []

        # Deal first round of cards:
        card, count = draw_card(shoe, count)
        user_hand.append(card)
        card, count = draw_card(shoe, count)
        comp_right_hand.append(card)
        card, count = draw_card(shoe, count)
        comp_left_hand.append(card)
        card, count = draw_card(shoe, count)
        dealer_hand.append(card)

        # Deal second round of cards:
        card, count = draw_card(shoe, count)
        user_hand.append(card)
        card, count = draw_card(shoe, count)
        comp_right_hand.append(card)
        card, count = draw_card(shoe, count)
        comp_left_hand.append(card)
        card, count = draw_card(shoe, count)
        dealer_hand.append(card)

        # (Optional extra update on dealer’s visible card as in original code)
        count = update_count(dealer_hand[0], count)
        true_count = calculate_true_count(count, shoe)

        # Check if user split is available.
        split_available = False
        if len(user_hand) == 2 and (user_hand[0][2] == user_hand[1][2]) and funds >= bet:
            split_available = True

        user_turn = True
        split_mode = False
        current_split_index = 0
        user_hands = []
        split_bets = []
        game_over = False

        # --- COMPUTER PLAYER (Right) TURN: plays before the user ---
        while calculate_hand_value(comp_right_hand) < 17:
            pygame.time.delay(1000)
            card, count = draw_card(shoe, count)
            comp_right_hand.append(card)
            draw_all_players(user_hand, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=True)
            draw_counts(count, calculate_true_count(count, shoe), funds)
            pygame.display.flip()
            if calculate_hand_value(comp_right_hand) > 21:
                break  # Computer busts

        # --- USER TURN (Interactive) ---
        while not game_over and user_turn:
            if not split_mode:
                draw_all_players(user_hand, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=True)
            else:
                draw_all_split_hands(user_hands, current_split_index, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=True)
            button_rects = draw_buttons(split_available, split_mode)
            draw_counts(count, calculate_true_count(count, shoe), funds)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if not split_mode:
                        if split_available and "SPLIT" in button_rects and button_rects["SPLIT"].collidepoint(pos):
                            if funds >= bet:
                                funds -= bet
                                split_mode = True
                                current_split_index = 0
                                hand1 = [user_hand[0]]
                                hand2 = [user_hand[1]]
                                card, count = draw_card(shoe, count)
                                hand1.append(card)
                                card, count = draw_card(shoe, count)
                                hand2.append(card)
                                user_hands = [hand1, hand2]
                                split_bets = [bet, bet]
                            else:
                                print("Not enough funds to split!")
                        elif "HIT" in button_rects and button_rects["HIT"].collidepoint(pos):
                            card, count = draw_card(shoe, count)
                            user_hand.append(card)
                            if calculate_hand_value(user_hand) > 21:
                                draw_all_players(user_hand, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=True)
                                pygame.display.flip()
                                pygame.time.delay(1000)
                                display_result("BUSTED!")
                                game_over = True
                                user_turn = False
                        elif "STAND" in button_rects and button_rects["STAND"].collidepoint(pos):
                            user_turn = False
                        elif "DOUBLE" in button_rects and button_rects["DOUBLE"].collidepoint(pos):
                            if funds >= bet:
                                funds -= bet
                                bet *= 2
                                card, count = draw_card(shoe, count)
                                user_hand.append(card)
                                draw_all_players(user_hand, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=True)
                                pygame.display.flip()
                                pygame.time.delay(1000)
                                if calculate_hand_value(user_hand) > 21:
                                    display_result("BUSTED!")
                                user_turn = False
                            else:
                                print("Not enough funds to double!")
                    else:
                        # In split mode the user plays each hand in turn.
                        if "HIT" in button_rects and button_rects["HIT"].collidepoint(pos):
                            card, count = draw_card(shoe, count)
                            user_hands[current_split_index].append(card)
                            if calculate_hand_value(user_hands[current_split_index]) > 21:
                                pygame.time.delay(500)
                                current_split_index += 1
                                if current_split_index >= len(user_hands):
                                    user_turn = False
                        elif "STAND" in button_rects and button_rects["STAND"].collidepoint(pos):
                            current_split_index += 1
                            if current_split_index >= len(user_hands):
                                user_turn = False
                        elif "DOUBLE" in button_rects and button_rects["DOUBLE"].collidepoint(pos):
                            if funds >= split_bets[current_split_index]:
                                funds -= split_bets[current_split_index]
                                split_bets[current_split_index] *= 2
                                card, count = draw_card(shoe, count)
                                user_hands[current_split_index].append(card)
                                pygame.time.delay(500)
                                current_split_index += 1
                                if current_split_index >= len(user_hands):
                                    user_turn = False
                            else:
                                print("Not enough funds to double on this hand!")
        # --- END OF USER TURN ---

        # --- COMPUTER PLAYER (Left) TURN: plays after the user ---
        if not game_over:
            while calculate_hand_value(comp_left_hand) < 17:
                pygame.time.delay(1000)
                card, count = draw_card(shoe, count)
                comp_left_hand.append(card)
                draw_all_players(user_hand, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=True)
                draw_counts(count, calculate_true_count(count, shoe), funds)
                pygame.display.flip()
                if calculate_hand_value(comp_left_hand) > 21:
                    break

        # --- DEALER TURN ---
        if not game_over:
            # Reveal dealer's hand.
            draw_all_players(user_hand, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=False)
            pygame.display.flip()
            pygame.time.delay(1000)
            while calculate_hand_value(dealer_hand) < 17:
                pygame.time.delay(1000)
                card, count = draw_card(shoe, count)
                dealer_hand.append(card)
                draw_all_players(user_hand, comp_left_hand, comp_right_hand, dealer_hand, hide_dealer=False)
                draw_counts(count, calculate_true_count(count, shoe), funds)
                draw_buttons()  # Inactive buttons.
                pygame.display.flip()
            dealer_value = calculate_hand_value(dealer_hand)

            # --- RESOLUTION ---
            results = {}
            # Resolve the user's outcome (if not split, one hand; otherwise, show each hand).
            if not split_mode:
                user_value = calculate_hand_value(user_hand)
                if user_value > 21:
                    results["You"] = "LOSE"
                elif dealer_value > 21 or user_value > dealer_value:
                    funds += bet * 2
                    results["You"] = "WIN"
                elif user_value == dealer_value:
                    funds += bet
                    results["You"] = "PUSH"
                else:
                    results["You"] = "LOSE"
            else:
                user_results = []
                for i, hand in enumerate(user_hands):
                    hand_value = calculate_hand_value(hand)
                    if hand_value > 21:
                        user_results.append("LOSE")
                    elif dealer_value > 21 or hand_value > dealer_value:
                        funds += split_bets[i] * 2
                        user_results.append("WIN")
                    elif hand_value == dealer_value:
                        funds += split_bets[i]
                        user_results.append("PUSH")
                    else:
                        user_results.append("LOSE")
                results["You"] = " / ".join([f"Hand {i+1}: {res}" for i, res in enumerate(user_results)])

            # Resolve computer player (right).
            comp_right_value = calculate_hand_value(comp_right_hand)
            if comp_right_value > 21:
                results["Computer Right"] = "LOSE"
            elif dealer_value > 21 or comp_right_value > dealer_value:
                results["Computer Right"] = "WIN"
            elif comp_right_value == dealer_value:
                results["Computer Right"] = "PUSH"
            else:
                results["Computer Right"] = "LOSE"

            # Resolve computer player (left).
            comp_left_value = calculate_hand_value(comp_left_hand)
            if comp_left_value > 21:
                results["Computer Left"] = "LOSE"
            elif dealer_value > 21 or comp_left_value > dealer_value:
                results["Computer Left"] = "WIN"
            elif comp_left_value == dealer_value:
                results["Computer Left"] = "PUSH"
            else:
                results["Computer Left"] = "LOSE"

            # Build a combined message in left-to-right order.
            message = f"You: {results['You']}"
            display_result(message)

        if funds < 20:
            print("You're out of funds! Game over.")
            running = False
        pygame.time.delay(1500)
    pygame.quit()

if __name__ == "__main__":
    play_blackjack()
