import pandas as pd

import numpy as np

class DataSet(object):
    
    def __init__(self):
        self.data = []
        self.num_instances = 0
        self.cant_votes_per_party = []
        self.votes_per_party = []

    def load_data_set(self, data_set):    
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

        # arreglo con cantidad de votantes por partido
        cant_votes_aux = self.data['party'].value_counts().sort_index()
        for cva in cant_votes_aux.values:
            self.cant_votes_per_party.append(cva)

        # vector de largo cantidad de instancias, con índice de partido político al que votan
        self.votes_per_party = self.data['party']
        self.votes_per_party = np.where(self.votes_per_party == 'Frente Amplio', 0, self.votes_per_party)
        self.votes_per_party = np.where(self.votes_per_party == 'Partido Nacional', 1, self.votes_per_party)
        self.votes_per_party = np.where(self.votes_per_party == 'Partido Colorado', 2, self.votes_per_party)
        self.votes_per_party = np.where(self.votes_per_party == 'La Alternativa', 3, self.votes_per_party)
        self.votes_per_party = np.where(self.votes_per_party == 'Partido de la Gente', 4, self.votes_per_party)

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
