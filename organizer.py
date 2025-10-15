import random
import math

# --- FUNÇÃO PRINCIPAL ATUALIZADA ---
def organizar_times(jogadores, num_times):
    """
    Função principal que agora chama a nova lógica recursiva,
    preservando o espírito do algoritmo original.
    """
    if num_times < 2:
        return [jogadores]
    
    # Se for 2, 3 ou 4, ainda podemos usar as funções originais e super testadas
    if num_times == 2:
        return _organizar_2_times(jogadores, sum(j[2] for j in jogadores))
    if num_times == 3:
        return _organizar_3_times(jogadores, sum(j[2] for j in jogadores))
    if num_times == 4:
        return _organizar_4_times(jogadores, sum(j[2] for j in jogadores))
    
    # Para 5 ou mais times, usamos a nova abordagem recursiva
    return _organizar_n_times_recursivo(jogadores, num_times)


# --- NOVA FUNÇÃO RECURSIVA GENÉRICA ---
def _organizar_n_times_recursivo(jogadores, num_times):
    """
    Organiza jogadores em 'n' times de forma recursiva, mantendo a aleatoriedade.
    """
    # Condição de parada: quando só faltam 2 times, usamos a função original.
    if num_times == 2:
        return _organizar_2_times(jogadores, sum(j[2] for j in jogadores))

    soma_total = sum(j[2] for j in jogadores)
    media_alvo_time = soma_total / num_times
    tamanho_time_ideal = len(jogadores) // num_times
    
    # Tenta encontrar o melhor time possível com o tamanho ideal
    tentativas = []
    # Usamos o método de tentativas, como no algoritmo original
    for _ in range(100):
        random.shuffle(jogadores)
        # Pega uma fatia do tamanho ideal
        time_candidato = jogadores[:tamanho_time_ideal]
        tentativas.append(time_candidato)
        
    # Usa a função original para encontrar o melhor grupo
    melhor_time = proximo_media(tentativas, media_alvo_time)
    
    # Prepara a recursão
    jogadores_restantes = [j for j in jogadores if j not in melhor_time]
    
    # Retorna o melhor time encontrado + o resultado da organização dos times restantes
    return [melhor_time] + _organizar_n_times_recursivo(jogadores_restantes, num_times - 1)


# --- SUAS FUNÇÕES ORIGINAIS (INTACTAS E USADAS COMO BASE) ---

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