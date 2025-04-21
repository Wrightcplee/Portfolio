from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player
from basic_ai import BasicAIPlayer
import time

class BetterAIPlayer(BasicAIPlayer):

	"""Creates a Better AI Player, and determines how they play the game"""
 
	def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
		"""
		Defines BetterAIPlayer's play card logic
		Arguments:
			trick => a list of Card being played by others
			broken_hearts => True or False if hearts has been broken
		
		Returns a strategically chosen Card
		"""
		valid_cards = []
		for card in self.hand:
			if self.check_valid_play(card,trick,broken_hearts)[0]:
				valid_cards.append(card)
		valid_cards.sort(reverse=True)
		if trick:																								#if there is a trick
			if self.suit_in_list(trick[0].suit,valid_cards):														#if have suit of trick
				if Card(Rank.Queen,Suit.Spades) in valid_cards:															#if have QS
					if Card(Rank.King,Suit.Spades) in trick or Card(Rank.Ace,Suit.Spades) in trick:							#if there is AS and KS in trick (meaning i wont win)
						card_played = Card(Rank.Queen,Suit.Spades)																#play QS
					else:																									#if no AS or KS
						if len(valid_cards) > 1:																				#if i have more than 2 valid cards to play
							valid_cards.remove(Card(Rank.Queen,Suit.Spades))														#except QS, play the strongest
							card_played = self.strongest(trick[0].suit,valid_cards)
						else:																									#else, play QS
							card_played = valid_cards[0]
				elif trick[0] == Card(Rank.Two, Suit.Clubs):															#if first trick
					card_played = self.strongest(Suit.Clubs,valid_cards)													#throw largest card
				elif not self.suit_in_list(Suit.Hearts,trick) or Card(Rank.Queen,Suit.Spades) not in trick:				#if hearts and QS not played
					if len(trick) == 3:																						#if last to play (4player)
						card_played = self.strongest(trick[0].suit,valid_cards)													#play your strongest card
					else:																									#if not last
						card_played = self.strongest_losing_card(self.strongest(trick[0].suit,trick),valid_cards)				#play strongest that cannot win
				else:																									#if no risk
					if len(trick) == 3:																						#if last to play, throw biggest card (4 player)
						card_played = self.strongest(trick[0].suit,valid_cards)
					elif self.weakest(valid_cards) < self.strongest(trick[0].suit,trick):									#if not, throw strongest losing
						card_played = self.strongest_losing_card(self.strongest(trick[0].suit,trick),valid_cards) 
					else:																									#else play weakest card possible
						card_played = self.weakest(valid_cards)
			else:																									#if dont have suit of the trick
				if Card(Rank.Queen,Suit.Spades) in valid_cards:															#play QS if you have it
					card_played = Card(Rank.Queen,Suit.Spades)
				elif Card(Rank.King,Suit.Spades) in valid_cards or Card(Rank.Ace,Suit.Spades) in valid_cards:			#throw AS or KS 
					card_played = self.strongest(Suit.Spades,valid_cards)
				else: 																									#throw your hearts, or strongest ranked card
					card_played = self.strongest(Suit.Hearts,valid_cards)
		else:																										#if you start the trick
			if self.strongest(Suit.Spades,valid_cards) < Card(Rank.Queen,Suit.Spades):									#play spades when leading to force out QS as early as possible if you don't have QS and above
				card_played = self.strongest(Suit.Spades,valid_cards)
			else:																										#play weakest card to stay safe
				card_played = self.weakest(valid_cards)
		self.hand.remove(card_played)
		time.sleep(2)
		return card_played

	def pass_cards(self) -> list[Card]:
		"""
		Defines BetterAIPlayer card passing logic. It determines which card to pass based on a weightage system.
		Returns a list of three strategically chosen Card to pass
		"""
		suits_list = [Suit.Clubs,Suit.Diamonds,Suit.Spades,Suit.Hearts]			#for easy reference
		cards_to_pass = []														#any chosen card is appended here
		while len(cards_to_pass) != 3:											#as cards are chosen one by one, there is no fear in infinite loops
			suit_count = [0,0,0,0]												#number of cards on hand based on suits in the same order as suits_list
			rank_score = [0,0,0,0]												#the stronger in rank, the higher the points
			average = []														#average score based on rank_score divide by suit_count
			for i in range(4):
				for card in self.hand:
					if card.suit == suits_list[i]:
						suit_count[i] += 1										#adding the count in suit_count
						if card.suit == Suit.Spades:
							if card.rank > Rank.Jack:
								rank_score[i] += 3								#you want to throw away anything above QS
						elif card.rank > Rank.Queen:							#if the card is an Ace or King
							rank_score[i] += 3
						elif card.rank > Rank.Ten:								#if the card is a Queen or Jack
							rank_score[i] += 2
			for i in range(4):
				if suit_count[i] != 0:											#to prevent ZeroDivisionError
					average.append(rank_score[i]/suit_count[i])
				else:
					average.append(0)
			strongest_suit = suits_list[average.index(max(average))]			#determines strongest suit based on average
			if self.only_valid_card():							#this is here only to prevent all cards from being hearts or QS after passing
				chosen_card = self.strongest(Suit.Hearts,self.hand)
			else:												#give away the strongest card of the strongest suit
				chosen_card = self.strongest(strongest_suit,self.hand)
			cards_to_pass.append(chosen_card)
			self.hand.remove(chosen_card)
		return cards_to_pass

	def strongest(self, suit: Suit, lst: list[Card]) -> Card:
		"""
		Searches for strongest card based on the trump suit stated.
		Arguments:
			suit => Suit of the trump suit, or any Suit of your choice
			lst => a list of Card to choose the output card from. Usually from self.hand or trick
		
		Returns the strongest card in lst based on the suit
		"""
		strongest = lst[0]
		for card in lst:
			if card.suit == suit:
				if strongest.suit != suit:
					strongest = card
				elif card.rank > strongest.rank:		#if both cards are trick suit
					strongest = card
			elif strongest.suit != suit:			  #if both card and strongest are not mentioned suit...
				if card.rank > strongest.rank:
					strongest = card
		return strongest

	def weakest(self, lst: list[Card]) -> Card:
		"""
		Searches for the weakest rank card regardless of suit.
		Arguments:
			lst => a list of Card to choose the output card from. Mainly from self.hand
		
		Returns the weakest ranked card
		"""
		weakest = lst[0]
		for card in lst:
			if card.rank < weakest.rank:
				weakest = card
		return weakest
	
	def strongest_losing_card(self, trick_strongest: Card, lst: list[Card]) -> Card:
		"""
		Searches for the strongest possible card that doesn't win the current trick.
		Arguments:
			trick_strongest => strongest card in the trick
			lst => a list of Card to choose the output card from. Usually from self.hand
		
		Returns the strongest card that doesn't take the trick
		"""
		strongest_losing_card = self.weakest(lst)
		for card in lst:
			if card.rank > strongest_losing_card.rank and trick_strongest.rank > card.rank:
				strongest_losing_card = card
		return strongest_losing_card

	def suit_in_list(self, checking_suit: Suit, lst: list[Card]) -> bool:
		"""
		Checks if a particular suit is in the list
		Arguments:
			checking_suit => Suit of choice to check if there is a Card of such Suit
			lst => a list of Card to check through. Usually from self.hand or trick

		Returns True if the checking_suit is in the lst. False otherwise
		"""
		for card in lst:
			if card.suit == checking_suit:
				return True
		return False

	def only_valid_card(self) -> bool:
		"""
		Checks if there is only one card playable at the start of the turn. 
		This is due to the way BetterAIPlayer selects which cards to pass.

		Returns True if there is only one card left that is not Hearts or QS. False otherwise
		"""
		valid = []																# QS and hearts are invalid
		for card in self.hand:
			if card.suit == Suit.Hearts or card == Card(Rank.Queen,Suit.Spades):
				valid.append(False)
			else:
				valid.append(True)
		return valid.count(True) == 1
