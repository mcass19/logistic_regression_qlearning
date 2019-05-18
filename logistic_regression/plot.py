from matplotlib import pyplot as plt

class DataSet(object):
    
    def __init__(self):
        pass

    def plot_pca(self, instances_transformed, cant_votes_per_party):
        plt.figure(figsize=(20,20))

        colors_index = 0
        colors = ['#F5340A', '#F5B10A', '#A0F50A', '#0AF5D9', '#0A3FF5', '#7C0AF5', '#CA0AF5', '#E70AF5', '#000000', '#838383', '#FFAD7B']
        
        j = 0
        for i in cant_votes_per_party:
            plt.plot(instances_transformed[0, j:(j + i)], instances_transformed[1, j:(j + i)], 'o', markersize=7, color=colors[colors_index], alpha=0.2)
            j = j + i
            colors_index += 1
        
        plt.title('Instancias transformadas (colores por partido)')
        plt.show()