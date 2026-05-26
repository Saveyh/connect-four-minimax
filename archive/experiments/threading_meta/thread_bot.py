import threading
import time
from interfaces import Strategy, Board, Token, IllegalMove
from minimax_bot import clone_board


class MinimaxBotV3(Strategy):
    def __init__(self):
        self.next_move_guess = None
        self._thinking_thread = None
        self._stop_thinking = threading.Event()
        self._start_time = None  # Pour mesurer le temps de réflexion

    def authors(self):
        return "Matteo - Minimax Bot avec réflexion rapide"

    def notify_opponent_move(self, board: Board, your_token: Token):
        """ Cette méthode est appelée lorsque l'adversaire joue (toi) """
        # Si un thread de réflexion était déjà en cours, on l'arrête pour en démarrer un nouveau
        self._stop_thinking.set()

        # Crée un nouveau thread pour que le bot puisse réfléchir pendant ton tour
        def background_think():
            self._stop_thinking.clear()
            fake_board = clone_board(board)
            try:
                self._start_time = time.time()  # Enregistrer l'heure de début de la réflexion
                # Réflexion avec un temps limité à 1 seconde
                _, move = self.limited_minimax(fake_board, depth=4, alpha=float("-inf"), beta=float("inf"), maximizing=True)
                if not self._stop_thinking.is_set():
                    self.next_move_guess = move  # Le coup calculé pour plus tard
            except Exception as e:
                print(f"Erreur lors du calcul du coup : {e}")

        self._thinking_thread = threading.Thread(target=background_think)
        self._thinking_thread.start()

    def limited_minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing: bool):
        """Minimax avec limite de temps de 1 seconde"""
        start_time = time.time()
        best_move = None
        best_value = float("-inf") if maximizing else float("inf")

        def minimax_with_time_limit(board, depth, alpha, beta, maximizing):
            nonlocal best_move, best_value
            if time.time() - start_time > 1:  # Vérifie si une seconde est écoulée
                return best_value, best_move

            if depth == 0 or board.is_game_over():
                return self.evaluate(board), None

            if maximizing:
                for col in range(board.width):
                    if board.is_valid_move(col):
                        board.play(col, Token.YELLOW)  # Token du bot
                        value, _ = minimax_with_time_limit(board, depth - 1, alpha, beta, False)
                        board.undo_move(col)
                        if value > best_value:
                            best_value = value
                            best_move = col
                        alpha = max(alpha, best_value)
                        if beta <= alpha:
                            break  # Alpha-beta pruning
            else:
                for col in range(board.width):
                    if board.is_valid_move(col):
                        board.play(col, Token.RED)  # Token du joueur humain
                        value, _ = minimax_with_time_limit(board, depth - 1, alpha, beta, True)
                        board.undo_move(col)
                        if value < best_value:
                            best_value = value
                            best_move = col
                        beta = min(beta, best_value)
                        if beta <= alpha:
                            break  # Alpha-beta pruning

            return best_value, best_move

        # Démarre le calcul de Minimax avec le timer
        return minimax_with_time_limit(board, depth, alpha, beta, maximizing)

    def play(self, current_board: Board, your_token: Token) -> int:
        """ Quand c'est à son tour, utilise le coup calculé précédemment """
        if self.next_move_guess is not None:
            move = self.next_move_guess
            self.next_move_guess = None  # On vide la mémoire pour le prochain tour
            return move
        else:
            # Si la réflexion n'est pas terminée, on calcule immédiatement avec une profondeur réduite
            _, move = self.limited_minimax(current_board, depth=2, alpha=float("-inf"), beta=float("inf"), maximizing=True)
            return move
