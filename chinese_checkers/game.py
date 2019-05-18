import os
from chinese_checkers.board import Board
from chinese_checkers.players.player import Player
from collections import deque

class Game(object):
    
    def __init__(self, board: Board):
        self.board = board
    
    #--------------------------------------------------------------------------------------------

    def print_board(self,board):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('*******CHINESE CHECKERS*******')
        for i in range(1,10):
            line = ""
            for j in range(1,10):
                if (i,j) in board.pieces_p1:
                    line = line + "| 1 / " + str(board.pieces_p1.index((i,j)))
                elif (i,j) in board.pieces_p2:
                    line = line + "| 2 / " + str(board.pieces_p2.index((i,j)))
                else:
                    line = line + "|      "
            line = line + "|"
            print(line)
        print(" Indice | Pos P1 | Pos P2")
        for x in range(10):
            print("     " + str(x) + "  | " + str(board.pieces_p1[x]) + " | " + str(board.pieces_p2[x]))

    #--------------------------------------------------------------------------------------------

    def play_game(self, player1: Player, player2: Player, start_player):
        if start_player not in (1, 2):
            raise Exception('Invalid player id')
        
        self.board.set_current_player(start_player)
        p1 = player1
        p2 = player2
        first_movement = True

        # Colas FIFO donde se guardan los ultimos cinco movimientos de un jugador.
        # Usadas para detectar empate.
        p1_prev_moves = deque([], 5)
        p2_prev_moves = deque([], 5)

        while (1):
            current_player = self.board.current_player

            if current_player == 1:
                # Se setea el valor previo con el valor actual del tablero
                # porque es antes de que el jugador haga su movimiento
                p1.set_prev_value_board(self.board)

                # Se calcula el mejor movimiento
                index, position_to_move = p1.do_move(self.board)

                # Se hacen los cambios en el tablero
                self.board.do_move(index, position_to_move)

                # Se agrega el ultimo movimiento realizado por el jugador a la 
                # lista de movimientos previos
                p1_prev_moves.append((index, position_to_move))

                # Se recalculan los pesos. Si es la primera ronda, como no existe 
                # valor previo, no se recalcula
                if not first_movement:
                    p2.recalc_weights(self.board)
                first_movement = False

                self.board.set_current_player(2)
            else:
                # Se setea el valor previo con el valor actual del tablero
                # porque es antes de que el jugador haga su movimiento
                p2.set_prev_value_board(self.board)

                # Se calcula el mejor movimiento
                index, position_to_move = p2.do_move(self.board)

                # Se hacen los cambios en el tablero
                self.board.do_move(index, position_to_move)

                # Se agrega el ultimo movimiento realizado por el jugador a la 
                # lista de movimientos previos
                p2_prev_moves.append((index, position_to_move))

                # Se recalculan los pesos. Si es la primera ronda, como no existe 
                # valor previo, no se recalcula
                if not first_movement:    
                    p1.recalc_weights(self.board)
                first_movement = False

                self.board.set_current_player(1)

            self.print_board(self.board)

            # Se verifica que algun jugador no este repitiendo la misma jugada que
            # en el turno anterior al anterior. En caso de detectarlo devuelve empate
            if((len(p1_prev_moves) == 5 
               and p1_prev_moves[0] == p1_prev_moves[2]
               and p1_prev_moves[0] == p1_prev_moves[4]
               and p1_prev_moves[1] == p1_prev_moves[3]) 
               or
               (len(p2_prev_moves) == 5 
               and p2_prev_moves[0] == p2_prev_moves[2]
               and p2_prev_moves[0] == p2_prev_moves[4]
               and p2_prev_moves[1] == p2_prev_moves[3])):
                return 0

            end, winner = self.board.end_of_game()
            if end:
                return winner          