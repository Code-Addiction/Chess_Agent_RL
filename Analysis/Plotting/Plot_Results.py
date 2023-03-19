from Analysis.Results import Version1 as v1
from Analysis.Results import Version2 as v2
from Analysis.Results import Version3 as v3
from Analysis.Results import Version4 as v4
from Analysis.Results import Version5 as v5
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
    plt.xticks(x)
    plt.xlabel("Training iteration")
    plt.ylabel("Evaluation")
    plt.title('Evaluation of agent version 1')
    plt.show()

def plot_v2():
    x, y = v2.prepare_for_plotting()
    plt.plot(x, y, 'b', linewidth=2)
    plt.plot(x, y, 'bx', markersize=12)
    plt.xticks(x)
    plt.xlabel("Training iteration")
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
    plt.xlabel("Training iteration")
    plt.ylabel("Evaluation")
    plt.title('Comparison of agent version 1 and 2')
    plt.legend()
    plt.show()

def plot_v3():
    x, y = v3.prepare_for_plotting()
    plt.plot(x, y, 'b', linewidth=2)
    plt.plot(x, y, 'bx', markersize=12)
    plt.xticks(x)
    plt.xlabel("Training iteration")
    plt.ylabel("Evaluation")
    plt.title('Evaluation of agent version 3')
    plt.show()

def plot_v123():
    x1, y1 = v1.prepare_for_plotting()
    x2, y2 = v2.prepare_for_plotting()
    x3, y3 = v3.prepare_for_plotting()
    plt.plot(x1, y1, 'b', linewidth=2, label='Version 1')
    plt.plot(x1, y1, 'bx', markersize=12)
    plt.plot(x2, y2, 'g', linewidth=2, label='Version 2')
    plt.plot(x2, y2, 'gx', markersize=12)
    plt.plot(x3, y3, 'orange', linewidth=2, label='Version 3')
    plt.plot(x3, y3, 'x', color='orange', markersize=12)
    plt.xticks(x1)
    plt.xlabel("Training iteration")
    plt.ylabel("Evaluation")
    plt.title('Comparison of agent version 1, 2 and 3')
    plt.legend()
    plt.show()

def plot_v4():
    x, y = v4.prepare_for_plotting()
    plt.plot(x, y, 'b', linewidth=2)
    plt.plot(x, y, 'bx', markersize=12)
    plt.xticks(x)
    plt.xlabel("Training iteration")
    plt.ylabel("Evaluation")
    plt.title('Evaluation of agent version 4')
    plt.show()

def plot_v1234():
    x1, y1 = v1.prepare_for_plotting()
    x2, y2 = v2.prepare_for_plotting()
    x3, y3 = v3.prepare_for_plotting()
    x4, y4 = v4.prepare_for_plotting()
    plt.plot(x1, y1, 'b', linewidth=2, label='Version 1')
    plt.plot(x1, y1, 'bx', markersize=12)
    plt.plot(x2, y2, 'g', linewidth=2, label='Version 2')
    plt.plot(x2, y2, 'gx', markersize=12)
    plt.plot(x3, y3, 'orange', linewidth=2, label='Version 3')
    plt.plot(x3, y3, 'x', color='orange', markersize=12)
    plt.plot(x4, y4, 'r', linewidth=2, label='Version 4')
    plt.plot(x4, y4, 'rx', markersize=12)
    plt.xticks(x1)
    plt.xlabel("Training iteration")
    plt.ylabel("Evaluation")
    plt.title('Comparison of agent version 1, 2, 3 and 4')
    plt.legend()
    plt.show()

def plot_v5():
    x, y = v5.prepare_for_plotting()
    plt.plot(x, y, 'b', linewidth=2)
    plt.plot(x, y, 'bx', markersize=12)
    plt.xticks(x)
    plt.xlabel("Training iteration")
    plt.ylabel("Evaluation")
    plt.title('Evaluation of agent version 5')
    plt.show()

def plot_v12345():
    x1, y1 = v1.prepare_for_plotting()
    x2, y2 = v2.prepare_for_plotting()
    x3, y3 = v3.prepare_for_plotting()
    x4, y4 = v4.prepare_for_plotting()
    x5, y5 = v5.prepare_for_plotting()
    plt.plot(x1, y1, 'b', linewidth=2, label='Version 1')
    plt.plot(x1, y1, 'bx', markersize=12)
    plt.plot(x2, y2, 'g', linewidth=2, label='Version 2')
    plt.plot(x2, y2, 'gx', markersize=12)
    plt.plot(x3, y3, 'orange', linewidth=2, label='Version 3')
    plt.plot(x3, y3, 'x', color='orange', markersize=12)
    plt.plot(x4, y4, 'r', linewidth=2, label='Version 4')
    plt.plot(x4, y4, 'rx', markersize=12)
    plt.plot(x5, y5, 'y', linewidth=2, label='Version 5')
    plt.plot(x5, y5, 'yx', markersize=12)
    plt.xticks(x1)
    plt.xlabel("Training iteration")
    plt.ylabel("Evaluation")
    plt.title('Comparison of agent version 1, 2, 3, 4 and 5')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    prepare_plots()
    plot_v5()