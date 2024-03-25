# Trading Bot con Python y CCXT

Este es un bot de trading escrito en Python que utiliza la biblioteca CCXT para interactuar con el intercambio Binance USDM. El bot está diseñado para detectar señales de cruce de medias móviles exponenciales (EMA) y ejecutar operaciones de compra o venta en función de estas señales.

## Requisitos

- Python 3.x
- Bibliotecas:
  - CCXT
  - Pandas

Puedes instalar las bibliotecas necesarias ejecutando el siguiente comando:

pip install ccxt pandas

## Configuración

Antes de ejecutar el bot, necesitas configurar las siguientes variables:

- `dontshare.API_KEY`: Tu clave de API para Binance USDM.
- `dontshare.API_SECRET`: Tu clave secreta de API para Binance USDM.
- `symbol`: El par de criptomonedas que deseas operar, por ejemplo, 'BTC/USDT'.
- `timeframe`: El marco temporal para los datos del gráfico, por ejemplo, '1h'.
- `amount`: La cantidad de la criptomoneda que deseas comprar o vender en cada operación.
- `rateTP`: El porcentaje de ganancia deseado para el take profit.
- `rateSL`: El porcentaje de pérdida máxima tolerada para el stop loss.

## Uso

Una vez que hayas configurado las variables, puedes ejecutar el bot ejecutando el script Python.

El bot continuará ejecutándose en un bucle infinito, verificando periódicamente las señales de trading y ejecutando operaciones según sea necesario.

## Importante

- Asegúrate de entender completamente el código y las estrategias de trading antes de ejecutar el bot en una cuenta real.
- Utiliza una cuenta de prueba o fondos que estés dispuesto a arriesgar.
- La eficacia del bot puede variar según las condiciones del mercado y otros factores.
