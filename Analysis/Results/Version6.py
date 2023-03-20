checkpoint100 = {'white': (25, 443, 32), 'black': (35, 436, 29)}
checkpoint200 = {'white': (33, 436, 31), 'black': (33, 441, 26)}
checkpoint300 = {'white': (36, 429, 35), 'black': (36, 430, 34)}
checkpoint400 = {'white': (28, 444, 28), 'black': (37, 423, 40)}
checkpoint500 = {'white': (29, 439, 32), 'black': (33, 431, 36)}
checkpoint600 = {'white': (27, 442, 31), 'black': (37, 436, 27)}
checkpoint700 = {'white': (38, 438, 24), 'black': (58, 416, 26)}
checkpoint800 = {'white': (56, 410, 34), 'black': (50, 412, 38)}
checkpoint900 = {'white': (53, 422, 25), 'black': (58, 415, 27)}
checkpoint1000 = {'white': (64, 414, 22), 'black': (61, 411, 28)}

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
