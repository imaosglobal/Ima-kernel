package com.ima.core.browser;

import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;

public class IMABrowserAccessibilityService extends AccessibilityService {

    private static IMABrowserAccessibilityService instance;

    public static IMABrowserAccessibilityService getInstance() {
        return instance;
    }

    @Override
    public void onServiceConnected() {
        super.onServiceConnected();
        instance = this;
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        // Browser content is read through the active accessibility tree.
    }

    @Override
    public void onInterrupt() {
    }

    public String readVisibleText() {
        AccessibilityNodeInfo root = getRootInActiveWindow();
        if (root == null) {
            return "";
        }

        StringBuilder out = new StringBuilder();
        collectText(root, out);
        return out.toString().trim();
    }

    private void collectText(
            AccessibilityNodeInfo node,
            StringBuilder out) {

        if (node == null) {
            return;
        }

        CharSequence text = node.getText();

        if (text != null && text.length() > 0) {
            out.append(text).append('\n');
        }

        for (int i = 0; i < node.getChildCount(); i++) {
            collectText(node.getChild(i), out);
        }
    }
}
