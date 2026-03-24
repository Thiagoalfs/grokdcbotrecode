import random
def respostas():
    dado = ["sim", "não", "talvez"]
    valor = random.randint(0, (len(dado)-1))
    easter_egg = random.randint(0, 100)
    if easter_egg == 100:
        return "smt"
    else:
        return dado[valor]