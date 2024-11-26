import pandas as pd

def criar_excel_com_abas(dicionario_dataframes, caminho_arquivo):
    """
    Cria um arquivo Excel com múltiplas abas a partir de um dicionário.
    
    :param dicionario_dataframes: Dicionário onde a chave é o nome da aba e o valor é um DataFrame.
    :param caminho_arquivo: Caminho para salvar o arquivo Excel, incluindo o nome do arquivo.
    """
    with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
        for aba, dataframe in dicionario_dataframes.items():
            dataframe.to_excel(writer, sheet_name=aba, index=False)
    print(f"Arquivo Excel criado com sucesso em: {caminho_arquivo}")

# Exemplo de uso
if __name__ == "__main__":
    print(bool({}))
