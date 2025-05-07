<<<<<<< HEAD
# Projeto ETL de Terremotos com API USGS

Este projeto realiza um pipeline de dados automatizado com Python, Airflow e Hadoop, consumindo dados sísmicos da API da USGS.

## Tecnologias

- Python
- Apache Airflow
- Hadoop HDFS
- Pandas, Requests

## Estrutura

- `scripts/etl.py`: Código de extração e transformação
- `dags/terremotos_etl.py`: DAG do Airflow
- `dados_brutos/`: Dados brutos
- `dados_processados/`: Dados limpos
- `notebooks/`: Análises

## Execução

```bash
pip install -r requirements.txt
airflow db init
airflow webserver --port 8080
airflow scheduler
```