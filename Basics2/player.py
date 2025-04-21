from __future__ import annotations
from cards import Card, Rank, Suit


class Player:

	"""Superclass for the different players. Includes the constructor and checking for valid play functions."""
	
	def __init__(self, name: str) -> None:
		"""
		Constructs the following when Player is being called.
		Arguments:
			name => string for the player's name
		"""
		self.name = name
		self.hand = []
		self.round_score = 0
		self.total_score = 0

	def __str__(self) -> None:
		"""Returns the player's name when printed"""
		return self.name

	def __repr__(self) -> None:
		"""Returns __str__ as instructed"""
		return self.__str__()

	def check_valid_play(self, card: Card, trick: list[Card], broken_hearts: bool) -> tuple(bool, str):
		"""
		Checks for valid plays.
		Arguments:
			card => Card that is being played
			trick => a list of Card being played
			broken_hearts => True or False if hearts have been broken

		Returns True if the card is a valid play, False otherwise
		"""
		if trick:																							#if trick is not empty
			if card.suit != trick[0].suit:																	#if card played is of different suit than the first trick
				for card_in_hand in self.hand:																#checks if there is other card of the same suit on hand
					if card_in_hand.suit == trick[0].suit:
						return (False,"Player still has cards from the suit of the current trick")
				if trick[0] == Card(Rank.Two, Suit.Clubs):													#if at the start of the round
					if card.suit == Suit.Hearts or card == Card(Rank.Queen,Suit.Spades):
						return (False,"Player cannot play Hearts or the Queen of Spades on the first turn!")
		else:																								#if you are starting the trick
			if Card(Rank.Two,Suit.Clubs) in self.hand:														#if you have the Two of Clubs, you must play it
				if card != Card(Rank.Two,Suit.Clubs):
					return (False,"Player needs to play the Two of Clubs!")
			elif card.suit == Suit.Hearts:																	#you cant play hearts if not broken, unless you only have hearts
				if broken_hearts == False:
					for cards in self.hand:
						if cards.suit != Suit.Hearts:
							return (False,"Hearts is not broken yet!")
		return (True,None)
