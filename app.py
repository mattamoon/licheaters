import berserk.exceptions

from src.gathercheater.gathercheater import GatherCheater
from src.gathercheater.functions import configure


def app():
    configure()
    lichess = GatherCheater()
    games = lichess.games_by_player_dates()
    player_from_games = lichess.get_players_from_games(games)
    players_df = lichess.data_to_df(player_from_games)

    # Loop through list of dataframes
    while True:
        try:
            players_df[lichess.df_index]
        except(Exception,):
            print('Data Analysis Complete! \n')
            break
        else:
            player_list = lichess.create_player_list(players_df)
            data = lichess.games_by_player_list(player_list)
            lichess.data_list.extend(data)
            lichess.df_index += 1

    lichess.display_data(lichess.data_list)


if __name__ == "__main__":
    app()
