from gathercheater.functions import lichess_access, configure, load_dotenv, players_to_df, game_dates, list_util, \
    pd, create_player_list, create_player_string
from gathercheater.gathercheater import GatherCheater
from gathercheater.constants import API_KEY, START, END, USER, dt
import gathercheater.constants as c
import berserk
import berserk.utils
import berserk.exceptions
import logging
import pytest

logging.basicConfig(filename='gathercheater.log', level=logging.DEBUG,
                    format='%(levelname)s:%(message)s')

__all__ = ('lichess_access',
           'configure',
           'load_dotenv',
           'configure',
           'GatherCheater',
           'API_KEY', 'START', 'END', 'USER',
           )


class TestClass:
    configure()
    lichess = GatherCheater()

    def test_user(self):
        user_id = 'BASILCANDLE'
        self.lichess.user = user_id
        assert self.lichess.user == 'basilcandle'
        assert self.lichess.user == user_id.lower()
        assert user_id != self.lichess.user

    def test_dates(self):
        value = dt.datetime(2022, 1, 1)
        self.lichess.start = '2022/1/1'
        self.lichess.end = '2022/1/1'
        assert self.lichess.start == value
        assert self.lichess.end == value

    def test_dates_bad_string_format(self):
        value = '11/5/2022'
        with pytest.raises(ValueError):
            self.lichess.start = value

        with pytest.raises(ValueError):
            self.lichess.end = value

    def test_dates_bad_string_value(self):
        value = 'YYYY/X/DD'
        with pytest.raises(ValueError):
            self.lichess.start = value

        with pytest.raises(ValueError):
            self.lichess.end = value

    def test_max_games(self):
        """Testing max_games from constants.py"""
        assert self.lichess.max_games == c.MAX_GAMES
        self.lichess.max_games = 50
        assert self.lichess.max_games == 50
        assert self.lichess.max_games > 0

        """ Test if max_games is <=-0"""
        with pytest.raises(ValueError):
            self.lichess.max_games = 0

    def test_api_limit(self):
        api_player_search_limit = self.lichess.api_limit
        assert api_player_search_limit <= 300

    def test_games_by_player_dates(self):
        """Test Dates, User connected, time variables, user has games"""
        b_start = game_dates(self.lichess.start)
        b_end = game_dates(self.lichess.end)
        games = self.lichess.games_by_player_dates(b_start, b_end)
        assert b_start == berserk.utils.to_millis(self.lichess.start)
        assert b_end == berserk.utils.to_millis(self.lichess.end)
        for game in games:
            assert game is not None

    def test_data_to_df(self):
        p_list = ['a', 'a', 'a', self.lichess.user]
        p_list = list_util(p_list, self.lichess.user)
        assert p_list == ['a']
        p_list = players_to_df(p_list)
        df1 = pd.DataFrame(['a'], columns=['users'])
        assert p_list[0].equals(df1) is True

    def test_create_player_list(self):
        df = pd.DataFrame(['a,b,c'], columns=['users'])
        test_player_list = create_player_list(df)
        assert test_player_list == ['a,b,c']
        test_player_list = create_player_string(test_player_list)
        assert test_player_list == 'a,b,c'

    def test_games_by_player_list(self):
        players = c.USER
        games = self.lichess.games_by_player_list(players)
        assert games[self.lichess.df_index] is not None

    def test_get_players_from_games(self):
        games = self.lichess.games_by_player_dates(game_dates(self.lichess.start), game_dates(self.lichess.end))
        players_from_games = self.lichess.get_players_from_games(games)
        assert players_from_games is not None

    def test_check_cheaters(self):
        test = [{'username': 'a', 'tosViolation': True}, {'username': 'b', 'disabled': True}, {'username': 'c'}]
        tos, closed, good = self.lichess.check_cheaters(test)

        assert tos == ['a']
        assert closed == ['b']
        assert good == ['c']


    def test_bad_key(self):
        test = [{'username': 'a', 'violation': True}, {'username': 'b', 'disabled': True}, {'username': 'c'}]

        with pytest.raises(KeyError):
            for item in test:
                item[2]['tosViolation']
