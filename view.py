import PySimpleGUI as sg

tamanho_botao = 11

def layout(tabela: object, vagas: list):
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    dias = ['DOM', 'SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB']
    tabela_itens = tabela.clientes if tabela.clientes != [] else [['Nenhum cliente adicionado']]
    tabela_headers = ['Nome', 'Sobrenome', 'CPF', 'Data de nascimento', 'Idade', 'É maior de idade?', 'Vaga']

    return [
        [sg.Frame('Formulário', [
            [sg.Sizer(v_pixels=5)],
            [sg.Column([
                [sg.Text('Nome:')], 
                [sg.Text('Sobrenome:')],
                [sg.Text('CPF:')],
                [sg.Text('Data de Nascimento:')],
                [sg.Text('Vaga:')]
            ]), sg.Column([
                [sg.Input(key='-NOME-', expand_x=True)],
                [sg.Input(key='-SOBRENOME-', expand_x=True)],
                [sg.Input(key='-CPF-', expand_x=True)],
                [sg.Input(key='-DATA_DE_NASCIMENTO-'), sg.CalendarButton('Calendário', default_date_m_d_y=(1, 1, 2000), size=tamanho_botao, format='%d/%m/%Y', month_names=meses, day_abbreviations=dias)],
                [sg.Combo(vagas, expand_x=True, key='-VAGA-')]
            ], element_justification='right')],
            [sg.Sizer(479), sg.Button('ADICIONAR', size=tamanho_botao, key='-ADICIONAR-')]
        ], pad=(10, 15), expand_x=True, element_justification='center')],
        [sg.Column([
            [sg.Table(tabela_itens, tabela_headers, auto_size_columns=False, num_rows=15, def_col_width=15, justification='center', expand_x=True, key='-TABELA-')],
            [sg.Button('SALVAR', size=tamanho_botao, key='-SALVAR-')]
        ], element_justification='right')]
    ]

def popup(mensagem):
    sg.popup_ok(mensagem)