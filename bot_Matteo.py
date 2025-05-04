from interfaces import Strategy, Token, Board, IllegalMove
import copy

class Kelawin(Strategy):
    def authors(self) -> str:
        return "Kay et Matteo"

    def play(self, current_board: Board, token: Token) -> int:
        pass

    def adversaire(self, nous:Token):
        #determiner la couleur de notre adversaire
        return Token.YELLOW if nous.RED else Token.RED

    def col_libres(self, board:Board):

        #Parcourt chaque colonne et regarde si la dernière case est vide.
        for i in range(board.width - 1):
            coups = []
            col = board.column(i)
            #si oui, il l'ajoute à la liste
            if col[0] == Token.EMPTY:
                coups.append(i)

        #retourne la liste des coups jouables
        return coups

    def simulation(self, board:Board, col:int, token:Token):

        # cette fonction sert à "simuler" un coup, pour voir ses conséquences
        # pour cela, elle crée une "copie parfaite" du tableau actuel

        #tout d'abord, on crée un nouveau tableau de jeu vide, avec les mêmes variables
        new_board = Board(board.height, board.width, board.to_win)

        #on regarde chaque pion et rejouons le meme dans le nouveau tab.
        for i in board.column():
            for j in board.line():
                pion = board.box(i,j)
                new_board.play(i,pion)

        #puis on ajoute le coup simulé dans ce nouveau tableau
        new_board.play(col, token)

        #on retourne la copie
        return new_board

    def suite_gagnante(self, suite, token:Token, to_win:int):

        #On regarde si dans une certaine ligne ou colonne, il y a une suite finie
        num = 0
        for case in suite:
            if case == token:
                num += 1
                if num == to_win:
                    return True
            else:
                num = 0
        return False

    def winner(self, board:Board, token:Token) -> bool:

        #le but de cette fonction est de voir si quelqu'un a win

        #on check toutes les lignes
        for i in range(board.height-1):
            ligne = board.line(i)
            if self.suite_gagnante(ligne, token, board.to_win):
                return True

        #on check toutes les colonnes
        for i in range(board.width-1):
            col = board.line(i)
            if self.suite_gagnante(col, token, board.to_win):
                return True

        #on check toutes les diagonales (un peu différent)
        for diag in board.diagonals():
            if self.suite_gagnante(diag, token, board.to_win):
                return True

    def fin(self, board:Board):

        #ici, on doit contrôler si la partie est finie

        #on regarde si un des deux joueurs s'est imposé
        if self.winner(board, Token.RED) or self.winner(board, Token.YELLOW):
            return True

        # ou s'il y a une égalité
        if self.col_libres(board) == 0:
            return True

        # sinon, la partie n'est pas finie
        return False

    def minimax(self, board:Board, profond:int, max:bool, token:Token):

        # cerveau du bot, c'est ici qu'il calcule les coups d'avance.

        #tout d'abord, on vérifie si c'est une fin de partie
        # ou si le bot doit arrêter de réfléchir
        if self.fin(board) == True or profond == 0:
            valeur = self.evalue(board, token)
            return valeur

        #si c'est à nous de jouer :
        if max == True:

            # on attribue un score très bas pour être sûrs d'avoir plus haut
            score = float(-9999999)

            # on récupère chaque coup possible
            for coup in self.col_libres(board):

                #et on le simule
                new_board = self.simulation(board, coup, token)


        #si c'est à l'adversaire
        else :

            #on récupère sa couleur
            adv = self.adversaire(token)

            #on attribue un score très haut
            score = float(99999999)

            # on récupère chaque coup possible
            for coup in self.col_libres(board):
                # et on le simule
                new_board = self.simulation(board, coup, token)




    def evalue(self, board, token) -> float:
        pass

























