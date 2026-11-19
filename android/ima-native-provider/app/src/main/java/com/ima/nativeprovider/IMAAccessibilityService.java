package com.ima.nativeprovider;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.accessibilityservice.GestureDescription;
import android.graphics.Bitmap;
import android.graphics.Path;
import android.graphics.Rect;
import android.hardware.HardwareBuffer;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.view.accessibility.AccessibilityNodeInfo;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;

import org.json.JSONObject;
import org.json.JSONArray;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Base64;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class IMAAccessibilityService extends AccessibilityService {
    private static final String BASE="http://127.0.0.1:8787";
    private final ExecutorService io=Executors.newSingleThreadExecutor();
    private final Handler main=new Handler(Looper.getMainLooper());
    private volatile boolean running=false;

    @Override protected void onServiceConnected() {
        super.onServiceConnected();
        AccessibilityServiceInfo info=getServiceInfo();
        info.flags |= AccessibilityServiceInfo.FLAG_RETRIEVE_INTERACTIVE_WINDOWS;
        setServiceInfo(info);
        running=true;
        io.execute(() -> registerLoop());
    }

    private void registerLoop() {
        while(running) {
            try {
                postJson("/native/register", new JSONObject().put("package",getPackageName()).put("version","1.0.0"));
                pollOnce();
                Thread.sleep(400);
            } catch(Exception e) {
                try { Thread.sleep(1200); } catch(Exception ignored) {}
            }
        }
    }

    private void pollOnce() throws Exception {
        HttpURLConnection c=(HttpURLConnection)new URL(BASE+"/native/poll").openConnection();
        c.setConnectTimeout(1500); c.setReadTimeout(2500); c.setRequestMethod("GET");
        if(c.getResponseCode()!=200) return;
        JSONObject body=new JSONObject(read(c.getInputStream()));
        if(!body.optBoolean("ok") || body.isNull("command")) return;
        JSONObject cmd=body.getJSONObject("command");
        JSONObject result;
        try { result=execute(cmd); }
        catch(Exception e) { result=new JSONObject().put("ok",false).put("id",cmd.optString("id")).put("error",e.toString()); }
        result.put("id",cmd.optString("id"));
        postJson("/native/result",result);
    }

    private JSONObject execute(JSONObject cmd) throws Exception {
        String a=cmd.optString("action");
        switch(a) {
            case "screenshot": return screenshot();
            case "tap": return tap(cmd.optDouble("x"),cmd.optDouble("y"));
            case "swipe": return swipe(cmd.optDouble("x1"),cmd.optDouble("y1"),cmd.optDouble("x2"),cmd.optDouble("y2"),cmd.optLong("duration_ms",350));
            case "back": return new JSONObject().put("ok",performGlobalAction(GLOBAL_ACTION_BACK));
            case "home": return new JSONObject().put("ok",performGlobalAction(GLOBAL_ACTION_HOME));
            case "navigate": {
                String u=cmd.optString("url");
                if(!u.startsWith("http://") && !u.startsWith("https://")) throw new IllegalArgumentException("url must be http(s)");
                Intent i=new Intent(Intent.ACTION_VIEW, Uri.parse(u)); i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK); startActivity(i);
                return new JSONObject().put("ok",true).put("url",u);
            }
            case "text": return setText(cmd.optString("text"));
            case "read_text": return readText();
            case "key": return key(cmd.optString("key"));
            case "status": return new JSONObject().put("ok",true).put("transport","native-android-loopback").put("accessibility",true);
            default: throw new IllegalArgumentException("unsupported action: "+a);
        }
    }

    private JSONObject tap(double x,double y) throws Exception {
        Path p=new Path(); p.moveTo((float)x,(float)y);
        GestureDescription g=new GestureDescription.Builder().addStroke(new GestureDescription.StrokeDescription(p,0,80)).build();
        boolean ok=dispatchGesture(g,null,main);
        return new JSONObject().put("ok",ok).put("x",x).put("y",y);
    }

    private JSONObject swipe(double x1,double y1,double x2,double y2,long duration) throws Exception {
        Path p=new Path(); p.moveTo((float)x1,(float)y1); p.lineTo((float)x2,(float)y2);
        GestureDescription g=new GestureDescription.Builder().addStroke(new GestureDescription.StrokeDescription(p,0,Math.max(100,duration))).build();
        boolean ok=dispatchGesture(g,null,main);
        return new JSONObject().put("ok",ok);
    }

    private JSONObject setText(String text) {
        AccessibilityNodeInfo n=getRootInActiveWindow();
        if(n==null) return new JSONObject().put("ok",false).put("error","no_active_window");
        AccessibilityNodeInfo f=findFocused(n);
        if(f==null) f=n;
        boolean ok=false;
        if(Build.VERSION.SDK_INT>=21) {
            android.os.Bundle args=new android.os.Bundle();
            args.putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE,text);
            ok=f.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT,args);
        }
        if(!ok) {
            ClipboardManager cm=(ClipboardManager)getSystemService(Context.CLIPBOARD_SERVICE);
            cm.setPrimaryClip(ClipData.newPlainText("IMA",text));
            ok=f.performAction(AccessibilityNodeInfo.ACTION_PASTE);
        }
        return new JSONObject().put("ok",ok);
    }

    private AccessibilityNodeInfo findFocused(AccessibilityNodeInfo n) {
        if(n==null) return null;
        if(n.isFocused() || n.isAccessibilityFocused()) return n;
        for(int i=0;i<n.getChildCount();i++){ AccessibilityNodeInfo x=findFocused(n.getChild(i)); if(x!=null)return x; }
        return null;
    }

    private JSONObject readText() throws Exception {
        AccessibilityNodeInfo root=getRootInActiveWindow();
        JSONArray out=new JSONArray();
        if(root!=null) collect(root,out);
        return new JSONObject().put("ok",true).put("text",out.toString());
    }

    private void collect(AccessibilityNodeInfo n,JSONArray out) throws Exception {
        CharSequence t=n.getText();
        CharSequence d=n.getContentDescription();
        if(t!=null && t.length()>0) out.put(t.toString());
        else if(d!=null && d.length()>0) out.put(d.toString());
        for(int i=0;i<n.getChildCount();i++){ AccessibilityNodeInfo x=n.getChild(i); if(x!=null) collect(x,out); }
    }

    private JSONObject key(String k) {
        boolean ok=false;
        if("Escape".equals(k) || "Back".equals(k)) ok=performGlobalAction(GLOBAL_ACTION_BACK);
        else if("Home".equals(k)) ok=performGlobalAction(GLOBAL_ACTION_HOME);
        else if("Enter".equals(k)) {
            AccessibilityNodeInfo n=findFocused(getRootInActiveWindow());
            ok=n!=null && n.performAction(AccessibilityNodeInfo.ACTION_CLICK);
        } else if("Backspace".equals(k)) {
            AccessibilityNodeInfo n=findFocused(getRootInActiveWindow());
            if(n!=null) ok=n.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT);
        }
        return new JSONObject().put("ok",ok).put("key",k);
    }

    private JSONObject screenshot() throws Exception {
        if(Build.VERSION.SDK_INT<30) throw new IllegalStateException("Android 11+ required for native screenshot");
        final JSONObject[] holder=new JSONObject[1];
        final Object lock=new Object();
        takeScreenshot(android.view.Display.DEFAULT_DISPLAY, io, new TakeScreenshotCallback() {
            @Override public void onSuccess(ScreenshotResult r) {
                try {
                    HardwareBuffer hb=r.getHardwareBuffer();
                    android.graphics.ColorSpace cs=r.getColorSpace();
                    Bitmap b=Bitmap.wrapHardwareBuffer(hb,cs);
                    ByteArrayOutputStream out=new ByteArrayOutputStream();
                    b.compress(Bitmap.CompressFormat.PNG,100,out);
                    b.recycle(); hb.close();
                    holder[0]=new JSONObject().put("ok",true).put("mime","image/png").put("data",Base64.getEncoder().encodeToString(out.toByteArray())).put("source","android-accessibility").put("transport","native-android-loopback");
                } catch(Exception e) { try { holder[0]=new JSONObject().put("ok",false).put("error",e.toString()); } catch(Exception ignored) {} }
                synchronized(lock){lock.notifyAll();}
            }
            @Override public void onFailure(int errorCode) {
                try { holder[0]=new JSONObject().put("ok",false).put("error","takeScreenshot_failed:"+errorCode); } catch(Exception ignored) {}
                synchronized(lock){lock.notifyAll();}
            }
        });
        long end=System.currentTimeMillis()+8000;
        synchronized(lock){ while(holder[0]==null && System.currentTimeMillis()<end) lock.wait(200); }
        if(holder[0]==null) throw new IllegalStateException("screenshot timeout");
        return holder[0];
    }

    private JSONObject postJson(String path,JSONObject body) throws Exception {
        HttpURLConnection c=(HttpURLConnection)new URL(BASE+path).openConnection();
        c.setConnectTimeout(1500); c.setReadTimeout(3000); c.setRequestMethod("POST"); c.setDoOutput(true);
        c.setRequestProperty("Content-Type","application/json");
        byte[] raw=body.toString().getBytes("UTF-8");
        try(OutputStream o=c.getOutputStream()){o.write(raw);}
        int code=c.getResponseCode(); String s=read(code>=200&&code<400?c.getInputStream():c.getErrorStream());
        if(code>=300) throw new IllegalStateException("bridge_http_"+code+":"+s);
        return s.isEmpty()?new JSONObject():new JSONObject(s);
    }

    private String read(InputStream in) throws Exception {
        if(in==null)return "";
        ByteArrayOutputStream b=new ByteArrayOutputStream(); byte[] buf=new byte[8192]; int n;
        while((n=in.read(buf))!=-1)b.write(buf,0,n);
        return b.toString("UTF-8");
    }

    @Override public void onInterrupt(){ running=false; }
    @Override public boolean onUnbind(Intent intent){ running=false; io.shutdownNow(); return super.onUnbind(intent); }
}
