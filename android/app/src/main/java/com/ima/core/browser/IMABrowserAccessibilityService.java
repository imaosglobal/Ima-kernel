package com.ima.core.browser;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.GestureDescription;
import android.graphics.Bitmap;
import android.graphics.ColorSpace;
import android.graphics.Path;
import android.hardware.HardwareBuffer;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.provider.MediaStore;
import android.view.Display;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import org.json.JSONObject;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

public class IMABrowserAccessibilityService extends AccessibilityService {
    private static IMABrowserAccessibilityService instance;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private final Executor screenshotExecutor = Executors.newSingleThreadExecutor();

    public static IMABrowserAccessibilityService getInstance() { return instance; }

    @Override public void onServiceConnected() {
        super.onServiceConnected();
        instance = this;
        handler.post(remotePoll);
    }

    @Override public void onDestroy() {
        instance = null;
        handler.removeCallbacks(remotePoll);
        super.onDestroy();
    }

    @Override public void onAccessibilityEvent(AccessibilityEvent event) {}
    @Override public void onInterrupt() {}

    private final Runnable remotePoll = new Runnable() {
        @Override public void run() {
            processCommand();
            handler.postDelayed(this, 700);
        }
    };

    private void processCommand() {
        try {
            String raw = readDownload("ima_remote_command.json");
            if (raw == null || raw.trim().isEmpty()) return;
            JSONObject c = new JSONObject(raw);
            if (!c.optBoolean("session", false)) {
                result(c, false, "REMOTE_SESSION_NOT_ENABLED");
                deleteDownload("ima_remote_command.json");
                return;
            }
            String action = c.optString("action", "");
            if ("screenshot".equals(action)) takeScreen(c.optString("id", ""));
            else if ("tap".equals(action)) {
                tap(c.optDouble("x"), c.optDouble("y"));
                result(c, true, "tap_dispatched");
            } else if ("swipe".equals(action)) swipe(c);
            else if ("back".equals(action)) result(c, performGlobalAction(GLOBAL_ACTION_BACK), "back");
            else if ("home".equals(action)) result(c, performGlobalAction(GLOBAL_ACTION_HOME), "home");
            else if ("recents".equals(action)) result(c, performGlobalAction(GLOBAL_ACTION_RECENTS), "recents");
            else if ("read_text".equals(action)) result(c, true, readVisibleText());
            else if ("status".equals(action)) result(c, true, "IMA_REMOTE_ACCESSIBILITY_ONLINE");
            else result(c, false, "UNKNOWN_ACTION");
            if (!"screenshot".equals(action)) deleteDownload("ima_remote_command.json");
        } catch (Exception ignored) {}
    }

    private void takeScreen(String id) {
        if (Build.VERSION.SDK_INT < 30) {
            writeDownload("ima_remote_result.json", errorJson(id, "SCREENSHOT_REQUIRES_ANDROID_11"));
            deleteDownload("ima_remote_command.json");
            return;
        }
        takeScreenshot(Display.DEFAULT_DISPLAY, screenshotExecutor, new TakeScreenshotCallback() {
            @Override public void onSuccess(ScreenshotResult result) {
                Bitmap bitmap = null;
                HardwareBuffer buffer = null;
                try {
                    buffer = result.getHardwareBuffer();
                    bitmap = Bitmap.wrapHardwareBuffer(buffer, ColorSpace.get(ColorSpace.Named.SRGB));
                    if (bitmap == null) throw new IllegalStateException("SCREENSHOT_BITMAP_NULL");
                    writePng("ima_remote_screen.png", bitmap);
                    writeDownload("ima_remote_result.json",
                            new JSONObject().put("ok", true).put("id", id)
                                    .put("action", "screenshot").put("path", "Download/ima_remote_screen.png").toString());
                } catch (Exception e) {
                    writeDownload("ima_remote_result.json", errorJson(id, e.toString()));
                } finally {
                    if (bitmap != null) bitmap.recycle();
                    if (buffer != null) buffer.close();
                }
                deleteDownload("ima_remote_command.json");
            }
            @Override public void onFailure(int errorCode) {
                writeDownload("ima_remote_result.json", errorJson(id, "SCREENSHOT_FAILED_" + errorCode));
                deleteDownload("ima_remote_command.json");
            }
        });
    }

    private void tap(double x, double y) {
        Path p = new Path();
        p.moveTo((float)x, (float)y);
        dispatchGesture(new GestureDescription.Builder()
                .addStroke(new GestureDescription.StrokeDescription(p, 0, 80)).build(), null, null);
    }

    private void swipe(JSONObject c) {
        Path p = new Path();
        p.moveTo((float)c.optDouble("x1"), (float)c.optDouble("y1"));
        p.lineTo((float)c.optDouble("x2"), (float)c.optDouble("y2"));
        long d = Math.max(100, Math.min(3000, c.optLong("duration_ms", 500)));
        dispatchGesture(new GestureDescription.Builder()
                .addStroke(new GestureDescription.StrokeDescription(p, 0, d)).build(), null, null);
        result(c, true, "swipe_dispatched");
    }

    public String readVisibleText() {
        AccessibilityNodeInfo root = getRootInActiveWindow();
        if (root == null) return "";
        StringBuilder out = new StringBuilder();
        collectText(root, out);
        return out.toString().trim();
    }

    private void collectText(AccessibilityNodeInfo node, StringBuilder out) {
        if (node == null) return;
        CharSequence text = node.getText();
        if (text != null && text.length() > 0) out.append(text).append('\n');
        for (int i = 0; i < node.getChildCount(); i++) collectText(node.getChild(i), out);
    }

    private void result(JSONObject c, boolean ok, String message) {
        try {
            writeDownload("ima_remote_result.json", new JSONObject()
                    .put("ok", ok).put("id", c.optString("id", ""))
                    .put("action", c.optString("action", "")).put("message", message).toString());
        } catch (Exception ignored) {}
    }

    private String errorJson(String id, String error) {
        try { return new JSONObject().put("ok", false).put("id", id).put("error", error).toString(); }
        catch (Exception e) { return "{\"ok\":false}"; }
    }

    private String readDownload(String name) {
        try {
            android.net.Uri uri = findDownload(name);
            if (uri == null) return null;
            try (InputStream in = getContentResolver().openInputStream(uri)) {
                byte[] data = new byte[in.available()];
                int n = in.read(data);
                return new String(data, 0, Math.max(0, n), StandardCharsets.UTF_8);
            }
        } catch (Exception e) { return null; }
    }

    private void writeDownload(String name, String content) {
        try {
            android.net.Uri uri = findDownload(name);
            if (uri == null) {
                android.content.ContentValues v = new android.content.ContentValues();
                v.put(MediaStore.Downloads.DISPLAY_NAME, name);
                v.put(MediaStore.Downloads.MIME_TYPE, "application/json");
                v.put(MediaStore.Downloads.RELATIVE_PATH, "Download/");
                uri = getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, v);
            }
            if (uri != null) try (OutputStream out = getContentResolver().openOutputStream(uri, "wt")) {
                out.write(content.getBytes(StandardCharsets.UTF_8));
            }
        } catch (Exception ignored) {}
    }

    private void writePng(String name, Bitmap bitmap) {
        try {
            android.net.Uri old = findDownload(name);
            if (old != null) getContentResolver().delete(old, null, null);
            android.content.ContentValues v = new android.content.ContentValues();
            v.put(MediaStore.Downloads.DISPLAY_NAME, name);
            v.put(MediaStore.Downloads.MIME_TYPE, "image/png");
            v.put(MediaStore.Downloads.RELATIVE_PATH, "Download/");
            android.net.Uri uri = getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, v);
            if (uri != null) try (OutputStream out = getContentResolver().openOutputStream(uri)) {
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, out);
            }
        } catch (Exception ignored) {}
    }

    private android.net.Uri findDownload(String name) {
        String[] projection = {MediaStore.Downloads._ID};
        try (android.database.Cursor c = getContentResolver().query(
                MediaStore.Downloads.EXTERNAL_CONTENT_URI, projection,
                MediaStore.Downloads.DISPLAY_NAME + "=?", new String[]{name}, null)) {
            if (c != null && c.moveToFirst())
                return android.content.ContentUris.withAppendedId(
                        MediaStore.Downloads.EXTERNAL_CONTENT_URI, c.getLong(0));
        } catch (Exception ignored) {}
        return null;
    }

    private void deleteDownload(String name) {
        try {
            android.net.Uri uri = findDownload(name);
            if (uri != null) getContentResolver().delete(uri, null, null);
        } catch (Exception ignored) {}
    }
}
