import dash
from dash import html

from datetime import datetime

from subgrounds.components import LinePlot
from subgrounds.schema import TypeRef
from subgrounds.subgraph import Subgraph, SyntheticField

uniswapV2 = Subgraph.of_url("https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")

# This is unecessary, but nice for brevity
Query = uniswapV2.Query
Swap = uniswapV2.Swap

# This is a synthetic field
Swap.price1 = abs(Swap.amount0In - Swap.amount0Out) / abs(Swap.amount1In - Swap.amount1Out)

# This is a synthetic field
Swap.datetime = SyntheticField(
  uniswapV2,
  lambda timestamp: str(datetime.fromtimestamp(timestamp)),
  TypeRef.Named('String'),
  Swap.timestamp,
)

# Dashboard
app = dash.Dash(__name__)

app.layout = html.Div(
  html.Div([
    html.Div([
      LinePlot(
        Query.swaps,
        component_id='price',
        orderBy=Swap.timestamp,
        orderDirection="desc",
        first=500,
        where=[
          Swap.pair == "0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc"
        ],
        x=Swap.datetime,
        y=Swap.price1
      )
    ])
  ])
)

if __name__ == '__main__':
  app.run_server(debug=True)