import pandas as pd

def salvar_dataframes_em_excel(df1, nome_aba1, df2, nome_aba2, nome_arquivo):
    """
    Salva dois DataFrames em um arquivo Excel, cada um em uma aba com os nomes especificados.

    :param df1: Primeiro DataFrame a ser salvo.
    :param nome_aba1: Nome da aba para o primeiro DataFrame.
    :param df2: Segundo DataFrame a ser salvo.
    :param nome_aba2: Nome da aba para o segundo DataFrame.
    :param nome_arquivo: Nome do arquivo Excel de saída.
    """
    with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name=nome_aba1, index=False)
        df2.to_excel(writer, sheet_name=nome_aba2, index=False)
    print(f"Arquivo Excel salvo como '{nome_arquivo}' com abas '{nome_aba1}' e '{nome_aba2}'.")

# Exemplo de uso:
if __name__ == "__main__":
    # Criando DataFrames de exemplo
    df1 = pd.DataFrame({'Coluna1': [1, 2, 3], 'Coluna2': ['A', 'B', 'C']})
    df2 = pd.DataFrame({'Coluna3': [4, 5, 6], 'Coluna4': ['D', 'E', 'F']})

    # Nome das abas
    nome_aba1 = 'Dados1'
    nome_aba2 = 'Dados2'

    # Nome do arquivo Excel
    nome_arquivo = 'resultado.xlsx'

    # Salvar os DataFrames no Excel
    salvar_dataframes_em_excel(df1, nome_aba1, df2, nome_aba2, nome_arquivo)