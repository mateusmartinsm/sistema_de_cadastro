import PySimpleGUI as sg
from back import *
from view import layout, popup

def adicionar():
    def idade(data_de_nascimento: str):
        nascimento = datetime.strptime(data_de_nascimento, '%d/%m/%Y')
        hoje = date.today()
        idade = relativedelta(hoje, nascimento).years
        return [idade, 'Sim' if idade >= 18 else 'Não']

    cliente = Cliente(values['-NOME-'], values['-SOBRENOME-'], values['-CPF-'], values['-DATA_DE_NASCIMENTO-'], values['-VAGA-'])
    erro = False
    if '' in cliente.dados:
        campos = ['Nome', 'Sobrenome', 'CPF', 'Data de Nascimento', 'Vaga']
        dados = cliente.dados
        for i, valor in enumerate(dados):
            if valor == '':
                sg.popup_ok(f'O campo "{campos[i]}" é obrigatório. Cliente não adicionado.')
                erro = True
                break
    else:
        c = 0
        vaga = cliente.dados[-1]
        for v in tabela.clientes:
            if vaga in v:
                c += 1
        if c >= consultas.max_cadastros(vaga):
            popup('Esta vaga já atingiu o número máximo de cadastros permitidos.')
            erro = True
    if not erro:
        cliente_adicionado = tabela.adicionar_cliente(cliente.dados)
        for i, cliente in enumerate(tabela.clientes):
            if cliente is tabela.clientes[-1]:
                cliente_novo_valor = cliente[:4] + idade(cliente[3]) + [cliente[4]]
                tabela.clientes = [cliente_novo_valor, i]
        window['-TABELA-'].update(list(tabela.clientes))
        if cliente_adicionado:
            for i in ['-NOME-', '-SOBRENOME-', '-CPF-', '-DATA_DE_NASCIMENTO-', '-VAGA-']:
                window[i].update('')
            window['-NOME-'].set_focus()

sg.theme('DefaultNoMoreNagging')


if __name__ == '__main__':
    tabela = Tabela()
    consultas = Consultas()

    window = sg.Window('Cadastro de clientes XPTO', layout(tabela, consultas.vagas()), element_padding=5)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        if event == '-ADICIONAR-':
            adicionar()
        if event == '-SALVAR-':
            tabela.salvar()
            popup('Clientes cadastrados com sucesso.')
            window['-TABELA-'].update(list(tabela.clientes))


        # event_key_list[event]()
    window.close()