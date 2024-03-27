import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import numpy as np
import yfinance as yf
def calcular_wavetrend(precios):
    n1 = 10  # Channel Length
    n2 = 21  # Average Length
    hlc3 = (precios['High'] + precios['Low'] + precios['Close']) / 3

    esa = hlc3.ewm(span=n1, adjust=False).mean()
    d = abs(hlc3 - esa).ewm(span=n1, adjust=False).mean()
    ci = (hlc3 - esa) / (0.015 * d)
    tci = ci.ewm(span=n2, adjust=False).mean()

    wt1 = tci
    wt2 = wt1.rolling(window=4).mean()

    return wt1, wt2
# Función para obtener tanto el precio de cierre ajustado como el volumen
def obtener_datos_volumen_accion(simbolo):
    fecha_final = dt.datetime.now()
    fecha_inicial = fecha_final - dt.timedelta(days=365)  # Último año
    
    ticker = yf.Ticker(simbolo)
    # Utilizar "history" para obtener los datos históricos del ticker
    datos = ticker.history(start=fecha_inicial, end=fecha_final)
    
    # Devuelve un DataFrame con las columnas 'Close' y 'Volume'
    return datos[['Close', 'Volume', 'High', 'Low']]
# Calcula el promedio de volumen en un período dado
def calcular_volumen_promedio(volumenes, periodo=20):
    return volumenes.rolling(window=periodo).mean()
# Calcula la Media Móvil Simple
def calcular_ma(precios, periodo):
    return precios.rolling(window=periodo).mean()

# Calcula el MACD
def calcular_macd(precios):
    exp1 = precios.ewm(span=12, adjust=False).mean()
    exp2 = precios.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# Calcula el RSI
def calcular_rsi(precios, periodo=14):
    delta = precios.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Calcula las Bandas de Bollinger
def calcular_bollinger_bands(precios, periodo=20, num_desviaciones=2):
    sma = precios.rolling(window=periodo).mean()
    std = precios.rolling(window=periodo).std()
    bollinger_up = sma + (std * num_desviaciones)
    bollinger_down = sma - (std * num_desviaciones)
    return bollinger_up, bollinger_down

# Función para obtener datos de una acción
def obtener_datos_accion(simbolo):
    fecha_final = dt.datetime.now()
    fecha_inicial = fecha_final - dt.timedelta(days=365)  # Último año
    
    ticker = yf.Ticker(simbolo)
    # Utilizar "history" para obtener los datos históricos del ticker
    datos = ticker.history(start=fecha_inicial, end=fecha_final)
    
    # Devuelve un DataFrame con las columnas 'Close' y 'Volume'
    return datos['Close']

# Análisis de la Media Móvil
def analizar_ma(simbolo):
    precios = obtener_datos_accion(simbolo)
    ma30 = calcular_ma(precios, 30)
    ma180 = calcular_ma(precios, 180)
    if ma30.iloc[-1] > ma180.iloc[-1]:
        return "Comprar"
    elif ma30.iloc[-1] < ma180.iloc[-1]:
        return "Vender"
    else:
        return "Mantener"

# Análisis de MACD
def analizar_macd(simbolo):
    precios = obtener_datos_accion(simbolo)
    macd, signal = calcular_macd(precios)
    
    if macd.iloc[-1] > signal.iloc[-1]:
        return "Comprar"
    elif macd.iloc[-1] < signal.iloc[-1]:
        return "Vender"
    else:
        return "Mantener"

# Análisis de RSI
def analizar_rsi(simbolo):
    precios = obtener_datos_accion(simbolo)
    rsi = calcular_rsi(precios)
    
    if rsi.iloc[-1] < 30:
        return "Comprar"
    elif rsi.iloc[-1] > 70:
        return "Vender"
    else:
        return "Mantener"

# Análisis de Bandas de Bollinger
def analizar_bollinger(simbolo):
    precios = obtener_datos_accion(simbolo)
    bollinger_up, bollinger_down = calcular_bollinger_bands(precios)
    
    # Accediendo al último valor de cada serie con .iloc[-1]
    if precios.iloc[-1] > bollinger_up.iloc[-1]:
        return "Vender"
    elif precios.iloc[-1] < bollinger_down.iloc[-1]:
        return "Comprar"
    else:
        return "Mantener"

def analizar_volumen(simbolo):
    datos = obtener_datos_volumen_accion(simbolo)
    precios = datos['Close']
    volumenes = datos['Volume']
    
    volumen_promedio = calcular_volumen_promedio(volumenes)
    ultimo_volumen = volumenes.iloc[-1]
    volumen_promedio_reciente = volumen_promedio.iloc[-1]
    
    # Establece tus propios umbrales para "significativamente más alto" o "más bajo"
    umbral_alto = 1.5  # Ejemplo: 50% más alto que el promedio
    umbral_bajo = 0.5  # Ejemplo: 50% más bajo que el promedio
    
    if ultimo_volumen > (volumen_promedio_reciente * umbral_alto):
        return "Comprar"
    elif ultimo_volumen < (volumen_promedio_reciente * umbral_bajo):
        return "Vender"
    else:
        return "Mantener"

def recomendacion_general(simbolo):
    try:
        resultados = {
            "Comprar": 0,
            "Vender": 0,
            "Mantener": 0
        }
        datos = obtener_datos_volumen_accion(simbolo)
        # Obtener recomendaciones individuales
        resultados[analizar_ma(simbolo)] += 1
        resultados[analizar_macd(simbolo)] += 1
        resultados[analizar_rsi(simbolo)] += 1
        resultados[analizar_bollinger(simbolo)] += 1
        resultados[analizar_volumen(simbolo)] += 1
                # Análisis de WaveTrend
        wt1, wt2 = calcular_wavetrend(datos)
        if wt1.iloc[-1] > wt2.iloc[-1]:  # Considera tus propias condiciones para Comprar o Vender basadas en WaveTrend
            resultados["Comprar"] += 1
        elif wt1.iloc[-1] < wt2.iloc[-1]:
            resultados["Vender"] += 1
        # Determinar la recomendación final basada en la mayoría de votos
        # pero requiere al menos 3 votos para Comprar o Vender, de lo contrario se mantiene
        if resultados["Comprar"] >= 3:
            recomendacion_final = "Comprar" + str(resultados["Comprar"])
        elif resultados["Vender"] >= 3:
            recomendacion_final = "Vender" + str(resultados["Vender"])
        else:
            recomendacion_final = "Mantener"
        return recomendacion_final
    except Exception as e:
        print(f"Error al procesar {simbolo}: {e}")
        raise