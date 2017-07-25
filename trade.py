# Data container class for trade history.
class Trade:
    def __init__(self, tradeid, tradepairid, market, ttype, rate, amount, total, fee, timestamp):
        self.TradeId = tradeid
        self.TradePairId = tradepairid
        self.Market = market
        self.Type = ttype
        self.Rate = rate
        self.Amount = amount
        self.Total = total
        self.Fee = fee
        self.TimeStamp = timestamp

    def tostring(self):
        formattedamount = "{0:.8f}".format(self.Amount)
        formattedrate = "{0:.8f}".format(self.Rate)
        formattedtotal = "{0:.8f}".format(self.Total)
        formattedfee = "{0:.8f}".format(self.Fee)
        retstr = str(self.TradeId) + "| " + self.Market + " - " + self.Type + ": " + formattedamount + " ("
        retstr = retstr + formattedfee + " Fee)"+ " @ " + formattedrate + " Return\Cost: " + formattedtotal
        return retstr
