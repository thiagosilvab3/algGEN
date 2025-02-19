import random

# Parâmetros do algoritmo
TAMANHO_POPULACAO = 20
TAXA_CRUZAMENTO = 0.8
TAXA_MUTACAO = 0.03
NUMERO_MAX_GERACOES = 1000
FITNESS_OTIMO = 28

# Função para calcular o fitness de um indivíduo
def calcular_fitness(individuo):
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return 28 - conflitos  # Fitness é o número de pares sem conflito

# Função para decodificar o cromossomo binário em um array de posições
def decodificar_individuo(cromossomo):
    individuo = []
    for i in range(0, 24, 3):
        gene = cromossomo[i:i+3]
        linha = int("".join(map(str, gene)), 2)
        individuo.append(linha)
    return individuo

# Função para gerar um indivíduo aleatório
def gerar_individuo():
    return [random.randint(0, 1) for _ in range(24)]

# Função para seleção dos pais (roleta)
def selecao_roleta(populacao, fitness):
    total_fitness = sum(fitness)
    probabilidades = [f / total_fitness for f in fitness]
    pais = random.choices(populacao, weights=probabilidades, k=2)
    return pais

# Função para cruzamento (ponto de corte)
def cruzamento(pai1, pai2):
    if random.random() < TAXA_CRUZAMENTO:
        ponto_corte = random.randint(1, 23)
        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
        return filho1, filho2
    else:
        return pai1, pai2

# Função para mutação (bit flip)
def mutacao(individuo):
    for i in range(len(individuo)):
        if random.random() < TAXA_MUTACAO:
            individuo[i] = 1 - individuo[i]  # Inverte o bit
    return individuo

# Função principal do algoritmo genético
def algoritmo_genetico():
    populacao = [gerar_individuo() for _ in range(TAMANHO_POPULACAO)]
    
    for _ in range(NUMERO_MAX_GERACOES):
        fitness = [calcular_fitness(decodificar_individuo(ind)) for ind in populacao]
        
        if max(fitness) == FITNESS_OTIMO:
            melhor_individuo = populacao[fitness.index(max(fitness))]
            return decodificar_individuo(melhor_individuo)
        
        nova_populacao = []
        elite = sorted(range(len(fitness)), key=lambda i: fitness[i], reverse=True)[:2]
        for i in elite:
            nova_populacao.append(populacao[i])
        
        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1, pai2 = selecao_roleta(populacao, fitness)
            filho1, filho2 = cruzamento(pai1, pai2)
            filho1 = mutacao(filho1)
            filho2 = mutacao(filho2)
            nova_populacao.extend([filho1, filho2])
        
        populacao = nova_populacao
    
    melhor_individuo = populacao[fitness.index(max(fitness))]
    return decodificar_individuo(melhor_individuo)

# Executa o algoritmo até encontrar 5 soluções distintas
solucoes_distintas = set()
num_solucoes_desejadas = 5

while len(solucoes_distintas) < num_solucoes_desejadas:
    solucao = algoritmo_genetico()
    if calcular_fitness(solucao) == FITNESS_OTIMO:
        solucoes_distintas.add(tuple(solucao))

# Função para exibir um tabuleiro com a solução
def exibir_tabuleiro(solucao):
    print("\nTabuleiro:")
    for linha in range(8):
        linha_str = ""
        for coluna in range(8):
            if solucao[coluna] == linha:
                linha_str += "♛ "
            else:
                linha_str += "• "
        print(linha_str)
    print("\n" + "="*20)

# Exibe as 5 melhores soluções distintas
print("\nCinco melhores soluções distintas encontradas:")
for i, solucao in enumerate(solucoes_distintas, 1):
    print(f"Solução {i}: {list(solucao)}")
    exibir_tabuleiro(list(solucao))
