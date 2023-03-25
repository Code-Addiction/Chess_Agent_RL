checkpoint100 = {'white': (17, 444, 39), 'black': (24, 415, 61)}
checkpoint200 = {'white': (18, 451, 31), 'black': (31, 425, 44)}
checkpoint300 = {'white': (21, 441, 38), 'black': (26, 432, 42)}
checkpoint400 = {'white': (20, 448, 32), 'black': (39, 436, 25)}
checkpoint500 = {'white': (25, 431, 44), 'black': (46, 427, 27)}
checkpoint600 = {'white': (22, 439, 39), 'black': (35, 429, 36)}
checkpoint700 = {'white': (15, 451, 34), 'black': (22, 445, 33)}
checkpoint800 = {'white': (15, 447, 38), 'black': (41, 424, 35)}
checkpoint900 = {'white': (16, 447, 37), 'black': (30, 443, 27)}
checkpoint1000 = {'white': (17, 446, 37), 'black': (27, 437, 36)}

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
