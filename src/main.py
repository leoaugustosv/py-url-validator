# Imports de bibliotecas
import requests
import time
import PySimpleGUI as pg
import pandas as pd

# Imports de arquivos
import gui
import validation
import clipboard
import export


# Armazena a janela atual na variável "window"
# Sempre que mudanças na estrutura da janela precisarem ser feitas, passar essa variável como parâmetro
window = gui.init_window()


# Inicializando dataframe e indicação se há um dataframe gerado + definindo colunas padrão para a área de transferência
df2 = pd.DataFrame()
isDataFrameReady = False
clipboard_Str = "URL\tSTATUS"



# INICIAR LOOP PARA MANTER JANELA ABERTA
while True:
    event, values = window.read() # Leitura e eventos da janela atual

   # FINALIZAR LOOP SE CANCELAR OU FECHAR JANELA
    if event == pg.WIN_CLOSED:
      break
   
    if event == "?":
      pg.popup("Insira os links separados por linha e clique em validar.\n", title="Como usar")
      continue
   

    #VALIDATION
    if event == "VALIDAR":

      # Inicializar contador de tempo de validação
      tempoInicio = time.perf_counter()

      # Limpar espaço de output, desabilitar botões de ação e atualizar status do programa
      window["-RESULT-"].update('')
      gui.disableActionButtons(window)
      window["-STATUS-"].update("Inicializando verificação...",text_color="navy")

      # Armazenar se o dataframe já foi gerado (para permitir exportação)
      lineNumber = 0              
      isDataFrameReady = False 
      clipboard_Str = "URL\tSTATUS"
      

      try:

          # Armazena em uma list todas as linhas inseridas, separando por quebra de linhas
          linksList = str(values["-LINES-"]).split(f"\n")
          
          # Valida se a primeira linha está vazia e não inicia a validação caso verdadeiro
          if validation.firstLine_IsEmpty(linksList,window):
            continue
          

          # Se a primeira linha não estiver vazia, inicializa um dataframe contendo as colunas
          datatest = pd.DataFrame(columns=['URL', 'CÓDIGO', 'STATUS'])
          
          
          for l in linksList:


              try:

                # Validar link atual usando regex, e ajustar a depender da condição
                verifiedURL = validation.get_URLString_Regex(l,window)

                # Verificar o código resultante da GET request, e retornar em string
                requestURLCode = validation.get_URLRequest_Code(verifiedURL)

                # Criar "simpleResult" para armazenar um resultado simples e de fácil entendimento ao usuário
                simpleResult = validation.get_ResultToString(requestURLCode)


              # EXCEPTION DE HTTP ou HTTPS faltante - TODO: VERIFICAR NECESSIDADE
              except requests.exceptions.MissingSchema:
                  simpleResult = "INVÁLIDO"
                  
                  if verifiedURL == "":
                   verifiedURL = "URL Vazia"
                  else:
                    pass

              # EXCEPTION DE URL INVÁLIDO - último recurso caso alguma validação de regex falhe
              except requests.exceptions.InvalidURL:
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
             

              # Incrementando a cada loop as infos de validação na variável "clipboard_Str" - usada para a área de transferência
              clipboard_Str = f"{clipboard_Str}\n{l}\t{simpleResult}"


              # Armazenando no dict "d" as infos validadas do link atual, checando se incorreu em exception ou não
              if simpleResult == "INVÁLIDO":
                 d = {'LINHA':[lineNumber],'URL':[l],'CÓDIGO':'null', 'STATUS':[simpleResult]}

              else:
                d = {'LINHA':[lineNumber],'URL':[verifiedURL],'CÓDIGO':[requestURLCode], 'STATUS':[simpleResult]}

              # Gerando o DataFrame usando Pandas (que poderá ser exportado mais tarde)
              df = pd.DataFrame(data=d)
              df2 = pd.concat([df,df2])
              
              isDataFrameReady = True
              
              #-------- FIM DO FOR-EACH

          # Setando index do dataframe pra coluna LINHA e ordenando
          df2.set_index("LINHA",inplace=True)
          df2 = df2.sort_values("LINHA")
          

          # Calculando tempo decorrido e atualizando status sobre sucesso da operação
          tempoFinal = time.perf_counter()
          window["-STATUS-"].update(f"Verificação finalizada!",text_color="green")
          window["-STATUS-"].print(f"\nTempo decorrido: {tempoFinal-tempoInicio:0.2f} segundos")

          # Habilitando novamente ao usuário os botões de ação
          gui.enableActionButtons(window)
      

      # Exception genérica - Marca que há um dataframe gerado como falso para não permitir export
      except Exception as err:
          print("1:",Exception)
          pg.Popup(f"Erro: {err}\n\nPor favor, abra uma issue no GitHub do projeto contendo um print dessa tela.\n\nO programa será fechado agora.", title="Erro")
          isDataFrameReady = False
          raise(err)
      continue
          
    
    #CLIPBOARD
    elif event == "COPIAR RESULTADO":
        clipboard.copyResultToClipboard(clipboard_Str,window)
        continue

    #EXPORT
    elif event == "EXPORTAR":
        export.To_xlsx(df2,isDataFrameReady,window)
        continue
    

    #TODO: INSERIR FUNCIONALIDADE PARA CANCELAR UMA VALIDAÇÃO EM ANDAMENTO
    elif event == "CANCELAR":
        gui.enableActionButtons(window)
        continue

   # DEBUG
   # EXE: pyinstaller main.py -F --noconsole --clean
   
   
window.close()