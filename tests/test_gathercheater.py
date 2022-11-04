from gathercheater.functions import lichess_access, configure, load_dotenv, os, remove_user, players_to_df, data_chunk
from gathercheater.gathercheater import GatherCheater
from gathercheater.constants import API_KEY, START, END, USER
import gathercheater.constants as c
import berserk.exceptions
import berserk
import pandas as pd
import pytest

__all__ = ('lichess_access',
           'configure',
           'load_dotenv',
           'configure',
           'GatherCheater',
           'API_KEY', 'START', 'END', 'USER',
           )


def test_configure_api_key(monkeypatch):
    """Testing api key config"""

    with monkeypatch.context() as m:
        assert os.getenv(API_KEY) is None
        configure()
        assert os.getenv(API_KEY) is not None
        m.setenv(API_KEY, '12345')
        assert os.getenv(API_KEY) == '12345'


def test_gathercheater_user_account(monkeypatch):
    configure()
    lichess = GatherCheater()
    user = lichess_access().account.get().get('id')
    assert lichess.user == user

    with monkeypatch.context() as m:
        m.setattr(lichess, 'user', 'incorrect+user')
        assert lichess.user != user
        m.setattr(lichess, 'user', '')
        assert lichess.user == ''


def test_gathercheater_attribute_setup(monkeypatch):
    """Testing assertions with attributes used"""
    lichess = GatherCheater()

    with monkeypatch.context() as m:
        assert lichess.user == lichess.user.lower()
        assert lichess.df_index < 1
        assert lichess.end > lichess.start
        m.setattr(lichess, 'api_limit', 300)
        assert lichess.api_limit <= 300
        assert lichess.data_list == []


def test_gathercheater_get_games(monkeypatch):
    """Testing if games by player dates returns games.
    Expecting a response error due to incorrect username. How to test berserk http response?
    """
    configure()
    lichess = GatherCheater()
    with monkeypatch.context() as m:
        m.setattr(lichess, 'user', 'incorrect+user')

        games = lichess.games_by_player_dates()
        with pytest.raises(berserk.exceptions.ResponseError):
            for game in games:
                assert game is None


def test_gathercheater_get_players_by_games():
    list_of_players = [{'players': {'white': {'user': {'name': c.USER, 'id': c.USER.lower()}}}}]
    assert list_of_players[0] is not None
    assert list_of_players[0]['players']['white']['user']['name'] == 'basilcandle'
    assert list_of_players[0]['players']['white']['user']['id'] == 'basilcandle'

    """Test for error when there is no dict key"""
    with pytest.raises(KeyError):
        for data in list_of_players:
            data[1]
            assert data is None


def test_gathercheater_data_to_df():
    lichess = GatherCheater()
    response = [{'id': c.USER}, {'id': 'a'}, {'id': 'a'}, {'id': 'a'}]
    players = ['a', 'a', 'a', lichess.user]

    assert type(players) == list

    """ Test if api user is in the list of games played"""
    get_ids = [d['id'] for d in response if 'id' in d]
    get_ids = list(set(get_ids))  # removing duplicates

    assert lichess.user in get_ids  # should be there
    """Test api user removed from response"""
    data = remove_user(lichess.user, get_ids)
    assert lichess.user not in data

    """Test player list converted to dataframe"""
    data_to_df = players_to_df(data)
    assert data_to_df.empty is False

    """Test player list larger than the api limit is chunked into a list of dataframes by the api limit"""
    df = [1] * 301
    df = players_to_df(df)
    chunked_data = data_chunk(df, lichess.api_limit)
    assert chunked_data[lichess.df_index].size == lichess.api_limit
    assert chunked_data[lichess.df_index+1].size == 1


def test_gathercheater_create_player_list():
    pass


def test_gathercheater_games_by_player_list():
    pass
