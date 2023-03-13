from Analysis.Results import Version1 as v1
from Analysis.Results import Version2 as v2
from Analysis.Results import Version3 as v3
import matplotlib.pyplot as plt

def prepare_plots():
    plt.rc('font', size=16)
    plt.rc('axes', titlesize=22)
    plt.rc('axes', labelsize=16)
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=16)
    plt.rc('figure', titlesize=30)

def plot_v1():
    x, y = v1.prepare_for_plotting()
    plt.plot(x, y, 'b', linewidth=2)
    plt.plot(x, y, 'bx', markersize=12)
    plt.title('Evaluation of agent version 1')
    plt.show()

def plot_v2():
    x, y = v2.prepare_for_plotting()
    plt.plot(x, y, 'b', linewidth=2)
    plt.plot(x, y, 'bx', markersize=12)
    plt.xticks(x)
    plt.xlabel("Training's iteration")
    plt.ylabel("Evaluation")
    plt.title('Evaluation of agent version 2')
    plt.show()

def plot_v12():
    x1, y1 = v1.prepare_for_plotting()
    x2, y2 = v2.prepare_for_plotting()
    plt.plot(x1, y1, 'b', linewidth=2, label='Version 1')
    plt.plot(x1, y1, 'bx', markersize=12)
    plt.plot(x2, y2, 'g', linewidth=2, label='Version 2')
    plt.plot(x2, y2, 'gx', markersize=12)
    plt.xticks(x1)
    plt.xlabel("Training's iteration")
    plt.ylabel("Evaluation")
    plt.title('Comparison of agent version 1 and 2')
    plt.legend()
    plt.show()

def plot_v3():
    x, y = v3.prepare_for_plotting()
    plt.plot(x, y, 'b', linewidth=2)
    plt.plot(x, y, 'bx', markersize=12)
    plt.xticks(x)
    plt.xlabel("Training's iteration")
    plt.ylabel("Evaluation")
    plt.title('Evaluation of agent version 3')
    plt.show()

def plot_v123():
    #x1, y1 = v1.prepare_for_plotting()
    x2, y2 = v2.prepare_for_plotting()
    x3, y3 = v3.prepare_for_plotting()
    #plt.plot(x1, y1, 'b', linewidth=2, label='Version 1')
    #plt.plot(x1, y1, 'bx', markersize=12)
    plt.plot(x2, y2, 'g', linewidth=2, label='Version 2')
    plt.plot(x2, y2, 'gx', markersize=12)
    plt.plot(x3, y3, 'orange', linewidth=2, label='Version 3')
    plt.plot(x3, y3, 'x', color='orange', markersize=12)
    plt.xticks(x2)
    plt.xlabel("Training's iteration")
    plt.ylabel("Evaluation")
    plt.title('Comparison of agent version 1, 2 and 3')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    prepare_plots()
    plot_v123()