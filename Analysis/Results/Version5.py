checkpoint100 = {'white': (27, 445, 28), 'black': (29, 441, 30)}
checkpoint200 = {'white': (29, 440, 31), 'black': (33, 443, 24)}
checkpoint300 = {'white': (36, 443, 21), 'black': (36, 438, 26)}
checkpoint400 = {'white': (40, 443, 17), 'black': (53, 418, 29)}
checkpoint500 = {'white': (33, 430, 37), 'black': (49, 426, 25)}
checkpoint600 = {'white': (55, 421, 24), 'black': (68, 413, 19)}
checkpoint700 = {'white': (56, 411, 33), 'black': (60, 418, 22)}
checkpoint800 = {'white': (46, 434, 20), 'black': (67, 413, 20)}
checkpoint900 = {'white': (67, 417, 16), 'black': (74, 399, 27)}
checkpoint1000 = {'white': (50, 425, 25), 'black': (56, 425, 19)}

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
