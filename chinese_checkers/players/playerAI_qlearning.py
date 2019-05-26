import tensorflow as tf

import numpy as np

from chinese_checkers.board import Board
from chinese_checkers.players.player import Player

class PlayerAIQLearning(Player):

    def __init__(self, id, learning_rate):
        super().__init__(id)

        self.coefficients = [0, 0, 0, 0, 0, 0]
        self.q_reward_movements = []
        self.y = .99

        # RED NEURONAL
        self.inputs = tf.placeholder(shape=[6], dtype=tf.float32)
        self.fetches = self.inputs

        self.nextQ = tf.placeholder(shape=[6], dtype=tf.float32)
        self.outQ = tf.placeholder(shape=[6], dtype=tf.float32)
        self.weights = tf.Variable(tf.ones([6], dtype=tf.dtypes.float32))

        self.loss = -(tf.log(self.nextQ) * self.weights)
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(self.loss)

        self.sess = tf.Session()
        init = tf.global_variables_initializer()
        self.sess.run(init)
        
    #--------------------------------------------------------------------------------------------
    
    # Devuelve la posicion donde el valor del tablero es mayor en la serie de saltos
    # hechos por las ficha index_piece_jumping, y ese resultado maximo.            
    # Si el salto no se puede hacer devuelve -1 en el numero del resultado maximo.
    def do_jump(self, piece_to_jump, index_piece_jumping, visited_positions, board): 
        jump_move = (0,0) # Coordenadas de la casilla diametralmente opuesta a la ficha a saltar
        max_value = 0

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
            return -1
        
        # Hace el movimiento en el tablero auxiliar
        previous_move = (0,0)
        if(self.id == 1):
            previous_move = board.pieces_p1[index_piece_jumping]
            board.pieces_p1[index_piece_jumping] = jump_move
        else:
            previous_move = board.pieces_p2[index_piece_jumping]
            board.pieces_p2[index_piece_jumping] = jump_move
        
        # Se halla el Q para el movimiento que se hizo
        q_value, reward = self.q_and_reward_value(board)
        # se agrega a la lista de (q, recompensa, (piece_to_move, position_to_move))
        item = (q_value, reward, (index_piece_jumping, jump_move))
        self.q_reward_movements.append(item)
        
        # Explora las seis posiciones a las que puede seguir saltando
        for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
            next_move = (jump_move[0] + i,jump_move[1] + j) # Movimiento a realizar inmediatamente
                
            if (next_move != piece_to_jump and 
               (next_move in board.pieces_p1 or next_move in board.pieces_p2)):
                # Puede dar un salto.
                max_value = self.do_jump(next_move, index_piece_jumping, visited_positions, board)
        
        # Revierte el movimiento en el tablero auxiliar
        if(self.id == 1):
            board.pieces_p1[index_piece_jumping] = previous_move
        else:
            board.pieces_p2[index_piece_jumping] = previous_move
        
        return max_value
        
    #--------------------------------------------------------------------------------------------

    # Devuelve el numero de ficha y posicion a mover, para realizar el mejor movimiento
    def do_move(self, board):
      
        _board = board
    
        if(self.id == 1): 
            pieces = board.pieces_p1
        else:
            pieces = board.pieces_p2
            
        max_value = float('-inf')
        position_to_move = (0,0) 
        piece_to_move = 0
        can_move = False
        
        for index in range(10):
            for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
                next_move = (pieces[index][0] + i, pieces[index][1] + j) # Movimiento a realizar inmediatamente
                next_value = 0                                           # Valor del tablero despues de hacer el movimiento
                
                if (next_move[0] > 0 and next_move[0] <= 9 and next_move[1] > 0 and next_move[1] <= 9):
                    # El movimiento no se va del tablero
                    if next_move in _board.pieces_p1 or next_move in _board.pieces_p2:
                        # Puede dar un salto. Llama a do_jump que es recursiva
                        aux_list = []
                        next_value = self.do_jump(next_move, index, aux_list, _board)
                        if next_value != -1:
                            can_move = True
                    else:
                        # Puede moverse a un espacio adyacente.
                        can_move = True

                        # Hace el movimiento en el tablero auxiliar
                        previous_move = (0,0)
                        if(self.id == 1):
                            previous_move = _board.pieces_p1[index]
                            _board.pieces_p1[index] = next_move
                        else:
                            previous_move = _board.pieces_p2[index]
                            _board.pieces_p2[index] = next_move
                        
                        # Se halla el Q para el movimiento que se hizo
                        q_value, reward = self.q_and_reward_value(board)
                        # se agrega a la lista de (q, recompensa, (piece_to_move, position_to_move))
                        item = (q_value, reward, (index, next_move))
                        self.q_reward_movements.append(item)
                        
                        # Revierte el movimiento en el tablero auxiliar
                        if(self.id == 1):
                            _board.pieces_p1[index] = previous_move
                        else:
                            _board.pieces_p2[index] = previous_move

        # Se halla el máximo Q, se entrena la red y se devuelve la ficha y la posición para realizar el movimiento       
        piece_to_move, position_to_move = self.train_network(board)
        
        if can_move:
            return piece_to_move, position_to_move
        else:
            # No hay movimiento posible
            pass
    #--------------------------------------------------------------------------------------------

    # Devuelve el complemento de la distancia promedio de las diez fichas a la posicion 
    # de la punta en la base enemiga
    def distance_average(self, pieces, target) -> float:
        count = 0

        for i in range(10):
            aux_1 = abs(target[0] - pieces[i][0]) 
            aux_2 = abs(target[1] - pieces[i][1])
            aux = aux_1 + aux_2
            count += aux

        count = count / 10  # Promedio real
        # Normaliza y devuelve el complemento
        count = count * 0.01
        return (1 - count)

    #--------------------------------------------------------------------------------------------

    # Devuelve el complemento del promedio de las distancias a la posicion libre mas cerca en 
    # la base enemiga de todas las fichas afuera de la base enemiga    
    def distance_average_not_in_base(self, pieces, target) -> float:
        cant_pieces = 1
        count = 0
        target_list = []

        for i in range(10):
            if not (target[i] in pieces):
                target_list.append(target[i])

        for i in range(10):
            if not (pieces[i] in target): 
            # La ficha no esta en el target, por lo que no esta en la base enemiga
                cant_pieces += 1 # Cantidad de fichas fuera de la base enemiga
                aux = 0
                distance_min = float('+inf')
                
                # Para cada posicion libre de la base enemiga calcula la distancia de la ficha
                # y se queda con la minima
                for target_index in target_list:
                    aux_1 = abs(target_index[0] - pieces[i][0]) 
                    aux_2 = abs(target_index[1] - pieces[i][1])
                    aux = aux_1 + aux_2
                    if (aux < distance_min):
                        distance_min = aux
                
                count += distance_min

        count = count / cant_pieces   # Promedio real
        # Normaliza y devuelve el complemento
        count = count * 0.01
        return (1 - count)

    #--------------------------------------------------------------------------------------------

    # Cantidad normalizada de fichas del jugador en la base enemiga
    def in_opponent_base(self, pieces, target) -> float:
        count = 0
        for i in range(10):
            if pieces[i] in target:
                count += 1
        return (count / 10)

    #--------------------------------------------------------------------------------------------
    
    # Devuelve el valor q de una acción o movimiento dado
    def q_and_reward_value(self, board) -> float:

        reward = 0
        end, winner = board.end_of_game()
        if end:
            if winner == self.id:
                reward = 1
            else:
                reward = -1

        if self.id == 1:
            self.coefficients[0] = self.distance_average(board.pieces_p1, board.target_p1[0])
            self.coefficients[1] = self.distance_average(board.pieces_p2, board.target_p2[0])
            self.coefficients[2] = self.in_opponent_base(board.pieces_p1, board.target_p1)
            self.coefficients[3] = self.in_opponent_base(board.pieces_p2, board.target_p2)
            self.coefficients[4] = self.distance_average_not_in_base(board.pieces_p1, board.target_p1)
            self.coefficients[5] = self.distance_average_not_in_base(board.pieces_p2, board.target_p2)
        else:
            self.coefficients[0] = self.distance_average(board.pieces_p2, board.target_p2[0])
            self.coefficients[1] = self.distance_average(board.pieces_p1, board.target_p1[0])
            self.coefficients[2] = self.in_opponent_base(board.pieces_p2, board.target_p2)
            self.coefficients[3] = self.in_opponent_base(board.pieces_p1, board.target_p1)
            self.coefficients[4] = self.distance_average_not_in_base(board.pieces_p2, board.target_p2)
            self.coefficients[5] = self.distance_average_not_in_base(board.pieces_p1, board.target_p1)

        q = self.sess.run(self.fetches, feed_dict={self.inputs:self.coefficients})
        
        return q, reward

    #--------------------------------------------------------------------------------------------

    # Se entrena la red con el q del mejor movimiento del turno, y se devuelve dicha ficha junto a su movimiento
    def train_network(self, board):
        q_max = 0
        for item in self.q_reward_movements:
            if np.mean(item[0]) > np.mean(q_max):
                q_max = item[0]
                reward = item[1]
                piece_to_move = item[2][0]
                position_to_move = item[2][1]

        # se simula movimiento
        _board = board
        if(self.id == 1):
            _board.pieces_p1[piece_to_move] = position_to_move
        else:
            _board.pieces_p2[piece_to_move] = position_to_move
        self.outQ, _ = self.q_and_reward_value(_board)

        # se halla Q
        targetQ = reward + (self.y * q_max)

        # entrenamiento
        _ = self.sess.run([self.weights, self.optimizer], feed_dict={self.inputs:self.coefficients, self.nextQ:targetQ})

        return piece_to_move, position_to_move

    #--------------------------------------------------------------------------------------------
    # Definición de procedimientos para ser robusto con lo ya implementado

    def recalc_weights(self, board):
        pass

    def set_actual_value_board(self, board):
        pass
    
    def set_prev_value_board(self, board):
        pass
