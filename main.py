import ccxt
import pandas as pd
import time
from datetime import datetime
import dontshare


# Configuración del intercambio
exchange = ccxt.binanceusdm({
    'apiKey': dontshare.API_KEY,
    'secret': dontshare.API_SECRET,
    'rateLimit': 1200,
    'enableRateLimit': True  # Reemplaza con tu propia API secret
})

# Configuración del par de criptomonedas y el período de tiempo
symbol = 'BTC/USDT'
timeframe = '1h'

amount = 0.00854
#los rates de de TP y SL se manejan en %10 == 0.01
rateTP = 0.0043
rateSL = 0.05

# Función para verificar si hay una posición abierta
def active_position(symbol,side):
        #long = 0
        #short = 1
        #pregunta si hay alguna position activa del simbolo
        try:
            postion = exchange.fetch_positions([symbol])
            if (side == 'long'):
                number_side = 0  
            elif(side == 'short'):
                number_side = 1
            else:
                return None
            PNL = postion[number_side]['info']['unRealizedProfit']
        
            if(float(PNL) != 0):
                    return True
            else:
                    return False
        except Exception as e:
            return None

# Funciones para detectar cruces alcistas (crossover) y bajistas (crossunder)
def crossover_series(x: pd.Series, y: pd.Series, cross_distance: int = None) -> pd.Series:
    shift_value = 1 if not cross_distance else cross_distance
    return (x > y) & (x.shift(shift_value) < y.shift(shift_value))

def crossunder_series(x: pd.Series, y: pd.Series, cross_distance: int = None) -> pd.Series:
    shift_value = 1 if not cross_distance else cross_distance
    return (x < y) & (x.shift(shift_value) > y.shift(shift_value))

# Función para realizar operaciones basadas en señales de cruces
def execute_trades():
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker['last']
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    ema_short_period = 12
    ema_long_period = 23
    df['ema_short'] = df['close'].rolling(window=ema_short_period).mean()
    df['ema_long'] = df['close'].rolling(window=ema_long_period).mean()

    crossover_signals = crossover_series(df['ema_short'],df['ema_long'])
    crossunder_signals = crossunder_series(df['ema_short'],df['ema_long'])

    if crossover_signals.iloc[-1] and (not active_position(symbol,'long')):
        position = active_position(symbol,'long')
        print(f"valor de la positio long:{position}")
        # Generar una señal de COMPRA
        print(f"[{current_time}] Señal de COMPRA detectada. Realizar operación de COMPRA.")
        print(f'[{current_time}] Precio actual de {symbol}: {current_price} USDT')
        
        # Aquí puedes colocar tu lógica para realizar una operación de COMPRA en el intercambio.
        #ordenes de short
       
        if (active_position(symbol,'short')):
            exchange.cancel_all_orders(symbol)
            cancelShort = exchange.create_order(symbol,'MARKET','buy' ,amount ,params={"positionSide":"SHORT"})
        
        #ordenes
        orden = exchange.create_order(symbol,'MARKET','buy' ,amount ,params={"positionSide":"LONG"})
        takeProfit = current_price+current_price*rateTP
        stopLoss = current_price-current_price*rateSL
        ordenTP = exchange.create_order(symbol,'TAKE_PROFIT_MARKET','sell' ,amount ,params={'stopPrice': takeProfit,"positionSide":"LONG"} )
        ordenSL = exchange.create_order(symbol,'STOP_MARKET','sell' ,amount ,params={'stopPrice': stopLoss,"positionSide":"LONG"} )


    elif crossunder_signals.iloc[-1] and (not active_position(symbol,'short')):
        position = active_position(symbol,'short')
        print(f"valor de la positio short:{position}")
        # Generar una señal de VENTA
        print(f"[{current_time}] Señal de VENTA detectada. Realizar operación de VENTA.")
        print(f'[{current_time}] Precio actual de {symbol}: {current_price} USDT')
        # Aquí puedes colocar tu lógica para realizar una operación de VENTA en el intercambio.
        
        if (active_position(symbol,'long')):
            exchange.cancel_all_orders(symbol)
            cancelLong = exchange.create_order(symbol,'MARKET','sell' ,amount ,params={"positionSide":"LONG"})
        
        #ordenes
        orden = exchange.create_order(symbol,'MARKET','sell' ,amount ,params={"positionSide":"SHORT"} )
        takeProfit = current_price-current_price*rateTP
        stopLoss = current_price+current_price*rateSL
        ordenTP = exchange.create_order(symbol,'TAKE_PROFIT_MARKET','buy' ,amount ,params={'stopPrice': takeProfit,"positionSide":"SHORT"} )
        ordenSL = exchange.create_order(symbol,'STOP_MARKET','buy' ,amount ,params={'stopPrice': stopLoss,"positionSide":"SHORT"} )


    else:
       print(f"[{current_time}] No se detectaron señales de {symbol} de trading en este momento.")
        

# Ejecuta el bot
if __name__ == '__main__':
    while True:
        execute_trades()
        time.sleep(900)
