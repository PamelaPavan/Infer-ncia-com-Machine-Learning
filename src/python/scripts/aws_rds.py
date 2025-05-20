import os
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

# Dados do dotenv
host = os.getenv('RDS_HOST')
user = os.getenv('RDS_USER')
password = os.getenv('RDS_PASSWORD')
port = int(os.getenv('RDS_PORT'))
dbname = os.getenv('DB_NAME')

# Crie uma string de conexão
connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'
# Crie uma conexão com o banco de dados
engine = sqlalchemy.create_engine(connection_string)

def upload(df, table_name):
    """_summary_

    Args:
        df (_type_): _description_
        table_name (_type_): _description_
    """
    try:
        # Importe os dados CSV para a tabela MySQL
        df.to_sql(table_name, engine, if_exists='append', index=False)

        # Mensagem de sucesso
        print(f"Os dados foram exportados com sucesso.")

    except Exception as e:
        print(f"Erro ao exportar dados: {str(e)}")


def download(table_name):
    """_summary_

    Args:
        table_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        # Carregar os dados da tabela MySQL para um DataFrame
        query = f'SELECT * FROM {table_name};'
        df = pd.read_sql(query, con=engine)

        # Mensagem de sucesso
        print(f"Os dados foram importados com sucesso.")
        return df

    except Exception as e:
        print(f"Erro ao exportar dados: {str(e)}")
