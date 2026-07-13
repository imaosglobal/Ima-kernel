#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "[IMA] STEP 1 - patch App.java"

cat > app/src/main/java/org/example/App.java <<'JAVA'
package org.example;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;

import java.io.File;

public class App extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Log.d("IMA", "IMA BRIDGE STARTED");

        try {
            File root = new File("/data/data/com.termux/files/home/ima_kernel");
            File[] list = root.listFiles();

            if (list != null) {
                for (File f : list) {
                    Log.d("IMA_FILE", f.getAbsolutePath());
                }
            }

            Runtime.getRuntime().exec(
                new String[]{"sh", "/data/data/com.termux/files/home/ima_kernel/ima_controller.sh"}
            );

        } catch (Exception e) {
            Log.e("IMA", "ERROR", e);
        }
    }
}
JAVA

echo "[IMA] STEP 2 - ensure manifest activity"

sed -i '/org.example.App/d' app/src/main/AndroidManifest.xml || true

cat > app/src/main/AndroidManifest.xml <<'XML'
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application android:label="IMA">
        <activity android:name="org.example.App"
                  android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>

</manifest>
XML

echo "[IMA] STEP 3 - build APK"

./gradlew clean assembleDebug --no-daemon

APK=$(find app/build/outputs/apk/debug -name "*.apk" | head -n 1)

echo "[IMA] APK: $APK"

cp "$APK" ~/ima_debug.apk

echo "[IMA] STEP 4 - copy to download"

cp ~/ima_debug.apk /sdcard/Download/ima_debug.apk || true

echo "[IMA] STEP 5 - open installer"

termux-open /sdcard/Download/ima_debug.apk || true

echo "[IMA] DONE"
