package com.ima.core;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.CookieManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public class MainActivity extends Activity {

    private static final String FACEBOOK_URL =
            "https://www.facebook.com/share/1FFdWxZt2a/";

    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        webView = new WebView(this);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);
        settings.setUserAgentString(
                "Mozilla/5.0 (Linux; Android 16) " +
                "AppleWebKit/537.36 (KHTML, like Gecko) " +
                "Chrome/140 Mobile Safari/537.36"
        );

        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(webView, true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);

                Toast.makeText(
                        MainActivity.this,
                        "IMA: Facebook נטען — מתחילה קריאה",
                        Toast.LENGTH_SHORT
                ).show();

                startIngestion();
            }
        });

        setContentView(webView);
        webView.loadUrl(FACEBOOK_URL);
    }

    private void startIngestion() {

        final String javascript =
                "(async function() {" +

                "const seen = new Set();" +
                "let stable = 0;" +

                "function collect() {" +
                "  const nodes = document.querySelectorAll('div[role=\"article\"], article');" +
                "  let out = [];" +

                "  for (const n of nodes) {" +
                "    const text = (n.innerText || '').trim();" +
                "    if (text.length < 30) continue;" +
                "    if (seen.has(text)) continue;" +
                "    seen.add(text);" +
                "    out.push(text);" +
                "  }" +

                "  return out;" +
                "}" +

                "async function send(items) {" +
                "  for (const text of items) {" +
                "    try {" +
                "      await fetch('http://127.0.0.1:8765/ingest', {" +
                "        method: 'POST'," +
                "        headers: {'Content-Type':'text/plain;charset=utf-8'}," +
                "        body: text" +
                "      });" +
                "    } catch(e) {}" +
                "  }" +
                "}" +

                "for (let i = 0; i < 60; i++) {" +
                "  const before = seen.size;" +
                "  const items = collect();" +
                "  await send(items);" +

                "  window.scrollBy(0, Math.floor(window.innerHeight * 0.85));" +
                "  await new Promise(r => setTimeout(r, 2500));" +

                "  if (seen.size === before) stable++;" +
                "  else stable = 0;" +

                "  if (stable >= 5) break;" +
                "}" +

                "const finalItems = collect();" +
                "await send(finalItems);" +

                "return 'IMA_INGEST_COMPLETE:' + seen.size;" +
                "})()";

        webView.evaluateJavascript(javascript, value -> {
            Toast.makeText(
                    MainActivity.this,
                    "IMA: " + value,
                    Toast.LENGTH_LONG
            ).show();
        });
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.destroy();
        }
        super.onDestroy();
    }
}
