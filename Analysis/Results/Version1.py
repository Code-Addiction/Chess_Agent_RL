checkpoint100 = {'white': (30, 429, 41), 'black': (40, 430, 30)}
checkpoint200 = {'white': (27, 438, 35), 'black': (27, 447, 26)}
checkpoint300 = {'white': (22, 447, 31), 'black': (31, 444, 25)}
checkpoint400 = {'white': (39, 431, 30), 'black': (37, 445, 18)}
checkpoint500 = {'white': (32, 436, 32), 'black': (34, 447, 19)}
checkpoint600 = {'white': (25, 441, 34), 'black': (26, 441, 33)}
checkpoint700 = {'white': (40, 437, 23), 'black': (31, 443, 26)}
checkpoint800 = {'white': (32, 448, 20), 'black': (36, 446, 18)}
checkpoint900 = {'white': (29, 440, 31), 'black': (32, 451, 17)}
checkpoint1000 = {'white': (41, 443, 16), 'black': (39, 434, 27)}

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
