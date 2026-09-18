package com.ima.core;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ApplicationInfo;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Device-owned intelligence broker.
 * Discovers AI apps owned by the current user and exposes only capabilities
 * that Android actually permits. It never reads credentials or app data.
 */
public final class LocalIntelligenceBroker {
    private final Context context;
    private final PackageManager pm;

    private static final String[][] PROVIDERS = {
        {"gemini", "com.google.android.apps.bard"},
        {"chatgpt", "com.openai.chatgpt"},
        {"claude", "com.anthropic.claude"}
    };

    public LocalIntelligenceBroker(Context context) {
        this.context = context.getApplicationContext();
        this.pm = this.context.getPackageManager();
    }

    public JSONArray discover() {
        JSONArray result = new JSONArray();
        for (String[] provider : PROVIDERS) {
            try {
                ApplicationInfo info = pm.getApplicationInfo(provider[1], PackageManager.MATCH_ALL);
                JSONObject item = new JSONObject();
                item.put("provider", provider[0]);
                item.put("package", provider[1]);
                item.put("installed", true);
                item.put("local_app", true);
                item.put("credential_access", false);
                item.put("direct_api", false);
                item.put("handoff", true);
                item.put("response_capture", "requires_supported_os_or_user_enabled_accessibility");
                result.put(item);
            } catch (PackageManager.NameNotFoundException ignored) {
            } catch (Exception ignored) {
            }
        }
        return result;
    }

    public boolean openProvider(String provider) {
        for (String[] candidate : PROVIDERS) {
            if (!candidate[0].equalsIgnoreCase(provider)) continue;
            Intent launch = pm.getLaunchIntentForPackage(candidate[1]);
            if (launch == null) return false;
            launch.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(launch);
            return true;
        }
        return false;
    }
}
