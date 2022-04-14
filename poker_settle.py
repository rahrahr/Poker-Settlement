from read_files import read_file, read_folder
import bisect
import sys
import os
import pandas as pd

def get_suggestion(df):
    entries = sorted(x.to_list()[::-1] for _, x in df.iterrows())
    def greedy_settle(list_of_entries):
        # match the biggest loser to the biggest winner
        if not list_of_entries or len(list_of_entries) == 1:
            return []

        top_loser = list_of_entries[0]
        transfer_amount = -top_loser[0]
        top_winner = list_of_entries.pop()
        top_winner[0] -= transfer_amount
        top_winner_name = top_winner[-1]

        bisect.insort(list_of_entries, top_winner)
        if transfer_amount == 0:
            return greedy_settle(list_of_entries[1:])
        return greedy_settle(list_of_entries[1:]) + [(top_loser[-1], f'To {top_winner_name}:{transfer_amount}')]

    suggestion = greedy_settle(entries)
    suggestion = pd.Series([x[1] for x in suggestion], index=[x[0] for x in suggestion])
    df = df.set_index('player')
    df.loc[suggestion.index, 'suggestion'] = suggestion
    df.fillna(0, inplace=True)
    return df

def main():
    path = sys.argv[1]
    if os.path.isfile(path):
        df = read_file(path)

    elif os.path.isdir(path):
        df = read_folder(path)

    df = get_suggestion(df)
    df.to_csv('suggestion.csv', encoding='gbk')

if __name__ == '__main__':
    main()
