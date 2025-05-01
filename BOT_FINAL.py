from interfaces import Strategy, Token, Board, IllegalMove
import copy

class Kelawin(Strategy):
    def authors(self) -> str:
        return "Kay et Matteo"

    def play(self, current_board: Board, your_token: Token) -> int:
        self.token = your_token
        self.opponent_token = Token.RED if your_token == Token.YELLOW else Token.YELLOW

        for col in self.coup_legal(current_board):
            if self.coup_gagnant(current_board, self.token, col):
                return col

        for col in self.coup_legal(current_board):
            if self.coup_gagnant(current_board, self.opponent_token, col):
                return col

        best_col, _ = self.minimax(current_board, profondeur=6, alpha=float('-inf'), beta=float('inf'), max_p=True)
        return best_col

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

    def score_position(self, board, token):
        score = 0

        col_centrale = board.column(board.width // 2)
        token_centraux = col_centrale.count(token)
        score += token_centraux * 3


        for ligne in range(board.height):
            ligne_suite = board.line(ligne)
            for col in range(board.width - 3):
                groupe = ligne_suite[col:col + 4]
                score += self.points_groupe(groupe, token)
                if groupe.count(self.opponent_token) == 3 and groupe.count(Token.EMPTY) == 1:
                    score -= 10

        for col in range(board.width):
            col_suite = board.column(col)
            for ligne in range(board.height - 3):
                groupe = col_suite[ligne:ligne + 4]
                score += self.points_groupe(groupe, token)
                if groupe.count(self.opponent_token) == 3 and groupe.count(Token.EMPTY) == 1:
                    score -= 10

        for diagonale in range(board.height - 3):
            for col in range(board.width - 3):
                groupe = [board.box(diagonale + i, col + i) for i in range(4)]
                score += self.points_groupe(groupe, token)
                if groupe.count(self.opponent_token) == 3 and groupe.count(Token.EMPTY) == 1:
                    score -= 10

        for diagonale in range(3, board.height):
            for col in range(board.width - 3):
                groupe = [board.box(diagonale - i, col + i) for i in range(4)]
                score += self.points_groupe(groupe, token)
                if groupe.count(self.opponent_token) == 3 and groupe.count(Token.EMPTY) == 1:
                    score -= 10

        return score

    def points_groupe(self, groupe:list[Token], token:Token) -> int:
        score = 0
        pion_adverse = Token.RED if token == Token.YELLOW else Token.YELLOW

        pion = groupe.count(token)
        adversare = groupe.count(pion_adverse)
        case_vide = groupe.count(Token.EMPTY)

        if pion == 4:
            score += 100
        elif pion == 3 and case_vide == 1:
            score += 5
        elif pion == 2 and case_vide == 2:
            score += 2

        if adversare == 3 and case_vide == 1:
            score -= 4

        return score

    def minimax(self, board: Board, profondeur: int, alpha: float, beta: float, max_p: bool):
        if profondeur == 0 or self.fin_partie(board):
            return None, self.score_position(board, self.token) if max_p else self.score_position(board,
                                                                                                  self.opponent_token)

        coups_legaux = self.coup_legal(board)

        if max_p:
            max_eval = -float('inf')
            best_col = coups_legaux[0]
            for col in coups_legaux:
                copie_board = copy.deepcopy(board)  # Copie du plateau juste avant de jouer un coup
                copie_board.play(col, self.token)
                _, eval = self.minimax(copie_board, profondeur - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_col = col
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_col, max_eval
        else:
            min_eval = float('inf')
            best_col = coups_legaux[0]
            for col in coups_legaux:
                copie_board = copy.deepcopy(board)  # Copie du plateau juste avant de jouer un coup
                copie_board.play(col, self.opponent_token)
                _, eval = self.minimax(copie_board, profondeur - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_col = col
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_col, min_eval

    def fin_partie(self, board:Board):
        for i in range(board.height):
            if self.aligne(board.line(i)):
                return True

        for j in range(board.width):
            if self.aligne(board.column(j)):
                return True

        for diag in board.diagonals():
            if self.aligne(diag):
                return True

        if not self.coup_legal(board):
            return True

        return False

    def aligne(self, liste: list[Token]) -> bool:
        compteur = 0
        dernier = None

        for t in liste:
            if t == dernier and t != Token.EMPTY:
                compteur += 1
                if compteur == 4:
                    return True
            else:
                compteur = 1
                dernier = t

        return False



