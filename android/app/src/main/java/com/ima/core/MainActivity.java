package com.ima.core;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.content.Intent;
import java.io.*;
import java.nio.charset.StandardCharsets;
import org.json.*;
import android.util.Base64;
import android.os.CancellationSignal;
import androidx.credentials.CredentialManager;
import androidx.credentials.CredentialManagerCallback;
import androidx.credentials.CustomCredential;
import androidx.credentials.GetCredentialRequest;
import androidx.credentials.GetCredentialResponse;
import androidx.credentials.exceptions.GetCredentialException;
import com.google.android.libraries.identity.googleid.GetSignInWithGoogleOption;
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential;
import com.google.android.libraries.identity.googleid.GoogleIdTokenParsingException;
import java.security.SecureRandom;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class MainActivity extends Activity {
    private WebView webView;
    private LocalIntelligenceBroker broker;
    private MobileImaRuntime runtime;
    private OtaUpdateManager ota;
    private TermuxCommandBridge termux;
    private GmailAccountBridge gmail;
    private CredentialManager credentialManager;
    private final Executor googleExecutor = Executors.newSingleThreadExecutor();

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
        @JavascriptInterface public String gmailStart() {
            return gmail.start().toString();
        }
        @JavascriptInterface public String gmailStatus() {
            return gmail.status().toString();
        }
        @JavascriptInterface public void googleSignIn(String serverClientId, String id) {
            startGoogleSignIn(serverClientId, id);
        }
    }

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        broker = new LocalIntelligenceBroker(this);
        runtime = new MobileImaRuntime(this, broker);
        termux = new TermuxCommandBridge(this);
        gmail = new GmailAccountBridge(this);
        credentialManager = CredentialManager.create(this);
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
            "window.__imaGmailStart=function(){try{return JSON.parse(IMA_LOCAL_AI.gmailStart());}catch(e){return {ok:false,error:String(e)};}};" +
            "window.__imaGmailStatus=function(){try{return JSON.parse(IMA_LOCAL_AI.gmailStatus());}catch(e){return {connected:false,error:String(e)};}};" +
            "window.__imaGoogleR=window.__imaGoogleR||{};" +
            "window.__imaGoogleDone=function(id,x){var p=window.__imaGoogleR[id];if(!p)return;delete window.__imaGoogleR[id];x&&x.ok?p.resolve(x):p.reject(new Error((x&&x.error)||'Google sign-in failed'));};" +
            "window.__imaGoogleSignIn=function(clientId){return new Promise(function(resolve,reject){var id='g'+Date.now()+Math.random();window.__imaGoogleR[id]={resolve:resolve,reject:reject};IMA_LOCAL_AI.googleSignIn(clientId,id);});};" +
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

    private void startGoogleSignIn(String serverClientId, String id) {
        if (serverClientId == null || serverClientId.trim().isEmpty()) {
            finishGoogle(id, false, null, "Google server client ID is not configured");
            return;
        }
        String nonce = secureNonce();
        GetSignInWithGoogleOption googleOption =
                new GetSignInWithGoogleOption.Builder(serverClientId.trim())
                        .setNonce(nonce)
                        .build();
        GetCredentialRequest request = new GetCredentialRequest.Builder()
                .addCredentialOption(googleOption)
                .build();
        credentialManager.getCredentialAsync(
                this,
                request,
                new CancellationSignal(),
                googleExecutor,
                new CredentialManagerCallback<GetCredentialResponse, GetCredentialException>() {
                    @Override public void onResult(GetCredentialResponse result) {
                        try {
                            if (!(result.getCredential() instanceof CustomCredential)) {
                                finishGoogle(id, false, null, "Google credential type unavailable");
                                return;
                            }
                            CustomCredential custom = (CustomCredential) result.getCredential();
                            if (!GoogleIdTokenCredential.TYPE_GOOGLE_ID_TOKEN_CREDENTIAL.equals(custom.getType())) {
                                finishGoogle(id, false, null, "Google ID token credential unavailable");
                                return;
                            }
                            GoogleIdTokenCredential googleCredential =
                                    GoogleIdTokenCredential.createFrom(custom.getData());
                            JSONObject server = postGoogleCredential(googleCredential.getIdToken());
                            if (server.optString("token", "").isEmpty()) {
                                finishGoogle(id, false, null, server.optString("error", "Google authentication failed"));
                                return;
                            }
                            finishGoogle(id, true, server, null);
                        } catch (GoogleIdTokenParsingException e) {
                            finishGoogle(id, false, null, "Google credential parsing failed");
                        } catch (Exception e) {
                            finishGoogle(id, false, null, "Google authentication failed");
                        }
                    }
                    @Override public void onError(GetCredentialException e) {
                        finishGoogle(id, false, null, e.getMessage() == null ? "Google sign-in cancelled or unavailable" : e.getMessage());
                    }
                });
    }

    private static String secureNonce() {
        byte[] bytes = new byte[32];
        new SecureRandom().nextBytes(bytes);
        return Base64.encodeToString(bytes, Base64.NO_WRAP | Base64.URL_SAFE | Base64.NO_PADDING);
    }

    private JSONObject postGoogleCredential(String idToken) throws Exception {
        java.net.URL url = new java.net.URL("https://ima-915m.onrender.com/ima-api/auth/google");
        java.net.HttpURLConnection connection = (java.net.HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setConnectTimeout(15000);
        connection.setReadTimeout(15000);
        connection.setDoOutput(true);
        connection.setRequestProperty("Content-Type", "application/json");
        JSONObject payload = new JSONObject();
        payload.put("credential", idToken);
        try (java.io.OutputStream out = connection.getOutputStream()) {
            out.write(payload.toString().getBytes(StandardCharsets.UTF_8));
        }
        int code = connection.getResponseCode();
        InputStream stream = code >= 200 && code < 300 ? connection.getInputStream() : connection.getErrorStream();
        String body = stream == null ? "{}" : new String(readAll(stream), StandardCharsets.UTF_8);
        JSONObject result = new JSONObject(body.isEmpty() ? "{}" : body);
        if (code < 200 || code >= 300) result.put("http_status", code);
        return result;
    }

    private void finishGoogle(String id, boolean ok, JSONObject server, String error) {
        JSONObject result = new JSONObject();
        try {
            result.put("ok", ok);
            if (server != null) {
                if (server.has("token")) result.put("token", server.getString("token"));
                if (server.has("user")) result.put("user", server.getJSONObject("user"));
            }
            if (error != null) result.put("error", error);
        } catch (JSONException ignored) {}
        String js = "window.__imaGoogleDone(" + JSONObject.quote(id) + "," + result + ")";
        runOnUiThread(() -> webView.evaluateJavascript(js, null));
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

    @Override protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (gmail != null) gmail.handleResult(requestCode, resultCode, data);
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
