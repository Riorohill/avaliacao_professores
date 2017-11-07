from optparse import OptionParser
from collections import defaultdict
import csv

def main():
    usage = """
    uso: %prog arquivos"
    Os arquivos devem ser .csv codificados como UTF-8 e separados por ','.
    O programa requer ao menos um .csv.
    """
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.error("Pelo menos um .csv requerido.")
    for arquivo in args:
        try:
            dados = defaultdict(list)
            disciplina, alunos = arquivo.strip(".csv").split('-')
            respostas = 0
            with open(arquivo, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    dados[disciplina,row[0]].append(row[1:])
                    respostas += 1
                print (disciplina, alunos)
                print (respostas)
        except FileNotFoundError:
            print("Arquivo {} não encontrado.".format(arquivo))
        except UnicodeDecodeError:
            print("Erro decodificando arquivo. Certeza que {} é um .csv UTF-8 com delimitador ','?".format(arquivo))
        except Exception as e:
            print("Erro muito bizarro. Chama o Fidel para dar uma olhada. Bate print do erro.")
            raise e
            #ybase = {(1234,"Roger"), [(5,3,3,3,3,3,1)]}

if __name__ == "__main__":
    main()
