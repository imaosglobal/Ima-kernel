package com.ima.core;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import java.io.*;
import java.nio.charset.StandardCharsets;
import org.json.*;

public class MainActivity extends Activity {
    private WebView webView;
    private LocalIntelligenceBroker broker;
    private MobileImaRuntime runtime;
    private OtaUpdateManager ota;
    private TermuxCommandBridge termux;

    public final class Bridge {
        @JavascriptInterface public String discover() {
            return broker.discover().toString();
        }
        @JavascriptInterface public boolean open(String provider) {
            return broker.openProvider(provider);
        }
        @JavascriptInterface public void ask(String message, String id) {
            new Thread(() -> runKernel(message, id)).start();
        }
        @JavascriptInterface public void runtime(String id) {
            new Thread(() -> runRuntime(id)).start();
        }
        @JavascriptInterface public String termux(String action) {
            return termux.dispatch(action).toString();
        }
    }

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        broker = new LocalIntelligenceBroker(this);
        runtime = new MobileImaRuntime(this, broker);
        termux = new TermuxCommandBridge(this);
        try {
            ota = new OtaUpdateManager(this);
            ota.check();
        } catch (Exception ignored) {
            ota = null;
        }
        webView = new WebView(this);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        webView.addJavascriptInterface(new Bridge(), "IMA_LOCAL_AI");
        webView.setWebViewClient(new WebViewClient() {
            @Override public void onPageFinished(WebView v, String url) {
                super.onPageFinished(v, url);
                installNativeApi();
            }
            @Override public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest r) {
                String p = r.getUrl().getPath();
                if (p == null || !p.startsWith("/Ima-kernel/")) return super.shouldInterceptRequest(v, r);
                String asset = "ima-ui/" + p.substring("/Ima-kernel/".length());
                try {
                    String type = asset.endsWith(".js") ? "application/javascript" :
                            asset.endsWith(".glb") ? "model/gltf-binary" : "application/octet-stream";
                    return new WebResourceResponse(type, "UTF-8", getAssets().open(asset));
                } catch (Exception e) { return super.shouldInterceptRequest(v, r); }
            }
        });
        setContentView(webView);
        loadBundledIma();
    }

    private void loadBundledIma() {
        try {
            InputStream in = getAssets().open("ima-ui/index.html");
            byte[] data = readAll(in);
            String html = new String(data, StandardCharsets.UTF_8)
                    .replace("/Ima-kernel/", "./");
            webView.loadDataWithBaseURL("file:///android_asset/ima-ui/",
                    html, "text/html", "UTF-8", null);
        } catch (Exception e) {
            webView.loadData("<h1>IMA</h1><p>UI load failed: " +
                    esc(e.toString()) + "</p>", "text/html", "UTF-8");
        }
    }
    private void installNativeApi() {
        String js = "" +
            "window.__imaAsk=function(m){return new Promise(function(r){" +
            "var id='a'+Date.now()+Math.random();window.__imaR=window.__imaR||{};" +
            "window.__imaR[id]=r;IMA_LOCAL_AI.ask(m,id);});};" +
            "window.__imaRuntime=function(){return new Promise(function(r){" +
            "var id='r'+Date.now()+Math.random();window.__imaRR=window.__imaRR||{};" +
            "window.__imaRR[id]=r;IMA_LOCAL_AI.runtime(id);});};" +
            "window.__imaTermux=function(a){return new Promise(function(r){" +
            "try{r(JSON.parse(IMA_LOCAL_AI.termux(a)));}catch(e){r({ok:false,error:String(e)});}});};" +
            "window.__imaDone=function(id,x){if(window.__imaR&&window.__imaR[id])" +
            "{window.__imaR[id](x);delete window.__imaR[id];}};" +
            "window.__imaRuntimeDone=function(id,x){if(window.__imaRR&&window.__imaRR[id])" +
            "{window.__imaRR[id](x);delete window.__imaRR[id];}};" +
            "(function(){const old=window.fetch;window.fetch=function(u,o){" +
            "if(String(u).includes('/ima-api/chat'))return window.__imaAsk((o&&o.body?" +
            "JSON.parse(o.body).message:'')).then(x=>new Response(JSON.stringify(x)," +
            "{status:200,headers:{'Content-Type':'application/json'}}));" +
            "if(String(u).includes('/ima-api/runtime'))return window.__imaRuntime()" +
            ".then(x=>new Response(JSON.stringify(x),{status:200,headers:{'Content-Type':'application/json'}}));" +
            "return old.apply(this,arguments);};})();";
        webView.evaluateJavascript(js, null);
    }

    private void runKernel(String message, String id) {
        JSONObject result = runtime.ask(message);
        String response = result.optString("response", "אני כאן.");
        finishAsk(id, response, result.optString("provider", "IMA Mobile Runtime"));
    }

    private void runRuntime(String id) {
        finishRuntime(id, runtime.runtimeState().toString());
    }

    private void finishAsk(String id, String text, String provider) {
        try {
            JSONObject o = new JSONObject();
            o.put("response", text);
            o.put("provider", provider);
            String js = "window.__imaDone(" + JSONObject.quote(id) + "," + o + ")";
            runOnUiThread(() -> webView.evaluateJavascript(js, null));
        } catch (Exception ignored) {}
    }

    private void finishRuntime(String id, String json) {
        String js = "window.__imaRuntimeDone(" + JSONObject.quote(id) + "," + json + ")";
        runOnUiThread(() -> webView.evaluateJavascript(js, null));
    }

    private String firstInstalledProvider() {
        JSONArray a = broker.discover();
        return a.length() > 0 ? a.optJSONObject(0).optString("provider", null) : null;
    }

    private String providerLabel(String p) {
        if ("gemini".equals(p)) return "Gemini";
        if ("chatgpt".equals(p)) return "ChatGPT";
        if ("claude".equals(p)) return "Claude";
        return "אמא";
    }

    private static byte[] readAll(InputStream in) throws IOException {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] b = new byte[8192]; int n;
        while ((n = in.read(b)) != -1) out.write(b, 0, n);
        return out.toByteArray();
    }

    private static String esc(String s) {
        return s.replace("&", "&amp;").replace("<", "&lt;");
    }

    @Override protected void onResume() {
        super.onResume();
        if (ota != null) ota.resume();
    }

    @Override protected void onDestroy() {
        if (webView != null) webView.destroy();
        super.onDestroy();
    }
}
