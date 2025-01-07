import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
# from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Crear un dataset con las características y el target
def create_features_and_target(df, lag=4):
    X, y = [], []
    for i in range(len(df) - lag):
        X.append(df['close'].iloc[i:i+lag].values)
        y.append(df['close'].iloc[i+lag])
    return np.array(X), np.array(y)

def train(global_st):
    # lag = 4  # Usaremos 4 precios pasados como input
    lag = global_st["models"]["lag"]
    data = global_st["dfs"]["data"].copy()
    data.rename(columns={'time': 'date'}, inplace=True)
    data = data[['date', 'close']]

    X, y = create_features_and_target(data, lag)

    # Dividir en datos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modelos
    global_st["models"]["all"] = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'S V R': SVR(kernel='rbf'),
        # 'MLP Regressor': MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=500, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
        'K-Nearest Neighbors': KNeighborsRegressor(n_neighbors=5)
    }

    # Entrenar y predecir con cada modelo
    predictions = {}
    for name, model in global_st["models"]["all"].items():
        # Entrenamiento
        model.fit(X_train, y_train)
        # Predicciones
        future_inputs = X_test[-1].reshape(1, -1)  # Últimos valores para predecir próximos 4
        pred = []
        for _ in range(lag):
            next_pred = model.predict(future_inputs)[0]
            pred.append(next_pred)
            # Actualizar las entradas futuras
            future_inputs = np.append(future_inputs[:, 1:], [[next_pred]], axis=1)
        predictions[name] = pred

    # Evaluación de los modelos
    global_st["dfs"]["score"] = pd.DataFrame()

    for name, model in global_st["models"]["all"].items():
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        global_st["dfs"]["score"][name] = {'MSE': mse, 'R2': r2}

    # Obtener los últimos 4 valores reales y sus fechas
    last_real_values = data[['date', 'close']].iloc[-lag:]
    last_real_values.columns = ['date', 'real']  # Renombrar las columnas

    # Crear un DataFrame para las predicciones de cada modelo
    global_st["dfs"]["trained"] = pd.DataFrame(last_real_values[['date', 'real']].copy())  # Copiar fechas y valores reales

    # Añadir columnas con predicciones de cada modelo
    for model_name, preds in predictions.items():
        model_short = ''.join([word[0] for word in model_name.split()]).lower()  # Abreviatura del modelo
        global_st["dfs"]["trained"][model_short] = preds  # Añadir predicciones como columna
        
    # Mostrar el resultado
    # print("global_st[dfs][trained]")
    # print(global_st["dfs"]["trained"].tail(3))