import os
import pandas as pd
import berserk
from dotenv import load_dotenv
from src.gathercheater.constants import API_KEY


def configure():
    load_dotenv()


def lichess_access():
    lichess_key = os.getenv(API_KEY)
    session = berserk.TokenSession(lichess_key)
    client = berserk.Client(session)

    return client


def remove_user(username, players):
    # if value is equal to username of the player analyzing, remove from list
    while username in players:
        players.remove(username)

    return players


def players_to_df(list_of_players):
    df = pd.DataFrame(list_of_players, columns=['users'])
    return df


def users_from_df(df):
    # Store all users from df to a list
    all_players = df['users'].tolist()

    return all_players


def data_chunk(df, chunk_size):
    # Lichess rate limit is 300 ids per call. Chunk dataframe in groups of 300
    list_df = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]

    return list_df
