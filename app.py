from src.gathercheater.gathercheater import GatherCheater
from src.gathercheater.functions import *


def app():
    configure()
    lichess = GatherCheater()
    games = lichess.games_by_player_dates(game_dates(lichess.start), game_dates(lichess.end))
    players_from_games = lichess.get_players_from_games(games)
    player_list = list_util(players_from_games, lichess.user)
    player_dfs = players_to_df(player_list)
    total_iterations = len(player_dfs)
    # Loop through list of dataframes
    while lichess.df_index <= total_iterations:
        try:
            player_dfs[lichess.df_index]
        except(IndexError,):
            print('Data Analysis Complete! \n')
            break
        else:
            player_list = create_player_list(player_dfs[lichess.df_index])
            data_string = create_player_string(player_list)
            data = lichess.games_by_player_list(data_string)
            lichess.data_list.extend(data)
            lichess.df_index += 1

    lichess.display_data(lichess.data_list)


if __name__ == "__main__":
    app()
