from gathercheater.functions import lichess_access, configure, players_to_df, list_util, create_player_list, create_player_string
from gathercheater.gathercheater import GatherCheater
from gathercheater.constants import API_KEY, START, END, USER
from dotenv import load_dotenv
import gathercheater.constants as c
import pandas as pd
import pytest

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
        user_id = c.USER.upper()
        self.lichess.user = user_id
        assert self.lichess.user == c.USER.lower()
        assert self.lichess.user == user_id.lower()
        assert user_id != self.lichess.user

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

    @pytest.mark.skip(reason="HTTP Error if api key is bad or missing")
    def test_games_by_player_dates(self):
        """Test Dates, time variables, user has games. If api key is bad or not present expect http 401
        - Removed game_dates function 12/13"""
        games = self.lichess.games_by_player_dates()
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

    @pytest.mark.skip(reason="HTTP Error if api key is bad or missing")
    def test_games_by_player_list(self):
        players = c.USER
        games = self.lichess.games_by_player_list(players)
        assert games[self.lichess.df_index] is not None

    def test_get_players_from_games(self):
        test_dict = [{'players': {'white': {'user': {'name': 'basilcandle'}}, 'black': {'user': {'name': 'raz'}}}}, {}]
        games = self.lichess.get_players_from_games(test_dict)
        assert games == ['basilcandle', 'raz']

    def test_check_cheaters(self):
        test = [{'username': 'a', 'tosViolation': True}, {'username': 'b', 'disabled': True}, {'username': 'c'}]
        tos, closed, good = self.lichess.check_cheaters(test)

        assert tos == ['a']
        assert closed == ['b']
        assert good == ['c']

    def test_bad_key(self):
        """Testing with bad user keys"""
        test = [{'user': 'a', 'violation': True}, {'user': 'b', 'disabled': True}, {'user': 'c'}]

        with pytest.raises(KeyError):
            self.lichess.check_cheaters(test)

    def test_display_data(self, capsys):
        """Not sure how to do this..."""
        pass
