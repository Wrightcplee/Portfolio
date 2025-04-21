from __future__ import annotations
from cards import Card, Rank, Suit
#3 locked

class Round:																		#check round.py for docstring and notes

	def __init__(self, players: list[Player]) -> None:
		broken_hearts = False
		n = 0
		for player in players:
			if Card(Rank.Two,Suit.Clubs) in player.hand:
				break
			n += 1
		while players[0].hand:
			trick = []
			for _ in range(len(players)):
				card_played = players[n%len(players)].play_card(trick,broken_hearts)
				print(f"{players[n%len(players)]} plays {card_played}")
				trick.append(card_played)
				if card_played.suit == Suit.Hearts and broken_hearts == False:
					broken_hearts = True
					print("Hearts have been broken!")
				n += 1
			strongest = trick[0]
			penalty = 0
			for i in range(len(trick)):
				if trick[i].suit == Suit.Hearts:
					penalty += 1
				elif trick[i] == Card(Rank.Queen,Suit.Spades):
					penalty += 13
				if trick[i].suit == trick[0].suit:
					if trick[i].rank > strongest.rank:
						strongest = trick[i]
			taker = players[(n+trick.index(strongest))%len(players)]
			n += trick.index(strongest)
			taker.round_score += penalty
			print (f"{taker} takes the trick. Points received: {penalty}")

