import pandas as pd
import chardet

class DeteccionEncoding:
    def __init__(self, archivo) -> None:
        self.archivo = archivo
        
    # Detectar la codificación del archivo
        with open(self.archivo, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

    # Mostrar el DataFrame resultante
        print(encoding)