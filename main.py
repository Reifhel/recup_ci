import re
import math
import os


tokens = []
TokenInfo = []

numeros = []
operador = []
especiais = []
resultados = []
nomesVariaveis = []
variaveis = {}
lexemas = []
conta = ""


def matcher(contas):
  for s in contas:
    tokens.clear()
    while (s != ""):
      houveMatch = False
      s = s.strip()
      for token in TokenInfo:
        igualdade = re.match(token[0], s)
        if igualdade != None and igualdade.group() != "":
          houveMatch = True
          s = re.sub(token[0], "", s, 1)
          tokens.append((token[1], igualdade.group(0)))
          lexemas.append(igualdade.group(0))
          break
      if not houveMatch:
        print(f"Linha {conta.index(calculo)+1}: lexemas {[s[0]]} inválidos")
        raise Exception(f"Linha {conta.index(calculo)+1}: Erro léxico")
        break
    valido()


def valido():
  for token in tokens:
    if token[0] == "NUMERO":
      numeros.append(token[1])
    if token[0] == "OPERADORES":
      operador.append(token[1])
    if token[0] == "ESPECIAIS":
      especiais.append(token[1])
    if token[0] == "RESULTADO":
      resultados.append(token[1])
    if token[0] == "VARIAVEL":
      nomesVariaveis.append(token[1])
      if token[1] in variaveis:
        numeros.append(variaveis[token[1]])
        resultados.remove(variaveis[token[1]])
  calcular()


def calcular():
  if (len(operador) == 0):
    resultados.append(numeros[0])
    numeros.pop(0)
    armazenarVar()

  for operacao in operador[::-1]:
    if operacao == "+":
      conta = float(numeros[0]) + float(numeros[1])
      remove(2)
    elif operacao == "-":
      conta = float(numeros[0]) - float(numeros[1])
      remove(2)
    elif operacao == "*":
      conta = float(numeros[0]) * float(numeros[1])
      remove(2)
    elif operacao == "/":
      conta = float(numeros[0]) / float(numeros[1])
      remove(2)
    elif operacao == "exp":
      conta = float(numeros[0])**float(numeros[1])
      remove(2)
    elif operacao == "rot":
      conta = float(numeros[0])**(1 / float(numeros[1]))
      remove(2)
    elif operacao == "sin":
      conta = math.sin(float(math.radians(float(numeros[0]))))
      remove(1)
    elif operacao == "cos":
      conta = math.cos(float(math.radians(float(numeros[0]))))
      remove(1)

    numeros.append(conta)
    resultados.append(conta)

    if "?" in especiais:
        refaz()
    if len(nomesVariaveis) != 0:
      armazenarVar()


def refaz():
  for especial in especiais:
    if especial == "?":
      numeros.append(resultados[-1])


def remove(n):
  for i in range(n):
    numeros.pop(0)
  operador.pop(0)


def armazenarVar():
  for nome in nomesVariaveis:
    if nome not in variaveis.keys():
      variaveis[nome] = resultados[-1]


def limpa():
  numeros.clear()
  tokens.clear()
  especiais.clear()

def lerArquivo(nomeArquivo):
    arquivo = open(nomeArquivo, "r")
    linhas = arquivo.readlines()
    arquivo.close()
    return linhas
  
if __name__ == '__main__':
  #conta = input("digite o calculo: ")
    conta = []
    diretorio = "Recuperação_linguagem_formal/contas/"

    # lendo cada arquivo do diretorio
    for nomeArquivo in os.listdir(diretorio):
      with open(diretorio + nomeArquivo, "r") as arquivo:
        quantidade = arquivo.readline()
        for i in range(int(quantidade)):
          linha = arquivo.readline()
          linha = re.split(r'\).\(', linha)
          conta.append(linha)
        arquivo.close()
    print(conta)

    TokenInfo.append(('[\?|\(|\)|\|;]', "ESPECIAIS"))
    TokenInfo.append(("\+|\-|\/|\*|sin|cos|rot|exp", "OPERADORES"))
    TokenInfo.append(("[0.-9.]*", "NUMERO"))
    TokenInfo.append(('[A-Za-z0-9]*', "VARIAVEL"))

    for calculo in conta:
        try:
            matcher(calculo)
            str_calculo = ""
            print(f"Linha {conta.index(calculo)+1}: lexemas {lexemas} todos válidos")
            print(f"Linha {conta.index(calculo)+1}: sintaxe: correta")
            print(f"Linha {conta.index(calculo)+1}: resposta: %.3f" % float(resultados[-1]))
            numeros = []
            operador = []
            especiais = []
            resultados = []
            nomesVariaveis = []
            variaveis = {}
            lexemas = []
        except Exception:
            print(f"Linha {conta.index(calculo)+1}: sintaxe: incorreta")

    

