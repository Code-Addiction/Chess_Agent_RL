checkpoint100 = {'white': (57, 407, 36), 'black': (44, 416, 40)}
checkpoint200 = {'white': (46, 428, 26), 'black': (44, 429, 27)}
checkpoint300 = {'white': (62, 405, 33), 'black': (59, 405, 36)}
checkpoint400 = {'white': (52, 429, 19), 'black': (51, 415, 34)}
checkpoint500 = {'white': (50, 420, 30), 'black': (70, 397, 33)}
checkpoint600 = {'white': (49, 412, 39), 'black': (48, 426, 26)}
checkpoint700 = {'white': (52, 416, 32), 'black': (61, 418, 21)}
checkpoint800 = {'white': (54, 409, 37), 'black': (64, 407, 29)}
checkpoint900 = {'white': (47, 422, 31), 'black': (32, 434, 34)}
checkpoint1000 = {'white': (54, 427, 19), 'black': (58, 419, 23)}

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
