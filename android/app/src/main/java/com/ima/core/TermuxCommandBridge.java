package com.ima.core;

import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import org.json.JSONObject;

import java.util.UUID;

public final class TermuxCommandBridge {
    public static final String ACTION_RESULT = "com.ima.core.TERMUX_RESULT";
    private static final String TERMUX = "com.termux";
    private static final String SERVICE = "com.termux.app.RunCommandService";
    private static final String ACTION_RUN = "com.termux.RUN_COMMAND";
    private static final String KEY_PATH = "com.termux.RUN_COMMAND_PATH";
    private static final String KEY_ARGS = "com.termux.RUN_COMMAND_ARGUMENTS";
    private static final String KEY_WORKDIR = "com.termux.RUN_COMMAND_WORKDIR";
    private static final String KEY_BACKGROUND = "com.termux.RUN_COMMAND_BACKGROUND";
    private static final String KEY_PENDING = "com.termux.RUN_COMMAND_PENDING_INTENT";
    private static final String RESULT_BUNDLE = "com.termux.RUN_COMMAND_RESULT_BUNDLE";
    private static final String RESULT_STDOUT = "com.termux.plugin_result_bundle_stdout";
    private static final String RESULT_STDERR = "com.termux.plugin_result_bundle_stderr";
    private static final String RESULT_EXIT = "com.termux.plugin_result_bundle_exit_code";

    private final Context context;

    public TermuxCommandBridge(Context context) {
        this.context = context.getApplicationContext();
    }

    public JSONObject dispatch(String action) {
        JSONObject out = new JSONObject();
        try {
            String command = commandFor(action);
            if (command == null) return out.put("ok", false).put("error", "ACTION_NOT_ALLOWED");
            if (!isInstalled()) return out.put("ok", false).put("error", "TERMUX_NOT_INSTALLED");

            String id = UUID.randomUUID().toString();
            Intent resultIntent = new Intent(context, ResultReceiver.class)
                    .setAction(ACTION_RESULT).putExtra("execution_id", id);
            int flags = PendingIntent.FLAG_UPDATE_CURRENT;
            if (Build.VERSION.SDK_INT >= 23) flags |= PendingIntent.FLAG_MUTABLE;
            PendingIntent pending = PendingIntent.getBroadcast(context, id.hashCode(), resultIntent, flags);

            Intent intent = new Intent();
            intent.setClassName(TERMUX, SERVICE);
            intent.setAction(ACTION_RUN);
            intent.putExtra(KEY_PATH, "/data/data/com.termux/files/usr/bin/bash");
            intent.putExtra(KEY_ARGS, new String[]{"-lc", command});
            intent.putExtra(KEY_WORKDIR, "/data/data/com.termux/files/home/Ima-kernel");
            intent.putExtra(KEY_BACKGROUND, true);
            intent.putExtra(KEY_PENDING, pending);
            context.startService(intent);

            return out.put("ok", true).put("dispatched", true).put("execution_id", id)
                    .put("action", action).put("command", command);
        } catch (Exception e) {
            try { return out.put("ok", false).put("error", e.toString()); }
            catch (Exception ignored) { return out; }
        }
    }

    private boolean isInstalled() {
        try { context.getPackageManager().getPackageInfo(TERMUX, 0); return true; }
        catch (Exception e) { return false; }
    }

    private String commandFor(String action) {
        if ("status".equals(action)) return "git status --short --branch";
        if ("build".equals(action)) return "cd android && ./gradlew clean assembleDebug --no-daemon";
        if ("test".equals(action)) return "cd android && ./gradlew test --no-daemon";
        if ("verify".equals(action)) return "cd android && test -f app/build/outputs/apk/debug/app-debug.apk && sha256sum app/build/outputs/apk/debug/app-debug.apk";
        return null;
    }

    public static final class ResultReceiver extends BroadcastReceiver {
        @Override public void onReceive(Context context, Intent intent) {
            try {
                String id = intent.getStringExtra("execution_id");
                JSONObject result = new JSONObject();
                result.put("execution_id", id);
                Object bundleObj = intent.getBundleExtra(RESULT_BUNDLE);
                if (bundleObj instanceof android.os.Bundle) {
                    android.os.Bundle b = (android.os.Bundle) bundleObj;
                    result.put("stdout", b.getString(RESULT_STDOUT, ""));
                    result.put("stderr", b.getString(RESULT_STDERR, ""));
                    result.put("exit_code", b.getInt(RESULT_EXIT, -1));
                }
                context.getSharedPreferences("ima_termux", Context.MODE_PRIVATE)
                        .edit().putString("last_result", result.toString()).apply();
            } catch (Exception ignored) {}
        }
    }
}
