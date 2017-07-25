# Data container class for open orders.
class Order:
    def __init__(self, orderid, tradepairid, market, otype, rate, amount, total, remaining, timestamp):
        self.OrderId = orderid
        self.TradePairId = tradepairid
        self.Market = market
        self.Type = otype
        self.Rate = rate
        self.Amount = amount
        self.Total = total
        self.Remaining = remaining
        self.TimeStamp = timestamp

    def tostring(self):
        formattedamount = "{0:.8f}".format(self.Amount)
        formattedrate = "{0:.8f}".format(self.Rate)
        formattedtotal = "{0:.8f}".format(self.Total)
        formattedremaining = "{0:.8f}".format(self.Remaining)
        retstr = str(self.OrderId) + "| " + self.Market + " - " + self.Type + ": " + formattedamount + " ("
        retstr = retstr + formattedremaining + " remaining)" + " @ " + formattedrate + " Return\Cost: " + formattedtotal
        return retstr
