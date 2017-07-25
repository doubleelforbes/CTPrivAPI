# Python Dependencies
import time
import threading
import tkinter as tk
from tkinter import Label, LabelFrame, Entry, Text, Button, Listbox, messagebox, simpledialog
# Self Dependencies
import privcapi
import wallet
import order
import trade
import transaction
# Global variables
privapi = ""
# Object containers
wallets = {}
orders = {}
trades = {}
transactions = {}


# Functions
def auth():
    global privapi
    if window.txtpublickey.get() != "":
        if window.txtprivatekey.get() != "":
            # Instantiate API
            privapi = privcapi.PrivCApi(window.txtpublickey.get(), window.txtprivatekey.get())
            debugout("API Object Created with API Key : " + privapi.PublicKey)
            # Disable this button and API input boxes. So as to prevent API duplication.
            window.btnauth.config(state="disabled")
            window.txtprivatekey.config(state="disabled")
            window.txtpublickey.config(state="disabled")
            # Enable the rest of the functions
            window.btngetwallets.config(state="normal")
            window.btngetorders.config(state="normal")
            window.btngettrades.config(state="normal")
            window.btnreset.config(state="normal")
            window.btngettx.config(state="normal")
            window.btngetaddress.config(state="normal")
            window.btncancelorder.config(state="normal")
            window.btncanceltradepair.config(state="normal")
            window.btncancelalltrades.config(state="normal")
            window.txtmarket.config(state="normal")
            window.txtprice.config(state="normal")
            window.txtamount.config(state="normal")
            window.btntip.config(state="normal")
            window.btnwithdraw.config(state="normal")
            window.btntransfer.config(state="normal")
            window.btnbuy.config(state="normal")
            window.btnsell.config(state="normal")
        else:
            debugout("API Secret Empty!")
    else:
        debugout("API Key Empty!")


def getwallets():
    global privapi
    global wallets
    window.lstwallets.delete(0, tk.END)
    debugout("Requesting Wallet Data...")
    balances = privapi.getbalance()
    # Did it return an error or a list?!
    if isinstance(balances, str):
        debugout(balances)
    else:
        iwallets = 0
        inonzero = 0
        for balance in balances:
            # From each wallet in list, pull the vital stats.
            currencyid = balance["CurrencyId"]
            symbol = balance["Symbol"]
            total = balance["Total"]
            available = balance["Available"]
            unconfirmed = balance["Unconfirmed"]
            heldfortrades = balance["HeldForTrades"]
            pendingwithdraw = balance["PendingWithdraw"]
            address = balance["Address"]
            status = balance["Status"]
            statusmessage = balance["StatusMessage"]
            baseaddress = balance["BaseAddress"]
            # Put it in the list
            window.lstwallets.insert(tk.END, symbol)
            # Create a wallet object and store it in the wallets dict via it's currency symbol
            tmpwallet = wallet.Wallet(currencyid, symbol, total, available, unconfirmed, heldfortrades, pendingwithdraw,
                                      address, status, statusmessage, baseaddress)
            wallets[symbol] = tmpwallet
            # Increment the counter
            iwallets = iwallets + 1
            if total > 0:
                inonzero = inonzero + 1
        debugout("Wallet data received, " + str(iwallets) + " wallets, " + str(inonzero) + " wallets with a balance.")


def getdepositaddress():
    global privapi
    global wallets
    if window.lstwallets.curselection():
        selectedwallet = window.lstwallets.get(window.lstwallets.curselection())
        if not wallets[selectedwallet].Address:
            # We don't have one, request it.
            addresses = privapi.getdepositaddress(selectedwallet)
            # Addresses or Error Msg?
            if isinstance(addresses, str):
                debugout(addresses)
            else:
                wallets[selectedwallet].Address = addresses["Address"]
                wallets[selectedwallet].BaseAddress = addresses["BaseAddress"]
                debugout(wallets[selectedwallet].tostring())
        else:
            debugout("Wallet Addresses Exists!\r\n" + wallets[selectedwallet].tostring())
    else:
        debugout("Please select a wallet to fetch an address for!")


def getorders():
    global privapi
    global orders
    window.lstorders.delete(0, tk.END)
    debugout("Requesting Open Orders...")
    orderlist = privapi.getopenorders()
    # Did it return an error or a list?!
    if isinstance(orderlist, str):
        debugout(orderlist)
    else:
        iorders = 0
        for openorder in orderlist:
            orderid = openorder["OrderId"]
            tradepairid = openorder["TradePairId"]
            market = openorder["Market"]
            otype = openorder["Type"]
            rate = openorder["Rate"]
            amount = openorder["Amount"]
            total = openorder["Total"]
            remaining = openorder["Remaining"]
            timestamp = openorder["TimeStamp"]
            tmporder = order.Order(orderid, tradepairid, market, otype, rate, amount, total, remaining, timestamp)
            key = tmporder.tostring()
            orders[key] = tmporder
            window.lstorders.insert(tk.END, key)
            iorders = iorders + 1
        debugout("Open Order data received, " + str(iorders) + " Open orders found.")


def gettrades():
    global privapi
    global trades
    window.lsttrades.delete(0, tk.END)
    debugout("Requesting Trade History...")
    tradelist = privapi.gettradehistory()
    # Did it return an error or a list?!
    if isinstance(tradelist, str):
        debugout(tradelist)
    else:
        itrades = 0
        for tradeevent in tradelist:
            tradeid = tradeevent["TradeId"]
            tradepairid = tradeevent["TradePairId"]
            market = tradeevent["Market"]
            otype = tradeevent["Type"]
            rate = tradeevent["Rate"]
            amount = tradeevent["Amount"]
            total = tradeevent["Total"]
            fee = tradeevent["Fee"]
            timestamp = tradeevent["TimeStamp"]
            tmptrade = trade.Trade(tradeid, tradepairid, market, otype, rate, amount, total, fee, timestamp)
            key = tmptrade.tostring()
            trades[key] = tmptrade
            window.lsttrades.insert(tk.END, key)
            itrades = itrades + 1
        debugout("Trade History data received, " + str(itrades) + " Previous Trades found.")


def gettransactions():
    global privapi
    global transactions
    window.lsttransactions.delete(0, tk.END)
    debugout("Requesting Transaction History...")
    # The API Doesn't allow for Null type or "All" so we have to pull both dicts and combine them.
    txlist = privapi.gettransactions("Deposit")
    # After the first API call we'll check for an error string.
    if isinstance(txlist, str):
        debugout(txlist)
    else:
        txlist = txlist + privapi.gettransactions("Withdraw")
        itx = 0
        for tx in txlist:
            tid = tx["Id"]
            currency = tx["Currency"]
            txid = tx["TxId"]
            ttype = tx["Type"]
            amount = tx["Amount"]
            fee = tx["Fee"]
            status = tx["Status"]
            confirmations = tx["Confirmations"]
            timestamp = tx["Timestamp"]
            address = tx["Address"]
            tmptx = transaction.Transaction(tid, currency, txid, ttype, amount, fee, status, confirmations, timestamp,
                                            address)
            key = tmptx.tostring()
            transactions[key] = tmptx
            window.lsttransactions.insert(tk.END, key)
            itx = itx + 1
        debugout("Transaction History data received, " + str(itx) + " transactions found.")


# Cancel a single trade via it's OrderId
def canceltrade():
    global privapi
    global orders
    if len(orders) > 0:
        if window.lstorders.curselection():
            selectedorder = window.lstorders.get(window.lstorders.curselection())
            orderid = str(orders[selectedorder].OrderId)
            warning = messagebox.askokcancel("############ WARNING!! ############",
                                             "You have requested a cancel on order no: " + orderid)
            if warning:
                ttype = "Trade"
                debugout("Requesting Cancellation of order no. " + orderid)
                response = privapi.canceltrade(ttype, orderid)
                if isinstance(response, str):
                    debugout(response)
                else:
                    orderstr = "Cancel Order ID: " + orderid + " Submitted! "
                    if len(response) > 0:
                        orderstr = orderstr + "Cancelled Order ID's: "
                        for corder in response:
                            orderstr = orderstr + str(corder) + ", "
                    debugout(orderstr)
                getorders()
            else:
                debugout("User cancelled order: " + orderid + " cancellation after warning.")
        else:
            debugout("ERROR! - No Order Selected!")
    else:
        debugout("ERROR! - No Orders Found! Please try again.")
        getorders()


# Cancel All trades for a TradePair via TradePairId
def canceltradepair():
    global privapi
    global orders
    if len(orders) > 0:
        if window.lstorders.curselection():
            selectedorder = window.lstorders.get(window.lstorders.curselection())
            tradepairid = str(orders[selectedorder].TradePairId)
            marketname = orders[selectedorder].Market
            warning = messagebox.askokcancel("############ WARNING!! ############",
                                             "You have requested a cancel on ALL " + marketname + " orders.")
            if warning:
                ttype = "TradePair"
                debugout("Requesting Cancellation of all " + marketname + " trades...")
                response = privapi.canceltrade(ttype, tradepairid)
                if isinstance(response, str):
                    debugout(response)
                else:
                    orderstr = marketname + " TradePair Cancel Submitted! "
                    if len(response) > 0:
                        orderstr = orderstr + "Cancelled Order ID's: "
                        for corder in response:
                            orderstr = orderstr + str(corder) + ", "
                    debugout(orderstr)
                getorders()
            else:
                debugout("User cancelled All " + tradepairid + " cancellation after warning.")
        else:
            debugout("ERROR! - No Order Selected!")
    else:
        debugout("ERROR! - No Orders Found! Please try again.")
        getorders()


# Cancel ALL trades
def cancelalltrades():
    global privapi
    global orders
    if len(orders) > 0:
        warning = messagebox.askokcancel("############ WARNING!! ############",
                                         "You have requested a cancel on ALL trades!")
        if warning:
            ttype = "All"
            response = privapi.canceltrade(ttype)
            if isinstance(response, str):
                debugout(response)
            else:
                orderstr = "All Trade Cancel Submitted! "
                if len(response) > 0:
                    orderstr = orderstr + "Cancelled Order ID's: "
                    for corder in response:
                        orderstr = orderstr + str(corder) + ", "
                debugout(orderstr)
            getorders()
        else:
            debugout("User Cancelled All Trade Cancellation after warning.")
    else:
        debugout("ERROR! - No Orders Found! Please try again.")
        getorders()


# Just a way to use 2 button handlers to start the trade with a binary choice
def buytrade():
    submittrade("Buy")


def selltrade():
    submittrade("Sell")


def submittrade(ttype):
    global privapi
    # Grab the trade data
    market = window.txtmarket.get()
    price = window.txtprice.get()
    amount = window.txtamount.get()
    # Does the market contain something, no further checks
    if market == "":
        debugout("ERROR! - Please provide a market. eg. 'DOT/BTC' or '100'")
    else:
        # Is the price an int / float ?
        try:
            valprice = float(price)
            price = "{0:.8f}".format(valprice)
            # Is the amount an int / float?
            try:
                valamount = float(amount)
                amount = "{0:.8f}".format(valamount)
                warningmsg = "########### WARNING!! #############\r\n"
                warningmsg = warningmsg + "Your Submitted Trade entries have passed\r\n"
                warningmsg = warningmsg + "basic checks, in that market has been\r\n"
                warningmsg = warningmsg + "filled and price & amount are numerical.\r\n"
                warningmsg = warningmsg + "However, you should only proceed at your\r\n"
                warningmsg = warningmsg + "own risk!!\r\n\r\n"
                warningmsg = warningmsg + "No liability will be accepted by the person\r\n"
                warningmsg = warningmsg + "who wrote this free to use code example!\r\n"
                firstwarning = messagebox.askokcancel("WARNING!!!", warningmsg)
                # Annoy the user so they know the risks.
                if firstwarning:
                    debugout("Trade Approved by User after first warning.")
                    warningmsg = "########### WARNING!! #############\r\n"
                    warningmsg = warningmsg + "OK You're determined to do this aren't you?\r\n"
                    warningmsg = warningmsg + "Right! here are your order details\r\n\r\n" + ttype + "\r\n"
                    warningmsg = warningmsg + "Market: " + market + " | Expect (DOT/BTC) or (100)\r\n"
                    warningmsg = warningmsg + "Price: " + price + " | Expect Float / Integer\r\n"
                    warningmsg = warningmsg + "Amount: " + amount + " | Expect Float / Integer\r\n\r\n"
                    warningmsg = warningmsg + "The API should reject any errors, however if\r\n"
                    warningmsg = warningmsg + "any trades are matched in error or losses are\r\n"
                    warningmsg = warningmsg + "made. It's on you!!!"
                    secondwarning = messagebox.askokcancel("SERIOUSLY!!!", warningmsg)
                    # Annoy them again and provide their data to check.
                    if secondwarning:
                        # Submit the trade
                        debugout("Trade Approved by User after second warning.\r\nSubmitting Trade...")
                        response = privapi.submittrade(market, ttype, price, amount)
                        if isinstance(response, str):
                            debugout(response)
                        else:
                            orderid = response["OrderId"]
                            filledorders = response["FilledOrders"]
                            orderstr = market + " " + ttype + " order submitted! "
                            if orderid:
                                orderstr = orderstr + "Open Order No: " + str(orderid) + ". "
                            if len(filledorders) > 0:
                                orderstr = orderstr + "Filled Order ID's: "
                                for forder in filledorders:
                                    orderstr = orderstr + str(forder) + ", "
                            debugout(orderstr)
                        # Clear the form
                        window.txtmarket.delete(0, tk.END)
                        window.txtprice.delete(0, tk.END)
                        window.txtamount.delete(0, tk.END)
                        # Refresh the orders & trades
                        getorders()
                        gettrades()
                    else:
                        debugout("Trade Cancelled by User upon second warning.")
                else:
                    debugout("Trade Cancelled by User upon first warning.")
            except ValueError:
                debugout("ERROR! - Please provide a numerical amount.")
        except ValueError:
            debugout("ERROR! - Please provide a numerical price.")


def tip():
    global privapi
    currency = simpledialog.askstring("Currency Required", "Please provide the currency to tip in (eg. 'DOT' or '2')")
    if currency == "":
        debugout("ERROR! - Cannot tip without a currency!")
    else:
        amount = simpledialog.askfloat("Amount Required", "Please provide an amount of " + currency + " to tip")
        activeusers = simpledialog.askinteger("Number of Users Required",
                                              "Please provide a number of active users to tip (2-100):", initialvalue=2)
        formattedamount = "{0:.8f}".format(amount)
        activeusers = str(activeusers)
        confirm = messagebox.askokcancel("Confirm Tip", "Please confirm that you want to tip the trollbox\r\n" +
                                         "Tip Details:\r\nCurrency: " + currency + "\r\nAmount: " + formattedamount +
                                         "\r\nActive Users receiving: " + activeusers)
        if confirm:
            debugout("User confirmed " + formattedamount + " " + currency + " tip, to " + activeusers + " users.")
            response = privapi.submittip(currency, amount, activeusers)
            # The API is supposed to return a string in any event, it doesn't appear to be at the moment.
            # Just as well I coded my own confirmation!!
            if isinstance(response, str):
                # In this case, the response is always a string.
                debugout(response)
            else:
                # This next line is me getting over the fact that the API returns a Nonetype!!
                pass
                # debugout(str(response) + " is a " + str(type(response)))
        else:
            debugout("User Cancelled Tip after warning.")


def withdraw():
    global privapi
    currency = simpledialog.askstring("Currency Required", "Please provide the currency to withdraw(eg. 'DOT' or '2')")
    if currency == "" or not currency:
        debugout("ERROR! - Cannot withdraw without a currency.")
    else:
        currency = currency.upper()
        address = simpledialog.askstring("Withdrawal Address Required", "Please provide the address to withdraw the " +
                                         currency + " to")
        if address == "" or not address:
            debugout("ERROR! - Withdrawal Address not provided.")
        else:
            amount = simpledialog.askfloat("Amount Required", "Please provide an amount of " + currency +
                                           " to send to: " + address)
            if not amount:
                debugout("ERROR! - Cannot Withdraw without an amount.")
            else:
                amount = "{0:.8f}".format(amount)
                payidreq = messagebox.askyesno("PaymentID for CryptoNote currencies",
                                               "Would you like to provide a Payment ID?\r\n" +
                                               "Only required for CryptoNote.")
                if payidreq:
                    payid = simpledialog.askstring("PaymentID Entry",
                                                   "You have requested Payment ID Entry please provide it.")
                    if payid == "" or not payid:
                        debugout("ERROR! - User requested a Payment ID but failed to provide it.")
                    else:
                        debugout(amount + " " + currency + " withdrawal requested to: " + address + " with PaymentID: "
                                 + payid)
                        response = privapi.submitwithdraw(currency, address, amount, payid)
                        if isinstance(response, str):
                            debugout("Withdrawal submitted under ID: " + response)
                        else:
                            debugout(str(response) + " is a " + str(type(response)))
                        gettransactions()
                else:
                    debugout(amount + " " + currency + " withdrawal requested to: " + address)
                    response = privapi.submitwithdraw(currency, address, amount)
                    # API returns an int ID for the transaction
                    debugout("Withdrawal submitted under ID: " + str(response))
                    gettransactions()


def transfer():
    global privapi
    currency = simpledialog.askstring("Currency Required", "Please provide the currency to transfer (eg. 'DOT' or '2')")
    if currency == "" or not currency:
        debugout("ERROR! - Cannot transfer without a currency.")
    else:
        currency = currency.upper()
        username = simpledialog.askstring("Cryptopia Username Required", "Please provide the username to send " +
                                          currency + " to")
        if username == "" or not username:
            debugout("ERROR! - Transfer Username not provided.")
        else:
            amount = simpledialog.askfloat("Amount Required", "Please provide an amount of " + currency +
                                           " to transfer to " + username)
            if not amount or amount <= 0:
                debugout("ERROR! - Cannot transfer without a valid amount.")
            else:
                amount = "{0:.8f}".format(amount)
                debugout("Transferring " + amount + " " + currency + " to Cryptopia User: " + username)
                response = privapi.submittransfer(currency, username, amount)
                # Well for some reason the API transfers the funds and returns an API Error "Bad Request"
                if isinstance(response, str):
                    debugout(response)
                    debugout("!!! If you received an API error, check your balance, the funds probably sent !!!")
                else:
                    debugout(str(response) + " is a " + str(type(response)))
                    # Do more stuff!


def walletselect(event):
    if window.lstwallets.curselection():
        selectedwallet = window.lstwallets.get(window.lstwallets.curselection())
        debugout(wallets[selectedwallet].tostring())


def orderselect(event):
    if window.lstorders.curselection():
        selectedorder = window.lstorders.get(window.lstorders.curselection())
        debugout(orders[selectedorder].tostring())


def tradeselect(event):
    if window.lsttrades.curselection():
        selectedtrade = window.lsttrades.get(window.lsttrades.curselection())
        debugout(trades[selectedtrade].tostring())


def transactionselect(event):
    if window.lsttransactions.curselection():
        selectedtx = window.lsttransactions.get(window.lsttransactions.curselection())
        debugout(transactions[selectedtx].tostring())


def reset():
    global privapi
    global wallets
    global orders
    global trades
    global transactions
    # Nuke the API instance.
    del privapi
    # Enable the key inputs and auth button
    window.txtpublickey.config(state="normal")
    window.txtprivatekey.config(state="normal")
    window.txtpublickey.delete(0, tk.END)
    window.txtprivatekey.delete(0, tk.END)
    window.btnauth.config(state="normal")
    # Disable the rest
    window.btngetwallets.config(state="disabled")
    window.btngetorders.config(state="disabled")
    window.btngettrades.config(state="disabled")
    window.btngettx.config(state="disabled")
    window.btnreset.config(state="disabled")
    window.btngetaddress.config(state="disabled")
    window.btncancelorder.config(state="disabled")
    window.btncanceltradepair.config(state="disabled")
    window.btncancelalltrades.config(state="disabled")
    window.lstwallets.delete(0, tk.END)
    window.lstorders.delete(0, tk.END)
    window.lsttrades.delete(0, tk.END)
    window.lsttransactions.delete(0, tk.END)
    window.txtmarket.delete(0, tk.END)
    window.txtprice.delete(0, tk.END)
    window.txtamount.delete(0, tk.END)
    window.txtdebug.delete(1.0, tk.END)
    window.txtmarket.config(state="disabled")
    window.txtprice.config(state="disabled")
    window.txtamount.config(state="disabled")
    window.btntip.config(state="disabled")
    window.btnwithdraw.config(state="disabled")
    window.btntransfer.config(state="disabled")
    window.btnbuy.config(state="disabled")
    window.btnsell.config(state="disabled")
    debugout("API Object closed, Inputs Reset.")
    wallets = {}
    orders = {}
    trades = {}
    transactions = {}


def debugout(debugstr):
    window.txtdebug.insert(tk.END, debugstr + "\r\n")
    window.txtdebug.see(tk.END)


# Create top level window object and variables
window = tk.Tk()
# Base windows parameters
window.geometry("1024x768+450+150")
window.resizable(0, 0)
window.title("Cryptopia API")
window.iconbitmap("cryptopia.ico")
# Authentication Frame
window.authframe = LabelFrame(window, text="Authentication for Private API")
window.authframe.place(relx=0.01, rely=0.01, relheight=0.10, relwidth=0.30)
# Public Key Input
window.lblpublic = Label(window.authframe, text="API Key: ")
window.lblpublic.place(relx=0.01, rely=0.01, relheight=0.35, relwidth=0.16)
window.txtpublickey = Entry(window.authframe)
window.txtpublickey.place(relx=0.19, rely=0.01, relheight=0.35, relwidth=0.80)
# Private Key Input
window.lblprivate = Label(window.authframe, text="API Secret: ")
window.lblprivate.place(relx=0.01, rely=0.46, relheight=0.35, relwidth=0.16)
window.txtprivatekey = Entry(window.authframe, show="*")
window.txtprivatekey.place(relx=0.19, rely=0.46, relheight=0.35, relwidth=0.80)
# Functions Frame
window.funcframe = LabelFrame(window, text="Functions")
window.funcframe.place(relx=0.31, rely=0.01, relheight=0.10, relwidth=0.68)
# Auth Button, First and only button enabled, once authed the rest become available.
window.btnauth = Button(window.funcframe, text="Auth", background="green", command=auth)
window.btnauth.place(relx=0.01, rely=0.01, height=24, width=40)
# Fetch Wallets
window.btngetwallets = Button(window.funcframe, text="Get Wallets", state="disabled", command=getwallets)
window.btngetwallets.place(relx=0.07, rely=0.01, height=24, width=85)
# Fetch Open Orders
window.btngetorders = Button(window.funcframe, text="Get Open Orders", state="disabled", command=getorders)
window.btngetorders.place(relx=0.195, rely=0.01, height=24, width=103)
# Get Trade History
window.btngettrades = Button(window.funcframe, text="Get Trade History", state="disabled", command=gettrades)
window.btngettrades.place(relx=0.345, rely=0.01, height=24, width=105)
# Get Transaction History
window.btngettx = Button(window.funcframe, text="Get Transaction History", state="disabled", command=gettransactions)
window.btngettx.place(relx=0.50, rely=0.01, height=24, width=130)
# Reset
window.btnreset = Button(window.funcframe, text="Reset", state="disabled", background="red", command=reset)
window.btnreset.place(relx=0.01, rely=0.45, height=24, width=40)
# Get Deposit Address
window.btngetaddress = Button(window.funcframe, text="Get Deposit Address", state="disabled", command=getdepositaddress)
window.btngetaddress.place(relx=0.07, rely=0.45, height=24, width=120)
# Cancel Single Trade
window.btncancelorder = Button(window.funcframe, text="Cancel Order", state="disabled", background="orange",
                               command=canceltrade)
window.btncancelorder.place(relx=0.245, rely=0.45, height=24, width=75)
# Cancel All TradePair Trades
window.btncanceltradepair = Button(window.funcframe, text="Cancel TradePair Orders", state="disabled",
                                   background="orange", command=canceltradepair)
window.btncanceltradepair.place(relx=0.352, rely=0.45, height=24, width=136)
# Cancel All Trades
window.btncancelalltrades = Button(window.funcframe, text="Cancel All Orders", state="disabled", background="orange",
                                   command=cancelalltrades)
window.btncancelalltrades.place(relx=0.547, rely=0.45, height=24, width=98)
# Tip, Withdraw & Transfer buttons.
window.btntip = Button(window.funcframe, text="Tip", state="disabled", background="orange", command=tip)
window.btntip.place(relx=0.69, rely=0.01, height=17, width=60)
window.btnwithdraw = Button(window.funcframe, text="Withdraw", state="disabled", background="orange", command=withdraw)
window.btnwithdraw.place(relx=0.69, rely=0.32, height=17, width=60)
window.btntransfer = Button(window.funcframe, text="Transfer", state="disabled", background="orange", command=transfer)
window.btntransfer.place(relx=0.69, rely=0.62, height=17, width=60)
# Submit Trade Form
window.lblmarket = Label(window.funcframe, text="Market ID: ")
window.lblmarket.place(relx=0.78, rely=0.01, relwidth=0.09, relheight=0.29)
window.txtmarket = Entry(window.funcframe, state="disabled")
window.txtmarket.place(relx=0.88, rely=0.01, relwidth=0.11, relheight=0.29)
window.lblprice = Label(window.funcframe, text="Rate: ")
window.lblprice.place(relx=0.78, rely=0.30, relwidth=0.045, relheight=0.29)
window.txtprice = Entry(window.funcframe, state="disabled")
window.txtprice.place(relx=0.83, rely=0.30, relwidth=0.12, relheight=0.29)
window.lblamount = Label(window.funcframe, text="Sum: ")
window.lblamount.place(relx=0.78, rely=0.59, relwidth=0.045, relheight=0.29)
window.txtamount = Entry(window.funcframe, state="disabled")
window.txtamount.place(relx=0.83, rely=0.59, relwidth=0.12, relheight=0.29)
window.btnbuy = Button(window.funcframe, text="BUY", state="disabled", background="orange", command=buytrade)
window.btnbuy.place(relx=0.95, rely=0.30, height=18, width=30)
window.btnsell = Button(window.funcframe, text="SELL", state="disabled", background="orange", command=selltrade)
window.btnsell.place(relx=0.95, rely=0.59, height=18, width=30)
# Main Interface Frame
window.mainframe = LabelFrame(window, text="Main")
window.mainframe.place(relx=0.01, rely=0.11, relheight=0.64, relwidth=0.98)
# List of Wallets
window.lblwallets = Label(window.mainframe, text="Wallets")
window.lblwallets.place(relx=0.01, rely=0.01, relheight=0.03, relwidth=0.08)
window.lstwallets = Listbox(window.mainframe)
window.lstwallets.bind("<<ListboxSelect>>", walletselect)
window.lstwallets.place(relx=0.01, rely=0.04, relheight=0.95, relwidth=0.08)
# List of Open Orders
window.lblorders = Label(window.mainframe, text="Open Orders")
window.lblorders.place(relx=0.09, rely=0.01, relheight=0.03, relwidth=0.90)
window.lstorders = Listbox(window.mainframe)
window.lstorders.bind("<<ListboxSelect>>", orderselect)
window.lstorders.place(relx=0.09, rely=0.04, relheight=0.29, relwidth=0.90)
# List of previous Trades
window.lbltrades = Label(window.mainframe, text="Trade History")
window.lbltrades.place(relx=0.09, rely=0.33, relheight=0.03, relwidth=0.90)
window.lsttrades = Listbox(window.mainframe)
window.lsttrades.bind("<<ListboxSelect>>", tradeselect)
window.lsttrades.place(relx=0.09, rely=0.36, relheight=0.30, relwidth=0.90)
# Transaction History
window.lbltransactions = Label(window.mainframe, text="Transaction History")
window.lbltransactions.place(relx=0.09, rely=0.67, relheight=0.03, relwidth=0.90)
window.lsttransactions = Listbox(window.mainframe)
window.lsttransactions.bind("<<ListboxSelect>>", transactionselect)
window.lsttransactions.place(relx=0.09, rely=0.70, relheight=0.29, relwidth=0.90)
# Debug Frame
window.debugframe = LabelFrame(window, text="Debug")
window.debugframe.place(relx=0.01, rely=0.75, relheight=0.25, relwidth=0.98)
window.txtdebug = Text(window.debugframe)
window.txtdebug.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)
# Start the gui loop.
window.mainloop()
