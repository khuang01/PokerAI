from Poker import *

# P2 has higher pair
input1 = ['2D', '3H', '2C', 'JS', 'KS', '5D', 'KC']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['5C', '4C', '2C', 'JS', 'KS', '5D', 'KC']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

# Tied hands
input1 = ['3C', 'TS', 'KD', 'AD', 'AS', '8S', 'QH']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['TD', '7C', 'KD', 'AD', 'AS', '8S', 'QH']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) == evaluatePile(pile2))

input1 = ['4D', '3D', '6C', '5H', '6D', 'QD', '2D']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['8C', 'AS', '6C', '5H', '6D', 'QD', '2D']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) > evaluatePile(pile2))

input1 = ['JH', '2C', 'AD', '9C', '6C', 'QS', '3H']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['TH', '8C', 'AD', '9C', '6C', 'QS', '3H']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) > evaluatePile(pile2))

input1 = ['QD', 'QS','4S', 'KH', '5C', '3H', '9D']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['6C', '2C','4S', 'KH', '5C', '3H', '9D']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

input1 = ['4C', '9H', '6S', '8C', '8S', '2C', '2D']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['QC', '6H', '6S', '8C', '8S', '2C', '2D']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

input1 = ['KD', 'KS', 'QD', 'AS', '8H', '6C', '4D']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['AC', 'QC', 'QD', 'AS', '8H', '6C', '4D']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

input1 = ['AD', '6D', '2D', 'AS', 'KD', 'QD', '6C']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['6H', '7H', '2D', 'AS', 'KD', 'QD', '6C']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) > evaluatePile(pile2))

input1 = ['4S', 'TD', '4D', '9D', '2S', '3S', 'AS']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['5S', 'KD', '4D', '9D', '2S', '3S', 'AS']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

input1 = ['QD', '5H', '4D', '5C', 'AC', '7D', '7H']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['5S', 'JS', '4D', '5C', 'AC', '7D', '7H']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) == evaluatePile(pile2))

input1 = ['2C', '2S', 'AS', 'AC', '8C', '6D', 'QS']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['8S', '7C', 'AS', 'AC', '8C', '6D', 'QS']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

input1 = ['4S', '6S', 'QC', '7D', 'QS', '4C', 'KS']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['9D', '7C', 'QC', '7D', 'QS', '4C', 'KS']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

input1 = ['8H', 'QD', '8C', '8D', '6S', 'KC', '4D']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['KH', 'AC', '8C', '8D', '6S', 'KC', '4D']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) > evaluatePile(pile2))

input1 = ['5S', 'JH', 'KS', '6C', 'JC', '4C', '7D']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['7H', 'AH', 'KS', '6C', 'JC', '4C', '7D']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) > evaluatePile(pile2))

input1 = ['8D', 'AC', 'TD', '2C', '2H', 'QS', '7H']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['KH', 'QD', 'TD', '2C', '2H', 'QS', '7H']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

input1 = ['9C', '9H', '2S', '8D', '4C', '5H', 'AH']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['QS', 'AD', '2S', '8D', '4C', '5H', 'AH']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

input1 = ['8D', 'AD', '6C', 'KH', '3C', '6D', '5C']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['KD', '7D', '6C', 'KH', '3C', '6D', '5C']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))

input1 = ['8H', '8D', '7H', 'QC', '3H', '3C', 'TH']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['7S', '8C', '7H', 'QC', '3H', '3C', 'TH']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) > evaluatePile(pile2))

input1 = ['3S', '8D', 'JC', '9S', 'AS', '8H', '2S']
pile1 = cardsToID(GUIToCards(input1))
input2 = ['TH', 'AD', 'JC', '9S', 'AS', '8H', '2S']
pile2 = cardsToID(GUIToCards(input2))
assert (evaluatePile(pile1) < evaluatePile(pile2))