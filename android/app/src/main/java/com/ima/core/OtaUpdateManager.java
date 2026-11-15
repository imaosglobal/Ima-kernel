package com.ima.core;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import org.json.JSONObject;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import com.google.android.play.core.appupdate.AppUpdateInfo;
import com.google.android.play.core.appupdate.AppUpdateManager;
import com.google.android.play.core.appupdate.AppUpdateManagerFactory;
import com.google.android.play.core.appupdate.AppUpdateOptions;
import com.google.android.play.core.install.model.AppUpdateType;
import com.google.android.play.core.install.model.UpdateAvailability;

public final class OtaUpdateManager {
    private static final int REQUEST_CODE = 9101;
    private final Activity activity;
    private final AppUpdateManager manager;
    private volatile JSONObject canonicalManifest;
    private static final String MANIFEST_URL = "https://imaosglobal.github.io/Ima-kernel/ota/manifest.json";

    public OtaUpdateManager(Activity activity) {
        this.activity = activity;
        this.manager = AppUpdateManagerFactory.create(activity);
    }

    public void check() {
        checkCanonicalManifest();
        manager.getAppUpdateInfo().addOnSuccessListener(this::handle);
    }

    private void checkCanonicalManifest() {
        new Thread(() -> {
            try {
                java.net.HttpURLConnection c = (java.net.HttpURLConnection) new java.net.URL(MANIFEST_URL + "?t=" + System.currentTimeMillis()).openConnection();
                c.setConnectTimeout(8000); c.setReadTimeout(8000); c.setUseCaches(false);
                int code = c.getResponseCode();
                if (code < 200 || code >= 300) return;
                InputStream in = c.getInputStream();
                byte[] data = in.readAllBytes();
                JSONObject manifest = new JSONObject(new String(data, StandardCharsets.UTF_8));
                canonicalManifest = manifest;
                android.util.Log.i("IMA-OTA", "canonical manifest loaded webVersion=" + manifest.optString("webVersion") + " nativeVersion=" + manifest.optString("nativeVersionName"));
            } catch (Exception e) {
                android.util.Log.w("IMA-OTA", "canonical manifest unavailable: " + e.getMessage());
            }
        }).start();
    }

    public String statusJson() {
        JSONObject out = new JSONObject();
        try {
            out.put("manifestUrl", MANIFEST_URL);
            out.put("manifestLoaded", canonicalManifest != null);
            if (canonicalManifest != null) out.put("manifest", canonicalManifest);
        } catch (Exception ignored) {}
        return out.toString();
    }

    private void handle(AppUpdateInfo info) {
        boolean available = info.updateAvailability() == UpdateAvailability.UPDATE_AVAILABLE;
        boolean allowed = info.isUpdateTypeAllowed(AppUpdateType.IMMEDIATE);
        if (available && allowed) {
            try {
                manager.startUpdateFlowForResult(
                    info,
                    activity,
                    AppUpdateOptions.newBuilder(AppUpdateType.IMMEDIATE).build(),
                    REQUEST_CODE
                );
            } catch (Exception ignored) {
                // Play Store may be unavailable for sideloaded/debug builds.
            }
        }
    }

    public void resume() {
        manager.getAppUpdateInfo().addOnSuccessListener(info -> {
            if (info.updateAvailability() ==
                    UpdateAvailability.DEVELOPER_TRIGGERED_UPDATE_IN_PROGRESS) {
                handle(info);
            }
        });
    }
}
