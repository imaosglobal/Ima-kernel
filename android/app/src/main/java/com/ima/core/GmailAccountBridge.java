package com.ima.core;

import android.accounts.Account;
import android.accounts.AccountManager;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import org.json.JSONObject;

public final class GmailAccountBridge {
    public static final int REQUEST_ACCOUNT = 4901;
    public static final String TARGET_EMAIL = "imaosglobal@gmail.com";

    private final Activity activity;
    private final AccountManager accounts;
    private Account selected;

    public GmailAccountBridge(Activity activity) {
        this.activity = activity;
        this.accounts = AccountManager.get(activity);
    }    public JSONObject start() {
        try {
            Intent intent = AccountManager.newChooseAccountIntent(
                    null, null, new String[]{"com.google"}, false,
                    "בחר את חשבון Gmail של אמא", null, null, null);
            activity.startActivityForResult(intent, REQUEST_ACCOUNT);
            return new JSONObject().put("ok", true)
                    .put("state", "ACCOUNT_PICKER_OPENED");
        } catch (Exception e) {
            return error(e);
        }
    }

    public boolean handleResult(int requestCode, int resultCode, Intent data) {
        if (requestCode != REQUEST_ACCOUNT ||
            resultCode != Activity.RESULT_OK || data == null) return false;        String email = data.getStringExtra(AccountManager.KEY_ACCOUNT_NAME);
        if (email == null || !TARGET_EMAIL.equalsIgnoreCase(email)) {
            activity.getSharedPreferences("ima_gmail", 0).edit()
                    .putBoolean("connected", false)
                    .remove("email").apply();
            return true;
        }

        selected = new Account(email, "com.google");
        accounts.getAuthToken(selected,
                "oauth2:https://www.googleapis.com/auth/gmail.readonly",
                false, future -> {
                    try {
                        Bundle result = future.getResult();
                        String token = result.getString(AccountManager.KEY_AUTHTOKEN);
                        boolean ok = token != null && !token.isEmpty();
                        activity.getSharedPreferences("ima_gmail", 0).edit()
                                .putBoolean("connected", ok)
                                .putString("email", TARGET_EMAIL)
                                .putLong("linked_at", System.currentTimeMillis())
                                .apply();
                    } catch (Exception e) {
                        activity.getSharedPreferences("ima_gmail", 0).edit()
                                .putBoolean("connected", false).apply();
                    }
                }, null);
        return true;
    }    public JSONObject status() {
        try {
            android.content.SharedPreferences p =
                    activity.getSharedPreferences("ima_gmail", 0);
            return new JSONObject()
                    .put("connected", p.getBoolean("connected", false))
                    .put("email", p.getString("email", ""))
                    .put("target", TARGET_EMAIL);
        } catch (Exception e) {
            return error(e);
        }
    }

    private JSONObject error(Exception e) {
        try {
            return new JSONObject().put("ok", false)
                    .put("error", e.toString());
        } catch (Exception ignored) {
            return new JSONObject();
        }
    }
}