# Importa o módulo sqlite3 para trabalhar com banco de dados SQLite
import sqlite3

# Nome do arquivo do banco de dados
db_name = 'quiz.sqlite'

# Variáveis globais para conexão e cursor do banco
conn = None
cursor = None

# Função para abrir a conexão com o banco e criar o cursor
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)  # Conecta ao banco de dados
    cursor = conn.cursor()  # Cria o cursor para executar comandos SQL

# Função para fechar a conexão com o banco de dados
def close():
    cursor.close()  # Fecha o cursor
    conn.close()    # Fecha a conexão

# Função para executar uma query SQL simples e fazer commit
def do(query):
    cursor.execute(query)  # Executa a query
    conn.commit()          # Salva as alterações

# Função que apaga todas as tabelas do banco
def clear_db():
    '''Apaga todas as tabelas'''
    open()
    # Remove a tabela quiz_content se ela existir
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    # Remove a tabela question se ela existir
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    # Remove a tabela quiz se ela existir
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

# Função que cria as tabelas do banco de dados
def create():
    open()
    # Ativa as chaves estrangeiras (FOREIGN KEY)
    cursor.execute('''PRAGMA foreign_keys=on''')

    # Cria a tabela quiz, se não existir
    do('''CREATE TABLE IF NOT EXISTS quiz (
           id INTEGER PRIMARY KEY,
           name VARCHAR)''')

    # Cria a tabela question, se não existir
    do('''CREATE TABLE IF NOT EXISTS question (
               id INTEGER PRIMARY KEY,
               question VARCHAR,
               answer VARCHAR,
               wrong1 VARCHAR,
               wrong2 VARCHAR,
               wrong3 VARCHAR)''')

    # Cria a tabela de associação entre quiz e perguntas
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
               id INTEGER PRIMARY KEY,
               quiz_id INTEGER,
               question_id INTEGER,
               FOREIGN KEY (quiz_id) REFERENCES quiz (id),
               FOREIGN KEY (question_id) REFERENCES question (id) )''')
    close()

# Função que insere perguntas no banco de dados
def add_questions():
    questions = [
        ('Qual animal é conhecido por dormir de olhos abertos?', 'Peixe', 'Gato', 'Coruja', 'Cachorro'),
        ('O que é algo que quanto mais se tira, maior fica?', 'Buraco', 'Tempo', 'Memória', 'Espaço'),
        ('Qual objeto pode quebrar mesmo sem ser tocado?', 'Silêncio', 'Vidro', 'Espelho', 'Gelo'),
        ('O que acontece uma vez por minuto, duas vezes por momento, mas nunca em mil anos?', 'A letra M', 'O tempo', 'A respiração', 'A memória'),
        ('Se você tem apenas um fósforo e entra em um quarto escuro com uma vela, uma lamparina e uma lareira, o que você acende primeiro?', 'O fósforo', 'A vela', 'A lareira', 'A lamparina'),
        ('O que sobe mas nunca desce?', 'Idade', 'Temperatura', 'Balão', 'Pressão'),
    ]
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()

# Função que insere quizzes no banco de dados
def add_quiz():
    # Lista de quizzes (nome)
    quizes = [
        ('Own game', ),
        ('Who wants to be a millionaire?', ),
        ('The smartest', )
    ]
    open()
    # Insere todos os quizzes na tabela quiz
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()

# Função que associa perguntas a quizzes
def add_links():
    open()
    # Ativa verificação de chaves estrangeiras
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    
    # Solicita ao usuário se deseja adicionar links
    answer = input("Add a link (y/n)?")
    while answer != 'n':
        quiz_id = int(input("quiz id: "))  # ID do quiz
        question_id = int(input("question id: "))  # ID da pergunta
        # Associa a pergunta ao quiz
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Add a link (y/n)?")
    close()

# Função que exibe todos os dados de uma tabela
def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())  # Exibe todos os registros da tabela
    close()

# Função que mostra todas as tabelas com seus dados
def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

# Função que retorna a próxima pergunta de um quiz após uma pergunta específica
def get_question_after(question_id = 0, quiz_id=1):
    '''
    Retorna a próxima pergunta após o ID informado,
    para um determinado quiz. Se ID for 0, retorna a primeira.
    '''
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id '''
    cursor.execute(query, [question_id, quiz_id] )
    result = cursor.fetchone()  # Retorna apenas a próxima pergunta
    close()
    return result

# Função principal que organiza a execução
def main():
    clear_db()         # Apaga as tabelas existentes
    create()           # Cria as tabelas do banco
    add_questions()    # Adiciona as perguntas
    add_quiz()         # Adiciona os quizzes
    add_links()        # Associa perguntas aos quizzes
    show_tables()      # Exibe os dados das tabelas
    # Exibe no console a próxima pergunta após a de ID 3 no quiz de ID 1
    print(get_question_after(3, 1))

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()
