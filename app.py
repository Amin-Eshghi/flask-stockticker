
import requests
import pandas
import simplejson as json
from bokeh.plotting import figure
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from bokeh.resources import CDN
from bokeh.models.renderers import DataRenderer
from flask import Flask,render_template,request,redirect,session
import datetime as dt
import quandl

app = Flask(__name__)

app.vars={}
quandl.ApiConfig.api_key = "oAFnyLMisuxB9D8u8_mU"

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/graph', methods=['POST'])
def graph():   

    app.vars['ticker'] = request.form['ticker']

    stockticker = app.vars['ticker']
    df = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['ticker', "date", "open", "high", "low", "close"] },\
            ticker = [stockticker])

    df['date'] = pandas.to_datetime(df['date'])

    p = figure(title='Stock prices for %s' % app.vars['ticker'],
        x_axis_label='date',
        x_axis_type='datetime')
        
    if request.form.get('close'):
        p.line(x=df['date'].values, y=df['close'].values,line_width=2, legend_label='Close')
    if request.form.get('open'):
        p.line(x=df['date'].values, y=df['open'].values,line_width=2, line_color="green", legend_label='Open')
    if request.form.get('high'):
        p.line(x=df['date'].values, y=df['high'].values,line_width=2, line_color="red", legend_label='High')
    if request.form.get('low'):
        p.line(x=df['date'].values, y=df['low'].values,line_width=2, line_color="purple", legend_label='Low')
    script, div = components(p)
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)
