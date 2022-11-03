from gathercheater.functions import lichess_access, configure, load_dotenv, os
from gathercheater.gathercheater import GatherCheater
from gathercheater.constants import API_KEY, dt, START, END, USER
import gathercheater.constants as c
import berserk.exceptions
import pytest

__all__ = ('lichess_access',
           'configure',
           'load_dotenv',
           'configure',
           'GatherCheater',
           'API_KEY', 'START', 'END', 'USER',
           )


def test_configure(monkeypatch):
    """Testing api key config"""

    monkeypatch.setenv(API_KEY, '12345')
    assert os.getenv(API_KEY) == '12345'


def test_gathercheater_attribute_setup(api_access, monkeypatch):
    """Testing assertions with attributes used"""
    lichess = api_access

    with monkeypatch.context() as m:
        m.setattr(lichess, 'user', 'basilcandle')
        m.setattr(lichess, 'api_limit', 300)

        assert lichess.user.lower() == 'basilcandle'
        assert lichess.api_limit <= 300


def test_gathercheater_get_games(api_access, monkeypatch):
    """Testing for a user that does not exist"""
    lichess = api_access
    with monkeypatch.context() as m:
        m.setattr(lichess, 'user', 'basilcandley')

        games = lichess.games_by_player_dates()
        with pytest.raises(berserk.exceptions.ResponseError):
            for game in games:
                assert game is False


def test_gathercheater_dates(api_access):
    lichess = api_access

    assert lichess.end > lichess.start
    assert isinstance(lichess.start, dt.datetime)
    assert isinstance(lichess.end, dt.datetime)


def test_gathercheater_api_limit(api_access, monkeypatch):
    lichess = api_access
    monkeypatch.setattr(lichess, 'api_limit', 300)

    assert lichess.api_limit <= 300


def test_gathercheater_get_players_by_games():
    list_of_players = [{'players': {'white': {'user': {'name': c.USER, 'id': c.USER.lower()}}}}]
    assert list_of_players[0] is not None
    assert list_of_players[0]['players']['white']['user']['name'] == 'basilcandle'
    assert list_of_players[0]['players']['white']['user']['id'] == 'basilcandle'

    """Test for error when there is no dict key"""
    with pytest.raises(KeyError):
        for data in list_of_players:
            data[1]
