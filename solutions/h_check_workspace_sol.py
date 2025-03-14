# ------------------------------------------------------------------------------------------------





def check_elbow_left(x, y):
    r = 75
    if (x + r) ** 2 + y ** 2 < r ** 2:
        return False
    if (x - r) ** 2 + y ** 2 <= r ** 2:
        return True
    if y < 0:
        return False
    if x ** 2 + y ** 2 <= (2 * r) ** 2:
        return True
    return False

def check_elbow_right(x, y):
    r = 75
    if (x + r) ** 2 + y ** 2 <= r ** 2:
        return True
    if (x - r) ** 2 + y ** 2 < r ** 2:
        return False
    if y < 0:
        return False
    if x ** 2 + y ** 2 <= (2 * r) ** 2:
        return True
    return False
    




# ------------------------------------------------------------------------------------------------