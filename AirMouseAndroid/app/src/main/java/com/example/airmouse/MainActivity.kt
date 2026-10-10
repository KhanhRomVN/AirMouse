package com.example.airmouse

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.text.InputType
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import java.net.Inet4Address
import java.net.NetworkInterface

class MainActivity : Activity() {

    private lateinit var info: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val prefs = getSharedPreferences(Config.PREFS, MODE_PRIVATE)
        val pad = (20 * resources.displayMetrics.density).toInt()

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(pad, pad, pad, pad)
        }

        val title = TextView(this).apply {
            text = "AirMouse"
            textSize = 28f
        }
        info = TextView(this).apply {
            textSize = 16f
            setPadding(0, pad / 2, 0, pad / 2)
        }
        val label = TextView(this).apply {
            text = "Mật khẩu (phải trùng với --secret trên máy tính):"
        }
        val secret = EditText(this).apply {
            setText(prefs.getString(Config.KEY_SECRET, Config.DEFAULT_SECRET))
            inputType = InputType.TYPE_CLASS_TEXT
            setSingleLine()
        }
        val save = Button(this).apply {
            text = "Lưu mật khẩu"
            setOnClickListener {
                val v = secret.text.toString().trim().ifEmpty { Config.DEFAULT_SECRET }
                prefs.edit().putString(Config.KEY_SECRET, v).apply()
                Toast.makeText(context, "Đã lưu", Toast.LENGTH_SHORT).show()
            }
        }
        val open = Button(this).apply {
            text = "Mở cài đặt Trợ năng"
            setOnClickListener {
                startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
            }
        }
        val help = TextView(this).apply {
            textSize = 14f
            setPadding(0, pad, 0, 0)
            text = "Cách dùng:\n" +
                "1. Bấm \"Mở cài đặt Trợ năng\" → tìm AirMouse → bật. (Nếu máy chặn: Cài đặt → Ứng dụng → AirMouse → ⋮ → \"Cho phép cài đặt bị hạn chế\", rồi bật lại.)\n" +
                "2. Điện thoại và máy tính cùng mạng Wi-Fi.\n" +
                "3. Trên máy tính chạy: python3 airmouse_laptop.py --phone <IP ở trên>\n" +
                "4. Đẩy chuột sang mép phải màn hình laptop (hoặc Ctrl+Alt+M) để chuột sang điện thoại.\n\n" +
                "Chuột trái = chạm / giữ / kéo, lăn chuột = cuộn, chuột phải = Back, chuột giữa = Home.\n" +
                "Kéo con trỏ ra mép trái màn hình điện thoại để trả chuột về máy tính."
        }

        listOf(title, info, label, secret, save, open, help).forEach { root.addView(it) }
        setContentView(ScrollView(this).apply { addView(root) })
    }

    override fun onResume() {
        super.onResume()
        val ips = localIps().ifEmpty { listOf("(chưa kết nối Wi-Fi)") }
        val status = if (isServiceEnabled()) "ĐANG BẬT ✅" else "CHƯA BẬT ❌"
        info.text = "IP điện thoại: ${ips.joinToString(", ")}\n" +
            "Cổng UDP: ${Config.PORT}\n" +
            "Dịch vụ Trợ năng: $status"
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
}
