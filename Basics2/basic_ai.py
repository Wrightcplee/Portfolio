from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player
import time

class BasicAIPlayer(Player):

	"""Creates a Basic AI player, and determines how they play the game"""
	
	def play_card(self, trick: list[Card], broken_hearts: bool)-> Card:
		"""
		Defines Basic AI card logic for playing cards.
		Arguments:
			trick => a list of Card being played by others
			broken_hearts => True or False if hearts has been broken
		
		Returns the weakest legally playable Card
		"""
		
		valid_cards = []
		for card in self.hand:												#checks for all playable cards
			if super().check_valid_play(card,trick,broken_hearts)[0]:
				valid_cards.append(card)
		weakest = min(valid_cards)											#choose the lowest rank and suit cards among the playable cards
		self.hand.remove(weakest)
		time.sleep(2)
		return weakest

	def pass_cards(self) -> list[Card]:
		"""
		Defines Basic AI logic for passing cards.
		Returns a list of three weakest Card to pass
		"""
		self.hand.sort()
		cards_passed = self.hand[-3:]										#passes the three strongest cards (due to sort)
		for card in cards_passed:
			self.hand.remove(card)
		return cards_passed

