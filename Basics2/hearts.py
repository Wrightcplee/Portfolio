from __future__ import annotations
import random
from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer
from better_ai import BetterAIPlayer
from round import Round
from human import Human, int_input

class Hearts:

	"""Plays a game of Hearts when called"""

	def __init__(self) -> None:
		"""The game of Hearts"""
		players = []																					#a list of players
		rounds = 1																						#number of rounds
		self.target_score = 0
		while self.target_score <= 0:
			self.target_score = int_input("Please enter a target score to end the game: ")				#prompts input for target score, restricted to positive numbers only
		self.number_of_players = int_input("Please enter the number of players (3-5): ",[3,4,5])		#prompts input for number of players, restricted to 3,4,5 players only
		players.append(Human(input("Please enter your name: ")))										#creates a Human player
		for i in range(self.number_of_players-2):														#creates other basic ai players
			players.append(BasicAIPlayer(f"noob {i+1}"))
		players.append(BetterAIPlayer("Genius"))														#creates one better ai player
		while self.endgame(players):																	#while players have not reached the target score...
			print (f"========= Starting round {rounds} =========")
			self.shuffle_deck(players)																	#shuffles deck and hands out the cards
			while self.check_invalid_hand(players):														#reshuffles the deck again if invalid hand
				self.shuffle_deck(players)
			pass_cards = []
			if (rounds % len(players)) != 0:																	#passing cards logic
				for i in range(len(players)):
					cards_to_pass = players[i].pass_cards()
					pass_cards.append(cards_to_pass)
				for i in range(len(players)):
					players[i].hand += pass_cards[(i-rounds)%len(players)]
				print("Cards have been passed")
			else:																						#doesn't have to pass for such rounds
				print("No cards will be passed this round!")
			Round(players)
			for i in range(len(players)):																#shoot the moon logic
				if players[i].round_score == 26:
					for player in players:
						player.round_score = 26
					players[i].round_score = 0
					print(f"{players[i]} has shot the moon! Everyone else receives 26 points")
					break
			print (f"========= End of round {rounds} =========")
			for player in players:																		#tally up the score to total score from the current round
				player.total_score += player.round_score
				player.round_score = 0
				print(f"{player}'s total score: {player.total_score}")
			rounds += 1
		winner = players[0]
		for player in players:																			#if someone reaches the target score, checks for the winner
			if player.total_score < winner.total_score:
				winner = player
		print (f"{winner} is the winner!")

	def endgame(self, players: list[Player]) -> bool:
		"""
		Checks if any player's score hits the target score.
		Arguments:
			players => a list of players of the game

		Returns True if a player's score is larger or equal to the target score
		"""
		for player in players:
			if player.total_score >= self.target_score:
				return False
		return True

	def shuffle_deck(self, players: list[Player]) -> None:
		"""
		Shuffles the deck and hands out the card to players
		Arguments:
			players => a list of players of the game
		"""
		deck = []
		for suit in Suit:
			for rank in Rank:
				deck.append(Card(rank,suit))					#creates the deck by creating every combination of Suit and Rank
		if self.number_of_players in (3,5):						#removes card for 3 or 5 players
			deck.remove(Card(Rank.Two,Suit.Diamonds))
			if self.number_of_players == 5:
				deck.remove(Card(Rank.Two,Suit.Spades))
		for player in players:									#choose a random card and hands them out to players
			for _ in range(52//len(players)):
				card = random.choice(deck)
				player.hand.append(card)
				deck.remove(card)
	
	def check_invalid_hand(self, players: list[Player]) -> bool:
		"""
		Checks if there is an invalid hand for all players.
		Arguments:
			players => a list of players of the game
		
		Returns True if there is a player with no card that is not of suit hearts or QS. False otherwise.
		"""
		for i in range(len(players)):
			invalid = []															#invalid card if QS or hearts
			for card in players[i].hand:
				if card.suit != Suit.Hearts and card != Card(Rank.Queen, Suit.Spades):
					invalid.append(False)
				else:
					invalid.append(True)
			if all(invalid):														#if all are True
				return True
		return False

if __name__ == "__main__":
	Hearts()
