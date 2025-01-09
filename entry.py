import pandas as pd

def entry(global_st):
        # Obtener el último valor de las columnas 'date' y 'real' del DataFrame origen
    last_date = pd.to_datetime(global_st['dfs']['trained']['date'].iloc[-1])
    last_real = global_st['dfs']['trained']['real'].iloc[-1]
    # Crear una nueva fila para insertar
    new_row = {col: last_real if col != 'date' else last_date for col in global_st['dfs']['future'].columns}
    # Insertar como primera fila en el DataFrame destino
    global_st['dfs']['future'] = pd.concat([pd.DataFrame([new_row]), global_st['dfs']['future']], ignore_index=True)

    print(global_st['dfs']['future'])

    df = global_st['dfs']['future'].copy()
    # Calcular la diferencia entre los valores en índice 4 y 0 para cada columna
    price_differences = df.iloc[4, 1:] - df.iloc[0, 1:]

    # Determinar si suben o bajan
    price_trends = price_differences.apply(lambda x: "Sube" if x > 0 else "Baja")

    # Verificar si todas las columnas apuntan a la misma dirección o si solo una es diferente
    if price_trends.nunique() == 1:  # Todas apuntan en la misma dirección
        final_trend = price_trends.iloc[0]
    elif price_trends.value_counts().min() == 1:  # Solo una es diferente
        final_trend = price_trends[price_trends != price_trends.value_counts().idxmax()].iloc[0]
    else:
        final_trend = "Indeterminado"  # No cumple ninguna de las dos condiciones

    return final_trend