# Resumen de la Clase `LeerDatos`

La clase `LeerDatos` está diseñada para manejar y procesar datos en un DataFrame, aplicando varias técnicas de limpieza y transformación de datos. A continuación se describen sus principales métodos:

## Métodos de la Clase

### 1. `contar_caracteres(self, nombre_columna: str, cantidad_caracteres: int)`

**Descripción**:
- Cuenta y muestra las filas en la columna especificada cuyo número de caracteres es mayor que `cantidad_caracteres`.

**Funcionamiento**:
- Convierte la columna a tipo cadena.
- Filtra las filas cuya longitud es mayor al valor dado.
- Imprime las filas que cumplen con la condición o un mensaje si no se encuentran coincidencias.

### 2. `formato_entero(self, lista_columnas: list)`

**Descripción**:
- Convierte las columnas especificadas en números enteros después de limpiar los caracteres no numéricos.

**Funcionamiento**:
- Elimina caracteres no numéricos, manteniendo puntos y comas.
- Reemplaza valores vacíos y nulos por `0`.
- Convierte las cadenas limpias a enteros.

### 3. `limpiar_datos(self, nombre_columna: str, lista_caracteres: list)`

**Descripción**:
- Limpia caracteres especiales de una columna en el DataFrame.

**Funcionamiento**:
- Crea una expresión regular para los caracteres a eliminar.
- Aplica la limpieza usando `re.sub` para reemplazar los caracteres especificados.

### 4. `limpiar_multiples_columnas(self, dict_columnas_caracteres: dict)`

**Descripción**:
- Aplica la limpieza de datos a múltiples columnas, utilizando un diccionario que mapea columnas a listas de caracteres especiales.

**Funcionamiento**:
- Itera sobre el diccionario, aplicando el método `limpiar_datos` a cada columna con su respectiva lista de caracteres.

### 5. `contar_caracteres(self, nombre_columna: str)`

**Descripción**:
- Cuenta y muestra caracteres especiales en cada columna del DataFrame.

**Funcionamiento**:
- Recorre las columnas del DataFrame.
- Identifica y cuenta caracteres especiales en cada columna de tipo objeto.
- Imprime el número de filas con caracteres especiales por columna.

## Instrucciones de Uso

1. **Inicialización**: 
   - Instancia la clase `LeerDatos` con un DataFrame cargado.

2. **Aplicar Métodos**:
   - Usa `contar_caracteres` para identificar caracteres especiales en columnas.
   - Usa `formato_entero` para convertir datos a enteros, limpiando caracteres no numéricos.
   - Usa `limpiar_datos` y `limpiar_multiples_columnas` para limpiar caracteres especiales de una o varias columnas.

3. **Guardar Cambios**:
   - Asegúrate de guardar o exportar el DataFrame modificado según sea necesario.

Este resumen proporciona una visión general de cómo utilizar la clase `LeerDatos` para procesar y limpiar datos en un DataFrame.
