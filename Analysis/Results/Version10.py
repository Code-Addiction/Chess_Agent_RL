checkpoint100 = {'white': (42, 429, 29), 'black': (47, 427, 26)}
checkpoint200 = {'white': (46, 420, 34), 'black': (61, 397, 42)}
checkpoint300 = {'white': (48, 430, 22), 'black': (52, 418, 30)}
checkpoint400 = {'white': (38, 443, 19), 'black': (57, 414, 29)}
checkpoint500 = {'white': (45, 414, 41), 'black': (52, 419, 29)}
checkpoint600 = {'white': (41, 425, 34), 'black': (57, 419, 24)}
checkpoint700 = {'white': (57, 410, 33), 'black': (56, 411, 33)}
checkpoint800 = {'white': (116, 360, 24), 'black': (75, 393, 32)}
checkpoint900 = {'white': (54, 417, 29), 'black': (57, 412, 31)}
checkpoint1000 = {'white': (55, 424, 21), 'black': (48, 415, 37)}

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
