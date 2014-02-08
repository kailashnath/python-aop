from aop import around

class TransactionHandler(object):

    def doTransaction(self, card, amount):
        return card.debit(amount)


class Card(object):
    def __init__(self, name, balance=100):
        self.name = name
        self.balance = balance

    def debit(self, amount):
        self.balance -= amount
        return self.balance


class Vendor(object):
    def __init__(self, trans=TransactionHandler):
        self.transHandler = trans()

    def transact(self, card):
        return self.transHandler.doTransaction(card, 300)


def checkBalance(transHandler, card, amount):
    if card.balance < amount:
        raise Exception("invalid balance")


def logDebit(transHandler, card, reqAmount, result=None):
    print 'Amount of %d has been successfully debited towards your card %s' % (result, card.name)


around(TransactionHandler.doTransaction, checkBalance, logDebit)

citi = Card('citi', balance=500)


samsung = Vendor()
print samsung.transact(citi)
