Google play service - experimentation
=====================================

In your `AndroidManifest.xml`, add under the application tag::

	<meta-data android:name="com.google.android.gms.games.APP_ID" android:value="@string/app_id"/>

In your `res/values/string.xml`, add this tag, and replace the X with your real app_id from the Google play console.::

	<string name="app_id">XXXXXXXXX</string>

Download the Google Play Service sdk addons (via `android sdk`), and copy the `google-play-services.jar` into `libs`.

And finally, use `on-activity-result` branch of python-for-android.
