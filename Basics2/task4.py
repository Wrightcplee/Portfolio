from __future__ import annotations
import random
from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer
from task3 import Round


class Hearts:																				#check hearts.py for docstring and notes

	def __init__(self) -> None:
		players = []
		rounds = 1
		Card.card_art_print = False
		self.target_score = int(input("Please enter a target score to end the game: "))
		self.number_of_players = int(input("Please enter the number of players (3-5): "))
		for i in range(self.number_of_players):
			players.append(BasicAIPlayer(f"bot {i+1}"))
		while self.endgame(players):
			print (f"========= Starting round {rounds} =========")
			self.shuffle_deck(players)
			while self.check_invalid_hand(players):
				self.shuffle_deck(players)
			for player in players:
				player.hand.sort()
				print (f"{player.name} was dealt {player.hand}")
			pass_cards = []
			for i in range(len(players)):
				cards_to_pass = players[i].pass_cards()
				pass_cards.append(cards_to_pass)
			for i in range(len(players)):
				players[i].hand += pass_cards[(i-rounds)%len(players)]
				print(f"{players[i].name} passed {pass_cards[(i)%len(players)]} to {players[(i+rounds)%len(players)].name}")
			Round(players)
			for i in range(len(players)):
				if players[i].round_score == 26:
					for player in players:
						player.round_score = 26
					players[i].round_score = 0
					print(f"{players[i]} has shot the moon! Everyone else receives 26 points")
					break
			print (f"========= End of round {rounds} =========")
			for player in players:
				player.total_score += player.round_score
				player.round_score = 0
				print(f"{player}'s total score: {player.total_score}")
			rounds += 1
		winner = players[0]
		for player in players:
			if player.total_score < winner.total_score:
				winner = player
		print (f"{winner} is the winner!")

	def endgame(self,players):
		for player in players:
			if player.total_score >= self.target_score:
				return False
		return True

	def shuffle_deck(self,players):
		deck = []
		for suit in Suit:
			for rank in Rank:
				deck.append(Card(rank,suit))
		if self.number_of_players in (3,5):
			deck.remove(Card(Rank.Two,Suit.Diamonds))
			if self.number_of_players == 5:
				deck.remove(Card(Rank.Two,Suit.Spades))
		for player in players:
			for _ in range(52//len(players)):
				card = random.choice(deck)
				player.hand.append(card)
				deck.remove(card)
	
	def check_invalid_hand(self,players):
		for i in range(len(players)):
			invalid = []
			for card in players[i].hand:
				if card.suit != Suit.Hearts and card != Card(Rank.Queen, Suit.Spades):
					invalid.append(False)
				else:
					invalid.append(True)
			if all(invalid):
				return True
		return False


if __name__ == "__main__":
	Hearts()
