import random


def blackjack(cards: list):
    '''
    Check for blackjack occurence
    '''
    if len(cards) == 2:
        # black jack
        if 1 in cards and \
                sum([1 if i in cards else 0 for i in range(10, 14)]) != 0:
            return True
    return False


def end_game_check(p, d):
    '''
    Check for end game condition
    1: win
    2: lose
    3: draw
    '''d
    if blackjack(p.show_cards()) == True:
        return 1
    if blackjack(d.show_cards()) == True:
        return 2
    p_total = p.check()
    d_total = d.check()
    if 16 <= p_total <= 21:
        if len(p.show_cards()) == 5 or p_total > d_total or d_total > 21:
            return 1
        if p_total == d_total:
            return 3
        if (p_total < d_total and d_total <= 21) or \
                (len(d.show_cards()) == 5 and 16 <= d_total <= 21):
            return 2
    if (p_total > 21 and d_total > 21) or \
        (p_total > 21 and d_total < 16) or \
            (p_total < 16 and d_total > 21):
        return 3
    return 2


def check_input(options: list):
    '''
    Check user input and continue asking if the input is invalid
    '''
    user_input = input()
    while sum([1 if user_input == i else 0 for i in options]) == 0:
        print("Invalid input. Try again: ", end='')
        user_input = input()
    return user_input


class Deck:
    '''
    Standard 52-card deck
    '''

    def __init__(self):
        self.cards = {i: 4 for i in range(1, 14)}

    def get(self):
        card = random.randint(1, 13)
        while self.cards.get(card) == 0:
            card = random.randint(1, 13)
        self.cards[card] -= 1
        return card

    def reset(self):
        self.cards = {i: 4 for i in range(1, 14)}


class Player:
    '''
    Player
    Basic behavior:
    - Hit
    - Bet
    - Check cards
    - Check balance
    - Return holding cards
    '''

    def __init__(self, money):
        self.__money = money
        self.__cards_holding = []
        self.__total = 0

    def __total_cal(self):
        '''
        Calculate cards value
        Ace can be 1 or 11
        '''
        total = 0
        for i in self.__cards_holding:
            if i == 1:
                total += 11
            else:
                total += i
            if total > 21 and i == 1:
                total -= 10
        self.__total = total

    def hit(self, d):
        '''
        Get cards from deck and keep
        '''
        card = d.get()
        self.__cards_holding.append(card)
        return card

    def bet(self, money):
        '''
        Choose amount of money for betting
        '''
        if money <= self.__money:
            return True
        return False

    def check(self):
        '''
        Check current cards' total value
        '''
        self.__total_cal()
        return self.__total

    def won(self, money):
        self.__money += money

    def lost(self, money):
        self.__money -= money

    def show_balance(self):
        return self.__money

    def return_card(self):
        self.__cards_holding = []

    def show_cards(self):
        return self.__cards_holding


class Dealer(Player):
    '''
    Automatic dealer
    '''

    def __init__(self):
        Player.__init__(self, 0)

    def bet(self):
        return True

    def won(self, money):
        pass

    def lost(self, money):
        pass

    def show_balance(self):
        pass

    def autorun(self, d):
        '''
        Automatically hit and check total
        '''
        total = 0
        while True:
            card = self.hit(d)
            if blackjack(self.show_cards()) == True:
                break
            # Consider ace is 11
            if card == 1:
                total += 11
            else:
                total += card
            # Reconsider ace
            if total > 21 and card == 1:
                total -= 10
            if total > 21 or total >= 16:
                break
        # Hit or stand randomly while in safe values' range
        if total <= 20 and random.randint(0, 1) == 1:
            self.hit(d)


if __name__ == "__main__":
    print("How much you want to play:")
    money = input()
    while not money.isnumeric() or int(money) <= 0:
        print("Invalid amount of money. Try again: ", end='')
        money = input()
    player = Player(int(money))
    dealer = Dealer()
    deck = Deck()
    cont_game = True
    winner = None
    while cont_game == True:
        # 1 win 2 lose 3 draw
        end_game = 0
        valid_bet = False
        while valid_bet == False:
            print("Bet?: ", end='')
            bet = input()
            while not bet.isnumeric() or int(bet) <= 0:
                print("Invalid input. Try again: ", end='')
                bet = input()
            bet = int(bet)
            if player.bet(bet) == True:
                valid_bet = True
            else:
                print("Not enough money. Continue? (y/n): ", end='')
                user_input = check_input(['y', 'n'])
                if user_input == 'n':
                    exit()
        while end_game == 0:
            print("Hit or Stand (h/s): ", end='')
            user_input = check_input(['h', 's'])
            if user_input == 'h':
                player.hit(deck)
                print(player.show_cards())
            else:
                dealer.autorun(deck)
                end_game = end_game_check(player, dealer)
                if end_game == 1:
                    player.won(bet)
                    print("You won. Current balance: {}".format(
                        player.show_balance()))
                elif end_game == 3:
                    print("Draw. Current balance: {}".format(
                        player.show_balance()))
                elif end_game == 2:
                    player.lost(bet)
                    print("You lost. Current balance: {}".format(
                        player.show_balance()))
                print("Your cards: {}".format(player.show_cards()))
                print("Dealer cards: {}".format(dealer.show_cards()))
        if player.show_balance() <= 0:
            print("Your out of money. Game over!")
            exit()
        print("Continue?(y/n):", end='')
        user_input = check_input(['y', 'n'])
        if user_input == 'n':
            cont_game = False
        else:
            player.return_card()
            dealer.return_card()
            deck.reset()
