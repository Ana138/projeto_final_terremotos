import requests
import pandas as pd
import os

def extrair_terremotos():
    """Extrai dados de terremotos da API USGS e salva arquivos brutos."""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": "2024-01-01",
        "endtime": "2024-12-31",
        "minmagnitude": 5
    }

    # Faz a requisição para a API
    response = requests.get(url, params=params)
    
    # Verifica se a resposta foi bem-sucedida
    if response.status_code != 200:
        print(f"Erro ao acessar a API: {response.status_code}")
        return None
    
    # Converte a resposta para JSON
    data = response.json()
    
    # Verifica se a resposta contém dados válidos
    if "features" not in data:
        print("Nenhum dado encontrado na resposta.")
        return None

    terremotos = []
    for feature in data["features"]:
        props = feature["properties"]
        geom = feature["geometry"]

        terremotos.append({
            "data_hora": pd.to_datetime(props["time"], unit='ms'),
            "local": props["place"],
            "magnitude": props["mag"],
            "profundidade_km": geom["coordinates"][2],
            "longitude": geom["coordinates"][0],
            "latitude": geom["coordinates"][1]
        })

    # Cria um DataFrame com os dados
    df = pd.DataFrame(terremotos)

    # Cria o diretório 'dados_brutos' caso não exista
    os.makedirs("dados_brutos", exist_ok=True)
    
    # Salva os dados em formato JSON e CSV
    df.to_json("dados_brutos/terremotos_2024.json", orient='records', lines=True)
    df.to_csv("dados_brutos/terremotos_2024.csv", index=False)

    return df

def transformar_dados(df):
    """Faz limpeza e transformação dos dados e salva em CSV processado."""
    # Remove linhas com dados faltantes nas colunas essenciais
    df = df.dropna(subset=["magnitude", "profundidade_km", "longitude", "latitude"])
    
    # Filtra terremotos com magnitude maior que 0
    df = df[df["magnitude"] > 0]
    
    # Cria uma coluna de 'nivel' para classificar os terremotos
    df["nivel"] = df["magnitude"].apply(lambda x: "leve" if x < 6 else "forte")
    
    # Converte a coluna 'data_hora' para formato de data
    df["data_hora"] = pd.to_datetime(df["data_hora"])

    # Cria o diretório 'dados_processados' caso não exista
    os.makedirs("dados_processados", exist_ok=True)
    
    # Salva os dados processados em CSV
    df.to_csv("dados_processados/terremotos_processados.csv", index=False)

    return df

# Função principal para extrair e transformar os dados
if __name__ == "__main__":
    df_terremotos = extrair_terremotos()
    if df_terremotos is not None:
        transformar_dados(df_terremotos)
