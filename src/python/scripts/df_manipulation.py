import pandas as pd

def season(x):
    """
    Mapeia o mês para a estação do ano correspondente.

    Args:
        x (int): Número do mês (1 a 12).

    Returns:
        str: Estação do ano (Autumn, Winter, Spring ou Summer).
    """
    if x in [9, 10, 11]:
        return 'Autumn'
    if x in [1, 2, 12]:
        return 'Winter'
    if x in [3, 4, 5]:
        return 'Spring'
    if x in [6, 7, 8]:
        return 'Summer'
    return x


def alter(df):
    """
    Realiza transformações no DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame original.

    Returns:
        pandas.DataFrame: DataFrame com colunas adicionais e transformações aplicadas.
    """
    # Remove colunas indesejadas
    df.drop(columns=['Booking_ID', 'booking_status'], axis=1, inplace=True)
    df_copy = df.copy()

    # Reorganiza as colunas
    custom_columns = ['label_avg_price_per_room']
    for i in range(len(df.columns[:-1])):
        if df.columns[i] != 'label_avg_price_per_room':
            custom_columns.append(df_copy.columns[i])
    df_copy = df_copy[custom_columns]

    # Cria novas colunas
    df_copy['no_total_people'] = df_copy['no_of_adults'] + df_copy['no_of_children']
    df_copy['no_total_nights'] = df_copy['no_of_weekend_nights'] + df_copy['no_of_week_nights']
    df_copy['season_group'] = df_copy['arrival_month'].apply(season)

    return df_copy
