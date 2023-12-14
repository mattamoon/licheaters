import os
import pandas as pd
import berserk
from dotenv import load_dotenv
from gathercheater.constants import LICHESS_API_LIMIT


def configure():
    load_dotenv()


def remove_user(username, players):
    # if value is equal to username of the player analyzing, remove from list
    while username in players:
        players.remove(username)
    return players


def players_to_df(list_of_players):
    df = pd.DataFrame(list_of_players, columns=['users'])
    list_of_player_dfs = data_chunk(df, LICHESS_API_LIMIT)

    return list_of_player_dfs


def data_chunk(df, chunk_size):
    # Lichess rate limit is 300 ids per call. Chunk dataframe in groups of 300
    list_df = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]

    return list_df


def list_util(player_list, user):
    # remove duplicates from list
    player_list = list(set(player_list))

    # remove current user from list
    if user in player_list:
        player_list = remove_user(user, player_list)

    return player_list


def create_player_list(df):
    """ """
    players = []
    for elements in df['users']:
        players.append(elements)

    return players


def create_player_string(player_list):
    players_string = ','.join(player_list)
    return players_string
