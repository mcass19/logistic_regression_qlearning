from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.decomposition import PCA

import numpy as np

class LogisticRegressionClassifiers(object):
    
    def __init__(self):
        pass

    def by_party(self, data_set, labels, cant_votes_per_party):
        # split del data_set en datos y etiquetas, 80% para entrenar y 20% para clasificar
        data_train, data_test, labels_train, labels_test = train_test_split(data_set, labels, test_size=0.2)
        # self.compare(data_train, labels_train, data_test, labels_test)

        print('\n')

        for i in range(2, 26):
            pca = PCA(n_components=i)
            aux = pca.fit_transform(data_train)

            print('N=' + str(i))
            self.compare(aux, labels_train, data_test, labels_test)

    def compare(self, data_train, labels_train, data_test, labels_test):
        # self.cross_validation_different_penalties(data_train, labels.astype('int'), 'sag', None)
        self.cross_validation_different_penalties(data_train, labels_train.astype('int'), 'sag', 'l2', data_test, labels_test.astype('int'))
        # self.cross_validation_different_penalties(data_train, labels.astype('int'), 'lbfgs', None)
        self.cross_validation_different_penalties(data_train, labels_train.astype('int'), 'lbfgs', 'l2', data_test, labels_test.astype('int'))
        # self.cross_validation_different_penalties(data_train, labels.astype('int'), 'newton-cg', None)
        self.cross_validation_different_penalties(data_train, labels_train.astype('int'), 'newton-cg', 'l2', data_test, labels_test.astype('int'))
        # self.cross_validation_different_penalties(data_train, labels.astype('int'), 'saga', None)
        self.cross_validation_different_penalties(data_train, labels_train.astype('int'), 'saga', 'l1', data_test, labels_test.astype('int'))
        self.cross_validation_different_penalties(data_train, labels_train.astype('int'), 'saga', 'l2', data_test, labels_test.astype('int'))
        # self.cross_validation_different_penalties(data_train, labels.astype('int'), 'saga', 'elasticnet')

    def cross_validation_different_penalties(self, data, labels, solver, penalty, data_test, labels_test):
        logisticRegr = LogisticRegression(solver=solver, penalty=penalty, multi_class='multinomial', max_iter=24681)
        logisticRegr.fit(data, labels)
        print('Solver=' + str(solver) + ' - Penalty=' + str(penalty))
        # score = logisticRegr.score(data_test, labels_test)
        # print('Accuracy del set de datos evaluados: ' + str(score))
        cross_val = cross_val_score(logisticRegr, data, labels, cv=3)
        print('Accuracy de validación cruzada: ' + str(cross_val))

    def by_candidate(self):
        pass