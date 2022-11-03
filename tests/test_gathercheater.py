import datetime

from gathercheater.functions import lichess_access, configure, load_dotenv, os
from gathercheater.gathercheater import GatherCheater
from gathercheater.constants import API_KEY, dt, START, END, TEST_API_KEY, USER
import gathercheater.constants as c
import berserk.exceptions
import pytest


def test_configure(monkeypatch):
    """Testing api key config"""

    monkeypatch.setenv(API_KEY, '12345')
    assert os.getenv(API_KEY) == '12345'


def test_gathercheater_attribute_setup(api_access, monkeypatch):
    """"""
    lichess = api_access

    with monkeypatch.context() as m:
        m.setattr(lichess, 'user', 'basilcandley')
        m.setattr(lichess, 'start', dt.datetime(2022, 1, 1))
        m.setattr(lichess, 'end', dt.datetime(2022, 12, 31))
        m.setattr(lichess, 'max_games', 10)
        m.setattr(lichess, 'api_limit', 300)

        assert lichess.user.lower() == 'basilcandley'
        assert lichess.start == c.START
        assert lichess.end == c.END
        assert lichess.end > lichess.start
        assert lichess.api_limit <= 300


def test_gathercheater_get_games(api_access, monkeypatch):
    """Testing for a user that does not exist"""
    lichess = api_access
    with monkeypatch.context() as m:
        m.setattr(lichess, 'user', 'basilcandley')

        games = lichess.games_by_player_dates()
        with pytest.raises(berserk.exceptions.ResponseError):
            for game in games:
                assert game is True


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
    pass
