import random, string

def random_alphanumeric(count):
    return [random.choice(string.letters + string.digits) for i in range(count)]