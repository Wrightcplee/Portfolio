from __future__ import annotations
from cards import Card, Rank, Suit


class Round:

	"""Starts a round of Hearts when called."""

	def __init__(self, players: list[Player]) -> None:
		"""One round of Hearts"""
		broken_hearts = False
		n = 0																			#counter for whose turn to play
		for player in players:
			if Card(Rank.Two,Suit.Clubs) in player.hand:								#checks for who starts the game
				break
			n += 1
		while players[0].hand:															#while there are cards in a player's hand
			trick = []
			for _ in range(len(players)):												#one turn of playing cards
				card_played = players[n%len(players)].play_card(trick,broken_hearts)
				if trick:
					print(f"{players[n%len(players)]} plays {card_played}")
				else:
					print(f"{players[n%len(players)]} leads with {card_played}")
				trick.append(card_played)
				if card_played.suit == Suit.Hearts and broken_hearts == False:			#logic for breaking hearts
					broken_hearts = True
					print("Hearts have been broken!")
				n += 1
			strongest = trick[0]														#strongest card of the trick
			penalty = 0																	#penalty points
			for i in range(len(trick)):
				if trick[i].suit == Suit.Hearts:										#tabulating penalty points in the trick
					penalty += 1
				elif trick[i] == Card(Rank.Queen,Suit.Spades):
					penalty += 13
				if trick[i].suit == trick[0].suit:										#checks for strongest card
					if trick[i].rank > strongest.rank:
						strongest = trick[i]
			taker = players[(n+trick.index(strongest))%len(players)]
			n += trick.index(strongest)													#the taker starts the next round
			taker.round_score += penalty												#increase the round score for the taker
			print (f"{taker} takes the trick. Points received: {penalty}")

