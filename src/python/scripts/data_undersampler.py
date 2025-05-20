from imblearn.under_sampling import RandomUnderSampler

def undersample_data(X, y):
    """
    Realiza o undersampling dos dados para balancear as classes.

    Args:
        X (array-like): Matriz de features (variáveis independentes).
        y (array-like): Vetor de rótulos (variável dependente).

    Returns:
        tuple: Dados undersampled (X_resampled, y_resampled).
    """
    # Cria uma instância do RandomUnderSampler
    rus = RandomUnderSampler(random_state=0)
    # Aplica o undersampling aos dados
    X_resampled, y_resampled = rus.fit_resample(X, y)
    return X_resampled, y_resampled
