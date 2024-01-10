#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class MunicipiosAnalyzer:
    def __init__(self, data_path):
        self.df = pd.read_excel(data_path)
    
    def remove_columns(self):
        columns_to_drop = ['Mesorregião_Geográfica', 'Nome_Mesorregião', 'Microrregião_Geográfica', 'Nome_Microrregião', 'Região_Geográfica_Imediata']
        self.df = self.df.drop(columns_to_drop, axis=1)
    
    def create_regiao_column(self):
        mapeamento_regioes = {
            range(11, 18): 'Região Norte',
            range(21, 30): 'Região Nordeste',
            range(31, 36): 'Região Sudeste',
            range(41, 44): 'Região Sul',
            range(50, 54): 'Região Centro-Oeste'
        }
        self.df['Região'] = self.df['UF'].apply(lambda x: next((v for k, v in mapeamento_regioes.items() if x in k), 'Outra Região'))
    
    def plot_estado_count(self):
        count_by_state = self.df['Nome_UF'].value_counts()
        plt.bar(count_by_state.index, count_by_state.values)
        plt.xlabel('Estado')
        plt.ylabel('Contagem de Municípios')
        plt.title('Contagem de Municípios por Estado')
        plt.xticks(rotation=90)
        plt.show()
    
    def plot_regiao_count(self):
        count_by_regiao = self.df['Região'].value_counts()
        plt.bar(count_by_regiao.index, count_by_regiao.values)
        plt.xlabel('Região')
        plt.ylabel('Contagem de Municípios')
        plt.title('Contagem de Municípios por Região')
        plt.xticks(rotation=90)
        plt.show()
    
    def plot_regiao_count_nordeste(self):
        nordeste_states = ['Bahia', 'Alagoas', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe']
        df_nordeste = self.df[self.df['Nome_UF'].isin(nordeste_states)]
        count_by_state = df_nordeste['Nome_UF'].value_counts()
        sns.set_palette("Pastel1")
        count_by_state.plot(kind='bar')
        plt.xlabel('Estado')
        plt.ylabel('Contagem de Municípios')
        plt.title('Contagem de Municípios por Estado (Região Nordeste)')
        plt.show()

# Criar uma instância do analisador de municípios
analyzer = MunicipiosAnalyzer("C:/Users/gabri/OneDrive/Documentos/poo-prova/dados.xlsx")

# Remover colunas desnecessárias
analyzer.remove_columns()

# Criar a coluna de região
analyzer.create_regiao_column()

# Plotar gráfico da contagem de municípios por estado
analyzer.plot_estado_count()

# Plotar gráfico da contagem de municípios por região
analyzer.plot_regiao_count()

# Plotar gráfico da contagem de municípios por estado na região Nordeste
analyzer.plot_regiao_count_nordeste()

# %%
