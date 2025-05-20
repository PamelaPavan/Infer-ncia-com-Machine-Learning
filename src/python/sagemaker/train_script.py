import argparse
import os
import logging
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from joblib import dump

# Configuração do logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Nível de log pode ser INFO, DEBUG, etc.

# Configuração do handler para redirecionar as mensagens para a saída de logs do SageMaker
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Hiperparâmetros
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=25)
    parser.add_argument("--min_samples_split", type=int, default=2)
    parser.add_argument("--min_samples_leaf", type=int, default=1)
    parser.add_argument("--bootstrap", type=str, default='True')

    args = parser.parse_args()

    # Converter string para booleano
    args.bootstrap = args.bootstrap.lower() in ['true', '1', 't', 'y', 'yes']

    logger.info("Argumentos: %s", args)

    # Local de entrada dos dados no SageMaker
    input_data_path = '/opt/ml/input/data'
    train_data_path = os.path.join(input_data_path, 'train', 'hotel_prices_train_xgboost.csv')
    val_data_path = os.path.join(input_data_path, 'validation', 'hotel_prices_test_xgboost.csv')

    # Verificar se os arquivos existem
    if not os.path.exists(train_data_path):
        logger.error(f"Arquivo de treino não encontrado: {train_data_path}")
        exit(1)
    else:
        logger.info(f"Arquivo de treino encontrado: {train_data_path}")

    if not os.path.exists(val_data_path):
        logger.error(f"Arquivo de validação não encontrado: {val_data_path}")
        exit(1)
    else:
        logger.info(f"Arquivo de validação encontrado: {val_data_path}")

    # Carregar dados
    logger.info("Carregando dados de treino")
    train_data = pd.read_csv(train_data_path)
    logger.info("Dados de treino carregados")

    logger.info("Carregando dados de validação")
    val_data = pd.read_csv(val_data_path)
    logger.info("Dados de validação carregados")

    # Separar recursos e rótulos
    X_train = train_data.iloc[:, 1:].values
    y_train = train_data.iloc[:, 0].values
    X_val = val_data.iloc[:, 1:].values
    y_val = val_data.iloc[:, 0].values

    # Treinamento do modelo
    logger.info("Treinando o modelo")
    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        min_samples_split=args.min_samples_split,
        min_samples_leaf=args.min_samples_leaf,
        bootstrap=args.bootstrap
    )

    model.fit(X_train, y_train)
    logger.info("Modelo treinado")

    # Avaliação do modelo
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)
    logger.info(f'Acurácia do modelo: {accuracy}')

    # Salvar o modelo
    logger.info("Salvando o modelo")
    model_output_path = '/opt/ml/model'
    os.makedirs(model_output_path, exist_ok=True)
    dump(model, os.path.join(model_output_path, "model.joblib"))
    logger.info("Modelo salvo")
