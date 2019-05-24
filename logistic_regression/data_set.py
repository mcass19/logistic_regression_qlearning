import pandas as pd

import numpy as np

class DataSet(object):
    
    def __init__(self):
        self.data = []
        self.num_instances = 0
        self.votes_per_candidate = []
        self.labels_candidates = []
        self.votes_per_party = []
        self.labels_parties = []

    def load_data_set(self, data_set, candidates=True):    
        self.data = data_set
        self.num_instances = 32499

        # ejercico 4 parte a
        # eliminar partidos con menos de 1000 votantes
        self.data = self.data[self.data.party != 'PERI']
        self.data = self.data[self.data.party != 'Partido Digital']
        self.data = self.data[self.data.party != 'Partido Verde']
        self.data = self.data[self.data.party != 'Partido de Todos']
        self.data = self.data[self.data.party != 'Partido de los Trabajadores']
        self.data = self.data[self.data.party != 'Unidad Popular']
       
        if candidates:
            # ejercico 4 parte a
            # eliminar candidatos con menos de 1000 votantes
            self.data = self.data[self.data.name != 'Carlos Iafigliola']
            self.data = self.data[self.data.name != 'Edgardo Martínez']
            self.data = self.data[self.data.name != 'Enrique Antía']
            self.data = self.data[self.data.name != 'Héctor Rovira']
            self.data = self.data[self.data.name != 'José Amorín']
            self.data = self.data[self.data.name != 'Pedro Etchegaray']
            self.data = self.data[self.data.name != 'Verónica Alonso']

            # vector de largo cantidad de instancias, con índice de candidato al que votan
            self.votes_per_candidate = self.data['name']
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Carolina Cosse', 0, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Daniel Martínez', 1, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Edgardo Novick', 2, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Ernesto Talvi', 3, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Jorge Larrañaga', 4, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Juan Sartori', 5, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Julio María Sanguinetti', 6, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Luis Lacalle Pou', 7, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Mario Bergara', 8, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Oscar Andrade', 9, self.votes_per_candidate)
            self.votes_per_candidate = np.where(self.votes_per_candidate == 'Pablo Mieres', 10, self.votes_per_candidate)

            self.labels_candidates = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # vector de largo cantidad de instancias, con índice de partido político al que votan
        self.votes_per_party = self.data['party']
        self.votes_per_party = np.where(self.votes_per_party == 'Frente Amplio', 0, self.votes_per_party)
        self.votes_per_party = np.where(self.votes_per_party == 'La Alternativa', 1, self.votes_per_party)
        self.votes_per_party = np.where(self.votes_per_party == 'Partido Colorado', 2, self.votes_per_party)
        self.votes_per_party = np.where(self.votes_per_party == 'Partido Nacional', 3, self.votes_per_party)
        self.votes_per_party = np.where(self.votes_per_party == 'Partido de la Gente', 4, self.votes_per_party)

        self.labels_parties = [0, 1, 2, 3, 4]

        # se mantienen solo los atributos correspondientes a las respuestas
        del self.data['id']
        del self.data['candidatoId']
        del self.data['fecha']
        del self.data['name']
        del self.data['party']

    def prepare_data(self):
        # se importan los datos utilizando pandas
        data = pd.read_csv("logistic_regression/data.csv")

        # tabla de candidatos 
        candidates = pd.DataFrame(
        [
            [1,'Oscar Andrade', 'Frente Amplio'],
            [2,'Mario Bergara', 'Frente Amplio'],
            [3,'Carolina Cosse', 'Frente Amplio'],
            [4,'Daniel Martínez', 'Frente Amplio'],
            [5,'Verónica Alonso', 'Partido Nacional'],
            [6,'Enrique Antía', 'Partido Nacional'],
            [8,'Carlos Iafigliola', 'Partido Nacional'],
            [9,'Luis Lacalle Pou', 'Partido Nacional'],
            [10,'Jorge Larrañaga', 'Partido Nacional'],
            [11,'Juan Sartori', 'Partido Nacional'],
            [12,'José Amorín', 'Partido Colorado'],
            [13,'Pedro Etchegaray', 'Partido Colorado'],
            [14,'Edgardo Martínez', 'Partido Colorado'],
            [15,'Héctor Rovira', 'Partido Colorado'],
            [16,'Julio María Sanguinetti', 'Partido Colorado'],
            [17,'Ernesto Talvi', 'Partido Colorado'],
            [18,'Pablo Mieres', 'La Alternativa'],
            [19,'Gonzalo Abella', 'Unidad Popular'],        
            [20,'Edgardo Novick', 'Partido de la Gente'],
            [21,'Cèsar Vega', 'PERI'],
            [22,'Rafael Fernández', 'Partido de los Trabajadores'],
            [23,'Justin Graside', 'Partido Digital'],        
            [24,'Gustavo Salle', 'Partido Verde'],
            [25,'Carlos Techera', 'Partido de Todos']
        ],
        columns=['candidatoId','name','party'],
        )

        data = data.merge(candidates, on=['candidatoId'])

        # se ordenan los datos por partido y luego por candidato
        data = data.sort_values(by=['party', 'name'])

        return data
