import funções
from time import sleep
import mysql.connector
from math import ceil
import os

funções.limpador()

try:
    arquivo = open('Config_db.txt', 'r')
    cont = 0
    for linha in arquivo:
        cont += 1
        if cont == 1:
            local = linha.replace('\n','')
        elif cont == 2:
            user = linha.replace("\n","")
        else:
            psword = linha.replace("\n","")
    arquivo.close()
except FileNotFoundError:
    print("é nescessário configurar o banco de dados antes de continuar.\n")
    local = str(input("Local do banco R:"))
    user = str(input("Usuario do banco R:"))
    psword = str(input("Senha de acesso ao banco de dados R:"))
    arquivo = open('Arquivos python/Config_db.txt', 'w')
    arquivo.write(f'{local}\n{user}\n{psword}')
    arquivo.close()


config_db = funções.BancoDeDados(local,user,psword)

funções.limpador()

try:
    config_db.Criar_banco()
except mysql.connector.errors.InterfaceError:
    print("As configuções do banco de dados estão erradas.")
    os.remove('Arquivos python/Config_db.txt')
    exit()
except mysql.connector.errors.ProgrammingError:
    print("As configuções do banco de dados estão erradas.")
    os.remove('Arquivos python/Config_db.txt')
    exit()
except UnicodeError:
    print("As configuções do banco de dados estão erradas.")
    os.remove('Arquivos python/Config_db.txt')
    exit()
except:
    pass


try:
    config_db.anotações_diarias()
except mysql.connector.errors.ProgrammingError:
    pass


try:
    config_db.criar_calculo()
except:
    pass

try:
    config_db.Criar_refeição()
except:
    pass


# == Entrada de dados (sexo).
def calculo_de_calorias(obrigatorio = False):
    continuar = True
    funções.limpador()
    while continuar == True:
        while True:
            try:
                if obrigatorio == False: print("Aperte ""ENTER"" para cancelar a função.")
                sexo = int(input('Qual é o seu sexo? [1 = Masculino] [2 = Feminino] R:'))
            except ValueError:
                if obrigatorio == False:
                    continuar = False
                    return False
                print("por favor, digite um numero.")
                sleep(1)
                funções.limpador()
            else:
                break
        if continuar:        
            if sexo == 1:
                sexo = "Masculino"
                break
            elif sexo == 2:
                sexo = "Feminino"
                break
            else:
                print('Opção invalida.')
                sleep(1)
                funções.limpador()
        return True
    # ====================================================================

    # == Entrada de dados (idade).
    if continuar:
        while continuar ==  True:
            while True:
                try:
                    idade = int(input("Quantos anos você tem?  R:"))
                except ValueError:
                        if obrigatorio == False: 
                            continuar = False 
                            break 
                        print("por favor, digite um numero.")
                        sleep(1)
                        funções.limpador()
                else:
                    break
            if continuar:
                if idade < 1:
                    print('Numero invalido.')
                    sleep(1)
                    funções.limpador()
                else:
                    break
    # =====================================================================

    # == Entrada de dados (peso).
    if continuar:
        while continuar ==  True:
            while True:
                try:
                    peso = float(input('Quantos kilos você pesa?  R:'))
                except ValueError:
                        if obrigatorio == False:
                            continuar = False 
                            break
                        print("por favor, digite um numero.")
                        sleep(1)
                        funções.limpador()
                else:
                    break
            if continuar:
                if peso < 1:
                    print('Numero invalido.')
                    sleep(1)
                    funções.limpador()
                else:
                    break
    # ==========================================================================
    funções.limpador()

# == Calculo de gasto diário de calorias e cadastros de dados no banco de dados.
    if continuar:
        if sexo == "Masculino":
            if idade <= 3:
                gasto_calorico = (59.512 * peso) - 30.4
                
            elif idade > 3 and idade <= 10:
                gasto_calorico = (22.706 * peso) + 504.4
                
            elif idade > 10 and idade <= 18:
                gasto_calorico = (17.686 * peso) + 658.2
                
            elif idade > 18 and idade <= 30:
                gasto_calorico = (15.057 * peso) + 692.2
                
            elif idade > 30 and idade <= 60:
                gasto_calorico = (11.472 * peso) + 873.1
                
            else:
                gasto_calorico = (11.711 * peso) + 587.7
                

        elif sexo == "Feminino":
            if idade <= 3:
                gasto_calorico = (58.317 * peso) - 31.1
            
            elif idade > 3 and idade <= 10:
                gasto_calorico = (20.315 * peso) + 485.9

            elif idade > 10 and idade <= 18:
                gasto_calorico = (13.384 * peso) + 692.6
            
            elif idade > 18 and idade <= 30:
                gasto_calorico = (14.818 * peso) + 486.6

            elif idade > 30 and idade <= 60:
                gasto_calorico = (8.126 * peso) + 845.6

            else:
                gasto_calorico = (9.082 * peso) + 658.5

        funções.limpador()

        while True:
            if not obrigatorio:
                opção = input(f"Seu gasto calórico diário é de {ceil(gasto_calorico * 1.55)} calorias. Usar esses dados? digite ""SIM"" (isso vai excluir os dados anteriores.)  R: ")

                if opção == 'SIM' or opção == 'sim':
                    try:
                        config_db.anotações_diarias()
                        config_db.Criar_tabela()
                        config_db.criar_calculo()

                    except mysql.connector.errors.DatabaseError:
                        config_db.excluir_tabela("dados")
                        config_db.excluir_tabela("anotações")
                        config_db.excluir_tabela("calculos")
                        config_db.anotações_diarias()
                        config_db.Criar_tabela()        
                else:
                    print("esses dados não serão usados.")
                    sleep(1)
                    funções.limpador()
            else:
                config_db.Criar_tabela()

            config_db.Adicionar_dados(ceil(gasto_calorico * 1.55))
            break
# =====================================================

funções.limpador()

# == menu principal.
while True:
    while True:
        # == soma de consumos de calórias.
        try:
            config_db.soma_de_consumo()
        except mysql.connector.errors.ProgrammingError:
            pass
        except mysql.connector.errors.InterfaceError:
            print("As configuções do banco de dados estão erradas.")
            os.remove('Arquivos python/Config_db.txt')
            exit()
        # =============================================================================    
        while True:
            funções.cadasmenu(["Calcular gasto calórico diário","Cardapio","Adicionar exercícios","Finalizar dia (calculos de calorias consumidas serão reniciados)","Ver finalizações de dias passados","Sair"],"CONTADOR DE CALÓRIAS")
            try:
                print(f'Seu gasto calórico é de {config_db.ler_dados()} calórias por dia.')
                break
            except mysql.connector.errors.ProgrammingError:
                calculo_de_calorias(obrigatorio = True)        
        try:
            print(f'Nesse momento sua calória é de {config_db.ler_dados() +  config_db.soma_de_consumo()} contando com as refeições consumidas hoje.')
        except:
            pass

        try:
            opção = int(input("Escolha a opção digitando um numero R: "))
        except ValueError:
            print("Por favor, digite um numero")
            sleep(1)
        else:
            if opção >= 1 and opção < 7:
                break
            else:
                print("Opção invalida.")
                sleep(1)
        funções.limpador()
    if opção == 6:
        break
# ============================================

# == menu do cardapio.
    while True:
        if opção == 1:
            funções.limpador()

            calculo_de_calorias()
            funções.limpador()
            break

        elif opção == 2:
            while True:
                funções.limpador()
                funções.cadasmenu(["Adicionar calórias de refeição pré-definida", "Pré-definidir refeição","Adicionar calórias indenpendente","Reniciar o cardapio","Voltar"],'Cardapio')
                try:
                    cardapio = int(input("Escolha a opção digitando um numero R: "))
                except ValueError:
                    print("Por favor, digite um numero")
                    sleep(1)
                else:
                    if cardapio >= 1 and cardapio < 6:
                        break
                    else:
                        print("Opção invalida.")
                        sleep(1)
            while True:
                if cardapio == 1:
                    funções.limpador()
                    config_db.Cardapio()
                    break

                elif cardapio == 2:
                    funções.limpador()
                    try:
                        config_db.Criar_refeição()
                    except mysql.connector.errors.ProgrammingError:
                        pass
                    print("Escreva ""SAIR"" para cancelar esse processo.\n")
                    comida = str(input("Qual é o nome da comida? R:"))
                    if comida == "SAIR" or comida == "sair":
                        break
                    print("digite ""0"" para sair desse processo.\n")
                    try:
                        calórias = int(input("Quantas calórias esse produto tem? (Em número inteiro) R:"))
                    
                    except ValueError:
                        print("por favor digite um numero inteiro.")

                    else:
                        if calórias <= 0:
                            break                        
                        config_db.add_cardapio(comida,calórias)
                        break
                elif cardapio == 3:
                    funções.limpador()
                    add_calorias = int(input("Quantas calórias você deseja adicionar? digite 0 para sair do processo (use numeros inteiros.) R:"))
                    if add_calorias <= 0:
                        break
                    config_db.add_calorias(add_calorias)
                    break
                elif cardapio == 4:
                    funções.limpador()
                    aviso = str(input("Tem certeza que você deseja excluir seu cardapio? Digite ""SIM"".\n(isso não pode ser restaurado depois.) R:"))
                    if aviso == "SIM" or aviso == "sim":
                        try:
                            config_db.Excluir_cardapio()
                            config_db.Criar_refeição()
                        except:
                            print("não é possível reniciar um cardapio vazio.")
                        finally:
                            break
                    print("função cancelada.")
                    sleep(1)
                    funções.limpador()
                    break

                elif cardapio == 5:
                    break
            if cardapio == 5:
                funções.limpador()
                break

        elif opção == 3:
            funções.limpador()
            add_exercícios = int(input("Quantas calórias você gastou fazendo exercícios? digite ""0"" para cancelar função. (use numeros inteiros.) R:"))
            if add_exercícios <= 0:
                print("função cancelada.")
                sleep(1)
                funções.limpador()
                break
            config_db.add_calorias(add_exercícios,exercicios = True)
            funções.limpador()
            break
        
        elif opção == 4:
                funções.limpador()
                aviso = str(input("Tem certeza que você deseja finalizar o dia? Digite ""SIM"".\n(isso não pode ser restaurado depois.) R:"))
                if  aviso == 'SIM' or aviso == 'sim':
                    
                    try:
                        config_db.finalizar_dia(config_db.ler_dados() +  config_db.soma_de_consumo())
                    
                    except TypeError:
                        config_db.finalizar_dia(config_db.ler_dados())

                    config_db.excluir_tabela("calculos")    
                
                    config_db.criar_calculo()

                    print("Dia finalizado.")
                    sleep(1)
                    funções.limpador()
                    break
                else:
                    print("função cancelada.")
                    sleep(1)
                    funções.limpador()
                    break

        elif opção == 5:
            config_db.ver_finalizações()
            input("ENTER PARA CONTINUAR")
            funções.limpador()
            break
# =========================================================================================================
                