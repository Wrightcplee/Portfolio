from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player


class Human(Player):

	"""Creates a Human player, and accepts inputs on how they play the game"""
		
	def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
		"""
		By printing out the current hand, lets the player decide which card they want to play.
		Arguments:
			trick => a list of Card being played by others
			broken_hearts => True or False if hearts have been broken
		
		Returns the chosen card that the player decides to play
		"""
		self.hand.sort()
		print(f"Your current hand: {Card.hand_view(self.hand)}")
		while True:																						#could use try/except, but i finished this part before that lesson
			chosen = self.hand[int_input("Select a card to play: ",list(range(len(self.hand))))]		#prompts input for card to play, restricted to the number of cards on hand
			if super().check_valid_play(chosen,trick,broken_hearts)[0]:									#checks for valid play
				break
			else:
				print(super().check_valid_play(chosen,trick,broken_hearts)[1])							#prints error message for invalid play
		self.hand.remove(chosen)
		return chosen

	def pass_cards(self) -> list[Card]:
		"""
		By printing out the current hand, lets the player decide which card they want to pass.
		Returns a list of three chosen Card to pass
		"""
		self.hand.sort()
		print(f"Your current hand: {Card.hand_view(self.hand)}")
		chosen = []
		chose = (input("Select three cards to pass off (e.g. '0, 4, 5'): ")).split(",")				#converts input string into a list
		while True:																					#loops until a valid player input
			try:
				assert len(chose) == 3, "Choose three cards!"
				for i in range(len(chose)):															#checks for every input
					assert chose[i].isdigit() and int(chose[i]) <= (len(self.hand)-1) and int(chose[i]) >= 0, f"Enter only numbers between 0-{len(self.hand)-1}!"
					assert chose[i] != chose[(i+1)%3] and chose[i] != chose[(i+2)%3], "No duplicate numbers!"
				break
			except Exception as error:
				print(error)
				chose = (input("Select three cards to pass off (e.g. '0, 4, 5'): ")).split(",")
		for choice in chose:
			chosen.append(self.hand[int(choice)])
		for card in chosen:
			self.hand.remove(card)
		return chosen


def int_input(prompt="", restricted_to=None):
    """
    Helper function that modifies the regular input method,
    and keeps asking for input until a valid one is entered. Input 
    can also be restricted to a set of integers.

    Arguments:
        - prompt: String representing the message to display for input
        - restricted: List of integers for when the input must be restricted
                    to a certain set of numbers

    Returns the input in integer type.
    """
    while True:
        player_input = input(prompt)
        try:                           
            int_player_input = int(player_input)
        except ValueError:
            continue
        if restricted_to is None:
            break
        elif int_player_input in restricted_to:
            break

    return int_player_input
