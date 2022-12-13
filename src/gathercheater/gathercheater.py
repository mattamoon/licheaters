from gathercheater.functions import lichess_access
import datetime as dt
import gathercheater.constants as c


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
        """Use YYYY/m/d format"""
        value_format = '%Y/%m/%d'
        try:
            self.__start = dt.datetime.strptime(value, value_format)

        except (Exception,):
            raise ValueError('Format is probably invalid')

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, value: str):
        """Use yyyy/m/d format to set datetime object"""
        value_format = '%Y/%m/%d'
        try:
            self.__end = dt.datetime.strptime(value, value_format)
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

    def games_by_player_dates(self, berserk_start, berserk_end):
        """Searches Lichess API for games from a user between 2 dates & returns those games as a generator"""

        starting = berserk_start
        ending = berserk_end

        games_data = self.lichess.games.export_by_player(self.__user, since=starting, until=ending,
                                                         max=self.__max_games)

        return games_data

    def games_by_player_list(self, players):
        data_list = []

        api_data = self.lichess.users.get_by_id(players)

        for data in api_data:
            data_list.append(data)

        return data_list

    @staticmethod
    def get_players_from_games(game_list):
        """get list of players from the list of dicts, returned from games_by_player_dates"""

        p_list = []
        for game in game_list:
            if game.get('players'):
                p_list.append(game['players']['white']['user']['name'].lower())
                p_list.append(game['players']['black']['user']['name'].lower())

        return p_list

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
