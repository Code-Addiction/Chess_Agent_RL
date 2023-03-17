checkpoint100 = {'white': (34, 433, 33), 'black': (32, 431, 37)}
checkpoint200 = {'white': (33, 438, 29), 'black': (31, 442, 27)}
checkpoint300 = {'white': (29, 438, 33), 'black': (36, 435, 29)}
checkpoint400 = {'white': (50, 413, 37), 'black': (44, 440, 16)}
checkpoint500 = {'white': (46, 427, 27), 'black': (45, 427, 28)}
checkpoint600 = {'white': (38, 431, 31), 'black': (52, 421, 27)}
checkpoint700 = {'white': (42, 434, 24), 'black': (50, 427, 23)}
checkpoint800 = {'white': (44, 429, 27), 'black': (49, 424, 27)}
checkpoint900 = {'white': (42, 435, 23), 'black': (43, 429, 28)}
checkpoint1000 = {'white': (47, 434, 19), 'black': (48, 425, 27)}

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
