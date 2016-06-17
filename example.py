import mahjong as mmt
import pandas as pd
import random

def main():
    players_list = [40,6,23,26,15,98,1,10,55,16,56,
                       97,96,12,13,41,52,88,66,94,
                       89,86,87,77,79,72,76]

    # Use pandas to import .csv to DataFrame object
    input_data = pd.read_csv('MahjongScores.csv')

    # Determine number of tables to create
    table_counts = mmt.get_table_counts(players_list)

    # Create empty pairings DataFrame for players
    pairings_df = mmt.create_pairings_table(players_list)

    # Populate pairings_df with matchups based on play frequency
    matchups_df = mmt.create_freq_matchups(pairings_df, input_data)

    # Apply matchmaking and print tables
    output_tables = mmt.match_by_rating(table_counts, matchups_df)
    print(output_tables)

main()