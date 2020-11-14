# Projeto-Os-Facil-v3-0

Programa para gerenciamento de Ordens de Serviço para a AM Estamparia de Sublimação.

Este é um programa que é a evolução daquilo que começou na versão 1, feita em Python em modo texto, utilizando somente estruturas 
de repetição while True.

O Os Fácil v3.0 foi feito utilizando como modelador da interface gráfica o programa Glade, foi gerado o arquivo glade que, 
nada mais é que um arquivo XML que monta toda a interface. No arquivo main.py fazemos a linkagem da XML para dentro do código
python através da utilização da classe Builder. Esta classe traz todos os widgets que precisam ser manipulador para dentro
do meu código Python. Semelhantemente ao que ocorre em JavaScript quando aplicamos o método getElementBy... , assim também
funciona a classe Build da biblioteca GTK3.

Foram utilizadas as seguintes Bibliotecas.

- **PyGtk3.0** - Interface Gráfica
- **Sqlite3** - Banco de Dados
- **Reportlab** - Gerador de PDF
- Bibliotecas padrão do Python.

