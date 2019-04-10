from abc import ABCMeta, abstractmethod

class ticket(object):
      __metaclass__ = ABCMeta

      @abstractmethod
      def __init__(self, ticket_type):
          self.ticket_type = ticket_type
          self.occupants =[]
          pin = random.randint(999, 9999)
          self.room_ID = pin

class book(ticket):
      pass
class reserve(ticket):
      pass
