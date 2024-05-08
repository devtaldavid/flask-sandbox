import base64
from io import BytesIO

from flask import Flask, request

from matplotlib.figure import Figure

share_price = 20.0
dps = 0.48

# DRIP function
def drip_shares(shares):
    shares = float(shares)
    shares_series = [shares]
    for i in range(1, 20):
        shares += shares * dps / share_price
        shares_series.append(shares)\

    return shares_series

# App

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/drip', methods=['GET'])
def drip():
    ticker = request.args.get('ticker')
    shares = request.args.get('shares')
    if not ticker:
        return "No ticker given."
    elif not shares:
        return "No shares given."
    
    shares = float(shares)
    y_series = drip_shares(shares)
    cost = shares * share_price
    portfolio_value = y_series[-1] * share_price
    
    # Generate the figure **without using pyplot**.
    fig = Figure()
    fig.set_figwidth(10)
    ax = fig.subplots()
    ax.plot(range(1, 21), y_series)
    ax.set_xticks(range(1, 21))
    ax.set_xlabel("Ex-Dividend Dates")
    ax.set_ylabel("Total Shares Accumulated")
    
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return f"""<h2>Ticker: {ticker}</h2>
        <h2>Shares: {shares}</h2>
        <h3>Share Price: ${share_price:.2f}</h3>
        <h3>Cost: ${cost:.2f}</h3>
        <h3>Dividend Per Share: ${dps:.2f}</h3>
        <h3>Ending Portfolio Value: ${portfolio_value:.2f}</h3>
        <img src='data:image/png;base64,{data}'/>"""

@app.route('/drip/api', methods=['GET'])
def drip_api():
    ticker = request.args.get('ticker')
    shares = request.args.get('shares')
    if not ticker:
        return "No ticker given."
    elif not shares:
        return "No shares given."
    
    shares = float(shares)
    y_series = drip_shares(shares)
    cost = shares * share_price
    portfolio_value = y_series[-1] * share_price
    
    return y_series