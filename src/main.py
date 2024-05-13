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


# Armazena a janela atual na variável "WINDOW"
# Sempre que mudanças na estrutura da janela precisarem ser feitas, passar essa variável como parâmetro
WINDOW = gui.init_window()


# Inicializando dataframe e indicação se há um dataframe gerado + definindo colunas padrão para a área de transferência
df2 = pd.DataFrame()
is_dataframe_ready = False
clipboard_str = "URL\tSTATUS"



# INICIAR LOOP PARA MANTER JANELA ABERTA
while True:
    event, values = WINDOW.read() # Leitura e eventos da janela atual

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
      WINDOW["-RESULT-"].update('')
      gui.disableActionButtons(WINDOW)
      WINDOW["-STATUS-"].update("Inicializando verificação...",text_color="navy")

      # Armazenar se o dataframe já foi gerado (para permitir exportação)
      line_number = 0              
      is_dataframe_ready = False

      # Reseta string que vai pra área de transferência
      clipboard_str = "URL\tSTATUS"
      

      try:

          # Armazena em uma list todas as linhas inseridas, separando por quebra de linhas
          LINKS_LIST = str(values["-LINES-"]).split(f"\n")

          # Atualiza tamanho de elementos para a barra de progresso
          WINDOW["-PROGRESS-"].update(current_count=0,max=len(LINKS_LIST))
          
          
          # Valida se a primeira linha está vazia e não inicia a validação caso verdadeiro
          if validation.firstLine_IsEmpty(LINKS_LIST,WINDOW):
            continue
          

          for l in LINKS_LIST:


              try:

                # Validar link atual usando regex, e ajustar a depender da condição
                verified_url = validation.get_URLString_Regex(l,WINDOW)

                # Verificar o código resultante da GET request, e retornar em string
                REQUEST_URL_CODE = validation.get_URLRequest_Code(verified_url)

                # Criar "simple_result" para armazenar um resultado simples e de fácil entendimento ao usuário
                simple_result = validation.get_ResultToString(REQUEST_URL_CODE)


              # EXCEPTION DE URL INCORRETO - caso alguma regex falhe
              except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
                  simple_result = "INVÁLIDO"
                  
                  if verified_url == "":
                   verified_url = "URL Vazia"
                  else:
                    pass
              
              # EXCEPTIONS DE CONEXÃO
              except requests.exceptions.ConnectionError as err:
                  if("NameResolutionError"in str(err)):
                    simple_result = "INVÁLIDO"
                    continue
                  
                  else:
                    WINDOW["-STATUS-"].update("Erro de conexão genérico!",text_color="red")
                    pg.Popup(f"Erro de conexão genérico: Por favor, abra uma issue no GitHub com um print desta tela.\nLink: {l}\nErro:{str(err)}")
                    continue
              
              
              
              # Incrementando número da linha atual para exibir corretamente no output
              line_number += 1


              # Atualizando caixa de resultado (output)
              WINDOW["-RESULT-"].print(f"Linha {line_number}: {verified_url} - {simple_result}")
             

              # Incrementando a cada loop as infos de validação na variável "clipboard_str" - usada para a área de transferência
              clipboard_str = f"{clipboard_str}\n{l}\t{simple_result}"


              # Armazenando no dict "d" as infos validadas do link atual, checando se incorreu em exception ou não
              if simple_result == "INVÁLIDO":
                 d = {'LINHA':[line_number],'URL':[l],'CÓDIGO':'null', 'STATUS':[simple_result]}

              else:
                d = {'LINHA':[line_number],'URL':[verified_url],'CÓDIGO':[REQUEST_URL_CODE], 'STATUS':[simple_result]}

              # Gerando o DataFrame usando Pandas (que poderá ser exportado mais tarde)
              df = pd.DataFrame(data=d)
              df2 = pd.concat([df,df2])
              

              # Atualizar barra de progresso
              WINDOW["-PROGRESS-"].update(current_count=line_number)

              #-------- FIM DO FOR-EACH

          # Setando index do dataframe pra coluna LINHA e ordenando
          is_dataframe_ready = True
          df2.set_index("LINHA",inplace=True)
          df2 = df2.sort_values("LINHA")
          

          # Calculando tempo decorrido e atualizando status sobre sucesso da operação
          tempo_final = time.perf_counter()
          WINDOW["-STATUS-"].update(f"Verificação finalizada!",text_color="green")
          WINDOW["-STATUS-"].print(f"\nTempo decorrido: {tempo_final-tempoInicio:0.2f} segundos")

          # Habilitando novamente ao usuário os botões de ação
          gui.enableActionButtons(WINDOW)
      

      # Exception genérica - Marca que há um dataframe gerado como falso para não permitir export
      except Exception as err:
          print("1:",Exception)
          pg.Popup(f"Erro: {err}\n\nPor favor, abra uma issue no GitHub do projeto contendo um print dessa tela.\n\nO programa será fechado agora.", title="Erro")
          is_dataframe_ready = False
          raise(err)
      
          
    
    #CLIPBOARD
    elif event == "COPIAR RESULTADO":
        clipboard.copyResultToClipboard(clipboard_str,WINDOW)
        

    #EXPORT
    elif event == "EXPORTAR":
        export.To_xlsx(df2,is_dataframe_ready,WINDOW)
        
    

    #TODO: INSERIR FUNCIONALIDADE PARA CANCELAR UMA VALIDAÇÃO EM ANDAMENTO
    elif event == "CANCELAR":
        gui.enableActionButtons(WINDOW)
        break

   # DEBUG
   # EXE: pyinstaller main.py -F --noconsole --clean
   
   
WINDOW.close()