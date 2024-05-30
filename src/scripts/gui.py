import PySimpleGUI as pg


def init_window():
    # Tema Default da GUI
    pg.theme('Default1')


    # OPÇÕES DE NAVEGADOR NA GUI
    nav_main = [

        
        [pg.Text("Digite abaixo os links a serem validados:", font=('Arial Bold', 16)), pg.Push(),pg.Button("?", font="Arial 12 bold")],
        [pg.Multiline(size=(60,5),key="-LINES-", autoscroll=True, expand_x=True, focus=True , auto_refresh=True)]
    ]

    # OPÇÕES DE SUBMIT NA GUI
    submit_column = [
    [pg.Button("VALIDAR"),pg.Button("CANCELAR", disabled=True),pg.Push(),pg.Button("COPIAR RESULTADO", disabled=True),pg.Button("EXPORTAR", disabled=True)]
    
    ]

    result_console = [

        
        [pg.Multiline(size=(90,5),key="-RESULT-", autoscroll=True, expand_x=True, focus=True , auto_refresh=True, background_color="#DCDCDC", disabled=True)],
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
    return pg.Window("Validador de Links 1.1.3 - Por leoaugustosv", layout)



# DESABILITAR BOTÕES DE AÇÃO
def disable_action_buttons(WINDOW):
   WINDOW['VALIDAR'].update(disabled=True)
   WINDOW['COPIAR RESULTADO'].update(disabled=True)
   WINDOW['EXPORTAR'].update(disabled=True)
   WINDOW['CANCELAR'].update(disabled=False)
   return

# HABILITAR BOTÕES DE AÇÃO
def enable_action_buttons(WINDOW):
   WINDOW['VALIDAR'].update(disabled=False)
   WINDOW['COPIAR RESULTADO'].update(disabled=False)
   WINDOW['EXPORTAR'].update(disabled=False)
   WINDOW['CANCELAR'].update(disabled=True)
   return