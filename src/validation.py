import requests
import gui
import PySimpleGUI as pg
import re



def firstLine_IsEmpty(linksList, window):

    # Valida se a primeira linha está vazia
    if linksList[0] == '' :
        pg.Popup("Erro: Verifique os espaços em branco antes de continuar.\n", title="Erro")
        window["-STATUS-"].update("Aguardando usuário...",text_color="black")
        gui.enableActionButtons(window)
        return True


def get_URLString_Regex(link, window):
        newlink = ""

        #Atualizar status avisando que a verificação de URLs está em curso
        window["-STATUS-"].update(f"Verificando URLs. Aguarde...", text_color="olive")


        #===== 1ª VALIDAÇÃO COM REGEX =====
        #Regex para verificar se o link está CORRETO:
        # 1. começa com HTTP ou HTTPS e depois tem "://"  
        #|E|
        # 2. se termina com ".com" (ou algo a mais além disso)
        if re.match(r"^https?://.*\.com(?:/.*)?$", link):
            print("caught in Regex 1: ",link)
            newlink = link


        #===== 2ª VALIDAÇÃO COM REGEX =====
        #Regex para ajustar um link INCORRETO, caso:
        # 1. começa com (HTTP ou HTTPS) e "://", 
        #|OU| 
        # 2. se NÃO termina com ".com" (ou algo a mais além disso)
        elif re.match(r"^(?!https?://|.*\.com.*$).*", link):
            newlink = f"https://{link}.com"
            print("caught in Regex 2: ",newlink)


        #===== 3ª VALIDAÇÃO COM REGEX =====
        #Regex para ajustar um link INCORRETO, caso:
        # 1. começa com HTTP ou HTTPS e "://" 
        #|E|
        # 2. não termina com ".com"
        elif re.match(r"^(?!https?://).*\.com.*$", link):
            newlink = f"https://{link}"
            print("caught in Regex 3: ",newlink)


        #===== 4ª VALIDAÇÃO COM REGEX =====
        #Regex para ajustar um link INCORRETO, caso:
        # 1. começa com HTTP ou HTTPS e depois tem "://"
        #|E|
        # 2. NÃO termina com ".com"
        elif re.match(r"^(https?://)(?:(?!\.com).)*$", link):
            newlink = f"{link}.com"
            print("caught in Regex 4: ",newlink)


        #===== VALIDAÇÃO ADICIONAL COM REPLACE =====
        # Se o link estiver incorreto, vai ser transformado em uma string vazia para pular verificações de request
        # e informar o usuário que a linha está vazia
        if link == "https://.com":
            newlink = ""
            print("caught in blank replace: ",newlink)

        return newlink

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