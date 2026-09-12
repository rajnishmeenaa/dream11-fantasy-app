package com.fantasy11.admin;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

public class AdminActivity extends AppCompatActivity {

    private static final String PREFS_NAME = "Fantasy11AdminPrefs";
    private static final String KEY_SERVER_URL = "admin_server_url";
    private static final String DEFAULT_ADMIN_URL = "http://10.191.72.249:8000/admin.html";

    private WebView webView;
    private SwipeRefreshLayout swipeRefreshLayout;
    private ProgressBar progressBar;
    private View errorContainer;
    private TextView errorText;
    private boolean doubleBackToExitPressedOnce = false;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_admin);

        webView = findViewById(R.id.adminWebView);
        swipeRefreshLayout = findViewById(R.id.adminSwipeRefresh);
        progressBar = findViewById(R.id.adminProgressBar);
        errorContainer = findViewById(R.id.adminErrorContainer);
        errorText = findViewById(R.id.adminErrorText);

        findViewById(R.id.btnAdminRetry).setOnClickListener(v -> reloadCurrentUrl());
        findViewById(R.id.btnAdminChangeServer).setOnClickListener(v -> showServerConfigDialog());

        setupWebView();
        setupSwipeRefresh();
        loadAppUrl();
    }

    private String getServerUrl() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        return prefs.getString(KEY_SERVER_URL, DEFAULT_ADMIN_URL);
    }

    private void saveServerUrl(String url) {
        if (!url.contains("/admin.html")) {
            if (!url.endsWith("/")) url += "/";
            url += "admin.html";
        }
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        prefs.edit().putString(KEY_SERVER_URL, url).apply();
    }

    private void loadAppUrl() {
        String url = getServerUrl();
        errorContainer.setVisibility(View.GONE);
        webView.setVisibility(View.VISIBLE);
        webView.loadUrl(url);
    }

    private void reloadCurrentUrl() {
        errorContainer.setVisibility(View.GONE);
        webView.setVisibility(View.VISIBLE);
        webView.reload();
    }

    @SuppressLint("SetJavaScriptEnabled")
    private void setupWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);

        // Sound effects enabled for boundary cheers & wicket sirens
        settings.setMediaPlaybackRequiresUserGesture(false);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (newProgress < 100) {
                    progressBar.setVisibility(View.VISIBLE);
                    progressBar.setProgress(newProgress);
                } else {
                    progressBar.setVisibility(View.GONE);
                    swipeRefreshLayout.setRefreshing(false);
                }
            }
        });

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                errorContainer.setVisibility(View.GONE);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                swipeRefreshLayout.setRefreshing(false);
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) {
                    webView.setVisibility(View.GONE);
                    errorContainer.setVisibility(View.VISIBLE);
                    errorText.setText("Cannot connect to Fantasy11 Admin Console:\n" + getServerUrl() + "\n\nCheck your Wi-Fi and server status.");
                }
            }
        });
    }

    private void setupSwipeRefresh() {
        swipeRefreshLayout.setOnRefreshListener(this::reloadCurrentUrl);
    }

    private void showServerConfigDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Configure Admin Console URL");
        builder.setMessage("Enter the server URL for Fantasy11 Admin Console:");

        final EditText input = new EditText(this);
        input.setText(getServerUrl());
        builder.setView(input);

        builder.setPositiveButton("Save & Connect", (dialog, which) -> {
            String newUrl = input.getText().toString().trim();
            if (!newUrl.isEmpty()) {
                if (!newUrl.startsWith("http://") && !newUrl.startsWith("https://")) {
                    newUrl = "http://" + newUrl;
                }
                saveServerUrl(newUrl);
                loadAppUrl();
            }
        });
        builder.setNegativeButton("Cancel", (dialog, which) -> dialog.cancel());
        builder.show();
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
            return;
        }

        if (doubleBackToExitPressedOnce) {
            super.onBackPressed();
            return;
        }

        this.doubleBackToExitPressedOnce = true;
        Toast.makeText(this, "Press BACK again to exit Admin Console", Toast.LENGTH_SHORT).show();
        new Handler(Looper.getMainLooper()).postDelayed(() -> doubleBackToExitPressedOnce = false, 2000);
    }
}
