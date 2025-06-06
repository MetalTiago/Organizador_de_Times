
import random
import math

def dividir_lista(lista, num_partes):
    tamanho_parte = len(lista) // num_partes
    return [lista[i * tamanho_parte : (i + 1) * tamanho_parte] for i in range(num_partes)]

def proximo_media(possibilidades, alvo):
    melhor_grupo = None
    menor_diferenca = float('inf')
    for grupo in possibilidades:
        total = sum(j[2] for j in grupo)
        diferenca = abs(total - alvo)
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            melhor_grupo = grupo
    return melhor_grupo

def organizar_times(jogadores, num_times):
    soma_total = sum(j[2] for j in jogadores)
    if num_times == 2:
        return _organizar_2_times(jogadores, soma_total)
    elif num_times == 3:
        return _organizar_3_times(jogadores, soma_total)
    elif num_times == 4:
        return _organizar_4_times(jogadores, soma_total)

def _organizar_2_times(jogadores, soma_total):
    tentativas = []
    for _ in range(100):
        random.shuffle(jogadores)
        partes = dividir_lista(jogadores, 2)
        tentativas.append(partes[0])
    metade = soma_total / 2
    time_a = proximo_media(tentativas, metade)
    time_b = [j for j in jogadores if j not in time_a]
    return [time_a, time_b]

def _organizar_3_times(jogadores, soma_total):
    tentativas_a = []
    for _ in range(100):
        random.shuffle(jogadores)
        partes = dividir_lista(jogadores, 3)
        tentativas_a.append(partes[0])
    terco = soma_total / 3
    time_a = proximo_media(tentativas_a, terco)
    resto = [j for j in jogadores if j not in time_a]
    time_b, time_c = _organizar_2_times(resto, sum(j[2] for j in resto))
    return [time_a, time_b, time_c]

def _organizar_4_times(jogadores, soma_total):
    tentativas_metade = []
    for _ in range(100):
        random.shuffle(jogadores)
        partes = dividir_lista(jogadores, 2)
        tentativas_metade.append(partes[0])
    metade = soma_total / 2
    parte_a = proximo_media(tentativas_metade, metade)
    parte_b = [j for j in jogadores if j not in parte_a]
    time_a, time_b = _organizar_2_times(parte_a, sum(j[2] for j in parte_a))
    time_c, time_d = _organizar_2_times(parte_b, sum(j[2] for j in parte_b))
    return [time_a, time_b, time_c, time_d]
