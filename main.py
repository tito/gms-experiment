__version__ = '0.1'

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

class Test(App):
    def build(self):
        print 'import game client'
        from google_play_service import GameClient
        print 'create game client'
        self.gameclient = gameclient = GameClient()
        print 'got game client', gameclient
        client = gameclient.client
        print 'check registration'
        print client.isConnectionCallbacksRegistered(gameclient._listener)
        print client.isConnectionFailedListenerRegistered(gameclient._listener)
        print 'connect to the game'
        client.connect()
        print 'schedule check'
        Clock.schedule_interval(self.check_connection, 1)
        return Label(text='Wait for username...')

    def check_connection(self, *args):
        client = self.gameclient.client
        print 'client.isConnected()', client.isConnected()
        print 'client.isConnecting()', client.isConnecting()

        if client.isConnected():
            print 'CONNECTED!'
            print 'client.getAppId()', client.getAppId()
            print 'client.getCurrentAccountName()', client.getCurrentAccountName()
            print 'client.getCurrentPlayer()', client.getCurrentPlayer()
            print 'client.getCurrentPlayerId()', client.getCurrentPlayerId()
            return False

    def on_pause(self):
        print '--> pause'
        return True

    def on_resume(self):
        print '--> resume!'
        return True


Test().run()
