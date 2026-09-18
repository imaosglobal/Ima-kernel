package com.ima.core;

import org.json.JSONArray;
import org.json.JSONObject;

/** Device capability registry. It never reads provider credentials. */
public final class CapabilityGraph {
    public JSONArray snapshot(JSONArray providers) {
        JSONArray out = new JSONArray();
        add(out, "conversation", "local", true, "IMA Mobile Runtime");
        add(out, "memory", "local", true, "IMA Memory");
        add(out, "provenance", "local", true, "IMA Provenance");
        add(out, "action", "android", true, "Android Intents");
        for (int i = 0; i < providers.length(); i++) {
            JSONObject p = providers.optJSONObject(i);
            if (p == null) continue;
            String name = p.optString("provider", "unknown");
            add(out, "ai:" + name, "installed_app", p.optBoolean("installed", false), name);
        }
        return out;
    }

    private void add(JSONArray out, String capability, String route, boolean available, String provider) {
        JSONObject x = new JSONObject();
        try { x.put("capability", capability); x.put("route", route); x.put("available", available); x.put("provider", provider); }
        catch (Exception ignored) {}
        out.put(x);
    }

    public String routeFor(String request) {
        String q = request == null ? "" : request.toLowerCase();
        if (q.contains("זכור") || q.contains("זיכרון") || q.contains("remember")) return "memory";
        if (q.contains("פתח") || q.contains("open") || q.contains("שלח") || q.contains("send")) return "action";
        return "conversation";
    }
}
