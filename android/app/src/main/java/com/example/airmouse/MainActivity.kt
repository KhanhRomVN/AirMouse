package com.example.airmouse

import android.app.Activity
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.Typeface
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.Settings
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.view.inputmethod.EditorInfo
import android.view.inputmethod.InputMethodManager
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import java.net.Inet4Address
import java.net.NetworkInterface

class MainActivity : Activity() {

    private val ui = Handler(Looper.getMainLooper())

    private lateinit var dot: PulseDot
    private lateinit var statusTitle: TextView
    private lateinit var statusSub: TextView
    private lateinit var cta: TextView
    private lateinit var ipText: TextView
    private lateinit var otherIps: TextView
    private lateinit var cmdText: TextView

    private var currentIp = ""

    private val refresher = object : Runnable {
        override fun run() {
            refresh()
            ui.postDelayed(this, 1000)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = Palette.BG
        window.navigationBarColor = Palette.BG

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(20), dp(24), dp(20), dp(28))
        }

        root.addView(header())
        root.addView(statusCard(), lp(MATCH, WRAP, t = dp(24)))
        root.addView(connectionCard(), lp(MATCH, WRAP, t = dp(14)))
        root.addView(securityCard(), lp(MATCH, WRAP, t = dp(14)))
        root.addView(guideCard(), lp(MATCH, WRAP, t = dp(14)))
        root.addView(
            label("AirMouse ${versionName()}  ·  Kéo con trỏ ra mép trái để trả chuột về laptop", 11f, Palette.FAINT).apply {
                gravity = Gravity.CENTER
            },
            lp(MATCH, WRAP, t = dp(22))
        )

        setContentView(ScrollView(this).apply {
            setBackgroundColor(Palette.BG)
            isFillViewport = true
            overScrollMode = View.OVER_SCROLL_NEVER
            addView(root, ViewGroup.LayoutParams(MATCH, WRAP))
        })
    }

    override fun onResume() {
        super.onResume()
        ui.removeCallbacks(refresher)
        ui.post(refresher)
    }

    override fun onPause() {
        ui.removeCallbacks(refresher)
        super.onPause()
    }

    // ───────────── các khối giao diện ─────────────
    private fun header(): View = LinearLayout(this).apply {
        orientation = LinearLayout.HORIZONTAL
        gravity = Gravity.CENTER_VERTICAL
        addView(LogoView(context), lp(dp(48), dp(48)))
        addView(LinearLayout(context).apply {
            orientation = LinearLayout.VERTICAL
            addView(label("AirMouse", 24f, Palette.TEXT, bold = true))
            addView(label("Chuột & bàn phím không dây từ laptop", 12.5f, Palette.MUTED), lp(WRAP, WRAP, t = dp(4)))
        }, lp(WRAP, WRAP, l = dp(14)))
    }

    private fun statusCard(): View = card().apply {
        val row = LinearLayout(context).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        dot = PulseDot(context)
        row.addView(dot, lp(dp(48), dp(48)))
        val col = LinearLayout(context).apply { orientation = LinearLayout.VERTICAL }
        statusTitle = label("", 18f, Palette.TEXT, bold = true)
        statusSub = label("", 13f, Palette.MUTED).apply { setLineSpacing(0f, 1.15f) }
        col.addView(statusTitle)
        col.addView(statusSub, lp(WRAP, WRAP, t = dp(4)))
        row.addView(col, LinearLayout.LayoutParams(0, WRAP, 1f).apply { leftMargin = dp(12) })
        addView(row)

        cta = button("Bật trong Cài đặt Trợ năng", BtnKind.PRIMARY) {
            startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
        }
        addView(cta, lp(MATCH, WRAP, t = dp(16)))
    }

    private fun connectionCard(): View = card().apply {
        addView(caption("ĐỊA CHỈ ĐIỆN THOẠI"))
        ipText = label("…", 30f, Palette.TEXT, mono = true).apply {
            isClickable = true
            setOnClickListener { copy(currentIp, "Đã sao chép địa chỉ IP") }
        }
        addView(ipText, lp(WRAP, WRAP, t = dp(10)))
        otherIps = label("", 12f, Palette.MUTED, mono = true)
        addView(otherIps, lp(WRAP, WRAP, t = dp(4)))
        addView(
            label("Nhập IP này vào AirMouse trên laptop. Chạm để sao chép.", 12.5f, Palette.MUTED)
                .apply { setLineSpacing(0f, 1.15f) },
            lp(MATCH, WRAP, t = dp(8))
        )

        // dòng lệnh dành cho ai dùng CLI
        cmdText = label("", 12f, Palette.CYAN, mono = true).apply {
            background = shape(Palette.SURFACE2, 12f, Palette.BORDER, 1f)
            setPadding(dp(14), dp(12), dp(14), dp(12))
            isClickable = true
            setOnClickListener { copy(cmdText.text.toString(), "Đã sao chép lệnh") }
        }
        addView(cmdText, lp(MATCH, WRAP, t = dp(14)))
        addView(label("UDP ${Config.PORT}", 11f, Palette.FAINT, mono = true), lp(WRAP, WRAP, t = dp(8)))
    }

    private fun securityCard(): View = card().apply {
        val prefs = getSharedPreferences(Config.PREFS, MODE_PRIVATE)
        addView(caption("MẬT KHẨU KẾT NỐI"))

        val box = LinearLayout(context).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            background = shape(Palette.SURFACE2, 12f, Palette.BORDER, 1f)
            setPadding(dp(14), 0, dp(14), 0)
        }
        val secret = EditText(context).apply {
            setText(prefs.getString(Config.KEY_SECRET, Config.DEFAULT_SECRET))
            setTextColor(Palette.TEXT)
            setHintTextColor(Palette.FAINT)
            textSize = 16f
            background = null
            setPadding(0, dp(14), 0, dp(14))
            setSingleLine()
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
            typeface = Typeface.MONOSPACE
            imeOptions = EditorInfo.IME_ACTION_DONE
        }
        var visible = false
        val eye = label("Hiện", 13f, Palette.MUTED, bold = true).apply {
            setPadding(dp(8), dp(10), 0, dp(10))
            setOnClickListener {
                visible = !visible
                val sel = secret.selectionEnd
                val variation = if (visible) InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD
                else InputType.TYPE_TEXT_VARIATION_PASSWORD
                secret.inputType = InputType.TYPE_CLASS_TEXT or variation
                secret.typeface = Typeface.MONOSPACE
                secret.setSelection(sel.coerceIn(0, secret.text.length))
                text = if (visible) "Ẩn" else "Hiện"
            }
        }
        box.addView(secret, LinearLayout.LayoutParams(0, WRAP, 1f))
        box.addView(eye)
        addView(box, lp(MATCH, WRAP, t = dp(12)))

        lateinit var save: TextView
        val doSave = {
            val v = secret.text.toString().trim().ifEmpty { Config.DEFAULT_SECRET }
            prefs.edit().putString(Config.KEY_SECRET, v).apply()
            save.text = "Đã lưu ✓"
            save.setTextColor(Palette.OK)
            ui.postDelayed({
                save.text = "Lưu mật khẩu"
                save.setTextColor(Palette.TEXT)
            }, 1500)
            (getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager)
                .hideSoftInputFromWindow(secret.windowToken, 0)
            secret.clearFocus()
        }
        save = button("Lưu mật khẩu", BtnKind.SECONDARY) { doSave() }
        secret.setOnEditorActionListener { _, id, _ ->
            if (id == EditorInfo.IME_ACTION_DONE) { doSave(); true } else false
        }
        addView(save, lp(MATCH, WRAP, t = dp(12)))
        addView(
            label("Phải trùng với mật khẩu nhập trên laptop (mặc định ${Config.DEFAULT_SECRET}). Nên đổi, và chỉ dùng trên mạng tin cậy.", 12f, Palette.FAINT)
                .apply { setLineSpacing(0f, 1.15f) },
            lp(MATCH, WRAP, t = dp(10))
        )
    }

    private fun guideCard(): View = card().apply {
        addView(caption("HƯỚNG DẪN NHANH"))
        val steps = listOf(
            "Bật Trợ năng" to "Cài đặt → Trợ năng → AirMouse → Bật. Nếu máy chặn: Thông tin ứng dụng → ⋮ → “Cho phép cài đặt bị hạn chế”.",
            "Cùng một mạng Wi-Fi" to "Điện thoại và laptop phải kết nối chung một mạng.",
            "Mở AirMouse trên laptop" to "Nhập IP và mật khẩu ở trên rồi bấm Kết nối.",
            "Điều khiển" to "Đẩy chuột sang mép phải màn hình laptop (hoặc Ctrl+Alt+M). Chuột trái = chạm / giữ / kéo, lăn = cuộn, chuột phải = Back, chuột giữa = Home."
        )
        steps.forEachIndexed { i, (title, desc) ->
            val row = LinearLayout(context).apply { orientation = LinearLayout.HORIZONTAL }
            val badge = label("${i + 1}", 13f, Palette.ACCENT, bold = true).apply {
                gravity = Gravity.CENTER
                background = shape(Palette.ACCENT_SOFT, 100f)
            }
            row.addView(badge, lp(dp(28), dp(28), t = dp(1)))
            val col = LinearLayout(context).apply { orientation = LinearLayout.VERTICAL }
            col.addView(label(title, 14.5f, Palette.TEXT, bold = true))
            col.addView(
                label(desc, 12.5f, Palette.MUTED).apply { setLineSpacing(0f, 1.15f) },
                lp(MATCH, WRAP, t = dp(3))
            )
            row.addView(col, LinearLayout.LayoutParams(0, WRAP, 1f).apply { leftMargin = dp(12) })
            addView(row, lp(MATCH, WRAP, t = dp(if (i == 0) 14 else 16)))
        }
    }

    // ───────────── trạng thái ─────────────
    private fun refresh() {
        val ips = localIps()
        val primary = ips.firstOrNull { it.startsWith("192.168.") || it.startsWith("10.") || it.startsWith("172.") }
            ?: ips.firstOrNull()
        currentIp = primary ?: ""
        ipText.text = primary ?: "Chưa có Wi-Fi"
        ipText.setTextColor(if (primary != null) Palette.TEXT else Palette.WARN)
        val extra = ips.filter { it != primary }
        otherIps.visibility = if (extra.isEmpty()) View.GONE else View.VISIBLE
        otherIps.text = "Khác: ${extra.joinToString(", ")}"
        cmdText.text = "python3 airmouse_laptop.py --phone ${primary ?: "<IP>"}"

        val enabled = isServiceEnabled()
        when {
            !enabled -> {
                dot.set(Palette.WARN, false)
                statusTitle.text = "Chưa bật Trợ năng"
                statusSub.text = "AirMouse cần quyền Trợ năng để vẽ con trỏ và thực hiện thao tác chạm thay bạn."
                cta.visibility = View.VISIBLE
            }
            AirState.remote && AirState.connected() -> {
                dot.set(Palette.ACCENT, true)
                statusTitle.text = "Đang được điều khiển"
                statusSub.text = "Kéo con trỏ ra mép trái màn hình để trả chuột về laptop."
                cta.visibility = View.GONE
            }
            AirState.connected() -> {
                dot.set(Palette.OK, false)
                statusTitle.text = "Đã kết nối laptop"
                statusSub.text = "${AirState.peer ?: "Laptop"} · Đẩy chuột sang mép phải màn hình laptop để bắt đầu."
                cta.visibility = View.GONE
            }
            else -> {
                dot.set(Palette.CYAN, true)
                statusTitle.text = "Sẵn sàng kết nối"
                statusSub.text = "Đang chờ laptop trên cổng UDP ${Config.PORT}."
                cta.visibility = View.GONE
            }
        }
    }

    private fun copy(text: String, toast: String) {
        if (text.isBlank()) return
        val cm = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        cm.setPrimaryClip(ClipData.newPlainText("AirMouse", text))
        Toast.makeText(this, toast, Toast.LENGTH_SHORT).show()
    }

    private fun versionName(): String = try {
        "v" + packageManager.getPackageInfo(packageName, 0).versionName
    } catch (_: Exception) {
        ""
    }

    private fun isServiceEnabled(): Boolean {
        val enabled = Settings.Secure.getString(
            contentResolver, Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
        ) ?: return false
        return enabled.split(':').any {
            it.startsWith("$packageName/") && it.endsWith("MouseService")
        }
    }

    private fun localIps(): List<String> = try {
        (NetworkInterface.getNetworkInterfaces()?.toList() ?: emptyList())
            .filter { it.isUp && !it.isLoopback }
            .flatMap { it.inetAddresses.toList() }
            .filterIsInstance<Inet4Address>()
            .mapNotNull { it.hostAddress }
    } catch (_: Exception) {
        emptyList()
    }

    private companion object {
        const val MATCH = ViewGroup.LayoutParams.MATCH_PARENT
        const val WRAP = ViewGroup.LayoutParams.WRAP_CONTENT
    }
}
