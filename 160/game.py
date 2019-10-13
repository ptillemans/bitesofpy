import csv
import os
from urllib.request import urlretrieve

BATTLE_DATA = os.path.join('/tmp', 'battle-table.csv')
if not os.path.isfile(BATTLE_DATA):
	urlretrieve('https://bit.ly/2U3oHft', BATTLE_DATA)


def _defeats(result):
	return [k for k,v in result.items() if v == 'win']


def _create_defeat_mapping():
	"""Parse battle-table.csv building up a defeat_mapping dict
	   with keys = attackers / values = who they defeat.
	"""
	with open(BATTLE_DATA) as f:
		results = list(csv.DictReader(f))
	return {r['Attacker']: _defeats(r) for r in results}


def get_winner(player1, player2, defeat_mapping=None):
	"""Given player1 and player2 determine game output returning the
	   appropriate string:
	   Tie
	   Player1
	   Player2
	   (where Player1 and Player2 are the names passed in)

	   Raise a ValueError if invalid player strings are passed in.
	"""
	defeat_mapping = defeat_mapping or _create_defeat_mapping()
	valid_plays = defeat_mapping.keys()

	if player1 not in valid_plays:
		raise ValueError(f'Player1 played invalid move {player1}')
	if player2 not in valid_plays:
		raise ValueError(f'Player2 played invalid move {player2}')

	if player1 == player2:
		return 'Tie'
	if player2 in defeat_mapping[player1]:
		return player1
	else:
		return player2
