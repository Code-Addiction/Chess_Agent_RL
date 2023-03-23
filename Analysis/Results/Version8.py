checkpoint100 = {'white': (37, 429, 34), 'black': (48, 421, 31)}
checkpoint200 = {'white': (35, 433, 32), 'black': (39, 423, 38)}
checkpoint300 = {'white': (40, 415, 45), 'black': (48, 428, 24)}
checkpoint400 = {'white': (49, 420, 31), 'black': (42, 431, 27)}
checkpoint500 = {'white': (40, 420, 40), 'black': (51, 415, 34)}
checkpoint600 = {'white': (42, 416, 42), 'black': (34, 438, 28)}
checkpoint700 = {'white': (47, 429, 24), 'black': (53, 425, 22)}
checkpoint800 = {'white': (58, 420, 22), 'black': (53, 427, 20)}
checkpoint900 = {'white': (43, 431, 26), 'black': (55, 429, 16)}
checkpoint1000 = {'white': (58, 410, 32), 'black': (54, 421, 25)}

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
