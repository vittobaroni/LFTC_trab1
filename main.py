import copy

def converter_afnd_epsilon(estados, alfabeto, transicoes, finais):
    # cópias para não estragar o autômato original durante a conversão
    novas_transicoes = copy.deepcopy(transicoes)
    novos_finais = set(finais)

    # Descobre quem o estado consegue alcançar andando SÓ pelo epsilon
    def alcancaveis_por_epsilon(estado_origem):
        alcancaveis = set()
        pilha = [estado_origem]
        while pilha:
            atual = pilha.pop()
            if 'epsilon' in transicoes.get(atual, {}):
                for vizinho in transicoes[atual]['epsilon']:
                    if vizinho not in alcancaveis:
                        alcancaveis.add(vizinho)
                        pilha.append(vizinho)
        return alcancaveis

    print("--- Iniciando a conversão ---")
    
    # Avalia cada estado (p1) do autômato
    for p1 in estados:
        # Descobre todos os estados (p2) que p1 alcança ao seguir epsilon
        estados_p2 = alcancaveis_por_epsilon(p1)
        
        for p2 in estados_p2:
            # Se p2 tem uma transição com uma letra para 'q', p1 herda essa transição.
            for letra in alfabeto:
                if letra in transicoes.get(p2, {}):
                    destinos_q = transicoes[p2][letra]
                    for q in destinos_q:
                        if letra not in novas_transicoes[p1]:
                            novas_transicoes[p1][letra] = set()
                        novas_transicoes[p1][letra].add(q)
                        print(f"Regra 1: Seta '{letra}' copiada de {p2} para {p1}. Novo caminho: {p1} ---{letra}--> {q}")

            # Se p2 é um estado final, p1 também vira estado final.
            if p2 in finais:
                if p1 not in novos_finais:
                    novos_finais.add(p1)
                    print(f"Regra 2: O estado {p1} virou FINAL porque alcança o estado final {p2} via epsilon.")

    for estado in novas_transicoes:
        if 'epsilon' in novas_transicoes[estado]:
            del novas_transicoes[estado]['epsilon']
            print(f"Limpando: Transição epsilon removida do estado {estado}.")

    return novas_transicoes, novos_finais


if __name__ == "__main__":
    
    # Conjuntos formais do Autômato
    estados  = {'1', '2', '3', '4', '5'}
    alfabeto = {'a', 'b'}
    finais   = {'4'}
    
    # Tabela de Transições do AFND
    # Estrutura: 'estado_origem': {'letra': {'estados_destino'}}
    transicoes = {

         #Questão 3 da prova do dia 10/10/2023

        '1': {
            'a': {'2'},               # Lê 'a' e avança para o estado 2
            'b': {'5', '1'}           # Lê 'b' e avança para o estado 5 e 1
        },
        
        '2': {
            'a': {'2'},                # Lê 'a' e faz um loop nele mesmo
            'epsilon': {'3', '4'}      # Transição vazia: escorrega para o estado 3 e 4
        },
        
        '3': {
            'a': {'4'},                # Lê 'a' e avança para o estado 4
            'b': {'3'}                 # Lê 'b' e faz um loop nele mesmo
        },
        
        '4': {
            'a': {'5'},                # Lê 'a' e avança para o estado 5
            'b': {'2'}                 # Lê 'b' e avança para o estado 4
        },
        '5': {
            'a': {'5'},                # Lê 'a' e faz um loop nele mesmo
            'b': {'1'}                 # Lê 'b' e avança para o estado 1
        }
    }

    novas_trans, novos_finais = converter_afnd_epsilon(estados, alfabeto, transicoes, finais)

    print("\n--- RESULTADO DA CONVERSÃO  ---")

    print(f"\nNovos Estados Finais: {novos_finais}")
    print("Novas Transições (Sem Epsilon):")
    for estado in sorted(estados):
        for simbolo, destinos in novas_trans.get(estado, {}).items():
            print(f"  δ({estado}, {simbolo}) = {destinos}")
