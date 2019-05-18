import random
from chinese_checkers.players.player import Player

class PlayerRandom(Player):
    
    def __init__(self, id):
        super().__init__(id)

    #--------------------------------------------------------------------------------------------

    # Devuelve una lista con movimientos validos al hacer un salto.            
    # Si el salto no se puede hacer devuelve vacia.
    def do_jump(self, piece_to_jump, index_piece_jumping, visited_positions, board):
        return_list = []
        jump_move = (0,0)

        if(self.id == 1): 
            piece_jumping = board.pieces_p1[index_piece_jumping]
        else:
            piece_jumping = board.pieces_p2[index_piece_jumping]
               
        visited_positions.append(piece_jumping)

        # Se setea el valor de i
        if (piece_jumping[0] < piece_to_jump[0]):
            jump_move = (piece_jumping[0] + 2, piece_jumping[1])
        elif (piece_jumping[0] > piece_to_jump[0]):
            jump_move = (piece_jumping[0] - 2, piece_jumping[1])
        else:
            jump_move = (piece_jumping[0], piece_jumping[1])
            
        # Se setea el valor de j
        if (piece_jumping[1] < piece_to_jump[1]):
            jump_move = (jump_move[0], piece_jumping[1] + 2)
        elif (piece_jumping[1] > piece_to_jump[1]):
            jump_move = (jump_move[0], piece_jumping[1] - 2)
        else:
            jump_move = (jump_move[0], piece_jumping[1])

        if(jump_move[0] <= 0 or jump_move[0] >= 10 or
           jump_move[1] <= 0 or jump_move[1] >= 10 or
           (jump_move in board.pieces_p1) or
           (jump_move in board.pieces_p2) or
           (jump_move in visited_positions)):
            # No puede realizar el salto:
            #   - La ficha se fue de rango
            #   - Hay otra ficha en el lugar que va a saltar
            #   - La casilla ya fue visitada antes (previene loops infinitos)
            return []
        
        return_list.append((index_piece_jumping,jump_move))

        # Hace el movimiento en el tablero auxiliar
        previous_move = (0,0)
        if(self.id == 1):
            previous_move = board.pieces_p1[index_piece_jumping]
            board.pieces_p1[index_piece_jumping] = jump_move
        else:
            previous_move = board.pieces_p2[index_piece_jumping]
            board.pieces_p2[index_piece_jumping] = jump_move

        for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
            next_move = (jump_move[0] + i,jump_move[1] + j)
                
            if (next_move != piece_to_jump and 
               (next_move in board.pieces_p1 or next_move in board.pieces_p2)):
                # Puede dar un salto.
                aux_list = self.do_jump(next_move, index_piece_jumping, visited_positions, board)
                return_list = return_list + aux_list
        
        # Revierte los movimientos en el tablero auxiliar
        if(self.id == 1):
            board.pieces_p1[index_piece_jumping] = previous_move
        else:
            board.pieces_p2[index_piece_jumping] = previous_move

        return return_list

    #--------------------------------------------------------------------------------------------

    # Devuelve un movimiento al azar, elegido de la lista de todos los movimientos posibles
    # que tiene para realizar actualmente
    def do_move(self, board):
        
        _board = board
    
        if(self.id == 1): 
            pieces = board.pieces_p1
        else:
            pieces = board.pieces_p2
        
        list_available_moves = []

        # La lista list_available_moves la genera agregando todos los movimientos adyacentes y los saltos
        # de cada ficha.
        for index in range(10):
            for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
                
                next_move = (pieces[index][0] + i, pieces[index][1] + j) # Movimiento a realizar inmediatamente
                
                if (next_move[0] > 0 and next_move[0] <= 9 and next_move[1] > 0 and next_move[1] <= 9):
                    if next_move in _board.pieces_p1 or next_move in _board.pieces_p2:
                        aux_list = []
                        list_available_moves_jump = self.do_jump(next_move, index, aux_list, _board)
                        list_available_moves = list_available_moves + list_available_moves_jump
                    else:
                        list_available_moves.append((index,next_move))
        
        result = random.choice(list_available_moves)

        return result

    #--------------------------------------------------------------------------------------------
    
    def recalc_weights(self, board):
        pass

    def set_actual_value_board(self, board):
        pass