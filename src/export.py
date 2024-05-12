import os
import pandas as pd
import PySimpleGUI as pg
import gui

from tkinter import filedialog
from datetime import datetime

def To_xlsx(df2,isDataFrameReady,window):
    if isDataFrameReady == True:
        gui.disableActionButtons(window)
        
        #TODO: CORRIGIR BUG ONDE SÓ É POSSÍVEL EXPORTAR UMA VEZ A CADA VALIDAÇÃO
        df2.set_index("URL", inplace=True)
        nowDate = datetime.now()
        dateString = nowDate.strftime("%d-%m-%Y--%H-%M-%S.%f")

        filename = (filedialog.asksaveasfilename(initialfile=dateString, initialdir=os.getcwd(), title = 'Exportar arquivo', filetypes=(('Excel File', '.xlsx'),('All Files','*.*')))+".xlsx")   
        
        #Se o prompt for cancelado, não terá nome. Retorna falso antes de continuar para cancelar export
        if filename == ".xlsx":
            window["-STATUS-"].update(f"Ação de exportar cancelada!",text_color="green")
            gui.enableActionButtons(window)
            return False
        else:
            pass


        print(f"SELECTED PATH: {filename}")
        df2.to_excel(filename, engine="xlsxwriter", sheet_name="ExportResults")
        window["-STATUS-"].update(f"Arquivo exportado com sucesso!\nCaminho: {filename}.",text_color="green")
        gui.enableActionButtons(window)
        return True

    elif isDataFrameReady == False:
        pg.Popup(f"Erro: Valide pelo menos uma URL antes de exportar o resultado.\n", title="Erro")
        window["-STATUS-"].update("Aguardando usuário...",text_color="black")
        gui.enableActionButtons(window)
        
        return False
        