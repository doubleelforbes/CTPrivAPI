# CTPrivAPI
Cryptopia Private API Frontend

Cryptopia.co.nz offers both Public and Private API's for accessing their market data.
CTPrivAPI (Cryptopia Private API) offers a desktop based interface to the users data,
this data is obtained via creating an account at Cryptopia.co.nz and generating API keys.

The Code
========
Order, Trade, Transaction and Wallet Classes are designed to store units of data from the JSON
object returned from the API.  main.py directs everything in this example as although comms is
more difficult the crossing over of functions is a lot easier.
Most should find it well commented enough to understand.
This is my second Python 3.6 piece.  I didn't thread it as I have the public one,
but I intend to.  As well as a few other updates and improvements to follow.

The GUI
=======
On launch, the GUI has everything input disabled bar the 2x API key fields and the Auth button.
Upon entry of acceptable keys an API object is created and the GUI is released.
The Reset button restores the GUI and destroys any objects created.
Get Wallets : Returns all wallets, the API can return a single.
Get Open Orders : Returns all open / unfilled trade orders.
Get Trade History : Returns previous trades for all tradepairs, API can return single.
Get Transaction History : Return all crypto Deposit / Withdraws - Needs sorting by date.
Get Deposit Address : Returns or Generates an address for given currency.
Cancel Order : Cancels the selected open order.
Cancel TradePair Order : Cancels all orders of the same TradePair type as the selected order.
Cancel All Orders : Cancels All Orders.
Tip : Tip the Trollbox (Chat), params: Currency, No. of Users to Tip, Amount.
Withdraw : Withdraw to another crypto wallet, params: Currency, Address, Amount, PayID(opt).
Transfer : Transfer funds to another Cryptopia user, params: Currency, Username, Amount
Buy & Sell : Using the MarketID, Rate and Sum fields the user may submit an open order.
All listboxes will invoke a ToString() for the object it represents.
There are a number of issues I have yet to remedy including threading, transaction sorting and
some UI tidying.  The Transfer function returns an API error even though the funds move, awaiting
cryptopias response on this.  These will follow in future commits, however all Get functions and
the submit trade functions operate as they should.
