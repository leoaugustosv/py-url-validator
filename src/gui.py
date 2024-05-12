import PySimpleGUI as pg


def init_window():
    # Tema Default da GUI
    pg.theme('Default1')


    # OPÇÕES DE NAVEGADOR NA GUI
    nav_main = [

        
        [pg.Text("Digite abaixo os links a serem validados:", font=('Arial Bold', 16)), pg.Push(),pg.Button("?", font="Arial 12 bold")],
        [pg.Multiline(size=(60,3),key="-LINES-", autoscroll=True, expand_x=True, focus=True , auto_refresh=True)]
    ]

    # OPÇÕES DE SUBMIT NA GUI
    submit_column = [
    [pg.Button("VALIDAR"),pg.Button("CANCELAR", disabled=True),pg.Push(),pg.Button("COPIAR RESULTADO"),pg.Button("EXPORTAR")]
    
    ]

    result_console = [

        
        [pg.Multiline(size=(90,3),key="-RESULT-", autoscroll=True, expand_x=True, focus=True , auto_refresh=True, background_color="#DCDCDC", disabled=True)],
        [pg.Text("Aguardando usuário...", key="-STATUS-"),pg.Push(), pg.ProgressBar(100, orientation='h', expand_x=True, size=(20, 20),  key='-PROGRESS-')]
        
    ]

    # JUNTAR LAYOUT
    layout = [
        [nav_main], 
        [pg.VPush()],
        [submit_column],
        [pg.VPush()],
        [result_console]
    ]

    # RETORNA CONSTRUÇÃO DA JANELA
    return pg.Window("Validador de Links 1.1 - Por Léo", layout)



# DESABILITAR BOTÕES DE AÇÃO
def disableActionButtons(window):
   window['VALIDAR'].update(disabled=True)
   window['COPIAR RESULTADO'].update(disabled=True)
   window['EXPORTAR'].update(disabled=True)
   window['CANCELAR'].update(disabled=False)
   return

# HABILITAR BOTÕES DE AÇÃO
def enableActionButtons(window):
   window['VALIDAR'].update(disabled=False)
   window['COPIAR RESULTADO'].update(disabled=False)
   window['EXPORTAR'].update(disabled=False)
   window['CANCELAR'].update(disabled=True)
   return