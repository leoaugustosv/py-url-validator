# py-validador-links

Uma interface gráfica simples que valida links em Python. Permite copiar o resultado da validação diretamente para a área de transferência ou exportar para um arquivo .xlsx.

### Objetivo

Esse projeto busca permitir ao usuário que valide múltiplos links rapidamente.
Pode ser útil em ocasiões onde você possui uma lista de links e precisa verificar quais funcionam e quais não.

## Quais bibliotecas foram usadas?

Requests, Pandas, PySimpleGui, tkinter, pyperclip. Para mais detalhes, verifique o arquivo **requirements.txt**.

## Como abrir o projeto em sua máquina

1. Clone o projeto para a sua máquina no diretório de preferência.
2. Abra o CMD e vá até o caminho em que o repositório está clonado.
3. Certifique-se de ter criado e ativado um [virtual environment](https://docs.python.org/3/library/venv.html) antes.
4. Execute o comando abaixo:

```
pip install -r /path/to/requirements.txt
```

5. Abra o arquivo main.py usando sua IDE preferida.

## Como transformar o projeto em um arquivo .exe único

1. Instale o pyinstaller:

```
pip install pyinstaller
```

2. Abra o CMD e vá até o caminho em que o repositório está clonado.
3. Certifique-se de ter criado e ativado um [virtual environment](https://docs.python.org/3/library/venv.html) antes.
4. Execute o comando abaixo:

```
pyinstaller main.py -F --noconsole --clean --onefile
```

5. Seu .exe estará na pasta **dist**. Você pode apagar ou ignorar a pasta **build**.
