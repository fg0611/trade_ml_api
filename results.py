import pandas as pd
import numpy as np


def predict_future_prices(model, last_known_prices, steps=4):
    """
    Predice los próximos `steps` precios utilizando un modelo entrenado.
    
    Params:
    - model: modelo entrenado (scikit-learn compatible).
    - last_known_prices: array con los últimos precios conocidos (lag).
    - steps: número de predicciones futuras.
    
    Returns:
    - Listado de precios futuros predichos.
    """
    future_prices = []
    current_input = np.array(last_known_prices).reshape(1, -1)  # Asegurar formato 2D
    
    for _ in range(steps):
        next_price = model.predict(current_input)[0]
        future_prices.append(next_price)
        # Actualizar la entrada con el nuevo precio predicho
        current_input = np.append(current_input[:, 1:], [[next_price]], axis=1)
    
    return future_prices


def results(global_st):
    # Ordenar el diccionario `results` en función del MSE
    sorted_results = sorted(global_st["dfs"]["score"].items(), key=lambda x: x[1]['MSE'])

    # Reasignar el orden de las keys en el diccionario `models` según el MSE
    global_st["models"]["all"] = {name: global_st["models"]["all"][name] for name, _ in sorted_results}

    # Crear un DataFrame con los resultados ordenados
    global_st["dfs"]["score"] = pd.DataFrame(
        [(name, metrics['MSE'], metrics['R2']) for name, metrics in sorted_results],
        columns=['Model', 'MSE', 'R2']
    )

    # print(global_st["models"]["all"])

    # print("sorted_results")
    # print(sorted_results)
    print("global_st dfs score")
    print(global_st["dfs"]["score"])
    # ---------------------------------
    # ---------------------------------
    # PREDICCION DE PRECIOS FUTUROS
    # ---------------------------------
    # ---------------------------------

    # Crear base para el DataFrame
    lag = global_st["models"]["lag"]
    print(lag)
    data = global_st["dfs"]["data"].copy()

    last_prices = data['close'].iloc[-lag:].values
    last_real_values = data[['time', 'close']].iloc[-lag:]
    last_real_values.columns = ['date', 'real']  # Renombrar columnas

    # Generar las fechas futuras (incrementando en 1 unidad temporal por predicción)
    # future_dates = [last_real_values['date'].iloc[-1] + pd.Timedelta(minutes=i+5) for i in range(lag)]
    # Generar las fechas futuras con incrementos de 5 minutos
    future_dates = [pd.to_datetime(last_real_values['date'].iloc[-1]) + pd.Timedelta(minutes=5 * (i + 1)) for i in range(lag)]

    # Predicción de los próximos 4 precios para cada modelo
    future_predictions = {}
    for name, model in global_st["models"]["all"].items():
        future_predictions[name] = predict_future_prices(model, last_prices, steps=lag)

    # Crear un DataFrame para las predicciones futuras
    predictions_df = pd.DataFrame({'date': future_dates})  # Fechas futuras
    for name, preds in future_predictions.items():
        model_short = ''.join([word[0] for word in name.split()]).lower()  # Abreviatura del modelo
        predictions_df[model_short] = preds  # Añadir predicciones

    # Mostrar el DataFrame final
    global_st["dfs"]["future"] = predictions_df.copy()

    # print(global_st["dfs"]["future"])