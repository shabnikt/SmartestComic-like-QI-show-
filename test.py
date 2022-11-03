score_dict = {"player1": 0, "player2": 0, "player3": 2, "player4": 0}

# l = sorted(list(score_dict.values()))
s = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
list(s.keys()).index('player1')


for item in score_dict:
    print(item)
print()