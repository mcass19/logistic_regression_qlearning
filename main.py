from logistic_regression.data_set import DataSet
from logistic_regression.classifiers import LogisticRegressionClassifiers

import random
from chinese_checkers.board import Board
from chinese_checkers.game import Game
from chinese_checkers.players.playerAI import PlayerAI
from chinese_checkers.players.playerAI_qlearning import PlayerAIQLearning
from chinese_checkers.players.playerRandom import PlayerRandom

print('*****************************************')
print('REGRESION LOGISTICA Y Q-LEARNING')
print('*****************************************')

option_algorithm = int(input('Ingrese 1 si desea ejecutar los clasificadores basados en regresión logística, \no 2 si desea ejecutar el nuevo jugador de damas chinas implementado con q-learning: '))
print('\n')

if option_algorithm == 1:
    option_classifier = int(input('Ingrese 1 si desea construir un clasificador para predecir los partidos políticos, \no 2 si desea construir un clasificador para predecir los candidatos: '))
    print('\n')

    k = int(input('Ingrese la cantidad de pliegues que desea utilizar para realizar validación cruzada (k-folds): '))
    print('\n')

    classifier = LogisticRegressionClassifiers(k)

    if option_classifier == 1:
        # manejo de los datos
        data_set = DataSet()
        data_prepared = data_set.prepare_data()
        data_set.load_data_set(data_prepared)

        classifier.classify(data_set.data, data_set.votes_per_party, data_set.labels_parties)
        print('************************************************************************************************************************', '\n')
        classifier.reprint_data()
    elif option_classifier == 2:
        # manejo de los datos
        data_set = DataSet()
        data_prepared = data_set.prepare_data()
        data_set.load_data_set(data_prepared, False)

        classifier.classify(data_set.data, data_set.votes_per_candidate, data_set.labels_candidates)
        print('************************************************************************************************************************', '\n')
        classifier.reprint_data()

        option_party = int(input('Ingrese 1 si desea predecir los partidos políticos con este clasificador, u otro número si no: '))
        if (option_party == 1):
            classifier.party_by_candidate(data_set.data, data_set.votes_per_party, data_set.labels_parties)
elif option_algorithm == 2:
    wons_p1 = 0     # Partidas ganados jugador 1
    wons_p2 = 0     # Partidas ganados jugador 2
    draws = 0       # Empates
    cant_init_1 = 0 # Partidas iniciadas jugador 1 
    cant_init_2 = 0 # Partidas iniciadas jugador 2

    for i in range(100):
        # Crea el tablero
        board = Board(9, 9)

        # Crea los jugadores
        # PlayerAI recibe: Numero de jugador, Tasa de aprendizaje, Aprendizaje activado/desactivado
        # PlayerRandom solo recibe el numero de jugador  
        p1 = PlayerAI(1, 0.001, False)
        # p2 = PlayerRandom(2) 
        p2 = PlayerAI(2, 0.001, True)

        game = Game(board)

        # Se elije al azar un jugador que inicia la partida
        if random.choice([True, False]):
            cant_init_1 += 1
            winner = game.play_game(p1, p2, 1)
            if winner == 1:
                wons_p1 += 1
            elif winner == 2:
                wons_p2 += 1
            else:
                draws += 1
        else:
            cant_init_2 += 1
            winner = game.play_game(p1, p2, 2)
            if winner == 1:
                wons_p1 += 1
            elif winner == 2:
                wons_p2 += 1
            else:
                draws += 1

        print('Partido {} finalizado'.format(i))

    print('Player 1 gano {} veces'.format(wons_p1))
    print('Player 2 gano {} veces'.format(wons_p2))
    print('Empataron {} veces'.format(draws))
    print('Empezo {} veces el jugador 1'.format(cant_init_1))
    print('Empezo {} veces el jugador 2'.format(cant_init_2))