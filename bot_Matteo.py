from interfaces import Strategy, Token, Board, IllegalMove
import copy

class Kelawin(Strategy):
    def authors(self) -> str:
        return "Kay et Matteo"

    def play(self, current_board: Board, your_token: Token) -> int:
        pass

    def score_position(board: Board, player_token: Token) -> int:
        """
        Évalue une position pour un joueur donné.
        :param board: état actuel du jeu
        :param player_token: Token.RED ou Token.YELLOW
        :return: score entier de la position
        """
        score = 0

        # On y ajoutera l’évaluation des lignes, colonnes, diagonales, etc.

        return score
