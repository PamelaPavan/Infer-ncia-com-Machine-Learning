from imblearn.over_sampling import RandomOverSampler

def oversample(X, y):
    """
    Realiza oversampling dos dados para balancear as classes.

    Args:
        X (array-like): Matriz de features (variáveis independentes).
        y (array-like): Vetor de rótulos (variável dependente).

    Returns:
        tuple: Dados oversampled (X_resampled, y_resampled).
    """
    # Cria uma instância do RandomOverSampler
    ros = RandomOverSampler(random_state=0)
    # Aplica o oversampling aos dados
    X_resampled, y_resampled = ros.fit_resample(X, y)
    return X_resampled, y_resampled
