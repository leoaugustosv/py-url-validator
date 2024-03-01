import requests
import PySimpleGUI as pg
import time
import pandas as pd
import os
import pyperclip
import re

from tkinter import filedialog
from datetime import datetime

#print (os.getcwd())


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

window = pg.Window("Validador de Links 1.0 - Por Léo", layout)

# Definindo variáveis e vetores

# Inicializando variáveis
erro = ""
output = ""
generatedDataFrame = False
firstColumn = "URL\tSTATUS"

# FUNÇÕES

def disableActionButtons():
   window['VALIDAR'].update(disabled=True)
   window['COPIAR RESULTADO'].update(disabled=True)
   window['EXPORTAR'].update(disabled=True)
   window['CANCELAR'].update(disabled=False)
   return

def enableActionButtons():
   window['VALIDAR'].update(disabled=False)
   window['COPIAR RESULTADO'].update(disabled=False)
   window['EXPORTAR'].update(disabled=False)
   window['CANCELAR'].update(disabled=True)
   return



# INICIAR LOOP PARA MANTER JANELA ABERTA
while True:
    event, values = window.read()

   # FINALIZAR LOOP SE CANCELAR OU FECHAR JANELA
    if event == pg.WIN_CLOSED:
      break
   
    if event == "?":
      pg.popup("Insira os links separados por linha e clique em validar.\n", title="Como usar")
      continue
   


# https://catalogcdns3.ulife.com.br/DisciplineFiles/PlanosEnsino/LEGEVA_9009.pdf
# https://catalogcdns3.ulife.com.br/DisciplineFiles/PlanosEnsino/LEGEVA_8997.pdf



# SELECIONAR WEBSITE 
   
    # DEBUG
    print(event)
    print(values)

   # INICIAR EVENTO DE "IR" 
    if event == "VALIDAR":
      tempoInicio = time.perf_counter()
      window["-RESULT-"].update('')
      disableActionButtons()
      window["-STATUS-"].update("Inicializando verificação...",text_color="navy")
      firstColumn = "URL\tSTATUS"
      lineNumber = 0
      generatedDataFrame = False
      df2 = pd.DataFrame()
      try:


          linksList = str(values["-LINES-"]).split(f"\n")

          print (linksList)

          if linksList[0] == '' :
            pg.Popup("Erro: Verifique os espaços em branco antes de continuar.\n", title="Erro")
            window["-STATUS-"].update("Aguardando usuário...",text_color="black")
            enableActionButtons()
            continue
          

          datatest = pd.DataFrame(columns=['URL', 'CÓDIGO', 'STATUS'])
          print(datatest)
          

          
          for l in linksList:

              try:

                verifiedURL = l
                isURLValid = 0
                window["-STATUS-"].update(f"Verificando URLs. Aguarde...", text_color="olive")

                print(l)

                #Regex para verificar se o link começa com HTTP ou HTTPS, se depois tem "://", e se termina com ".com" (ou algo a mais além disso)
                if re.match(r"^https?://.*\.com(?:/.*)?$", l):
                    verifiedURL = l
                    print("caught in Regex 1: ",verifiedURL)
                
                #Regex para verificar se o link NÃO começa com (HTTP ou HTTPS) e "://", OU se NÃO termina com ".com" (ou algo a mais além disso)
                elif re.match(r"^(?!https?://|.*\.com.*$).*", l):
                    verifiedURL = f"https://{l}.com"
                    print("caught in Regex 2: ",verifiedURL)

                #Regex para verificar se o link NÃO começa com HTTP ou HTTPS e "://", mas termina com ".com" --- E VICE VERSA
                elif re.match(r"^(?!https?://).*\.com.*$", l):
                    verifiedURL = f"https://{l}"
                    print("caught in Regex 3: ",verifiedURL)

                #Regex para verificar se o link começa com HTTP ou HTTPS e depois tem "://", mas NÃO termina com ".com"
                elif re.match(r"^(https?://)(?:(?!\.com).)*$", l):
                    verifiedURL = f"{l}.com"
                    print("caught in Regex 4: ",verifiedURL)

                #Se o link estiver incorreto, vai ser transformado em uma string vazia para pular a verificação e informar o usuário que a linha está vazia 
                if verifiedURL == "https://.com":
                   verifiedURL = ""
                   print("caught in blank replace: ",verifiedURL)

                print ("O L agora é:", verifiedURL)
                print (type(verifiedURL))
                
                requestURLResult = requests.get(verifiedURL)
                print(requestURLResult)

                requestURLCodeSplit1 = str(requestURLResult).replace("<Response [","")
                print(requestURLCodeSplit1)

                requestURLCode = str(requestURLCodeSplit1).replace("]>","")
                print(requestURLCode)
                      
                if str(requestURLResult) == "<Response [200]>":
                    simpleResult = "OK"
                elif str(requestURLResult) == "<Response [403]>":
                    simpleResult = "ERRO"
                elif str(requestURLResult) != "<Response [200]>" and str(requestURLResult) != "<Response [403]>":
                    isURLValid = 1
              
              
              except requests.exceptions.MissingSchema :
                  isURLValid = 2
                  requestURLResult = "Invalid"
              
              except requests.exceptions.ConnectionError:
                  window["-STATUS-"].update("Erro de conexão. Verifique sua conexão com a internet e tente novamente.",text_color="red")
                  pg.Popup(f"Erro de conexão. Abortando validação...")
                  continue
              
              if isURLValid == 0 :
                simpleResult = simpleResult
              elif isURLValid == 1 :
                simpleResult = f"VERIFICAR - {requestURLCode}"
              elif isURLValid == 2 :
                print (str(requestURLResult))
                simpleResult = "INVÁLIDO"


                if verifiedURL == "":
                   verifiedURL = "URL Vazia"
                else:
                   pass
              # firstIndexOfElement = linksList.index(l)
              # lastIndexOfElement = (len(linksList) - 1 - linksList[::-1].index(l))+1
              # window["-RESULT-"].print(f"Linha {int(lastIndexOfElement)}: {l} - {simpleResult}")
              
              lineNumber = lineNumber + 1
              window["-RESULT-"].print(f"Linha {lineNumber}: {verifiedURL} - {simpleResult}")

              output = f"{output}\nLinha {int(linksList.index(l))+1}: {verifiedURL} - {simpleResult}"
              firstColumn = f"{firstColumn}\n{l}\t{simpleResult}"

              if requestURLResult == "Invalid":
                 d = {'URL':[l],'CÓDIGO':'null', 'STATUS':[simpleResult]}
              elif requestURLResult != "Invalid":
                 d = {'URL':[verifiedURL],'CÓDIGO':[requestURLCode], 'STATUS':[simpleResult]}

              df = pd.DataFrame(data=d)
              df2 = pd.concat([df,df2])
              generatedDataFrame = True
              
          
          tempoFinal = time.perf_counter()
          window["-STATUS-"].update(f"Verificação finalizada!",text_color="green")
          window["-STATUS-"].print(f"\nTempo decorrido: {tempoFinal-tempoInicio:0.2f} segundos")
          enableActionButtons()
      except Exception as err:
          print("1:",Exception)
          pg.Popup(f"Erro: {err}\n\nPor favor, envie ao desenvolvedor (Léo) um print dessa tela.\n\nO programa será fechado agora.", title="Erro")
          generatedDataFrame = False
          print(firstColumn)
          #break
          raise(err)
          
    
    elif event == "COPIAR RESULTADO":
        if firstColumn != "URL\tSTATUS":
          pyperclip.copy(firstColumn)
          window["-STATUS-"].update(f"Resultado copiado para a área de transferência!",text_color="green")
        
        elif firstColumn == "URL\tSTATUS":
          pg.Popup(f"Erro: Valide pelo menos uma URL antes de copiar o resultado.\n", title="Erro")
          window["-STATUS-"].update("Aguardando usuário...",text_color="black")
          enableActionButtons()
          continue


    elif event == "EXPORTAR":
      
      


      if generatedDataFrame == True:
        disableActionButtons()  
        df2.set_index("URL", inplace=True)
        nowDate = datetime.now()
        dateString = nowDate.strftime("%d-%m-%Y--%H-%M-%S.%f")

        filename = (filedialog.asksaveasfilename(initialfile=dateString, initialdir=os.getcwd(), title = 'Exportar arquivo', filetypes=(('Excel File', '.xlsx'),('All Files','*.*')))+".xlsx")   
        if filename == ".xlsx":
           continue
        else:
           pass

        print(filename)

        print(f"SELECTED PATH: {filename}")
        df2.to_excel(filename, engine="xlsxwriter", sheet_name="ExportResults")
        window["-STATUS-"].update(f"Arquivo exportado com sucesso!\nCaminho: {filename}.",text_color="green")
        enableActionButtons()
      elif generatedDataFrame == False:
        pg.Popup(f"Erro: Valide pelo menos uma URL antes de exportar o resultado.\n", title="Erro")
        window["-STATUS-"].update("Aguardando usuário...",text_color="black")
        enableActionButtons()
        continue


    elif event == "CANCELAR":
       enableActionButtons()
       continue
   # ERROS 





   # COMANDOS: Virtual Environment

   # 1. python -m venv env
   # 2. cd caminhodoprojeto
   # 3. Set-ExecutionPolicy Unrestricted -Scope Process
   # 4. env/Scripts/Activate.ps1
   # 5. Set-ExecutionPolicy Default -Scope Process


   # DEBUG
   # EXE: pyinstaller  3-fetch_dataurl-onepertime.py -F --noconsole --clean
   
   
window.close()