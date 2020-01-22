def ranking():
    num_players = int(input("Enter number of players on leader board: "))
    leaderboard_scores = [int(x) for x in input("Enter scores on leader board: ").split()]
    alice_games = int(input("How many games will ALice play? "))
    alice_scores = [int(x) for x in input("Enter number of players on leader board: ").split()]
    print(alice_scores)
    print(leaderboard_scores)
    distinct_scores = sorted(set(leaderboard_scores), reverse=1)
    print(distinct_scores)
    for score in alice_scores:
        rank = 1
        for pos in distinct_scores:
            if score < pos:
                rank += 1
        print(rank)


ranking()