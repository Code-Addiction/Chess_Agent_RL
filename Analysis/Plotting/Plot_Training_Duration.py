import matplotlib.pyplot as plt


labels = ['Version 1', 'Version 2', 'Version 3', 'Version 4', 'Version 5',
          'Version 6', 'Version 7', 'Version 8', 'Version 9', 'Version 10']
training_time_secs = [93264.61471366882, 101255.86065530777, 90129.44551753998, 53526.764860630035, 50251.625046014786,
                      56348.13920235634, 53003.84216237068, 50497.646312236786, 51604.49959921837, 53683.23340797424]


def prepare_plots():
    plt.rc('font', size=16)
    plt.rc('axes', titlesize=22)
    plt.rc('axes', labelsize=16)
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=16)
    plt.rc('figure', titlesize=30)

def plot_trainings_duration():
    training_time_hours = [round(x / 3600, 2) for x in training_time_secs]
    plt.bar_label(plt.bar(labels, training_time_hours))
    plt.title("Comparison of the training time")
    plt.ylabel("Training time in hours")
    plt.xlabel('Agents')
    plt.show()


if __name__ == '__main__':
    prepare_plots()
    plot_trainings_duration()
