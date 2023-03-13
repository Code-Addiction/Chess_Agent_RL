checkpoint100 = {'white': (33, 445, 22), 'black': (22, 442, 36)}
checkpoint200 = {'white': (30, 443, 27), 'black': (38, 432, 30)}
checkpoint300 = {'white': (24, 448, 28), 'black': (32, 441, 27)}
checkpoint400 = {'white': (18, 441, 41), 'black': (33, 440, 27)}
checkpoint500 = {'white': (39, 433, 28), 'black': (35, 432, 33)}
checkpoint600 = {'white': (40, 430, 30), 'black': (38, 429, 33)}
checkpoint700 = {'white': (33, 445, 22), 'black': (38, 432, 30)}
checkpoint800 = {'white': (40, 441, 19), 'black': (38, 438, 24)}
checkpoint900 = {'white': (60, 417, 23), 'black': (62, 413, 25)}
checkpoint1000 = {'white': (50, 421, 29), 'black': (56, 420, 24)}

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
