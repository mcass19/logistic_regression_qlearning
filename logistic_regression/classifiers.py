import warnings
warnings.filterwarnings('ignore')

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.decomposition import PCA
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, accuracy_score

import numpy as np

class LogisticRegressionClassifiers(object):
    
    def __init__(self, k):
        # estructura para 
        self.data_train = []
        self.data_test = []
        self.labels_train = []
        self.labels_test = []
        self.labels = []

        # k-folds
        self.k = k
        
        # clasificador y sus respectivas metricas
        self.best_accuracy = np.zeros(1)
        self.classifier = None
        self.predictions = np.zeros(1)
        self.cross_val = 0
        self.score = 0
        self.precision = 0
        self.recall = 0
        self.f_score = 0
        self.conf_matrix = 0
        
        # clasificador reducido en best_n dimensiones con pca y sus respectivas metricas
        self.best_accuracy_pca = np.zeros(1)
        self.best_n = 0
        self.classifier_pca = None
        self.predictions_pca = np.zeros(1)
        self.cross_val_pca = 0
        self.score_pca = 0
        self.precision_pca = 0
        self.recall_pca = 0
        self.f_score_pca = 0
        self.conf_matrix_pca = 0

    def classify(self, data_set, votes, labels):
        self.labels = labels

        # ejercicio 4 parte b
        # split del data_set en datos y etiquetas, 80% para entrenar y 20% para predecir
        self.data_train, self.data_test, self.labels_train, self.labels_test = train_test_split(data_set, votes, test_size=0.2)
    
        # ejercico 4 parte c 
        # validaciones cruzadas
        self.cross_validation_different_penalties(self.data_train, self.data_test)

        # ejercicio 4 parte d
        # se aplica pca para todos los n posibles y luego nuevamente validacion cruzada 
        # para los datasets resultantes
        print('--------- PCA ---------')
        for i in range(1, 27):
            pca = PCA(n_components=i)
            reduced_data_set = pca.fit_transform(self.data_train)
            reduced_data_set_test = pca.fit_transform(self.data_test)
            print('N=' + str(i))
            self.cross_validation_different_penalties(reduced_data_set, reduced_data_set_test, True, i)

    # validacion cruzada con diferentes métodos de penalización
    def cross_validation_different_penalties(self, data_train, data_test, with_pca = False, n = 0):
        self.cross_validation_and_metrics(data_train, data_test, 'sag', 'l2', with_pca, n)
        self.cross_validation_and_metrics(data_train, data_test, 'lbfgs', 'l2', with_pca, n)
        self.cross_validation_and_metrics(data_train, data_test, 'newton-cg', 'l2', with_pca, n)
        self.cross_validation_and_metrics(data_train, data_test, 'saga', 'l1', with_pca, n)
        self.cross_validation_and_metrics(data_train, data_test, 'saga', 'l2', with_pca, n)

    # se crea la instancia de regresión logística con los parámetros pasados y se imprimen los mismos,
    # calculando accuracy para cada caso
    def cross_validation_and_metrics(self, data, data_test, solver, penalty, with_pca, n):
        logisticRegr = LogisticRegression(solver=solver, penalty=penalty, multi_class='multinomial', max_iter=24681)
        logisticRegr.fit(data, self.labels_train.astype('int'))
        print('Clasificador basado en regresión logística con solver=' + str(solver) + ' y penalty=' + str(penalty))
        cross_val = cross_val_score(logisticRegr, data, self.labels_train.astype('int'), cv=self.k)
        print('Accuracy de validación cruzada: ' + str(cross_val))

        # ejercicio 4 parte e
        # se calcula accuracy, precision, recall, medida f y matriz de confusion
        score = logisticRegr.score(data_test, self.labels_test.astype('int'))
        print('Accuracy del clasificador: ' + str(score))

        predictions = logisticRegr.predict(data_test)

        precision = precision_score(predictions.astype('int'), self.labels_test.astype('int'), average='macro', labels=self.labels)
        print('Precisión del clasificador: ' + str(precision))

        recall = recall_score(predictions.astype('int'), self.labels_test.astype('int'), average='macro', labels=self.labels)
        print('Recall del clasificador: ' + str(recall))

        f_score = f1_score(predictions.astype('int'), self.labels_test.astype('int'), average='macro', labels=self.labels)
        print('Medida-f del clasificador: ' + str(f_score))

        conf_matrix = confusion_matrix(predictions.astype('int'), self.labels_test.astype('int'), labels=self.labels)
        print('Matriz de confusión del clasificador: \n' + str(conf_matrix), '\n')

        # se guardan los mejores clasificadores (con y sin pca)
        if (not with_pca) and (np.mean(cross_val) > np.mean(self.best_accuracy)):
            self.best_accuracy = cross_val
            self.classifier = logisticRegr
            self.predictions = predictions
            self.cross_val = cross_val
            self.score = score
            self.precision = precision
            self.recall = recall
            self.f_score = f_score
            self.conf_matrix = conf_matrix
        elif (with_pca) and (np.mean(cross_val) > np.mean(self.best_accuracy_pca)):
            self.best_accuracy_pca = cross_val
            self.best_n = n
            self.classifier_pca = logisticRegr
            self.predictions_pca = predictions
            self.cross_val_pca = cross_val
            self.score_pca = score
            self.precision_pca = precision
            self.recall_pca = recall
            self.f_score_pca = f_score
            self.conf_matrix_pca = conf_matrix

    # reimpresion de metricas para los mejores clasificadores
    def reprint_metrics(self):
        print('El mejor clasificador es: ' + str(self.classifier))
        print('Accuracy del clasificador: ' + str(self.score))
        print('Precisión del clasificador: ' + str(self.precision))
        print('Recall del clasificador: ' + str(self.recall))
        print('Medida-f del clasificador: ' + str(self.f_score))
        print('Matriz de confusión del clasificador: \n' + str(self.conf_matrix), '\n')

        print('El mejor n es: ' + str(self.best_n))
        print('Accuracy del clasificador reducido en ' + str(self.best_n) + ' dimension(es) con pca: ' + str(self.score_pca))
        print('Precisión del clasificador reducido en ' + str(self.best_n) + ' dimension(es) con pca: ' + str(self.precision_pca))
        print('Recall del clasificador reducido en ' + str(self.best_n) + ' dimension(es) con pca: ' + str(self.recall_pca))
        print('Medida-f del clasificador reducido en ' + str(self.best_n) + ' dimension(es) con pca: ' + str(self.f_score_pca))
        print('Matriz de confusión del clasificador reducido en ' + str(self.best_n) + ' dimension(es) con pca: \n' + str(self.conf_matrix_pca), '\n')

    # ejercicio 4 parte f
    # se mapean los candidatos predecidos a sus respectivos partidos, se aplica pca y se realiza validacion 
    # cruzada con el mejor clasificador de candidatos, se halla el mejor n, y finalmente se comparan las 
    # predicciones (mapeadas vs. predecidas por el clasificador)
    def party_by_candidate_classifier(self, data_set, votes):
        _party_by_candidate = self.predictions.astype('int')
        _party_by_candidate = np.where(_party_by_candidate == 0, 0, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 1, 0, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 2, 4, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 3, 2, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 4, 3, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 5, 3, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 6, 2, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 7, 3, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 8, 0, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 9, 0, _party_by_candidate)
        _party_by_candidate = np.where(_party_by_candidate == 10, 1, _party_by_candidate)
        print('Partidos asociados a los candidatos que nuestro clasificador predijo: ' + str(_party_by_candidate), '\n')

        # split del data set segun partidos
        data_train, data_test, labels_train, labels_test = train_test_split(data_set, votes, test_size=0.2)
        
        best_accuracy = np.zeros(1)
        best_n = 0
        print('--------- PCA ---------')
        for i in range(1, 27):
            pca = PCA(n_components=i)
            reduced_data_set = pca.fit_transform(data_train)
            print('N=' + str(i))

            self.classifier.fit(reduced_data_set, labels_train.astype('int'))
            cross_val = cross_val_score(self.classifier, reduced_data_set, labels_train.astype('int'), cv=self.k)
            print('Accuracy de validación cruzada: ' + str(cross_val))

            if np.mean(cross_val) > np.mean(best_accuracy):
                best_accuracy = cross_val
                best_n = i

        print('\n')
        print('El mejor n es: ' + str(best_n))

        predictions = self.classifier.predict(data_test)
        accuracy = accuracy_score(_party_by_candidate, predictions)
        print('Accuracy entre partidos asociados a los candidatos predecidos, y partidos predecidos \ncon el clasificador de candidatos: ' + str(accuracy))
