'''
Google Play Service
===================

E/GamesIntentService(25103): Using Google Play games services requires a metadata tag with the name "com.google.android.gms.games.APP_ID" in the application tag of your manifest


'''

from jnius import autoclass, PythonJavaClass, java_method


PythonActivity = autoclass('org.renpy.android.PythonActivity')
GamesClient_Builder = autoclass('com.google.android.gms.games.GamesClient$Builder')

class GooglePlayServicesClientListener(PythonJavaClass):
    __javacontext__ = 'app'
    __javainterfaces__ = [
        'com/google/android/gms/common/GooglePlayServicesClient$ConnectionCallbacks',
        'com/google/android/gms/common/GooglePlayServicesClient$OnConnectionFailedListener']

    def __init__(self, client):
        super(GooglePlayServicesClientListener, self).__init__()
        self.client = client

    @java_method('()V')
    def onDisconnected(self):
        print('onDisconnected()')
        if self.client.on_disconnected:
            self.client.on_disconnected()

    @java_method('(Landroid/os/Bundle;)V')
    def onConnected(self, connectionHint):
        print('onConnected() {!r}'.format(connectionHint))
        if self.client.on_connected:
            self.client.on_connected(connectionHint)

    @java_method('(Lcom/google/android/gms/common/ConnectionResult;)V')
    def onConnectionFailed(self, result):
        print('onConnectionFailed() {!r}'.format(result))
        print('onConnectionFailed() toString={}'.format(result.toString()))
        print('onConnectionFailed() errorCode={}'.format(result.getErrorCode()))
        print('onConnectionFailed() hasResolution={}'.format(result.hasResolution()))
        if result.hasResolution():
            result.startResolutionForResult(PythonActivity.mActivity,
                    result.getErrorCode())
            return
        if self.client.on_connection_failed:
            self.client.on_connection_failed(result)

    @java_method('()I')
    def hashCode(self):
        return id(self)

    @java_method('(Ljava/lang/Object;)Z')
    def equals(self, obj):
        print('equals() {!r}'.format(obj))
        print('1---')
        print(dir(obj))
        print(obj.getClass())
        print(obj.getClass().getName())
        return True
        print(obj.hashCode())
        print('2---')
        print(self.hashCode())
        return obj.hashCode() == self.hashCode()

class ActivityResultListener(PythonJavaClass):

    __javacontext__ = 'app'
    __javainterfaces__ = ['org/renpy/android/PythonActivity$ResultListener']

    def __init__(self, client):
        super(ActivityResultListener, self).__init__()
        self.client = client

    @java_method('(IILandroid/content/Intent;)V')
    def onActivityResult(self, requestCode, resultCode, data):
        print('onActivityResult() {!r} {!r} {!r}'.format(
            requestCode, resultCode, data))
        if self.client.on_activity_result:
            self.client.on_activity_result(requestCode, resultCode, data)

class GameClient(object):

    RESULT_CODES = {
        0x2714: 'RESULT_APP_MISCONFIGURED',
        0x2715: 'RESULT_LEFT_ROOM',
        0x2713: 'RESULT_LICENSE_FAILED',
        0x2711: 'RESULT_RECONNECT_REQUIRED',
        0x2712: 'RESULT_SIGN_IN_FAILED'
    }

    def __init__(self, **kwargs):
        super(GameClient, self).__init__()
        self.on_disconnected = kwargs.get('on_disconnected')
        self.on_connected = kwargs.get('on_disconnected')
        self.on_connection_failed = kwargs.get('on_disconnected')

        self._listener = GooglePlayServicesClientListener(self)
        self._builder = GamesClient_Builder(
                PythonActivity.mActivity, self._listener, self._listener)
        self._client = self._builder.create()

        self._activityResultListener = ActivityResultListener(self)
        # register PythonActivity for result
        PythonActivity.mActivity.registerResultListener(self._activityResultListener)

    @property
    def client(self):
        return self._client

    def on_activity_result(self, requestCode, resultCode, data):
        if requestCode == 4: # SIGN_IN_REQUEST
            print 'SIGNIN RESULT', resultCode, GameClient.RESULT_CODES.get(resultCode, 'UNKNOWN')

