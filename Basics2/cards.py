from __future__ import annotations # for type hints of a class in itself
from enum import Enum


class Rank(Enum):

	"""Assign a value to the Rank of the cards"""

	Two = 2
	Three = 3
	Four = 4
	Five = 5
	Six = 6
	Seven = 7
	Eight = 8
	Nine = 9
	Ten = 10
	Jack = 11
	Queen = 12
	King = 13
	Ace = 14

	def __lt__(self, other: Rank) -> bool:
		"""
		Allows the Rank to be compared by its value
		Arguments:
			other -> Rank that is being compared with

		Returns True if rank of self is smaller that rank of other. False otherwise.
		"""
		return self.value < other.value


class Suit(Enum):

	"""Assigns a value to the Suit of the cards"""
	
	Clubs = 1
	Diamonds = 2
	Spades = 3
	Hearts = 4

	def __lt__(self, other: Suit) -> bool:
		"""
		Allows the Suit to be compared by its value
		Arguments:
			other -> Suit that is being compared with

		Returns True if suit of self is smaller that suit of other. False otherwise.
		"""
		return self.value < other.value


class Card:

	"""Card creation with its 2 variable, Rank and Suit"""

	card_art_print = True											#for the different card art required in Hearts and task4

	def __init__(self, rank: Rank, suit: Suit) -> None:
		"""Instance variable of a Card which is made up of Rank and Suit"""

		self.rank = rank
		self.suit = suit


	def card_art(self) -> str:
		"""
		Converts Card form to a card design.
		Returns the string for the card's art
		"""
		suit = ["♣","♦","♠","♥"]
		number = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
		x = suit[self.suit.value-1]
		y = number[self.rank.value-2]
		card_art = [
		f"┌─────┐",							# for all cards other than Rank Ten
		f"│{y}    │",
		f"│  {x}  │",
		f"│    {y}│",
		f"└─────┘",
		f"┌─────┐",							# for the Rank Ten as 10 has 2 digits
		f"│{y}   │",
		f"│  {x}  │",
		f"│   {y}│",
		f"└─────┘"
		]
		card = "\n"
		for i in range(5):
			if self.rank.value == 10:
				card += f"{card_art[i+5]}\n"
			else:
				card += f"{card_art[i]}\n"
		return card

	def hand_view(handsel: list[Card]) -> str:
		"""
		Converts multiple cards in a list to a horizontal view, as well as numbering of the cards
		Arguments:
			handsel => a list of Card of the player's hand
		
		Returns a string of card_art for horizontal view
		"""
		hand = ""
		for row in range(5):
			hand += "\n"
			for i in handsel:
				hand += i.__str__()[(row*8)+1:8*(row+1)]			
		selection = ""
		for i in range(len(handsel)):
			if i >= 10 and i%2 == 1:					# needs to reduce spacing for numbering above 10
				selection += f"  {i}  "
			else:
				selection += f"   {i}   "
		return f"{hand}\n{selection}"

	def __repr__(self) -> str:
		"""Returns __str__ as instructed"""

		return self.__str__()

	def __str__(self) -> str:
		"""
		How the card will look like when printed.
		Returns a string on how the card looks like when print is called
		"""

		if self.card_art_print == True: 							#for normal gameplay
			return self.card_art()
		else:														#for task4
			return f"{self.rank.name} of {self.suit.name}"

	def __eq__(self, other: Card) -> bool:
		"""
		Allow the cards to be compared by its Rank and Suit, checks whether or not they are equal.
		Arguments:
			other -> Card that is being compared with

		Returns True if both suit and rank are the same. False otherwise.
		"""

		return self.suit == other.suit and self.rank == other.rank

	def __lt__(self, other: Card) -> bool:
		"""
		Allow the cards to be compared by its Rank and Suit
		Arguments:
			other -> Card that is being compared with

		Returns True if the other Card has a stronger Suit, or of equal Suit but higher Rank. False otherwise.
		"""

		if self.suit < other.suit:
			return True
		elif self.suit == other.suit:
			return self.rank < other.rank
		else:
			return False

