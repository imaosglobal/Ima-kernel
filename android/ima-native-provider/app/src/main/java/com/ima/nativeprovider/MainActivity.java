package com.ima.nativeprovider;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Button;

public class MainActivity extends Activity {
    @Override public void onCreate(Bundle b) {
        super.onCreate(b);
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(32,32,32,32);
        TextView title = new TextView(this);
        title.setText("IMA — LIVE-001 Native Provider\n\nThis provider keeps the device connection local to Android + Termux. It does not use Wireless Debugging or ADB.");
        title.setTextSize(18);
        box.addView(title);
        Button settings = new Button(this);
        settings.setText("הפעל הרשאת נגישות ל־IMA");
        settings.setOnClickListener(v -> startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)));
        box.addView(settings);
        setContentView(box);
    }
}
