from optparse import OptionParser
from collections import defaultdict
import csv
import os
import matplotlib
import numpy as np
from pylatex import Document, NoEscape, Section, Subsection, Command, Figure, Head, MiniPage, PageStyle, Foot,  LargeText, \
    MediumText, LineBreak, simple_page_number, StandAloneGraphic, Package
from pylatex.utils import bold
import pylatex.config as cf
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def plot_graph(avals_t,int_i,int_s):
    q_i = []
    acum = 0
    for i in range(int_i,int_s):
        acum += sum(list(map(int,list(filter(None, avals_t[i])))))
        q_i.append([avals_t[i].count('1'),avals_t[i].count('2'),avals_t[i].count('3'),avals_t[i].count('4'),avals_t[i].count('5')])
    q_i_t = [list(i) for i in zip(*q_i)]
    ind = np.arange(int_s - int_i)
    width = 0.12
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, tuple(q_i_t[0]), width, color='r')
    rects2 = ax.bar(ind + width, tuple(q_i_t[1]), width, color='y')
    rects3 = ax.bar(ind + 2*width, tuple(q_i_t[2]), width, color='g')
    rects4 = ax.bar(ind + 3*width, tuple(q_i_t[3]), width, color='b')
    rects5 = ax.bar(ind + 4*width, tuple(q_i_t[4]), width, color='m')
    ax.set_ylabel('Avaliações')
    ax.set_title('Conceito e Número de Avaliações. Média {:04.2f}.'.format(acum/((int_s - int_i)*5)))
    ax.set_xticks(ind + width / (int_s - int_i))
    question_label = []
    for i in range(int_i,int_s):
        question_label.append('Q{}'.format(i))
    ax.set_xticklabels(tuple(question_label))
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0], rects5[0]), ('Péssimo', 'Ruim', 'Regular', 'Bom', 'Excelente'))

def generate_pdf(n_alunos, n_respostas, avals, cod, prof):
    avals_t = [list(i) for i in zip(*avals)]
    intro = """
    O Centro Acadêmico de Engenharia de Controle e Automação (CAECA) realizou uma pesquisa com os graduandos do curso sobre o desempenho dos professores do departamento nas disciplinas lecionadas. Com o principal objetivo de fornecer um feedback tanto para o departamento como para os professores, para que se possa melhorar o ensino   -aprendizagem do curso.

    A pesquisa foi realizada durante os dias 01/06 a 01/07 e poderia ser respondida online ou através de formulários impressos entregues aos graduandos. Os resultados da pesquisa não serão divulgados e apenas membros do centro acadêmico e os endereçados terão conhecimento dos mesmos. Por fim, somente matérias que obtiveram mais de 25\% de respostas (em relação ao total de alunos matriculados na disciplina) tiveram seus dados levantados e enviados aos respectivos professores.
    """
    resultados = """
    O formulário de pesquisa consiste em 15 perguntas divididas em 5 categorias: Perfil do Professor, Plano de Ensino, Metodologia de Ensino, Auto Avaliação e Crítica/Sugestões. Das 14 perguntas, 13 perguntas são quantitativas de 1 a 5, simbolizando respectivamente péssimo, ruim, regular, bom e excelente e 1 pergunta aberta.
    """
    matriculas = list(filter(None, avals_t[0]))
    participacao = """
    Porcentagem de alunos matriculados na disciplina que responderam à pesquisa: {}\% ({}/{}).

    Alunos que informaram a matrícula: {}.

    Total de alunos que não informaram a matrícula: {}.
    """.format(100*int(n_respostas)/int(n_alunos),n_respostas,n_alunos,', '.join(matriculas), len(avals_t[0])-len(matriculas))
    perfil = """
    Perguntas quantitativas:

    Q1. Qual é o grau de comprometimento do professor quanto ao horário de aula?

    Q2. O professor disponibiliza um horário extra para esclarecer dúvidas?

    Q3. O professor apresenta domínio do assunto ministrado?
    """
    plano = """
    Perguntas quantitativas:

    Q4. O professor apresenta um cronograma completo de aulas e avaliações?

    Q5. O professor corrige as provas e trabalhos dentro do prazo?

    Q6. São apresentados materiais/bibliografias sobre o conteúdo estudado?
    """
    metodologia = """
    Perguntas quantitativas:

    Q7. O professor é claro na explicação do conteúdo?

    Q8. O professor mostrou ter didática adequada?

    Q9. O professor procura trazer exemplos reais de engenharia nos problemas estudados?

    Q10. O conteúdo das avaliações estavam de acordo com o que foi ensinado?

    Q11. O método de avaliação é condizente com a disciplina?
    """
    auto = """
    Perguntas quantitativas :

    Q12. Sinto motivado a comparecer nas aulas?

    Q13. Sinto que consegui aprender o conteúdo que foi ensinado?
    """
    comments = list(filter(None, avals_t[14]))
    if len(comments) == 0 : comments.append("Nenhum comentário registrado.")
    sugestoes = """
    Foram recebidos os seguintes comentários:

    """
    '''
    q_i = []
    for i in range(1,4):
        q_i.append([avals_t[i].count('1'),avals_t[i].count('2'),avals_t[i].count('3'),avals_t[i].count('4'),avals_t[i].count('5')])
    q_i_t = [list(i) for i in zip(*q_i)]
    N = 3
    ind = np.arange(N)
    width = 0.12
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, tuple(q_i_t[0]), width, color='r')
    rects2 = ax.bar(ind + width, tuple(q_i_t[1]), width, color='y')
    rects3 = ax.bar(ind + 2*width, tuple(q_i_t[2]), width, color='g')
    rects4 = ax.bar(ind + 3*width, tuple(q_i_t[3]), width, color='b')
    rects5 = ax.bar(ind + 4*width, tuple(q_i_t[4]), width, color='m')

    ax.set_ylabel('Avaliações')
    ax.set_title('Conceito e Número de Avaliações')
    ax.set_xticks(ind + width / 3)
    ax.set_xticklabels(('Q1', 'Q2', 'Q3'))
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0], rects5[0]), ('Péssimo', 'Ruim', 'Regular', 'Bom', 'Excelente'))
    '''
    geometry_options = {
        "head": "40pt",
        "margin": "0.5in",
        "bottom": "0.6in",
        "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(Package('float'))
    header = PageStyle("header")
    with header.create(Head("C")):
        logo_file = os.path.join(os.path.dirname(__file__),'logo.png')
        header.append(StandAloneGraphic(image_options="width=360px", filename=logo_file))
    with header.create(Foot("C")):
        header.append("Universidade Federal de Santa Catarina – Conselho de Entidades do Centro Tecnológico – Campus Universitário, S/N - CEP 88045-108 – Florianópolis/SC –  (48) 3721-7698")

    doc.preamble.append(header)
    doc.change_document_style("header")
    with doc.create(MiniPage(align='c',width=r"0.9\textwidth")):
        doc.append(LargeText(bold('Avaliação da disciplina {} ministrada pelo professor {}'.format(cod,prof))))
        doc.append(LineBreak())
        doc.append(LineBreak())
        doc.append(MediumText(bold('CAECA')))
        doc.append(LineBreak())
    with doc.create(Section('Introdução')):
        doc.append(NoEscape(intro))
    with doc.create(Section('Resultados')):
        doc.append(NoEscape(resultados))
        with doc.create(Subsection('Participação da Pesquisa')):
            doc.append(NoEscape(participacao))
        with doc.create(Subsection('Perfil do Professor')):
            doc.append(NoEscape(perfil))
            plot_graph(avals_t,1,4)
            with doc.create(Figure(position='H')) as plot:
                plot.add_plot(width=NoEscape(r'0.5\textwidth'))
                #plot.add_caption('')
        with doc.create(Subsection('Plano de Ensino')):
            doc.append(NoEscape(plano))
            plot_graph(avals_t,4,7)
            with doc.create(Figure(position='H')) as plot:
                plot.add_plot(width=NoEscape(r'0.5\textwidth'))
        with doc.create(Subsection('Metodologia de Ensino e Avaliação')):
            doc.append(NoEscape(metodologia))
            plot_graph(avals_t,7,12)
            with doc.create(Figure(position='H')) as plot:
                plot.add_plot(width=NoEscape(r'0.5\textwidth'))
        with doc.create(Subsection('Auto Avaliação')):
            doc.append(NoEscape(auto))
            plot_graph(avals_t,12,14)
            with doc.create(Figure(position='H')) as plot:
                plot.add_plot(width=NoEscape(r'0.5\textwidth'))
        with doc.create(Subsection('Críticas/Sugestões')):
            doc.append(NoEscape(sugestoes))
            for comentario in comments:
                doc.append(NoEscape('"{}"'.format(comentario)))
                doc.append(NoEscape('\n'))
    doc.generate_pdf('Avaliacao_{}_{}'.format(cod,prof), clean_tex=False)
def main():
    usage = """%prog arquivos
    Os arquivos devem ser .csv codificados como UTF-8 e separados por ','.
    O programa requer ao menos um .csv. Os nomes dos arquivos devem conter o código da disciplina e o número de alunos separados por '-'.
    Notação do arquivo: XXX1000-50.csv
    """
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.error("Pelo menos um .csv requerido.")
    for arquivo in args:
        try:
            disciplina, alunos = arquivo.strip(".csv").split('-')
            dados = defaultdict(list)
            respostas = 0
            with open(arquivo, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    dados[disciplina,row[0]].append(row[1:])
                    respostas += 1
            for cod, prof in dados.keys():
                generate_pdf(alunos, respostas, dados[cod, prof], cod, prof)
        except ValueError:
            print("O nome do arquivo {} está no padrão código-alunos.csv?".format(arquivo))
        except FileNotFoundError:
            print("Arquivo {} não encontrado.".format(arquivo))
        except UnicodeDecodeError:
            print("Erro decodificando arquivo. Certeza que {} é um .csv UTF-8 com delimitador ','?".format(arquivo))
        except Exception as e:
            print("Erro muito bizarro. Chama o Fidel para dar uma olhada. Bate print do erro.")
            raise e

if __name__ == "__main__":
    main()
