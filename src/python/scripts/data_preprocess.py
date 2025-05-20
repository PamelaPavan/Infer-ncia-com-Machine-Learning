from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

def preprocess(df, target_column):
    """
    Realiza o pré-processamento dos dados.

    Args:
        df (pandas.DataFrame): DataFrame original contendo os dados.
        target_column (str): Nome da coluna alvo (variável dependente).

    Returns:
        tuple: Pré-processador, dados de features (X) e rótulos (y).
    """
    # Separar os recursos (X) e o alvo (y)
    X = df.drop(columns=target_column)
    y = df[target_column]
    
    # Identificar características numéricas e categóricas
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns
    
    # Definir transformadores para características numéricas e categóricas
    numeric_transformer = 'passthrough'  # Mantém as features numéricas sem alterações
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')  # Codifica as features categóricas
    
    # Criar um pré-processador usando ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    return preprocessor, X, y
