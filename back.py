import sqlite3
from view import popup
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

db = sqlite3.connect('XPTO_database.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS clientes(id INTEGER PRIMARY KEY, nome TEXT NOT NULL, sobrenome TEXT NOT NULL, cpf TEXT NOT NULL, data_de_nascimento TEXT NOT NULL, vaga TEXT NOT NULL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS vagas(id INTERGER PRIMARY KEY, cargo TEXT NOT NULL, vagas_disponiveis INTEGER NOT NULL, candidatos_por_vaga INTERGER NOT NULL)''')
db.commit()

class Consultas:
    def clientes(self):
        cursor.execute('SELECT * FROM clientes')
        return cursor.fetchall()

    def vagas(self):
        cursor.execute('SELECT cargo FROM vagas')
        vagas = cursor.fetchall()
        return vagas if vagas != [] else ['Nenhuma vaga disponível']

    def max_cadastros(self, vaga):
        cursor.execute(f'SELECT vagas_disponiveis, candidatos_por_vaga FROM vagas WHERE cargo = "{vaga}"')
        vagas, cand_p_vaga = cursor.fetchall()[0]
        return vagas * cand_p_vaga


class Cliente:
    def __init__(self, nome: str, sobrenome: str, cpf: str, data_de_nascimento: str, vaga: str):
        self.__nome = nome.strip()
        self.__sobrenome = sobrenome.strip()
        self.__cpf = cpf.strip()
        self.__data_de_nascimento = data_de_nascimento.strip()
        self.__vaga = vaga[0] if vaga != '' else vaga

    @property
    def dados(self):
        if list(self.__dict__.values()).count('') != 5:
            return [self.__nome, self.__sobrenome, self.__cpf, self.__data_de_nascimento, self.__vaga]
        return ['', '', '', '', '']
 

    def idade(self):
        data_de_nascimento = datetime.strptime(self.__data_de_nascimento, '%d/%m/%Y')
        hoje = date.today()
        idade = relativedelta(hoje, data_de_nascimento).years
        return idade

class Tabela:
    def __init__(self):
        self.__vagas = None
        self.__clientes = []

    def adicionar_cliente(self, dados_do_cliente: list):
        if self.__clientes == [] or self.__dados_validos(dados_do_cliente):
            self.__clientes.append(dados_do_cliente)
            return True
        popup('Este CPF já está cadastrado.')
        return False

    def __dados_validos(self, dados_do_cliente):
        cursor.execute('SELECT cpf FROM clientes')
        cpfs_cadastrados = cursor.fetchall()

        for cliente in self.__clientes:
            cpfs_cadastrados.append(cliente[2])
            if dados_do_cliente[2] in cpfs_cadastrados:
                return False
        return True

    def adicionar_vaga(self, vaga):
        self.__vagas.append(vaga)

    def salvar(self):
        for cliente in self.__clientes:
            cursor.execute('INSERT INTO clientes VALUES(NULL, ?, ?, ?, ?, ?)', (cliente[:-3] + [cliente[-1]]))
        db.commit()
        self.__clientes = []

    @property
    def clientes(self):
        return list(self.__clientes)

    @property
    def cargos(self):
        return self.__vagas

    @clientes.setter
    def clientes(self, cliente):
        indice = cliente[1]
        self.__clientes[indice] = cliente[0]

class Vaga:
    def __init__(self, cargo: str, vagas_disponiveis: int, candidatos_por_vaga: int):
        self.__cargo = cargo
        self.__vagas_disponiveis = vagas_disponiveis
        self.__candidatos_por_vaga = candidatos_por_vaga

        cursor.execute('INSERT INTO vagas VALUES(NULL, ?, ?, ?)', (self.__cargo, self.__vagas_disponiveis, self.__candidatos_por_vaga))
        db.commit()