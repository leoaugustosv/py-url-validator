import requests
import gui
import PySimpleGUI as pg
import re



def firstLine_IsEmpty(LINKS_LIST, WINDOW):

    # Valida se a primeira linha está vazia
    if LINKS_LIST[0] == '' :
        pg.Popup("Erro: Verifique os espaços em branco antes de continuar.\n", title="Erro")
        WINDOW["-STATUS-"].update("Aguardando usuário...",text_color="black")
        gui.enableActionButtons(WINDOW)
        return True


def get_URLString_Regex(link, WINDOW):
        new_link = ""

        #Atualizar status avisando que a verificação de URLs está em curso
        WINDOW["-STATUS-"].update(f"Verificando URLs. Aguarde...", text_color="olive")

        #Desinfetando linha antes de entrar em regex
        link = re.sub("[^a-zA-Z0-9:/ $\-_.+!*'(),]","",link)


        #===== 1ª VALIDAÇÃO COM REGEX =====
        #Regex para verificar se o link está CORRETO:
        # 1. começa com HTTP ou HTTPS e depois tem "://"  
        #|E|
        # 2. se termina com ".com" (ou algo a mais além disso)
        if re.match(r"^https?://.*\.com(?:/.*)?$", link):
            print("caught in Regex 1: ",link)
            new_link = link


        #===== 2ª VALIDAÇÃO COM REGEX =====
        #Regex para ajustar um link INCORRETO, caso:
        # 1. começa com HTTP ou HTTPS e "://" 
        #|E|
        # 2. não termina com ".com"
        elif re.match(r"^(?!https?://).*\.com.*$", link):
            new_link = f"https://{link}"
            print("caught in Regex 2: ",new_link)


        #===== 3ª VALIDAÇÃO COM REGEX =====
        #Regex para ajustar um link INCORRETO, caso:
        # 1. começa com HTTP ou HTTPS e depois tem "://"
        #|E|
        # 2. NÃO termina com ".com"
        elif re.match(r"^(https?://)(?:(?!\.com).)*$", link):
            new_link = f"{link}.com"
            print("caught in Regex 3: ",new_link)

        else:
            new_link = link


        #===== VALIDAÇÃO ADICIONAL COM REPLACE =====
        # Se o link estiver incorreto, vai ser transformado em uma string vazia para pular verificações de request
        # e informar o usuário que a linha está vazia
        if link == "https://.com":
            new_link = ""
            print("caught in blank replace: ",new_link)

        return new_link

def get_URLRequest_Code(link):

    
    #Verificar status do GET no link
    requestURLResult = requests.get(link)

    #Transformar resultado em uma string com apenas o código
    requestURLCodeSplit1 = str(requestURLResult).replace("<Response [","")
    requestURLCode = str(requestURLCodeSplit1).replace("]>","")

    #Retornar apenas o código (como string?! então tá...)
    return requestURLCode

def get_ResultToString(code):
    result = ""
    
    match code:
        case "200":
            result = "OK"
        case "403":
            result = "ERRO"
        case _:
            result = f"VERIFICAR - {code}"


    return result