import pandas as pd, requests

#Extrai os dados do arquivo csv e coloca os valores de cada linha como itens de uma lista
df = pd.read_csv('Carteira.csv')
carteira = [[row['Ativos'], row['Quantidade'], row['Preco de compra']] for (index, row) in df.iterrows()]

#Busca a ultima cotacao de cada ativo com a API
def pega_ultima_cotacao(acao):
    PARAMETROS = {
        "function": "TIME_SERIES_DAILY",
        "symbol": acao,
        "apikey": "SUA CHAVE API AQUI"
    }

    response = requests.get("https://www.alphavantage.co/query", params=PARAMETROS)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]
    data_list = [valor for (chave, valor) in data.items()]
    fechamento_anterior = float(data_list[0]['4. close'])

    return fechamento_anterior

#Calcula o valor inicial da carteira e compara com o valor final
valor_inicial_carteira = sum([(item[1]*item[2]) for item in carteira])

#Acessa os valores de cada item na carteira para buscar o valor atual de cada ativo e calcular o valor total
valor_final_carteira = 0
for dados in carteira:
    ativo = f"{dados[0]}.SAO"
    quantidade = dados[1]

    preco = pega_ultima_cotacao(ativo)
    valor_final_carteira += preco * quantidade

diferenca_percentual = (valor_final_carteira - valor_inicial_carteira) * 100 / valor_inicial_carteira

#Carrega em um arquivo de texto uma mensagem a respeito da variacao da carteira
with open("Mensagem.txt", "w") as mensagem:
    if diferenca_percentual > 0:
        mensagem.write(f"Sua carteira teve uma valorizacao de {diferenca_percentual:.2f}%")

    elif diferenca_percentual < 0:
        mensagem.write(f"Sua carteira teve uma desvalorizacao de {abs(diferenca_percentual):.2f}%")

    else:
        mensagem.write(f"Nao houve variacao no valor da carteira")