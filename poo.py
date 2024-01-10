#%%
from wget import download
from requests import get
from datetime import datetime
from zipfile import ZipFile
from os import path, remove
import pandas as pd

class ExtractDTB:
    " Extrair dados da divisão territorial do Brasil a partir do IBGE "

    print( 'Inicializando o processo de extração...' )

    def __init__(self, urlname, destdir):
        self.urlname = urlname
        self.destdir = destdir

    def __log__(self, msg):
        data = datetime.now().strftime('%d-%m-%Y %Hh%Mm%Ss')
        print(f'--->> {data} INFO {msg.upper()}...')

    def download(self):

        self.__log__( 'Verificando se a URL está ativa' )

        response = get(self.urlname, timeout=600, stream=True)

        if response.ok:
            self.__log__( 'Baixando os dados' )
            download(self.urlname, self.destdir)

    def uncompress(self, string = "MUNICIPIO.xls"):
        " Descomprimir dados baixados da DTB "

        self.__log__( 'Verificando arquivo compactado' )

        nome_arquivo = path.basename(self.urlname)

        if 'zip' in nome_arquivo:
            with ZipFile(f'{self.destdir}/{nome_arquivo}', 'r') as zip:
                zip.printdir()
                lista_zip= zip.filelist

        print(lista_zip)

        xls_zip = [i.filename for i in lista_zip if string in i.filename][0]

        self.__log__( f'Descompactando o arquivo: {xls_zip}' )

        with ZipFile(f'{self.destdir}/{nome_arquivo}', 'r') as zip:
            zip.extract(xls_zip, path = self.destdir)

        return f'{self.destdir}/{nome_arquivo}'

    def ziprm(self):
        " Remoção do arquivo ZIP "
        arquivo_local = self.uncompress()

        if path.exists(arquivo_local):
            self.__log__( f'Removendo o arquivo: {arquivo_local}' )
            remove(arquivo_local)


# Diretórios
urlname = 'https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/divisao_territorial/2022/DTB_2022.zip'

destdir = 'C:/Users/gabri/OneDrive/Documentos/poo-prova'

# Instanciando o processo de extração da DTB
extract = ExtractDTB(urlname, destdir)

# Download
extract.download()

# Uncompress
extract.uncompress()

# Gestão de arquivos baixados
extract.ziprm()


#%%
class TransformDTB:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.DataFrame()

    def transform(self):
        print("Inicializando processo de tratamento dos dados...")
        df = pd.read_excel(self.file_path, header=6)

        # Padronizando nome das colunas
        print("Padronizando nome das colunas...")
        coluna_corrigida = {}
        for coluna in df.columns:
            coluna_corrigida[coluna] = coluna.replace(' ', '_')

        df = df.rename(columns=coluna_corrigida)

        self.df = df
        

# Instantiate the TransformDTB class
transform_instance = TransformDTB("c:/Users/gabri/OneDrive/Documentos/poo-prova/RELATORIO_DTB_BRASIL_MUNICIPIO.xls")
transform_instance.transform()


#%%
class LoadDTB:
    def __init__(self, transform_instance):
        self.transform_instance = transform_instance

    def to_excel(self, filename):
        print(f"Exporting data to Excel file: {filename}")
        self.transform_instance.df.to_excel(filename, index=False)



# Instantiate the LoadDTB class with the TransformDTB instance
loader = LoadDTB(transform_instance)

# Export the transformed data to Excel
loader.to_excel("dados.xlsx")

