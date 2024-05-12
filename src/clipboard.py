import gui
import pyperclip
import PySimpleGUI as pg

# Checar se a variável que armazena os resultados gerados possui apenas as colunas iniciais
# Não copiar para a área de transferência e avisar ao usuário para realizar uma validação antes.
# Por fim, atualizar o status para refletir a ação tomada pelo programa.
def copyResultToClipboard(clipboard_Str, window):
    if clipboard_Str != "URL\tSTATUS":
        pyperclip.copy(clipboard_Str)
        window["-STATUS-"].update(f"Resultado copiado para a área de transferência!",text_color="green")
        
    elif clipboard_Str == "URL\tSTATUS":
        pg.Popup(f"Erro: Valide pelo menos uma URL antes de copiar o resultado.\n", title="Erro")
        window["-STATUS-"].update("Aguardando usuário...",text_color="black")
        gui.enableActionButtons(window)
        