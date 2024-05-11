# Imports de bibliotecas
import requests
import time
import PySimpleGUI as pg
import pandas as pd
import os
import pyperclip


# Imports de funcionalidades específicas
from tkinter import filedialog # Dialog para selecionar caminho de arquivo
from datetime import datetime # Para verificar data e hora do sistema

# Imports de arquivos
import gui
import validation

#print (os.getcwd())


# Armazena a janela atual na variável "window"
window = gui.init_window()


# Inicializando variáveis
erro = ""
output = ""
generatedDataFrame = False
firstColumn = "URL\tSTATUS" #Inicializando as colunas do resultado


# INICIAR LOOP PARA MANTER JANELA ABERTA
while True:
    event, values = window.read() # Leitura e eventos da janela atual

   # FINALIZAR LOOP SE CANCELAR OU FECHAR JANELA
    if event == pg.WIN_CLOSED:
      break
   
    if event == "?":
      pg.popup("Insira os links separados por linha e clique em validar.\n", title="Como usar")
      continue
   

   # INICIAR EVENTO DE "VALIDAR LINKS" 
    if event == "VALIDAR":

      # Inicializar contador de tempo de validação
      tempoInicio = time.perf_counter()

      # Limpar espaço de output, desabilitar botões de ação e atualizar status do programa
      window["-RESULT-"].update('')
      gui.disableActionButtons(window)
      window["-STATUS-"].update("Inicializando verificação...",text_color="navy")

      # Armazenar se o dataframe já foi gerado (para permitir exportação) + inicializando dataframe
      requestURLResult = ""
      lineNumber = 0              
      generatedDataFrame = False  
      df2 = pd.DataFrame()        #TODO: VERIFICAR NECESSIDADE

      try:

          # Armazena em uma list todas as linhas inseridas, separando por quebra de linhas
          linksList = str(values["-LINES-"]).split(f"\n")
          
          # Valida se a primeira linha está vazia e alerta ao usuário sobre espaços em branco
          # Não inicia a validação até que a primeira linha tenha conteúdo
          if validation.LinksList_IsEmpty(linksList,window):
            continue
          

          # Se a primeira linha não estiver vazia, inicializa um dataframe contendo as colunas
          else:
            datatest = pd.DataFrame(columns=['URL', 'CÓDIGO', 'STATUS'])
          
          
          for l in linksList:

              # 
              try:

                # Função para validar link atual usando regex, e ajustar a depender da condição
                # Depois, armazenar link validado na variável "verifiedURL"
                # Passa o link e a janela atual como parâmetros
                verifiedURL = validation.Get_URLString_Regex(l,window)

                # Função para verificar o código resultando da GET request, e retornar uma string com o resultado
                
                # Armazenar resultado na variável "requestURLCode"
                requestURLCode = validation.Get_URLRequest_Code(verifiedURL)


                # Criar "simpleResult" para armazenar um resultado simples e de fácil entendimento ao usuário
                simpleResult = validation.Get_ResultToString(requestURLCode)


              # EXCEPTION DE URL INVÁLIDO 1 - servem de último recurso caso alguma validação de regex falhe
              # Caso essa exception ocorra, marca o resultado simples e o código como inválidos, e sinaliza o link como vazio.
              except requests.exceptions.MissingSchema:
                  requestURLResult = "Invalid"
                  simpleResult = "INVÁLIDO"
                  
                  if verifiedURL == "":
                   verifiedURL = "URL Vazia"
                  else:
                    pass

              # EXCEPTION DE URL INVÁLIDO 2 - servem de último recurso caso alguma validação de regex falhe
              # Caso essa exception ocorra, marca o resultado simples e o código como inválidos, e sinaliza o link como vazio.
              except requests.exceptions.InvalidURL:
                  requestURLResult = "Invalid"
                  simpleResult = "INVÁLIDO"
                  
                  if verifiedURL == "":
                   verifiedURL = "URL Vazia"
                  else:
                    pass
              
              # EXCEPTION DE CONEXÃO - interrompe a validação.
              except requests.exceptions.ConnectionError:
                  window["-STATUS-"].update("Erro de conexão. Verifique sua conexão com a internet e tente novamente.",text_color="red")
                  pg.Popup(f"Erro de conexão. Abortando validação...")
                  continue
              
              
              # Incrementando número da linha atual para exibir corretamente no output
              lineNumber += 1


              # Atualizando caixa de resultado (output)
              window["-RESULT-"].print(f"Linha {lineNumber}: {verifiedURL} - {simpleResult}")
              output = f"{output}\nLinha {int(linksList.index(l))+1}: {verifiedURL} - {simpleResult}" #TODO: VERIFICAR NECESSIDADE

              # Incrementando a cada loop as infos de validação na variável "firstColumn"
              # Ela é usada para validar mais abaixo se há conteúdo a ser copiado para o CTRL+C ou não
              # Caso haja conteúdo, o pyperclip copia direto dela para a área de transferência.
              firstColumn = f"{firstColumn}\n{l}\t{simpleResult}" #TODO: AJUSTAR NOME DE VARIÁVEL PARA ALGO MAIS INTUITIVO

              # Armazenando no dict "d" as infos validadas do link atual
              if requestURLResult == "Invalid":     # Caso incorra na exception missingSchema
                 d = {'URL':[l],'CÓDIGO':'null', 'STATUS':[simpleResult]}

              elif requestURLResult != "Invalid":   # Caso não incorra na exception missingSchema
                 d = {'URL':[verifiedURL],'CÓDIGO':[requestURLCode], 'STATUS':[simpleResult]}

              # Gerando o DataFrame usando Pandas (que poderá ser exportado mais tarde)
              df = pd.DataFrame(data=d)
              df2 = pd.concat([df,df2])
              generatedDataFrame = True
              
              # FIM DO FOR-EACH
          
          # Calculando tempo decorrido e atualizando status sobre sucesso da operação
          tempoFinal = time.perf_counter() #Inicializando tempo final
          window["-STATUS-"].update(f"Verificação finalizada!",text_color="green") #Atualizando status
          window["-STATUS-"].print(f"\nTempo decorrido: {tempoFinal-tempoInicio:0.2f} segundos") #Exibindo tempo decorrido (TF-TI)

          # Habilitando novamente ao usuário os botões de ação, uma vez que as operações de validação já terminaram
          gui.enableActionButtons(window)
      
      # Chamando uma exception genérica caso algo dê errado no caminho
      except Exception as err:
          print("1:",Exception)
          pg.Popup(f"Erro: {err}\n\nPor favor, abra uma issue no GitHub do projeto contendo um print dessa tela.\n\nO programa será fechado agora.", title="Erro")
          generatedDataFrame = False # Marcando que há um dataframe gerado como falso (para não permitir export)
          raise(err)
          
    



    elif event == "COPIAR RESULTADO":
        # Checar se a variável que armazena os resultados gerados possui apenas as colunas iniciais
        # Não copiar para a área de transferência e avisar ao usuário para realizar uma validação antes.
        # Por fim, atualizar o status para refletir a ação tomada pelo programa.
        if firstColumn != "URL\tSTATUS":
          pyperclip.copy(firstColumn)
          window["-STATUS-"].update(f"Resultado copiado para a área de transferência!",text_color="green")
        
        elif firstColumn == "URL\tSTATUS":
          pg.Popup(f"Erro: Valide pelo menos uma URL antes de copiar o resultado.\n", title="Erro")
          window["-STATUS-"].update("Aguardando usuário...",text_color="black")
          gui.enableActionButtons()
          continue


    elif event == "EXPORTAR":
      

      if generatedDataFrame == True:
        gui.disableActionButtons()  
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
        gui.enableActionButtons()
      elif generatedDataFrame == False:
        pg.Popup(f"Erro: Valide pelo menos uma URL antes de exportar o resultado.\n", title="Erro")
        window["-STATUS-"].update("Aguardando usuário...",text_color="black")
        gui.enableActionButtons()
        continue

    #TODO: INSERIR FUNCIONALIDADE PARA CANCELAR UMA VALIDAÇÃO EM ANDAMENTO
    elif event == "CANCELAR":
       gui.enableActionButtons()
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