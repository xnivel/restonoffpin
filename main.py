from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from datetime import datetime
from sysfs.gpio import Controller, OUTPUT, INPUT, RISING
import urllib2
import time


import cgi
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Gpioclass():
    __metaclass__ = Singleton
    pin=0
    def powerOn(self):
        #self.pin.set()
        self.pin.reset()
    def powerOff(self):
        #self.pin.reset()
        self.pin.set()
    def __init__(self):
        Controller.available_pins = [4]

        self.pin = Controller.alloc_pin(4, OUTPUT)

class PowerONPage(Resource):
    def render_GET(self, request):
        print datetime.now().time(),"ON"
        gpio=Gpioclass()
        gpio.powerOn()
        return 'Turn ON the radio'

class PowerOFFNPage(Resource):
    def render_GET(self, request):
        print datetime.now().time(),"OFF"
        gpio=Gpioclass()
        gpio.powerOff()
        return 'Turn OFF the radio'

class main():
    startHour=8
    endHour=20
    def setGpio(self):
        t=Gpioclass()
    def runServer(self):
        print "Server starting"
        root = Resource()
        root.putChild("on", PowerONPage())
        root.putChild("off", PowerOFFNPage())
        factory = Site(root)
        reactor.listenTCP(8880, factory)
        self.setGpio()
        print "Server started"
        reactor.callInThread(self.init)
        reactor.run()
    def init(self):
        timenow=datetime.now().time().hour
        contex=""
        if timenow>=self.startHour and timenow<self.endHour:
            print "wlacz"
            contex=urllib2.urlopen("http://localhost:8880/on").read()
        else:
            print "wylacz"
            contex=urllib2.urlopen("http://localhost:8880/off").read()
        print "Init -",timenow,"-",contex

main = main()
main.runServer()
