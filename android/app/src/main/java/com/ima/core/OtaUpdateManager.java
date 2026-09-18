package com.ima.core;

import android.app.Activity;
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

    public OtaUpdateManager(Activity activity) {
        this.activity = activity;
        this.manager = AppUpdateManagerFactory.create(activity);
    }

    public void check() {
        manager.getAppUpdateInfo().addOnSuccessListener(this::handle);
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
