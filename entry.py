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