from aop import watchable, after
from functools import wraps


def inj(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        return func(*args, **kwargs)
    return wrap


class TransactionHandler(object):

    def doTransaction(self, card, amount):
        return card.debit(amount)


class Card(object):
    def __init__(self, name, balance=100):
        self.name = name
        self._balance = balance

    def showBalance(self):
        return self._balance

    def setBalance(self, bal):
        self._balance = bal

    balance = property(showBalance, setBalance)

    @inj
    @watchable
    def debit(self, amount):
        self.balance -= amount
        return self.balance

    @staticmethod
    @watchable
    def dumb():
        print 'dumb'


class Vendor(object):
    def __init__(self, trans=TransactionHandler):
        self.transHandler = trans()

    def transact(self, card):
        return self.transHandler.doTransaction(card, 300)


def checkBalance(card, amount, result=None):
    if card.balance < amount:
        raise Exception("invalid balance")


def logDebit(card, reqAmount, result=None):
    print 'Amount of %d has been successfully debited towards your card %s' % (result, card.name)


def dummy():
    pass


def printBalance(card, result):
    print result

citi = Card('citi', balance=20)

after(Card.showBalance, printBalance)


citi.showBalance()

