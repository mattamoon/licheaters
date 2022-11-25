from gathercheater.functions import lichess_access
import datetime as dt
import gathercheater.constants as c


class GatherCheater:

    def __init__(self):
        self.__lichess = lichess_access()
        self._user = c.USER.lower()
        self._start = c.START
        self._end = c.END
        self._max_games = c.MAX_GAMES
        self.df_index = 0
        self.__api_limit = c.LICHESS_API_LIMIT
        self.data_list = []

    @property
    def user(self):
        """Return the currently set user"""
        return self._user

    @user.setter
    def user(self, value: str):
        """Set user for games to check"""
        self._user = value.lower()

    @property
    def start(self):
        """Return the set Start Datetime"""
        return self._start

    @start.setter
    def start(self, value: str):
        """Set the start date using YYYY/m/d format"""
        value_format = '%Y/%m/%d'
        try:
            self._start = dt.datetime.strptime(value, value_format)

        except (ValueError,):
            raise ValueError('Format is probably invalid')

    @property
    def end(self):
        """Return the set end date for games to check"""
        return self._end

    @end.setter
    def end(self, value: str):
        """Use yyyy/m/d format to set datetime object"""
        value_format = '%Y/%m/%d'
        try:
            self._end = dt.datetime.strptime(value, value_format)
        except (ValueError,):
            raise ValueError('Format is probably invalid')

    @property
    def max_games(self):
        """Return the set number of max games to review"""
        return self._max_games

    @max_games.setter
    def max_games(self, value: int):
        """Set the total number of games to review"""
        if value > 0:
            self._max_games = value
        else:
            raise ValueError('Value cannot be <= 0')

    @property
    def api_limit(self):
        return self.__api_limit

    def games_by_player_dates(self, berserk_start, berserk_end):
        """Search Lichess API for games from a user between 2 dates & returns those games as a generator"""

        starting = berserk_start
        ending = berserk_end

        games_data = self.__lichess.games.export_by_player(self._user, since=starting, until=ending,
                                                           max=self._max_games)

        return games_data

    def games_by_player_list(self, players):
        """Get game data by a string of player names"""
        api_data = self.__lichess.users.get_by_id(players)
        return api_data

    @staticmethod
    def get_players_from_games(game_list):
        """get list of player usernames from the list of dicts returned from the games_by_player_list function"""

        p_list = []
        for game in game_list:
            if game.get('players'):
                p_list.append(game['players']['white']['user']['name'].lower())
                p_list.append(game['players']['black']['user']['name'].lower())

        return p_list

    @staticmethod
    def check_cheaters(players):
        """Returns 3 list: violated ToS accounts, Closed Accounts, and accounts with no infractions"""
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
        """Displays the 3 lists populated from the check_cheaters function"""
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
