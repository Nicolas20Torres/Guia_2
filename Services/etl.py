# Importacion de recursos
import pandas as pd
import re
from collections import defaultdict

class LeerDatos:
    def __init__(self, ruta_completa: str, tipo_archivo: str) -> None:
        self.ruta_completa = ruta_completa
        self.tipo_archivo = tipo_archivo
        self.df = None

    def read_DataFrame(self,datos):
        self.df = pd.DataFrame(datos)

    def leer_archivo_csv(self, separador: str = ',') -> pd.DataFrame:
        """
        Lee un archivo CSV y carga su contenido en un DataFrame.

        Parámetros:
        - separador: Caracter utilizado para separar las columnas en el archivo CSV (por defecto ',').

        Retorna:
        - DataFrame con el contenido del archivo CSV.
        """
        if self.tipo_archivo.lower() == 'csv':
            try:
                self.df = pd.read_csv(self.ruta_completa, encoding='utf-8', sep=separador)
            except FileNotFoundError:
                print(f"Error: El archivo en la ruta {self.ruta_completa} no se encuentra.")
                self.df = None
            except pd.errors.EmptyDataError:
                print("Error: El archivo está vacío.")
                self.df = None
            except pd.errors.ParserError:
                print("Error: Error de análisis del archivo CSV.")
                self.df = None
            except Exception as e:
                print(f"Error inesperado: {e}")
                self.df = None
        else:
            print("Error: Tipo de archivo no soportado. Se esperaba 'csv'.")
        return self.df

    def filtrar_tabla(self,nombre_columna,lista_validacion=None,presentes=True,filtrar_vacios=False):
        """
        Realiza una validación cruzada en el DataFrame basado en una lista de valores, una columna específica,
        y/o campos vacíos.

        Este método filtra el DataFrame según los valores especificados en `lista_validacion` 
        para la columna `nombre_columna`. Dependiendo del parámetro `presentes`, se puede 
        filtrar para mantener solo las filas con valores presentes en `lista_validacion` 
        o eliminar dichas filas. También puede filtrar campos vacíos.

        Args:
            nombre_columna (str): El nombre de la columna en el DataFrame para realizar la validación cruzada.
            lista_validacion (list, optional): Una lista de valores a validar en la columna especificada. 
                                            Por defecto es None.
            presentes (bool, optional): Si es True, mantiene las filas con valores presentes en 
                                        `lista_validacion`. Si es False, elimina las filas con 
                                        valores presentes en `lista_validacion`. El valor 
                                        predeterminado es True.
            filtrar_vacios (bool, optional): Si es True, filtra los campos vacíos (NaN). El valor 
                                            predeterminado es False.

        Returns:
            pd.DataFrame: El DataFrame filtrado según los criterios especificados.
        
        Example:
            >>> df = pd.DataFrame({
            ...     'A': [1, 2, 3, 4, 5],
            ...     'B': ['a', 'b', 'c', 'd', 'e']
            ... })
            >>> mi_clase = MiClase(df)
            >>> resultado = mi_clase.validacion_cruzada('A', [2, 4], presentes=True)
            >>> print(resultado)
            A  B
            1  2  b
            3  4  d
        """
        datos = self.df.copy()
        
        if filtrar_vacios:
            if presentes:
                filtro = datos[nombre_columna].notna()
            else:
                filtro = datos[nombre_columna].isna()
        else:
            if lista_validacion is None:
                raise ValueError("Debe proporcionar una lista de validación o habilitar el filtrado de vacíos.")
            
            if presentes:
                filtro = datos[nombre_columna].isin(lista_validacion)
            else:
                filtro = ~datos[nombre_columna].isin(lista_validacion)
        
        resultado = datos[filtro]
        self.df = resultado
        return self.df
    
    def resumen_caracteres_especiales(self):
        """
        resumen_caracteres_especiales: Resume el número de filas con caracteres especiales en cada columna de tipo 'object'.
        
        Parámetros:
        - df (DataFrame): El DataFrame a analizar.

        Retorna:
        - resumen (dict): Un diccionario con el nombre de la columna como clave y el número de filas con caracteres especiales como valor.
        """
        resumen = {}
        
        for column in self.df.columns:
            if self.df[column].dtype == 'object':
                caracteres_especiales = self.df[column].str.contains(r'[^\w\s]', regex=True).sum()
                if caracteres_especiales > 0:
                    resumen[column] = caracteres_especiales
        
        return resumen

    def caracteres_especiales_encontrados(self):
        """
        caracteres_especiales_encontrados: Identifica y lista los caracteres especiales encontrados en las columnas de tipo 'object'.
        
        Parámetros:
        - df (DataFrame): El DataFrame a analizar.

        Retorna:
        - caracteres_encontrados (dict): Un diccionario donde la clave es el nombre de la columna y el valor es una lista de caracteres especiales encontrados en esa columna.
        """
        caracteres_encontrados = defaultdict(set)
        
        # Patrón para encontrar caracteres especiales
        patron = re.compile(r'[^\w\s]')
        
        for column in self.df.columns:
            if self.df[column].dtype == 'object':
                # Unir todas las filas de la columna en una sola cadena de texto
                texto_completo = ' '.join(self.df[column].dropna().astype(str))
                
                # Encontrar todos los caracteres especiales en el texto
                caracteres = patron.findall(texto_completo)
                
                if caracteres:
                    # Almacenar los caracteres especiales únicos en el diccionario
                    caracteres_encontrados[column].update(caracteres)
        
        # Convertir los conjuntos a listas
        caracteres_encontrados = {col: list(chars) for col, chars in caracteres_encontrados.items()}
        
        return caracteres_encontrados


    def limpiar_datos(self, nombre_columna, lista_caracteres):
        # Unir los caracteres en una expresión regular
        patron = f"[{''.join(re.escape(caracter) for caracter in lista_caracteres)}]"
        
        # Aplicar la limpieza a la columna especificada
        self.df[nombre_columna] = self.df[nombre_columna].apply(lambda x: re.sub(patron, '', x) if isinstance(x, str) else x)

        return self.df
    
    def Limpiar_multiples_columnas(self,dict_columnas_caracteres:dict):
        """
        limpiar_multiples_columnas: Aplica la función de limpieza de datos a múltiples columnas en el DataFrame.
        
        Parámetros:
        - dict_columnas_caracteres (dict): Diccionario donde la clave es el nombre de la columna y el valor es una lista de caracteres especiales a limpiar.
        
        Retorna:
        - self.df: El DataFrame con las columnas limpias.
        """
        for columna, lista_caracteres in dict_columnas_caracteres.items():
            # Llamar al método limpiar_datos para cada columna y su lista de caracteres
            self.limpiar_datos(columna, lista_caracteres)
        
        return self.df

    def formato_entero(self,lista_columnas):
        """
        formato_entero: Convierte a números enteros las columnas seleccionadas.
        - lista_columnas (list): Lista de nombres de las columnas a convertir en enteros.
        """
        for col in lista_columnas:
            # Eliminar de la cadena de texto los valores no numericos
            self.df[col] = self.df[col].astype(str).str.replace(r'[^0-9.,]', '', regex=True)
            
            # Manejo de valores vacio nulos o con 0
            self.df[col] = self.df[col].replace('', '0')
            self.df[col] = self.df[col].replace('nan', '0')
            self.df[col] = self.df[col].fillna('0')

            # Convertir a float y luego a entero, para manejar decimales como '.0'
            self.df[col] = self.df[col].astype(float).astype(int)

        return self.df
    
    def contar_caracteres(self,nombre_columna:str,cantidad_caracteres:int):
        # Asegurar el forma str para trabajar con cadena de texto
        self.df[nombre_columna] = self.df[nombre_columna].astype(str)
        # Filtrar para mostrar solo las filas que la logitud es mayor a  cantidad_caracteres
        filas_largas = self.df[self.df[nombre_columna].apply(len)>cantidad_caracteres]
        if not filas_largas.empty:
            print(filas_largas)
        else: 
            print(f'Cantidad de caracteres: {cantidad_caracteres} no superada en {nombre_columna}')

class AnalisisExploratorio:
    def __init__(self,df:pd.DataFrame) -> None:
        self.df = pd.DataFrame(df)

    def informacion_Dataset(self):
        print(f'Informacion sobre el DataFrame:')
        print(self.df.info())
        print('\n')
    
    def estadistiva_descriptiva(self) -> None:
        print('Informacion sobre medidas de tendencia central')
        return self.df.describe()

    def cantidad_valores(self) -> None:
        print(f'Cantidad de valores')
        print(self.df.count())
        print('\n')

    def Filtro_nulos(self) -> None:
        print(f'Cantidad de valores nulos por columna:')
        nulos_por_columna = self.df.isnull().sum()
        print(nulos_por_columna)
        print(f'\nTotal de valores nulos en el DataFrame: {nulos_por_columna.sum()}')