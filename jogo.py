import json 
import random 
import os 

#Naipes 
SAUDAVEIS = {
    "Maçã": 2, "Banana": 3, "Brócolis": 1, "Peixe": 4, "Frango": 5,
    "Arroz Integral": 3, "Aveia": 2, "Ovos": 1, "Nozes": 6, "Iogurte": 2
} 

FAST_FOOD = {
    "Hambúrguer": 10, "Pizza": 9, "Batata Frita": 8, "Refrigerante": 7,
    "Sorvete": 6, "Donut": 5, "Cachorro-Quente": 4, "Milkshake": 3
}

PERGUNTAS_LOGICAS = [
    {
        "pergunta": "Se 'Todo médico é saudável' e 'João é médico', então:",
        "opcoes": ["João é saudável", "João não é saudável", "Nenhuma das anteriores"],
        "resposta": 0
    },
    {
        "pergunta": "A negação de 'Todos os alunos comem maças' é:",
        "opcoes": ["Nenhum aluno come maça", "Algum aluno não come maça", "Todos os alunos não comem maças"],
        "resposta": 1
    },
    {
        "pergunta": "Se 'p → q' é falso, então:",
        "opcoes": ["p é verdadeiro e q é falso", "p é falso e q é verdadeiro", "p e q são falsos"],
        "resposta": 0
    },
    {
        "pergunta": "'Nenhum fast food é saudável' é equivalente a:",
        "opcoes": ["Todo fast food não é saudável", "Algum fast food não é saudável", "Todo saudável não é fast food"],
        "resposta": 0
    },
    {
        "pergunta": "Se 'p ∧ q' é verdadeiro, então:",
        "opcoes": ["p é verdadeiro ou q é verdadeiro", "p é verdadeiro e q é verdadeiro", "p é falso ou q é falso"],
        "resposta": 1
    }
] 

RANKING_FILE = "ranking.json" 

def carregar_ranking():
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar_ranking(ranking):
    with open(RANKING_FILE, 'w') as f:
        json.dump(ranking, f, indent=2) 
        
def adicionar_jogador_ranking(nome, pontos):
    ranking = carregar_ranking()
    ranking.append({"nome": nome, "pontos": pontos}) 
    
    # Ordenar por pontos (decrescente) 
    ranking.sort(key=lambda x: x["pontos"], reverse=True) 
    
    # Manter apenas os top 10
    if len(ranking) > 10:
        ranking = ranking[:10]
    salvar_ranking(ranking)

def mostrar_ranking():
    ranking = carregar_ranking()
    print("\n=== TOP 10 JOGADORES ===")
    
    for i, jogador in enumerate(ranking, 1):
        print(f"{i}. {jogador['nome']}: {jogador['pontos']} pontos")
    print()

#Funções do jogo 
def criar_baralho():
    baralho = [] 
    for alimento ,valor in SAUDAVEIS.items():
        baralho.append(alimento , valor , "saudavel") 
    for alimento, valor in FAST_FOOD.items():
        baralho.append((alimento, valor, "fastfood"))
        
    random.shuffle(baralho)
    return baralho


def comprar_carta(baralho):
    if not baralho:
        baralho = criar_baralho()
    return baralho.pop()

def calcular_pontos(mao):
    pontos = sum(carta[1] for carta in mao)
    # Verificar se há fast food na mão
    tem_fast_food = any(carta[2] == "fastfood" for carta in mao)
    
    if tem_fast_food and pontos > 21:
        # Se tiver fast food e estourar, perde pontos extras
        pontos += 5
    elif not tem_fast_food and pontos > 21:
        # Se não tiver fast food mas estourar, penalidade menor
        pontos += 2
    return pontos 

def mostrar_mao(mao, esconder_ultima=False):
    for i, carta in enumerate(mao):
        if esconder_ultima and i == len(mao) - 1:
            print(f"{i+1}. [Carta oculta]")
        else:
            print(f"{i+1}. {carta[0]} ({carta[1]} pontos) - {'🍎' if carta[2] == 'saudavel' else '🍔'}")

def fazer_pergunta_logica():
    pergunta = random.choice(PERGUNTAS_LOGICAS)
    print("\n=== PERGUNTA DE LÓGICA ===")
    print(pergunta["pergunta"])
    for i, opcao in enumerate(pergunta["opcoes"], 1):
        print(f"{i}. {opcao}")
    
    while True:
        try:
            resposta = int(input("Sua resposta (1-3): ")) - 1
            if 0 <= resposta <= 2:
                break
            print("Por favor, digite 1, 2 ou 3.")
        except ValueError:
            print("Entrada inválida. Digite um número.")
    
    return resposta == pergunta["resposta"]

def jogar_blackjack():
    print("""
    === BLACKJACK DA SAÚDE ===
    Regras especiais:
    - Alimentos saudáveis valem menos pontos
    - Fast foods valem mais pontos mas podem prejudicar sua saúde (pontuação)
    - Se sua mão tiver fast food e estourar 21, perde pontos extras
    - Responda perguntas de lógica corretamente para ganhar bônus!
    """)
    
    nome_jogador = input("Digite seu nome: ")
    baralho = criar_baralho()
    pontos_jogador = 0
    
    while True:
        mao_jogador = []
        mao_cpu = []
        
        # Distribuir cartas iniciais
        mao_jogador.append(comprar_carta(baralho))
        mao_cpu.append(comprar_carta(baralho))
        mao_jogador.append(comprar_carta(baralho))
        mao_cpu.append(comprar_carta(baralho))
        
        print("\n=== SUA MÃO ===")
        mostrar_mao(mao_jogador)
        print("\n=== MÃO DO CPU ===")
        mostrar_mao(mao_cpu, esconder_ultima=True)
        
        # Turno do jogador
        while True:
            pontos_atual = calcular_pontos(mao_jogador)
            print(f"\nPontos atuais: {pontos_atual}")
            
            if pontos_atual >= 21:
                break
                
            acao = input("\nDeseja (1) Comprar, (2) Parar ou (3) Responder pergunta de lógica (bônus)? ").strip()
            
            if acao == "1":
                nova_carta = comprar_carta(baralho)
                mao_jogador.append(nova_carta)
                print(f"\nVocê comprou: {nova_carta[0]} ({nova_carta[1]} pontos) - {'🍎' if nova_carta[2] == 'saudavel' else '🍔'}")
                mostrar_mao(mao_jogador)
                
                if calcular_pontos(mao_jogador) > 21:
                    print("Você estourou 21 pontos!")
                    break
                    
            elif acao == "2":
                break
                
            elif acao == "3":
                if fazer_pergunta_logica():
                    print("Resposta correta! Você ganha 2 pontos de bônus.")
                    pontos_jogador += 2
                else:
                    print("Resposta incorreta! Nenhum bônus desta vez.")
            else:
                print("Opção inválida. Digite 1, 2 ou 3.")
        
        # Turno da CPU
        print("\n=== VEZ DO CPU ===")
        mostrar_mao(mao_cpu)
        while calcular_pontos(mao_cpu) < 17:
            nova_carta = comprar_carta(baralho)
            mao_cpu.append(nova_carta)
            print(f"\nCPU comprou: {nova_carta[0]} ({nova_carta[1]} pontos) - {'🍎' if nova_carta[2] == 'saudavel' else '🍔'}")
        
        pontos_jogador_final = calcular_pontos(mao_jogador)
        pontos_cpu_final = calcular_pontos(mao_cpu)
        
        print("\n=== RESULTADO FINAL ===")
        print(f"Sua pontuação: {pontos_jogador_final}")
        print(f"Pontuação do CPU: {pontos_cpu_final}")
        
        # Determinar vencedor
        if pontos_jogador_final > 21 and pontos_cpu_final > 21:
            print("Ambos estouraram! Ninguém ganha pontos.")
        elif pontos_jogador_final > 21:
            print("Você estourou! CPU vence.")
        elif pontos_cpu_final > 21:
            print("CPU estourou! Você vence!")
            pontos_jogador += 1
        elif pontos_jogador_final > pontos_cpu_final:
            print("Você venceu!")
            pontos_jogador += 1
        elif pontos_jogador_final < pontos_cpu_final:
            print("CPU venceu!")
        else:
            print("Empate!")
        
        print(f"\nSeus pontos totais: {pontos_jogador}")
        
        continuar = input("\nDeseja jogar novamente? (s/n): ").strip().lower()
        if continuar != 's':
            break
    
    print(f"\nFim do jogo! Sua pontuação final: {pontos_jogador}")
    adicionar_jogador_ranking(nome_jogador, pontos_jogador)
    mostrar_ranking()

# Menu principal
while True:
    print("\n=== MENU PRINCIPAL ===")
    print("1. Jogar Blackjack dos Alimentos")
    print("2. Ver Ranking")
    print("3. Sair")
    
    opcao = input("Escolha uma opção: ").strip()
    
    if opcao == "1":
        jogar_blackjack()
    elif opcao == "2":
        mostrar_ranking()
    elif opcao == "3":
        print("Obrigado por jogar! Até mais!")
        break
    else:
        print("Opção inválida. Tente novamente.")