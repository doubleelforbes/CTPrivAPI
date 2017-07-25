# Data Container for wallet
class Wallet:
    def __init__(self, currencyid, symbol, total, available, unconfirmed, heldfortrades, pendingwithdraw, address,
                 status, statusmessage, baseaddress):
        self.CurrencyId = currencyid
        self.Symbol = symbol
        self.Total = total
        self.Available = available
        self.Unconfirmed = unconfirmed
        self.HeldForTrades = heldfortrades
        self.PendingWithdraw = pendingwithdraw
        self.Address = address
        self.Status = status
        self.StatusMessage = statusmessage
        self.BaseAddress = baseaddress

    def tostring(self):
        formattedtotal = "{0:.8f}".format(self.Total)
        formattedheld = "{0:.8f}".format(self.HeldForTrades)
        formattedavailable = "{0:.8f}".format(self.Available)
        strcurrid = str(self.CurrencyId)
        retstr = "|" + self.Symbol + "(" + strcurrid + ")| Total: " + formattedtotal + " | " + formattedheld
        retstr = retstr + " for trades, leaving " + formattedavailable
        if self.Address:
            retstr = retstr + "\r\nAddress: " + self.Address
        if self.BaseAddress:
            retstr = retstr + "\r\nBase Address: " + self.BaseAddress
        if self.Status:
            retstr = retstr + "\r\nStatus: " + self.Status
        if self.StatusMessage:
            retstr = retstr + "\r\nMessage: " + self.StatusMessage
        return retstr
