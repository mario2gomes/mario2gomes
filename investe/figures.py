import matplotlib.pyplot as plt

def minha_figura():
    fig, ax = plt.subplots()
    ax.plot(['janeiro', 'fevereiro', 'março'], [30, 20, 50])
    return fig