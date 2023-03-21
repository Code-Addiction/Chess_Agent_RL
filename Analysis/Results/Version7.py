checkpoint100 = {'white': (26, 447, 27), 'black': (35, 422, 43)}
checkpoint200 = {'white': (33, 433, 34), 'black': (29, 435, 36)}
checkpoint300 = {'white': (38, 432, 30), 'black': (30, 432, 38)}
checkpoint400 = {'white': (41, 427, 32), 'black': (39, 421, 40)}
checkpoint500 = {'white': (31, 449, 20), 'black': (45, 431, 24)}
checkpoint600 = {'white': (35, 441, 24), 'black': (37, 437, 26)}
checkpoint700 = {'white': (50, 429, 21), 'black': (44, 428, 28)}
checkpoint800 = {'white': (44, 418, 38), 'black': (34, 437, 29)}
checkpoint900 = {'white': (52, 420, 28), 'black': (49, 410, 41)}
checkpoint1000 = {'white': (61, 411, 28), 'black': (50, 433, 17)}

all_results = [checkpoint100, checkpoint200, checkpoint300, checkpoint400, checkpoint500,
               checkpoint600, checkpoint700, checkpoint800, checkpoint900, checkpoint1000]

def calculate_evaluation_value() -> list:
    results = []
    for result in all_results:
        value = 0
        for color in ['white', 'black']:
            win, draw, loss = result[color]
            value += win - loss
        results.append(value)
    return results

def prepare_for_plotting() -> tuple[list, list]:
    return [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], calculate_evaluation_value()
