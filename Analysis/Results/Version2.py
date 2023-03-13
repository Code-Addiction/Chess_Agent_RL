checkpoint100 = {'white': (31, 430, 39), 'black': (39, 428, 33)}
checkpoint200 = {'white': (22, 437, 41), 'black': (37, 421, 42)}
checkpoint300 = {'white': (26, 436, 38), 'black': (33, 429, 38)}
checkpoint400 = {'white': (25, 441, 34), 'black': (34, 425, 41)}
checkpoint500 = {'white': (37, 419, 44), 'black': (33, 416, 51)}
checkpoint600 = {'white': (40, 433, 27), 'black': (42, 416, 42)}
checkpoint700 = {'white': (45, 422, 33), 'black': (53, 414, 33)}
checkpoint800 = {'white': (39, 423, 38), 'black': (48, 429, 23)}
checkpoint900 = {'white': (53, 418, 29), 'black': (44, 419, 37)}
checkpoint1000 = {'white': (52, 425, 23), 'black': (35, 434, 31)}

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
