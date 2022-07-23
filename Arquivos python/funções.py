from os import system
import platform
from time import sleep
import mysql.connector
from datetime import datetime


# == Cores no terminal de rapido acesso.
def vermelho(txt):
  return f'\033[31m{txt}\033[m'
def verde (txt):
  return f'\033[32m{txt}\033[m'
def amarelo (txt):
  return f'\033[33m{txt}\033[m'
def azul (txt):
  return f'\033[34m{txt}\033[m'
def roxo (txt):
  return f'\033[35m{txt}\033[m'
def ciano (txt):
  return f'\033[36m{txt}\033[m'
def cinza (txt):
  return f'\033[37m{txt}\033[m' 
# ========================================  

# == Funções do bando de dados.

class BancoDeDados:
    def __init__(self,host,user,passwd):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.banco = "cdc_cache"

    def Criar_banco(self):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd
        )
        cursor = banco.cursor()
        cursor.execute("CREATE DATABASE cdc_cache")
        banco.close()

    def Criar_tabela(self):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE dados (gasto_calorico INT(5))")
        banco.close()

    def add_calorias(self,calórias,exercicios = False):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        if exercicios:
            comando_SQL = f"INSERT INTO calculos (calculos_de_calórias) VALUES ({calórias * -1})"
        else:
            comando_SQL = f"INSERT INTO calculos (calculos_de_calórias) VALUES ({calórias})"
        cursor.execute(comando_SQL)
        banco.commit()
        banco.close()

    def Excluir_cardapio(self):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        cursor.execute("DROP TABLE cardapio")
        banco.close()

    def Criar_refeição(self):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE cardapio (refeição VARCHAR(200),calórias INT(5))")
        banco.close()

    def add_cardapio(self,comida,calórias):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        comando_SQL = "INSERT INTO cardapio (refeição,calórias) VALUES (%s,%s)"
        dados = comida,calórias
        cursor.execute(comando_SQL,dados)
        banco.commit()
        banco.close()

    def Adicionar_dados(self,dados):
            banco = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                database = self.banco
            )
            cursor = banco.cursor()
            comando_SQL = f"INSERT INTO dados (gasto_calorico) VALUES ({dados})"
            cursor.execute(comando_SQL)
            banco.commit()
            banco.close()
    
    def criar_calculo(self):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE calculos (calculos_de_calórias INT(5))")
        banco.close()

    def excluir_tabela(self,tabela):
        """
        Remove qualquer tabela especifivada.
        """
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        cursor.execute(f"DROP TABLE {tabela}")
        banco.commit()
        banco.close()

    def Cardapio(self):
        quebrar = False

        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        comando_SQL = "SELECT * FROM cardapio"
        cursor.execute(comando_SQL)
        valor = cursor.fetchall()
        banco.close()
        while True:
            limpador()
            numeração = 1
            for comida,calórias in valor:
                print(f'{numeração}° Refeição: {comida:<30} {calórias} calórias')
                numeração += 1
            try:
                print("\nAperte ENTER para sair do processo.")
                OpçCardapio = int(input("Escolha um alimento para adicionar calórias R:"))
                quantidade = int(input("Quantas unidades foi consumida? R:"))
            except ValueError:
                quebrar = True
            else:
                try:
                    banco = mysql.connector.connect(
                        host = self.host,
                        user = self.user,
                        passwd = self.passwd,
                        database = self.banco
                    )
                    cursor = banco.cursor()
                    cursor.execute("CREATE TABLE calculos (calculos_de_calórias INT(5))")
                    banco.close()

                except mysql.connector.errors.ProgrammingError:
                    pass
                try:
                    banco = mysql.connector.connect(
                        host = self.host,
                        user = self.user,
                        passwd = self.passwd,
                        database = self.banco
                    )
                    cursor = banco.cursor()
                    comando_SQL = f"INSERT INTO calculos (calculos_de_calórias) VALUES ({valor[OpçCardapio - 1][1] * quantidade})"
                    cursor.execute(comando_SQL)
                    banco.commit()
                    banco.close()
                except:
                    print("opção indísponivel.")
                    sleep(1)
            if quebrar:        
                break



    def ler_dados(self):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        comando_SQL = "SELECT * FROM dados"
        cursor.execute(comando_SQL)
        valor = cursor.fetchall()
        banco.close()  
        return valor[0][0] * -1

    def soma_de_consumo(self):
        """
        Seleciona todas as calórias comsumidas anotadas na tabela "calculos" e soma tudo para mostrar o quanto de calórias foi consumida.
        """
        db = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        ) 
        cursor = db.cursor() 
        cursor.execute("SELECT SUM(calculos_de_calórias) FROM calculos") 
        valor = cursor.fetchall()[0][0]
        return valor

    def anotações_diarias(self):    
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE anotações (DATA CHAR(10), CALÓRIAS_NO_FINAL_DO_DIA INT(5))")
        banco.close()
    
    def finalizar_dia(self,calorias_do_dia):
        data = datetime.today().strftime('%d-%m-%Y')
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        comando_sql = "INSERT INTO anotações (DATA, CALÓRIAS_NO_FINAL_DO_DIA) VALUES (%s,%s)"
        valores = data,calorias_do_dia
        cursor.execute(comando_sql,valores)
        banco.commit()
        banco.close()

    def ver_finalizações(self):
        banco = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.banco
        )
        cursor = banco.cursor()
        comando_SQL = "SELECT * FROM anotações"
        cursor.execute(comando_SQL)
        valor = cursor.fetchall()
        banco.close()
        limpador()
        for data,calórias in valor:
            print(f'{data:<30} {calórias} calórias')

# ==============================================================================================

# == Titulo.
def titulo(txt):
  print('==='*15)
  print(txt.center(44))
  print('==='*15)
# ======================

# == Menu versátil.
def cadasmenu(lista,txt='MENU PRINCIPAL'):
  c=1
  titulo(txt)
  for items in lista:
    print(f'{c} - {roxo(items)}')
    c+=1
  print('==='*15)
# ============================================

# == Limpador de terminal multiplataforma.
def limpador():
    sistema_operacional = platform.system()

    if sistema_operacional == "Windows":
        limpador = "cls"
    elif sistema_operacional == "Linux":
        limpador = "clear"
    return system(f"{limpador}")
# =========================================
