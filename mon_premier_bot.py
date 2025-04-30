from interfaces import Strategy, Token, Board, IllegalMove
import copy

class Kelawin(Strategy):
    def authors(self) -> str:
        return "Kay et Matteo"

    def play(self, current_board: Board, your_token: Token) -> int:
        coup_legal = self.coup_legal(current_board)
        adversaire = Token.RED if your_token == Token.YELLOW else Token.YELLOW

        for col in coup_legal:
            if self.coup_gagnant(current_board, your_token, col):
                return col

        for col in coup_legal:
            if self.coup_gagnant(current_board, adversaire, col):
                return col


        prio = [3, 2, 4, 1, 5, 0, 6]
        for col in prio:
            if Token.EMPTY in current_board.column(col):
                return col

        return coup_legal[0]
    
    def coup_legal(self, board:Board) -> list[int]:
        colonnes_valides = []
        for colonnes in range(board.width):
            if Token.EMPTY in board.column(colonnes):
                colonnes_valides.append(colonnes)
        return colonnes_valides

    def coup_gagnant(self, board:Board, token:Token, column:int) ->bool:
        try:
            copie_board = copy.deepcopy(board)
            copie_board.play(column,token)
        except IllegalMove:
            return False

        def compte_suites(tokens):
            compte = 0
            for t in tokens:
                if t == token:
                    compte += 1
                    if compte == board.to_win:
                        return True
                else:
                    compte = 0
            return False

        for i in range(board.height):
            if compte_suites(copie_board.line(i)):
                return True

        for j in range(board.width):
            if compte_suites(copie_board.column(j)):
                return True

        for diagonale in copie_board.diagonals():
            if compte_suites(diagonale):
                return True

        return False