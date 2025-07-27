import os
from tinydb import TinyDB, Query
from colorama import Fore, Back, Style

db = TinyDB('db.json')
config = TinyDB('config.json')
Estoque = Query()


# Initial Setup
os.system("title Gerenciamento de estoque para impressora 3D")
if not config.search(Query().cepm.exists()):
    config.insert({'cepm': 0.0025})
else:
    cepm = config.search(Query().cepm.exists())[0]['cepm']



def pause():
    input("Pressione ENTER para continuar...")

def menuDisplay(name, length=10):
    os.system('cls')
    line = "=" * length
    print(f"{line}> "+Fore.RED+f"{name}"+Fore.WHITE+f" <{line}\n")

def bottomDisplay(length=10):
    line = "=" * length
    print(f"-{line}|{line}-\n")


def error(err_msg):
    menuDisplay("Erro")
    print(f"Erro: {err_msg}\n")
    pause()
    main()

def warning(wrn_msg):
    menuDisplay(Fore.YELLOW+"Aviso")
    print(f"{wrn_msg}\n")
    pause()

def stockbar(value, total=1000, width=25):
    percent = int((value / total) * 100)
    filled = int(width * value / total)
    bar = '█' * filled + '-' * (width - filled)
    return f"{Fore.GREEN}[{bar}] {Fore.WHITE}{percent:3d}%{Style.RESET_ALL}"

def stockgraphics():
    for fillament in db.all():
            tipo = f"{fillament['Tipo']}".ljust(12)
            cor = f"{fillament['Cor']}".ljust(15)
            out1 = Fore.RED + f"{str(fillament.doc_id).rjust(2)}." + Fore.WHITE + f" Tipo: {tipo} | Cor: {cor} | "
            out2 = stockbar(fillament['Peso'])
            print(out1 + out2)

def opt1():
    menuDisplay('Registrar filamento no estoque')
    print("Por favor, digite os dados abaixo: ")
    type = input("Tipo de filamento: ").upper()
    color = input("Cor: ").capitalize()
    size = float(input("Peso (em gramas): "))
    quantity = int(input("Número de unidades: "))
    price = float(input("Preço unitário (em R$): "))
    cpg = price/size
    # Verificação de similaridade (adiciona apenas a quantidade)
    similarity = db.search(
        (Estoque.Tipo == type) &
        (Estoque.Cor == color) &
        (Estoque.Peso == size) &
        (Estoque.Preco == price)
        )
    if similarity:
        i = db.search(Estoque.Tipo == type and Estoque.Cor == color and Estoque.Peso == size and Estoque.Preco == price)
        addqnt = int(i[0]['Quantidade']) + quantity
        db.update({'Quantidade': addqnt})
    else:
        db.insert({'Tipo': type, 'Cor': color, 'Peso': size, 'Quantidade': quantity, 'Preco': price, 'cpg': cpg})
    warning("Filamento registrado com sucesso!")
    main()

def opt2():
    menuDisplay('Registrar impressão')
    filqnt = int(input(("Digite quantos filamentos foram utilizados: ")))
    utilist = {}
    allweight = 0
    for i in range(1, filqnt+1):
        menuDisplay('Registrar impressão')
        print(f"Filamentos no estoque:")
        stockgraphics()
        utilized = int(input("Digite qual o filamento utilizado: "))
        qnt = float(input("Digite quantas gramas do filamentos foram utilizadas: "))
        utilist[utilized] = qnt
        # A partir de tudo isso, nós temos o dicionário no formato: Filamento utilizado | quantidade de gramas
    for y in utilist:
        cpg = db.get(doc_id=y)['cpg']
        print(cpg) #
        allweight = (utilist[y] * cpg) + allweight
        weight = db.get(doc_id=y)['Peso'] - utilist[y]
        db.update({'Peso': weight}, doc_ids=[y])
    time = int(input("Digite o tempo de impressão (em minutos): "))
    salecost = float(input("Por quanto deseja vender o produto? (em R$):")) 
    fcost = (time * cepm) + allweight
    if salecost < fcost:
        error("Preço de venda menor que o custo da impressão!")
    else:
        profit = salecost - fcost
        warning("Impressão registrada com sucesso!")
        menuDisplay("Relatório")
        print("O relatório leva em consideração o custo da energia\ne o custo proporcional de acordo com o peso/preço filamento.\n-==============|==============-\n")
        print("Tempo de impressão: "+Fore.GREEN+f"{time} minutos\n"+Fore.WHITE+"Custo total: "+Fore.GREEN+f"R${fcost:.2f}\n"+Fore.WHITE+"Margem de lucro: "+Fore.GREEN+f"{profit/salecost*100:.2f}%\n"+Fore.WHITE+"Lucro: "+Fore.GREEN+f"R${profit:.2f}\n"+Fore.WHITE)
        pause()
        main()

def opt3():
    menuDisplay("Estoque", 35)
    stockgraphics()
    print()
    bottomDisplay(39)
    pause()
    main()

def opt4():
    global cepm
    menuDisplay("Configurações")
    print("Alterar variáveis de configuração:\n"+Fore.RED+"1. "+Fore.WHITE+"Resetar ao Padrão\n"+Fore.RED+"2. "+Fore.WHITE+"Custo de energia por minuto: "+Fore.YELLOW+f"{cepm:.4f}\n"+Fore.RED+"3. "+Fore.WHITE+"Voltar\n")
    opt = int(input("Digite a opção: "))
    if opt == 1:
        cepm = 0.0025
        config.update({'cepm': cepm})
        warning("Configuração resetada ao padrão!")
        main()
    elif opt == 2:
        cepm = float(input("Digite o novo valor: "))
        config.update({'cepm': cepm})
        warning("Configuração alterada com sucesso!")
        main()
    elif opt == 3:
        main()
    else:
        error("Opção inválida")

def opt5():
    menuDisplay("Sobre")
    print("Projeto desenvolvido por: "+Fore.GREEN+"Gustavo Hirota\n"+Fore.WHITE+"\n")
    print("Github: "+Fore.GREEN+"https://github.com/dethstruck"+Fore.WHITE+"\n")
    pause()
    main()

def opt6():
    warning("Obrigado por utilizar o programa!\nDesenvolvido por: "+Fore.GREEN+"Gustavo Hirota\n"+Fore.WHITE+"Github: "+Fore.GREEN+"https://github.com/dethstruck"+Fore.WHITE)
    exit()

def main():
    opt = 0
    menuDisplay("Gerenciamento de impressora 3D")
    print("Operações:\n"+Fore.RED+"1. "+Fore.WHITE+"Registrar filamento no estoque\n"+Fore.RED+"2. "+Fore.WHITE+"Registrar impressão\n"+Fore.RED+"3. "+Fore.WHITE+"Acessar estoque\n"+Fore.RED+"4. "+Fore.WHITE+"Configurações\n"+Fore.RED+"6. "+Fore.WHITE+"Sair\n")
    opt = int(input("Digite a opção: "))
    if opt == 1:
        opt1()
    elif opt == 2:
        opt2()
    elif opt == 3:
        opt3()
    elif opt == 4:
        opt4()
    elif opt ==5:
        opt5()
    elif opt == 6:
        opt6()
    else:
        error("Opção inválida")

main()
