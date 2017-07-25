# Data container class for transaction history.
class Transaction:
    def __init__(self, id, currency, tid, ttype, amount, fee, status, confirmations, timestamp, address):
        self.Id = id
        self.Currency = currency
        self.TxId = tid
        self.Type = ttype
        self.Amount = amount
        self.Fee = fee
        self.Status = status
        self.Confirmations = confirmations
        self.Timestamp = timestamp
        self.Address = address

    def tostring(self):
        formattedamount = "{0:.8f}".format(self.Amount)
        formattedfee = "{0:.8f}".format(self.Fee)
        retstr = str(self.Id) + "| " + self.Currency + " " + self.Type + ": " + formattedamount + " Fee: "
        retstr = retstr + formattedfee + " Status: " + self.Status + " Confirmations: " + str(self.Confirmations)
        retstr = retstr + " Timestamp: " + self.Timestamp
        if self.Address:
            retstr = retstr + "| To: " + self.Address
        return retstr
