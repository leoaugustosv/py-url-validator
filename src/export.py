import os
import PySimpleGUI as pg
import gui

from tkinter import filedialog
from datetime import datetime

def To_xlsx(df2,is_dataframe_ready,WINDOW):
    if is_dataframe_ready == True:
        gui.disableActionButtons(WINDOW)
        now_date = datetime.now()
        DATE_STRING_FORMAT = now_date.strftime("%d-%m-%Y--%H-%M-%S.%f")

        filename = (filedialog.asksaveasfilename(initialfile=DATE_STRING_FORMAT, initialdir=os.getcwd(), title = 'Exportar arquivo', filetypes=(('Excel File', '.xlsx'),('All Files','*.*')))+".xlsx")   
        
        #Se o export for cancelado, não terá nome. Retorna falso antes de continuar para cancelar export
        if filename == ".xlsx":
            WINDOW["-STATUS-"].update(f"Ação de exportar cancelada!",text_color="green")
            gui.enableActionButtons(WINDOW)
            return False
        
        elif filename.endswith(".xlsx.xlsx"):
            filename.replace(".xlsx.xlsx",".xlsx")



        print(f"SELECTED PATH: {filename}")
        df2.to_excel(filename, engine="xlsxwriter", sheet_name="ExportResults")
        WINDOW["-STATUS-"].update(f"Arquivo exportado com sucesso!\nCaminho: {filename}.",text_color="green")
        gui.enableActionButtons(WINDOW)
        return True

    elif is_dataframe_ready == False:
        pg.Popup(f"Erro: Valide pelo menos uma URL antes de exportar o resultado.\n", title="Erro")
        WINDOW["-STATUS-"].update("Aguardando usuário...",text_color="black")
        gui.enableActionButtons(WINDOW)
        
        return False
        