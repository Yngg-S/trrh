# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 03:44:39 2017
#full functions here http://www.robin-stocks.com/en/latest/functions.html
@author: Yangyang Sun
"""
import robin_stocks as r
import matplotlib.pyplot as plt
import numpy as np
import time


#%%

login =r.login('sunyangyang925st@gmail.com','Qbao925@rh')


#r.authentication.logout()



#%%
my_stocks = r.build_holdings()
for key,value in my_stocks.items():
    print(key,value)
    
    
    
#%%
# get all the positions
positions_data = r.get_open_stock_positions()
for item in positions_data:
    item['symbol'] = r.get_symbol_by_url(item['instrument'])

#SHOPData = [item for item in positions_data if item['symbol'] == 'SHOP']

#%%
###################################
# place order
order_result = r.orders.order(symbol='shop', 
                          quantity=1, 
                          orderType='limit',
                          trigger='immediate', 
                          side='sell', 
                          limitPrice='822', 
                          stopPrice=None, 
                          timeInForce='gtc', 
                          extendedHours=True)



#A generic order function. All parameters must be supplied.
#
#Parameters:	
#symbol (str) – The stock ticker of the stock to sell.
#quantity (int) – The number of stocks to sell.
#orderType (str) – Either ‘market’ or ‘limit’
#trigger (str) – Either ‘immediate’ or ‘stop’
#side (str) – Either ‘buy’ or ‘sell’
#limitPrice (float) – The price to trigger the market order.
#stopPrice (float) – The price to trigger the limit or market order.
#timeInForce (str) – Changes how long the order will be in effect for. ‘gtc’ = good until cancelled. ‘gfd’ = good for the day. ‘ioc’ = immediate or cancel. ‘opg’ execute at opening.
#extendedHours (Optional[str]) – Premium users only. Allows trading during extended hours. Should be true or false.
#

#%%
#check stock information
st_info = r.stocks.get_historicals('shop', span='week', bounds='regular')    
plt.plot([float(data['close_price']) for data in st_info],'.-')
#%%
top_movers = r.markets.get_top_movers(direction='up', info=None)
for  data in top_movers:
    print(data['symbol'], data['price_movement']['market_hours_last_movement_pct'])

#%%
plt.ion()
plt.close('all')
fig,ax = plt.subplots(nrows=3, ncols=1)
plt.subplots_adjust(hspace=0.5)

while True:
    try:
        ax[0].clear()
        ax[1].clear()
        ax[2].clear()
        price_book = r.stocks.get_pricebook_by_symbol(symbol = 'shop', info=None)
        ax[0].plot([float(data['price']['amount']) for data in price_book['asks']],[float(data['quantity']) for data in price_book['asks']],'r.-')
        ax[0].plot([float(data['price']['amount']) for data in price_book['bids']],[float(data['quantity']) for data in price_book['bids']],'g.-')
        ax[0].set_title('bids-spread '+
                        price_book['bids'][0]['price']['amount']+'  '+
                        str(round(float(price_book['asks'][0]['price']['amount'])-
                                  float(price_book['bids'][0]['price']['amount']),2)
                              )
                        )
        ax[0].set_xlim(float(price_book['bids'][0]['price']['amount'])-9,
                       float(price_book['asks'][0]['price']['amount'])+9)
        ax[0].set_ylim(0,1000)
        
        price_book = r.stocks.get_pricebook_by_symbol(symbol = 'spy', info=None)
        ax[1].plot([float(data['price']['amount']) for data in price_book['asks']],[float(data['quantity']) for data in price_book['asks']],'r.-')
        ax[1].plot([float(data['price']['amount']) for data in price_book['bids']],[float(data['quantity']) for data in price_book['bids']],'g.-')
        ax[1].set_title('bids-spread '+
                        price_book['bids'][0]['price']['amount']+'  '+
                        str(round(float(price_book['asks'][0]['price']['amount'])-
                                  float(price_book['bids'][0]['price']['amount']),2)
                              )
                        )
        ax[1].set_xlim(float(price_book['bids'][0]['price']['amount'])-2,
                       float(price_book['asks'][0]['price']['amount'])+2)
        ax[1].set_ylim(0,5000)
        
        
        price_book = r.stocks.get_pricebook_by_symbol(symbol = 'dia', info=None)
        ax[2].plot([float(data['price']['amount']) for data in price_book['asks']],[float(data['quantity']) for data in price_book['asks']],'r.-')
        ax[2].plot([float(data['price']['amount']) for data in price_book['bids']],[float(data['quantity']) for data in price_book['bids']],'g.-')
        ax[2].set_title('bids-spread '+
                        price_book['bids'][0]['price']['amount']+'  '+
                        str(round(float(price_book['asks'][0]['price']['amount'])-
                                  float(price_book['bids'][0]['price']['amount']),2)
                              )
                        )
        ax[2].set_xlim(float(price_book['bids'][0]['price']['amount'])-2,
                       float(price_book['asks'][0]['price']['amount'])+2)
        ax[2].set_ylim(0,1000)
        
        
        
        
        plt.pause(0.8)
        fig.canvas.draw()
        
    except KeyboardInterrupt:
        break
#%%
plt.ion()
plt.close('all')
fig,ax = plt.subplots(nrows=1, ncols=2)
while (1):
    
    
    
    
        
        
    price_book = r.stocks.get_pricebook_by_symbol(symbol = 'shop', info=None)
    ax[0].plot([float(data['price']['amount']) for data in price_book['asks']],[float(data['quantity']) for data in price_book['asks']],'r.-')
    ax[0].plot([float(data['price']['amount']) for data in price_book['bids']],[float(data['quantity']) for data in price_book['bids']],'g.-')
    ax[0].set_title('bids-asks distribution')
    ax[0].set_xlim(float(price_book['asks'][0]['price']['amount'])-20,
                   float(price_book['asks'][0]['price']['amount'])+20)
    
    st_info = r.stocks.get_historicals('shop', span='day', bounds='regular')    
    ax[1].plot([float(data['close_price']) for data in st_info],'.-')
    ax[1].set_title(['price one day: ',st_info[-1]['close_price']])
    plt.pause(2)
    plt.draw()
    
#%%
    
# market buy
#Buy 10 shares of Apple at market price
r.order_buy_market('shop',10)

#limit sell
positions_data = r.get_open_stock_positions()
## Note: This for loop adds the stock ticker to every order, since Robinhood
## does not provide that information in the stock orders.
## This process is very slow since it is making a GET request for each order.



#for item in positions_data:
#    item['symbol'] = r.get_symbol_by_url(item['instrument'])
#TSLAData = [item for item in positions_data if item['symbol'] == 'SHOP']
#sellQuantity = float(TSLAData['quantity'])//2.0
#r.order_sell_limit('SHOP',sellQuantity,200.00)

#%%
#dict_keys(['chain_id', 
#           'chain_symbol', 
#           'created_at', 
#           'expiration_date', 
#           'id', 
#           'issue_date', 
#           'min_ticks', 
#           'rhs_tradability', 
#           'state', 
#           'strike_price', 
#           'tradability', 
#           'type', 
#           'updated_at', 
#           'url',
#           'sellout_datetime',
#           'adjusted_mark_price',
#           'ask_price', 'ask_size',
#           'bid_price', 'bid_size', 
#           'break_even_price',
#           'high_price',
#           'instrument',
#           'last_trade_price', 'last_trade_size', 
#           'low_price', 
#           'mark_price', 
#           'open_interest', 
#           'previous_close_date',
#           'previous_close_price',
#           'volume',
#           'chance_of_profit_long', 'chance_of_profit_short',
#           'delta', 'gamma', 'implied_volatility', 'rho', 'theta', 'vega', 
#           'high_fill_rate_buy_price', 'high_fill_rate_sell_price', 'low_fill_rate_buy_price', 'low_fill_rate_sell_price'])

optionData = r.find_options_for_list_of_stocks_by_expiration_date(['shop'],
             expirationDate='2020-06-26',optionType='call')

print(' symbol - ',optionData[0]['chain_symbol'],' Market price - ',optionData[0]['mark_price'],' exp - ',optionData[0]['expiration_date'])

for item in optionData:
    if item['volume']>2 and item['open_interest']>200:
        print(' price: ',item['strike_price'],'/',item['break_even_price'],' open interest',item['open_interest'],'/',item['volume'],' delta - ',item['delta'],' theta - ',item['theta'])