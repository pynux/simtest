from smartcard.System import readers
from smartcard.util import toHexString

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver

from smartcard.CardMonitoring import CardMonitor, CardObserver

from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
from smartcard.sw.ISO7816_4ErrorChecker import ISO7816_4ErrorChecker
from smartcard.sw.ISO7816_8ErrorChecker import ISO7816_8ErrorChecker
from smartcard.sw.SWExceptions import SWException, WarningProcessingException

# a simple card observer that prints inserted/removed cards
class SimpleCardObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            print("+Inserted: ", toHexString(card.atr))
        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))


r = readers()
print r

cardmonitor = CardMonitor()
cardobserver = SimpleCardObserver()
cardmonitor.addObserver(cardobserver)

# request any card type
cardrequest = CardRequest(timeout=1, cardType=AnyCardType())
cardservice = cardrequest.waitforcard()

# our error checking chain
errorchain = []
errorchain = [ErrorCheckingChain(errorchain, ISO7816_9ErrorChecker()),
              ErrorCheckingChain(errorchain, ISO7816_8ErrorChecker()),
              ErrorCheckingChain(errorchain, ISO7816_4ErrorChecker())]
cardservice.connection.setErrorCheckingChain(errorchain)

# attach the console tracer
observer = ConsoleCardConnectionObserver()
cardservice.connection.addObserver(observer)

# connect to the card
cardservice.connection.connect(CardConnection.T0_protocol)

atr = cardservice.connection.getATR()
print toHexString(atr)
atr.dump()

while True:
  sleep(1)

cardmonitor.deleteObserver(cardobserver)



