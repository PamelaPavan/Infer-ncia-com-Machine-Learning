def generate(table_name, df, dtype_mapping):
    """
    Gera uma consulta SQL para criar uma tabela no banco de dados.

    Args:
        table_name (str): Nome da tabela a ser criada.
        df (pandas.DataFrame): DataFrame contendo as colunas da tabela.
        dtype_mapping (dict): Mapeamento dos tipos de dados do DataFrame para tipos SQL.

    Returns:
        str: Consulta SQL para criar a tabela.
    """

    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("       # Inicializa a consulta com o comando CREATE TABLE
    
    # Itera pelas colunas do DataFrame
    for column in df.columns:
        
        sql_dtype = dtype_mapping[str(df[column].dtype)]                    # Obtém o tipo de dado SQL correspondente ao tipo de dado do DataFrame
       
        create_table_query += f"\n    {column} {sql_dtype},"                # Adiciona a coluna e seu tipo à consulta
    

    create_table_query = create_table_query.rstrip(',') + "\n);"            # Remove a vírgula extra no final e fecha a consulta
    
    return create_table_query
