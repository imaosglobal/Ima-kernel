package com.ima.core;

import android.app.*;
import android.content.*;
import android.graphics.*;
import android.hardware.display.DisplayManager;
import android.hardware.display.VirtualDisplay;
import android.media.*;
import android.media.projection.MediaProjection;
import android.media.projection.MediaProjectionManager;
import android.os.*;
import android.view.Surface;
import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.util.UUID;
import java.util.concurrent.*;

public class ImaScreenRelayService extends Service {
    public static final String ACTION_START = "com.ima.core.SCREEN_RELAY_START";
    public static final String ACTION_STOP = "com.ima.core.SCREEN_RELAY_STOP";
    public static final String EXTRA_RESULT_CODE = "result_code";
    public static final String EXTRA_RESULT_DATA = "result_data";
    public static final String EXTRA_ENDPOINT = "endpoint";
    public static final String EXTRA_DEVICE_KEY = "device_key";

    private static final String CHANNEL = "ima_screen_relay";
    private static final int NOTIFICATION_ID = 41001;
    private static final int MAX_FPS = 4;
    private static final int JPEG_QUALITY = 55;

    private MediaProjection projection;
    private VirtualDisplay display;
    private ImageReader reader;
    private Surface surface;
    private ExecutorService worker;
    private volatile boolean running;
    private String endpoint;
    private String deviceKey;
    private String deviceId;

    @Override public void onCreate() {
        super.onCreate();
        deviceId = getSharedPreferences("ima_screen_relay", MODE_PRIVATE)
                .getString("device_id", null);
        if (deviceId == null) {
            deviceId = UUID.randomUUID().toString();
            getSharedPreferences("ima_screen_relay", MODE_PRIVATE).edit()
                    .putString("device_id", deviceId).apply();
        }
        createNotificationChannel();
    }

    @Override public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent == null) return START_NOT_STICKY;
        if (ACTION_STOP.equals(intent.getAction())) {
            stopCapture();
            stopSelf();
            return START_NOT_STICKY;
        }
        if (!ACTION_START.equals(intent.getAction())) return START_NOT_STICKY;

        endpoint = intent.getStringExtra(EXTRA_ENDPOINT);
        deviceKey = intent.getStringExtra(EXTRA_DEVICE_KEY);
        int resultCode = intent.getIntExtra(EXTRA_RESULT_CODE, Activity.RESULT_CANCELED);
        Intent resultData = getResultData(intent);

        if (endpoint == null || !endpoint.startsWith("https://") ||
                deviceKey == null || deviceKey.trim().isEmpty() ||
                resultData == null || resultCode != Activity.RESULT_OK) {
            stopSelf();
            return START_NOT_STICKY;
        }

        startAsForeground();
        startCapture(resultCode, resultData);
        return START_NOT_STICKY;
    }

    private Intent getResultData(Intent intent) {
        if (Build.VERSION.SDK_INT >= 33) return intent.getParcelableExtra(EXTRA_RESULT_DATA, Intent.class);
        return (Intent) intent.getParcelableExtra(EXTRA_RESULT_DATA);
    }

    private void startAsForeground() {
        Notification.Builder b = Build.VERSION.SDK_INT >= 26
                ? new Notification.Builder(this, CHANNEL)
                : new Notification.Builder(this);
        b.setContentTitle("IMA — שיתוף מסך פעיל")
                .setContentText("המסך משודר דרך האינטרנט ל־IMA")
                .setSmallIcon(android.R.drawable.ic_menu_view)
                .setOngoing(true);
        if (Build.VERSION.SDK_INT >= 29) {
            startForeground(NOTIFICATION_ID, b.build(),
                    android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION);
        } else {
            startForeground(NOTIFICATION_ID, b.build());
        }
    }

    private void startCapture(int resultCode, Intent data) {
        stopCapture();
        try {
            MediaProjectionManager manager =
                    (MediaProjectionManager) getSystemService(MEDIA_PROJECTION_SERVICE);
            projection = manager.getMediaProjection(resultCode, data);
            if (projection == null) throw new IllegalStateException("MediaProjection unavailable");

            projection.registerCallback(new MediaProjection.Callback() {
                @Override public void onStop() { stopCapture(); stopSelf(); }
            }, new Handler(Looper.getMainLooper()));

            DisplayMetricsCompat metrics = DisplayMetricsCompat.get(this);
            int width = metrics.width;
            int height = metrics.height;
            int density = metrics.densityDpi;

            reader = ImageReader.newInstance(width, height,
                    PixelFormat.RGBA_8888, 2);
            surface = reader.getSurface();
            display = projection.createVirtualDisplay(
                    "IMA-LIVE-001", width, height, density,
                    DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
                    surface, null, null);

            running = true;
            worker = Executors.newSingleThreadExecutor();
            worker.execute(this::relayLoop);
        } catch (Exception e) {
            stopCapture();
            stopSelf();
        }
    }

    private void relayLoop() {
        long frameInterval = 1000L / MAX_FPS;
        while (running) {
            long started = System.currentTimeMillis();
            Image image = null;
            try {
                image = reader.acquireLatestImage();
                if (image != null) {
                    byte[] jpeg = encodeJpeg(image);
                    if (jpeg != null) upload(jpeg);
                }
            } catch (Throwable ignored) {
            } finally {
                if (image != null) image.close();
            }
            long wait = frameInterval - (System.currentTimeMillis() - started);
            if (wait > 0) {
                try { Thread.sleep(wait); } catch (InterruptedException e) { break; }
            }
        }
    }

    private byte[] encodeJpeg(Image image) {
        Image.Plane plane = image.getPlanes()[0];
        ByteBuffer buffer = plane.getBuffer();
        int pixelStride = plane.getPixelStride();
        int rowStride = plane.getRowStride();
        int rowPadding = rowStride - pixelStride * image.getWidth();

        Bitmap bitmap = Bitmap.createBitmap(
                image.getWidth() + rowPadding / pixelStride,
                image.getHeight(), Bitmap.Config.ARGB_8888);
        buffer.rewind();
        bitmap.copyPixelsFromBuffer(buffer);
        Bitmap cropped = bitmap;
        if (bitmap.getWidth() != image.getWidth()) {
            cropped = Bitmap.createBitmap(bitmap, 0, 0,
                    image.getWidth(), image.getHeight());
            bitmap.recycle();
        }

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        cropped.compress(Bitmap.CompressFormat.JPEG, JPEG_QUALITY, out);
        cropped.recycle();
        return out.toByteArray();
    }

    private void upload(byte[] jpeg) {
        HttpURLConnection c = null;
        try {
            URL url = new URL(endpoint + "/api/device/frame");
            c = (HttpURLConnection) url.openConnection();
            c.setConnectTimeout(8000);
            c.setReadTimeout(8000);
            c.setRequestMethod("POST");
            c.setDoOutput(true);
            c.setFixedLengthStreamingMode(jpeg.length);
            c.setRequestProperty("Content-Type", "image/jpeg");
            c.setRequestProperty("Cache-Control", "no-store");
            c.setRequestProperty("X-IMA-Device-Key", deviceKey);
            c.setRequestProperty("X-IMA-Device-Serial", deviceId);
            try (OutputStream out = c.getOutputStream()) { out.write(jpeg); }
            c.getResponseCode();
        } catch (Exception ignored) {
        } finally {
            if (c != null) c.disconnect();
        }
    }

    private void stopCapture() {
        running = false;
        if (worker != null) { worker.shutdownNow(); worker = null; }
        if (display != null) { display.release(); display = null; }
        if (surface != null) { surface.release(); surface = null; }
        if (reader != null) { reader.close(); reader = null; }
        if (projection != null) {
            try { projection.unregisterCallback(new MediaProjection.Callback() {}); } catch (Exception ignored) {}
            projection.stop();
            projection = null;
        }
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT < 26) return;
        NotificationManager nm = getSystemService(NotificationManager.class);
        nm.createNotificationChannel(new NotificationChannel(
                CHANNEL, "IMA screen sharing", NotificationManager.IMPORTANCE_LOW));
    }

    @Override public void onDestroy() {
        stopCapture();
        stopForeground(true);
        super.onDestroy();
    }

    @Override public android.os.IBinder onBind(Intent intent) { return null; }

    private static final class DisplayMetricsCompat {
        final int width, height, densityDpi;
        DisplayMetricsCompat(int w, int h, int d) { width=w; height=h; densityDpi=d; }
        static DisplayMetricsCompat get(Context c) {
            android.util.DisplayMetrics m = new android.util.DisplayMetrics();
            android.view.WindowManager wm = (android.view.WindowManager)c.getSystemService(WINDOW_SERVICE);
            wm.getDefaultDisplay().getRealMetrics(m);
            return new DisplayMetricsCompat(m.widthPixels, m.heightPixels, m.densityDpi);
        }
    }
}
