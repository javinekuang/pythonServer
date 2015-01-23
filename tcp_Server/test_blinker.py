__author__ = 'Administrator'
# coding=utf-8

from blinker import signal


class Processor:
    def __init__(self,name):
        self.name = name

    def go(self):
        global ready
        #ready = signal('ready')
        ready.send(self)
        print "Processing."
        complete = signal('complete')
        complete.send(self)

    def __repr__(self):
        return '<Processor %s>' % self.name


def subscriber(sender):
    print("Got a signal by %r" % sender)


def b_subscriber(sender):
    print("Caught signal from processor_b.")
    assert sender.name == 'b'

ready = signal('ready')
ready.connect(subscriber)
processor = Processor('a')


processor_b = Processor('b')
ready.connect(b_subscriber,sender=processor_b)

processor_b.go()
processor.go()
