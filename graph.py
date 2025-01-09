import matplotlib
matplotlib.use('Agg')  # Set non-GUI backend before importing pyplot
import matplotlib.pyplot as plt
import pandas as pd

def graph(global_st, symbol):
    # Verifica que la columna 'real' exista en predictions_df
    if 'real' not in global_st["dfs"]["trained"].columns:
        real_values = global_st["dfs"]["close"].iloc[-global_st["models"]["lag"]:].values  # Últimos valores reales
        global_st["dfs"]["trained"]['real'] = real_values  # Asignar a la columna 'real'

    # Crear la figura y los subgráficos
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # 2 filas, 1 columna

    # Gráfico 1: Valores Reales vs Predicciones de Modelos
    axes[0].plot(global_st["dfs"]["trained"]['date'], global_st["dfs"]["trained"]['real'], label='Real', marker='o', color='black')

    draw_df = global_st["dfs"]["trained"].copy()
    draw_df = draw_df.iloc[:, :-1]

    # Graficar predicciones de cada modelo
    for col in draw_df.columns[2:]:
        axes[0].plot(draw_df['date'], draw_df[col], label=col.upper(), marker='x')

    axes[0].set_title(f'Real vs Entrenado ({symbol})')
    axes[0].set_xlabel('Fecha')
    axes[0].set_ylabel('Precio')
    axes[0].legend(title="Modelos")
    axes[0].grid(True)
    axes[0].tick_params(axis='x', rotation=45)

    # Convertir de nuevo a datetime si es necesario para el gráfico
    global_st['dfs']['trained']['date'] = pd.to_datetime(global_st['dfs']['trained']['date'])
    global_st['dfs']['future']['date'] = pd.to_datetime(global_st['dfs']['future']['date'])

    # Gráfico en axes[1]
    # Graficar los valores reales
    axes[1].plot(global_st['dfs']['trained']['date'], global_st['dfs']['trained']['real'], label='Valores Reales', color='black', marker='o')

    # print(global_st['dfs']['data'].head(2))
    # print(global_st['dfs']['trained'])
    # print(global_st['dfs']['future'])


    # Obtener el último valor de las columnas 'date' y 'real' del DataFrame origen
    last_date = global_st['dfs']['trained']['date'].iloc[-1]
    last_real = global_st['dfs']['trained']['real'].iloc[-1]
    # Crear una nueva fila para insertar
    new_row = {col: last_real if col != 'date' else last_date for col in global_st['dfs']['future'].columns}
    # Insertar como primera fila en el DataFrame destino
    global_st['dfs']['future'] = pd.concat([pd.DataFrame([new_row]), global_st['dfs']['future']], ignore_index=True)   

    # Graficar los valores predichos para cada modelo
    for col in global_st['dfs']['future'].columns[1:]:  # Excluyendo la columna de fecha
        axes[1].plot(global_st['dfs']['future']['date'], global_st['dfs']['future'][col], label=f'Predicciones {col.upper()}', marker='x')

    # Configurar el gráfico
    axes[1].set_title(f'Real - Predict ({symbol})')
    axes[1].set_xlabel("Fecha")
    axes[1].set_ylabel("Precio")
    axes[1].legend(title="Modelos")
    axes[1].grid(True)
    axes[1].tick_params(axis='x', rotation=45)  # Rotar las etiquetas del eje X para mayor claridad

    # Ajustar el diseño de la figura
    plt.tight_layout()

    # Mostrar la figura combinada
    # plt.show()

    # Save chart to file
    chart_path = global_st["chart_path"]
    plt.savefig(chart_path)
    plt.close()  # Close the figure
    return chart_path
