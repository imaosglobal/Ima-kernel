package com.ima.core;

import android.content.Context;
import android.content.SharedPreferences;
import org.json.JSONArray;
import org.json.JSONObject;
import java.security.MessageDigest;

/** Append-only lightweight provenance for device-created IMA interactions. */
public final class ImaProvenance {
    private final SharedPreferences prefs;
    public ImaProvenance(Context context) { prefs = context.getSharedPreferences("ima_provenance", Context.MODE_PRIVATE); }

    public JSONObject record(String type, String source, String result) {
        JSONObject x = new JSONObject();
        try {
            x.put("type", type); x.put("source", source); x.put("result_hash", sha256(result));
            x.put("created_at", System.currentTimeMillis());
            JSONArray a = new JSONArray(prefs.getString("records", "[]"));
            a.put(x); prefs.edit().putString("records", a.toString()).apply();
        } catch (Exception ignored) {}
        return x;
    }

    public int count() { try { return new JSONArray(prefs.getString("records", "[]")).length(); } catch (Exception e) { return 0; } }

    private static String sha256(String s) throws Exception {
        byte[] b = MessageDigest.getInstance("SHA-256").digest((s == null ? "" : s).getBytes("UTF-8"));
        StringBuilder h = new StringBuilder(); for (byte v : b) h.append(String.format("%02x", v)); return h.toString();
    }
}
