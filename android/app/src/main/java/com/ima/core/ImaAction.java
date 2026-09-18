package com.ima.core;

import org.json.JSONObject;
import java.util.UUID;

/** Canonical action envelope shared by local and external intelligence routes. */
public final class ImaAction {
    public static JSONObject create(String goal, String capability, String target, String route) {
        JSONObject x = new JSONObject();
        try {
            x.put("action_id", UUID.randomUUID().toString());
            x.put("goal", goal == null ? "" : goal);
            x.put("capability", capability == null ? "" : capability);
            x.put("target", target == null ? "" : target);
            x.put("route", route == null ? "" : route);
            x.put("confirmation", "required_for_external_or_destructive_action");
            x.put("verification", "required");
            x.put("status", "planned");
        } catch (Exception ignored) {}
        return x;
    }
}
