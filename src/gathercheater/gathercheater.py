from gathercheater.functions import lichess_access
import datetime as dt
import gathercheater.constants as c
import berserk


class GatherCheater:

    def __init__(self):
        self._lichess = lichess_access()
        self.__user = c.USER.lower()
        self.__start = c.START
        self.__end = c.END
        self.__max_games = c.MAX_GAMES
        self.df_index = 0
        self.__api_limit = c.LICHESS_API_LIMIT
        self.data_list = []

    @property
    def lichess(self):
        return self._lichess

    @lichess.setter
    def lichess(self, client):
        self._lichess = client

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value: str):
        """Set user to check games"""
        self.__user = value.lower()

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value: str):
        """Use ISO Format YYYY-MM-DD"""
        try:
            self.__start = dt.datetime.fromisoformat(value)

        except (Exception,):
            raise ValueError('Format is probably invalid')

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, value: str):
        """Use ISO format YYYY-DD-MM"""
        try:
            value = '2022-01-01'
            self.__end = dt.datetime.fromisoformat(value)
        except (Exception,):
            raise ValueError('Format is probably invalid')

    @property
    def max_games(self):
        return self.__max_games

    @max_games.setter
    def max_games(self, value: int):
        if value > 0:
            self.__max_games = value
        else:
            raise ValueError('Value cannot be <= 0')

    @property
    def api_limit(self):
        return self.__api_limit

    def games_by_player_dates(self):
        """Searches Lichess API for games from a user between 2 dates & returns those games as a generator"""

        starting = berserk.utils.to_millis(self.__start)
        ending = berserk.utils.to_millis(self.__end)

        games_data = self._lichess.games.export_by_player(self.__user, since=starting, until=ending,
                                                          max=self.__max_games)

        return games_data

    def games_by_player_list(self, players):
        api_data = self._lichess.users.get_by_id(players)
        return api_data

    @staticmethod
    def get_players_from_games(game_list):
        """get list of players from the list of dicts, returned from games_by_player_dates"""

        list_of_players = []
        for game in game_list:
            try:
                list_of_players.append(game['players']['white']['user']['name'].lower())
                list_of_players.append(game['players']['black']['user']['name'].lower())
            except KeyError:
                continue

        return list_of_players

    @staticmethod
    def check_cheaters(players):
        cheater_list = []
        closed_accounts = []
        not_cheater = []

        try:
            for item in players:
                if item.get('tosViolation'):
                    cheater_list.append(item['username'])
                elif item.get('disabled'):
                    closed_accounts.append(item['username'])
                else:
                    not_cheater.append(item['username'])

        except KeyError:
            raise KeyError

        return cheater_list, closed_accounts, not_cheater

    @staticmethod
    def display_data(players):  # pragma: no cover
        (violated, closed, good) = GatherCheater.check_cheaters(players)
        (v_total, c_total, g_total) = [len(violated), len(closed), len(good)]

        # Display new lists
        print(f'Violated Lichess ToS: {violated}')
        print(f'Total violated: {v_total} \n')
        print(f'Closed accounts: {closed} ')
        print(f'Total closed: {c_total} \n')
        print(f'Good Status...for now: {good} ')
        print(f'Total good: {g_total}')

        users_total = v_total + c_total + g_total
        print(f'\nTotal user accounts reviewed: {users_total}')
