# Private API Class for cryptopia.co.nz
import json
import base64
import hashlib
import hmac
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import time


class PrivCApi:
    def __init__(self, apipublickey, apisecretkey):
        self.iNonce = 0
        self.PublicKey = apipublickey
        self.SecretKey = apisecretkey
        self.BaseURL = "https://www.cryptopia.co.nz/Api"

    # Auto increment the nonce, stick it to a timestamp and return the string
    def __noncifier__(self):
        self.iNonce = self.iNonce + 1
        noncehash = str(self.iNonce) + "." + str(int(time.time()))
        return noncehash

    # Return all or one specific balance.
    def getbalance(self, currency=None):
        # Set up JSON object for parameters.
        params = {}
        # Has a coin been specified?
        if not currency:
            params["Currency"] = ""
        else:
            curkey = self.currencykeyer(currency)
            params[curkey] = currency
        return self.makejsonquery("/GetBalance", params)

    # Return / Generate a deposit address
    def getdepositaddress(self, currency):
        params = {}
        curkey = self.currencykeyer(currency)
        params[curkey] = currency
        return self.makejsonquery("/GetDepositAddress", params)

    # Return Open order list
    def getopenorders(self, market=None, count="100"):
        params = {}
        if not market:
            params["Market"] = ""
        else:
            markey = self.marketkeyer(market)
            params[markey] = market
        # Either pass the overridden parameter or use the default of 100.
        params["Count"] = str(count)
        return self.makejsonquery("/GetOpenOrders", params)

    # Return Trade History list.
    def gettradehistory(self, market=None, count="100"):
        params = {}
        if not market:
            params["Market"] = ""
        else:
            markey = self.marketkeyer(market)
            params[markey] = market
        # Either pass the overridden parameter or use the default of 100.
        params["Count"] = str(count)
        return self.makejsonquery("/GetTradeHistory", params)

    # Returns deposit and withdrawal history
    def gettransactions(self, ttype, count="100"):
        params = {}
        params["Type"] = ttype
        params["Count"] = count
        return self.makejsonquery("/GetTransactions", params)

    # Submits a live trade
    def submittrade(self, market, ttype, rate, amount):
        params = {}
        markey = self.marketkeyer(market)
        params[markey] = market
        params["Type"] = ttype
        params["Rate"] = rate
        params["Amount"] = amount
        return self.makejsonquery("/SubmitTrade", params)

    # Cancels a live trade.
    def canceltrade(self, ttype, cancelid=None):
        params = {}
        params["Type"] = ttype
        if ttype == "All":
            # No further Parameters, cancel All!
            pass
        elif ttype == "Trade":
            # It's a single cancel, ID = OrderID
            if not cancelid:
                return "ERROR! - Specific Order Cancel requested without Order ID."
            else:
                params["OrderId"] = str(cancelid)
        elif ttype == "TradePair":
            # It's a broad TradePair Cancel, ID = TradePairID
            if not cancelid:
                return "ERROR! - Broad TradePair Cancel requested without TradePair ID."
            else:
                params["TradePairId"] = str(cancelid)
        else:
            return "ERROR! - Invalid Cancel Type: (" + ttype + ").  Please provide (All, Trade or TradePair)"
        return self.makejsonquery("/CancelTrade", params)

    # Tip the trollbox
    def submittip(self, currency, amount, activeusers):
        params = {}
        curkey = self.currencykeyer(currency)
        params[curkey] = currency
        params["Amount"] = amount
        params["ActiveUsers"] = activeusers
        return self.makejsonquery("/SubmitTip", params)

    # Withdraw any currency
    def submitwithdraw(self, currency, address, amount, paymentid=None):
        params = {}
        curkey = self.currencykeyer(currency)
        params[curkey] = currency
        params["Address"] = address
        params["Amount"] = amount
        if paymentid:
            params["PaymentId"] = paymentid
        return self.makejsonquery("/SubmitWithdraw", params)

    # Transfer any currency to another Cryptopia user.
    def submittransfer(self, currency, username, amount):
        params = {}
        curkey = self.currencykeyer(currency)
        params[curkey] = currency
        params["Username"] = username
        params["Amount"] = amount
        return self.makejsonquery("/SubmitTransfer", params)

    # Takes a market input and returns whether it's a Market name or a TradePairID
    def marketkeyer(self, market):
        try:
            # Is it an int?
            # Worst case for future proofing I can imagine is that a 1337/42 market emerges and somehow this returns,
            # 31.83333333333333 !!!!! :|
            val = int(market)
            return "TradePairID"
        except ValueError:
            # Character containing, Definitely a market.  As I hinted above any '/' should really always trigger this
            # clause.......... I hope!
            return "Market"

    # Takes a currency input and returns whether it's a Currency name or a CurrencyID
    def currencykeyer(self, currency):
        # List of numerical symbol names, add to this list as currencies emerge with these symbols.
        # In future I intend to make this Public and set it when the wallets are fetched.
        lstnumsymstr = [42, 300, 611, 808, 888, 1337]
        try:
            # Is it an int?
            val = int(currency)
            # Is it a sneaky currency symbol which is in fact an int ?
            if val in lstnumsymstr:
                # It's actually a numerical symbol string
                return "Currency"
            else:
                # OK! Definitely a currency ID
                return "CurrencyId"
        except ValueError:
            # Contains characters! Definitely a currency string.
            return "Currency"

    # Takes subdir (API Function) & parameter dict. Returns error or data.
    def makejsonquery(self, command, params):
        # Append the command to the URL
        uri = self.BaseURL + command
        # Grab the keys, probably don't need to str() them.
        strsecret = str(self.SecretKey)
        strpublic = str(self.PublicKey)
        # Generate and grab the nonce
        tmpnonce = self.__noncifier__()
        # Set up MD5 object, encode params to bytes, MD5 hash
        md5params = hashlib.md5()
        encparams = json.dumps(params).encode("UTF-8")
        md5params.update(encparams)
        # Base64 the MD5 Hash & Return the bytes to a string, then assemble the request string
        b64request = base64.b64encode(md5params.digest())
        str64request = b64request.decode("UTF-8")
        reqstr = strpublic + "POST" + quote_plus(uri).lower() + tmpnonce + str64request
        # Sign the request string with the private key
        try:
            hmacraw = hmac.new(base64.b64decode(strsecret), reqstr.encode("UTF-8"), hashlib.sha256).digest()
        except:
            return "HMAC-SHA256 Signature failed! Check Private Key."
        # Base64 the signed parameters, assemble the header string and dict.
        hmacreq = base64.b64encode(hmacraw)
        header_value = "amx " + strpublic + ":" + hmacreq.decode("UTF-8") + ":" + tmpnonce
        headers = {"Authorization": header_value, "Content-Type": "application/json; charset=utf-8"}
        # Pack into HTTP request and try to open the URL.
        rapi = Request(uri, data=encparams, headers=headers, method="POST")
        try:
            response = urlopen(rapi).read().decode("UTF-8-SIG")
        except HTTPError as e:
            return "HTTP ERROR! : " + e.reason
        # If we got a response it's a json object, Success is bool and either Data or Error strings are returned.
        jsondata = json.loads(response)
        if jsondata.get("Success"):
            return jsondata.get("Data")
        else:
            return "API ERROR! : " + jsondata.get("Error")
