import json
import csv

f = open('config.json')

config = json.load(f)
players = {}
max_base = 6
k_factor = 30

def find_bucket_by_rating(loser_score: int):
    for b in config['Buckets']:
        if loser_score >= b['LowScorePoint'] and loser_score <= b['HighScorePoint']:
            return b['Points']
    raise Exception(f'No ratings found for {loser_score}')

def find_bucket_by_diff(p1_rating, p2_rating):
    diff = abs(p1_rating - p2_rating)
    for b in config['Buckets']:
        if diff >= b['LowDiffPoint'] and diff <= b['HighDiffPoint']:
            return b['Points']
    raise Exception(f'No point range found for {diff}')

def initialize_players():
    with open('PlayerInitialRating.csv', newline='') as csvfile:
        reader = list(csv.reader(csvfile, delimiter=','))
        for row in reader:
            players[row[0]] = {
                'Name': row[0],
                'Ratings' : [[int(row[1]),{'Initial Rating'}]]
            }

def process_ratings():
    with open('ScoreData.csv', newline='') as csvfile:
        reader = list(csv.reader(csvfile, delimiter=','))
        for row in reader:
            play_date = row[0]
            p1 = [row[1], int(row[2])]
            p2 = [row[3], int(row[4])]
            winner = loser = None
            
            if p1[1] > p2[1]:
                winner = p1
                loser = p2
            else:
                winner = p2
                loser = p1

            actual = int(find_bucket_by_rating(loser[1]))/max_base

            winner_prev_rating = players[winner[0]]['Ratings'][-1][0]
            loser_prev_rating = players[loser[0]]['Ratings'][-1][0]

            winner_msg = f'{winner[0]}({winner_prev_rating}) beat {loser[0]}({loser_prev_rating}) {winner[1]}-{loser[1]} on {play_date}'
            loser_msg = f'{loser[0]}({loser_prev_rating}) lost to {winner[0]}({winner_prev_rating}) {winner[1]}-{loser[1]} on {play_date}'

            expected = (find_bucket_by_diff(winner_prev_rating, loser_prev_rating) - 1)/max_base
            if (winner_prev_rating > loser_prev_rating):
                winner_new_rating = winner_prev_rating + k_factor*(actual - expected)
                loser_new_rating = loser_prev_rating - k_factor*(actual-expected)
                players[winner[0]]['Ratings'].append([winner_new_rating, winner_msg])
                players[loser[0]]['Ratings'].append([loser_new_rating, loser_msg])
            else:
                winner_new_rating = winner_prev_rating + k_factor*(actual - expected)
                loser_new_rating = loser_prev_rating - k_factor*(actual-expected)
                players[winner[0]]['Ratings'].append([winner_new_rating, winner_msg])
                players[loser[0]]['Ratings'].append([loser_new_rating, loser_msg])

def print_ratings():
    for p in players:
        player = players[p]
        print(f'{player["Name"]}')
        print(f'---------------------------------------------')
        for i in player['Ratings']:
            print(i)
        print(f'*********************************************')

    rank = (dict(sorted(players.items(), key=lambda item: item[1]['Ratings'][-1][0], reverse=True)))
    for i in rank:
        p = rank[i]
        print(f'{p["Name"]}: {p["Ratings"][-1][0]}')


def main():
    initialize_players()
    process_ratings()
    print_ratings()

main()







    

