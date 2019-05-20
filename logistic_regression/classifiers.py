from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.decomposition import PCA

class LogisticRegressionClassifiers(object):
    
    def __init__(self):
        self.data_train = []
        self.data_test = []
        self.labels_train = []
        self.labels_test = []

    def classify(self, data_set, labels):
        # ejercicio 4 parte b
        # split del data_set en datos y etiquetas, 80% para entrenar y 20% para clasificar
        self.data_train, self.data_test, self.labels_train, self.labels_test = train_test_split(data_set, labels, test_size=0.2)
    
        # ejercico 4 parte c 
        # validaciones cruzadas
        self.cross_validation_different_penalties(self.data_train, self.data_test)
        print('\n')

        # ejercicio 4 parte d
        # se aplica pca para todos los n posibles y luego nuevamente validacion cruzada 
        # para los datasets resultantes
        print('----- PCA -----')
        for i in range(1, 27):
            pca = PCA(n_components=i)
            reduced_data_set = pca.fit_transform(self.data_train)
            reduced_data_set_test = pca.fit_transform(self.data_test)
            print('N=' + str(i))
            self.cross_validation_different_penalties(reduced_data_set, reduced_data_set_test)

    # validacion cruzada con diferentes métodos de penalización
    def cross_validation_different_penalties(self, data_train, data_test):
        self.cross_validation_and_metrics(data_train, data_test, 'sag', 'l2')
        self.cross_validation_and_metrics(data_train, data_test, 'lbfgs', 'l2')
        self.cross_validation_and_metrics(data_train, data_test, 'newton-cg', 'l2')
        self.cross_validation_and_metrics(data_train, data_test, 'saga', 'l1')
        self.cross_validation_and_metrics(data_train, data_test, 'saga', 'l2')

    # se crea la instancia de regresión logística con los parámetros pasados y se imprimen los mismos,
    # calculando accuracy para cada caso
    def cross_validation_and_metrics(self, data, data_test, solver, penalty):
        logisticRegr = LogisticRegression(solver=solver, penalty=penalty, multi_class='multinomial', max_iter=24681)
        logisticRegr.fit(data, self.labels_train.astype('int'))
        print('Solver=' + str(solver) + ' - Penalty=' + str(penalty))
        cross_val = cross_val_score(logisticRegr, data, self.labels_train.astype('int'), cv=3)
        print('Accuracy de validación cruzada: ' + str(cross_val))

        # ejercicio 4 parte e
        # se calcula accuracy, precision, recall, medida f y matriz de confusion
        score = logisticRegr.score(data_test, self.labels_test.astype('int'))
        print('Accuracy del set de datos a predecir: ' + str(score), '\n')

