package com.ima.core;

import android.content.Context;
import android.content.SharedPreferences;
import org.json.JSONArray;
import org.json.JSONObject;
import java.util.Locale;

/** Device runtime: no Git repository, Termux, or developer credentials required. */
public final class MobileImaRuntime {
    private final SharedPreferences prefs;
    private final LocalIntelligenceBroker broker;
    private final CapabilityGraph capabilities;
    private final ImaProvenance provenance;

    public MobileImaRuntime(Context context, LocalIntelligenceBroker broker) {
        this.prefs = context.getSharedPreferences("ima_memory", Context.MODE_PRIVATE);
        this.broker = broker;
        this.capabilities = new CapabilityGraph();
        this.provenance = new ImaProvenance(context);
    }

    public JSONObject ask(String message) {
        String text = message == null ? "" : message.trim();
        String response = localAnswer(text);
        remember(text, response);
        JSONObject out = new JSONObject();
        try {
            String route = capabilities.routeFor(text);
            JSONObject action = ImaAction.create(text, route, text, "local");
            action.put("status", "completed");
            provenance.record("conversation", "IMA Mobile Runtime", response);
            out.put("response", response);
            out.put("provider", "IMA Mobile Runtime");
            out.put("status", "ok");
            out.put("local", true);
            out.put("route", route);
            out.put("action", action);
            out.put("memory_records", prefs.getInt("records", 0));
            out.put("provenance_records", provenance.count());
        } catch (Exception ignored) {}
        return out;
    }

    private String localAnswer(String text) {
        String q = text.toLowerCase(Locale.ROOT);
        if (q.contains("מי את") || q.contains("מי אתה")) {
            return "אני אמא. אני שכבת האינטליגנציה שלך: זוכרת, לומדת ומחברת אותך ליכולות של המכשיר והבינות שבחרת.";
        }
        if (q.contains("מה את יכולה") || q.contains("מה אפשר לעשות")) {
            return "אני יכולה לדבר איתך, לשמור הקשר מקומי, ללמוד מהאינטראקציות שלך, לזהות בינות זמינות במכשיר ולפתוח אותן כשנדרש.";
        }
        if (q.contains("זיכרון") || q.contains("זוכרת")) {
            return "יש לי כרגע " + prefs.getInt("records", 0) + " רשומות זיכרון מקומיות במכשיר הזה.";
        }
        if (q.contains("שלום") || q.equals("היי") || q.equals("הי")) {
            return "אני כאן. אפשר להתחיל מכאן.";
        }
        JSONArray providers = broker.discover();
        if (providers.length() > 0) {
            return "קיבלתי. אמא המקומית פעילה. במכשיר הזה זמינות " + providers.length() +
                    " בינות חיצוניות שאפשר לחבר דרך האינטגרציה הנתמכת.";
        }
        return "קיבלתי. אמא המקומית פעילה ושומרת את ההקשר בינינו במכשיר.";
    }

    private void remember(String question, String response) {
        int n = prefs.getInt("records", 0) + 1;
        prefs.edit().putInt("records", n)
                .putString("last_question", question)
                .putString("last_response", response)
                .apply();
    }

    public JSONObject runtimeState() {
        JSONObject out = new JSONObject();
        try {
            out.put("source", "IMA Mobile Runtime");
            out.put("memory", new JSONObject().put("available", true)
                    .put("records", prefs.getInt("records", 0)));
            JSONArray agents = broker.discover();
            out.put("learning", new JSONObject().put("available", true)
                    .put("records", prefs.getInt("records", 0)));
            out.put("agents", agents);
            out.put("capabilities", capabilities.snapshot(agents));
            out.put("provenance", new JSONObject().put("available", true)
                    .put("records", provenance.count()));
            out.put("architecture", new JSONObject()
                    .put("local_first", true)
                    .put("provider_credentials_access", false)
                    .put("repo_required_on_device", false)
                    .put("action_protocol", "IMA-Action-1"));
            out.put("kernel_on_device", false);
        } catch (Exception ignored) {}
        return out;
    }
}
