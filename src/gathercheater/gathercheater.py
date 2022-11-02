from src.gathercheater.functions import lichess_access, remove_user, players_to_df, data_chunk, users_from_df
from src.gathercheater import constants as c
from src.gathercheater.constants import dt, berserk


class GatherCheater:

    def __init__(self):
        self.lichess = lichess_access()
        self.user = c.USER.lower()
        self.start = c.START
        self.end = c.END
        self.max_games = c.MAX_GAMES
        self.df_index = c.DF_INDEX
        self.api_limit = c.LICHESS_API_LIMIT
        self.data_list = []

    def games_by_player_dates(self):
        # Start time variables
        start_y = int(self.start.strftime('%Y'))
        start_m = int(self.start.strftime('%m'))
        start_d = int(self.start.strftime('%d'))

        # End time variables
        end_y = int(self.end.strftime('%Y'))
        end_m = int(self.end.strftime('%m'))
        end_d = int(self.end.strftime('%d'))

        starting = berserk.utils.to_millis(dt.datetime(start_y, start_m, start_d))
        ending = berserk.utils.to_millis(dt.datetime(end_y, end_m, end_d))

        games_data = self.lichess.games.export_by_player(self.user, since=starting, until=ending, max=self.max_games)

        return games_data

    def data_to_df(self, p_list):
        # remove duplicates from list
        p_list = list(dict.fromkeys(p_list))

        # remove current user from list
        if self.user in p_list:
            p_list = remove_user(self.user, p_list)

        # convert players to dataframe in order to chunk
        p_list_df = players_to_df(p_list)

        # chunk data regardless of size
        p_list_df = data_chunk(p_list_df, self.api_limit)

        return p_list_df

    def create_player_list(self, list_df):

        player_list = users_from_df(list_df[self.df_index])

        # convert list of players to string
        player_list_string = ','.join(player_list)

        return player_list_string

    def games_by_player_list(self, players):

        api_data = self.lichess.users.get_by_id(players)

        return api_data

    @staticmethod
    def get_players_from_games(game_list):
        # get list of players from the list of dicts returned from games_by_player_dates
        p_list = []

        for game in game_list:
            try:
                p_list.append(game['players']['white']['user']['name'].lower())
                p_list.append(game['players']['black']['user']['name'].lower())
            except KeyError:
                break

        return p_list

    @staticmethod
    def check_cheaters(players):
        cheater_list = []
        closed_accounts = []
        not_cheater = []

        for item in players:
            if item.get('tosViolation'):
                cheater_list.append(item['username'])
            elif item.get('disabled'):
                closed_accounts.append(item['username'])
            else:
                not_cheater.append(item['username'])

        return cheater_list, closed_accounts, not_cheater

    @staticmethod
    def display_data(players):
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
