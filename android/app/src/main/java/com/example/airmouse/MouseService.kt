package com.example.airmouse

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Path
import android.graphics.PixelFormat
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.os.SystemClock
import android.util.Base64
import android.util.DisplayMetrics
import android.util.Log
import android.view.Gravity
import android.view.KeyEvent
import android.view.WindowManager
import android.view.accessibility.AccessibilityEvent
import android.widget.Toast
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress
import java.net.SocketTimeoutException
import kotlin.concurrent.thread
import kotlin.math.hypot

/**
 * Nhận lệnh chuột & bàn phím từ laptop qua UDP, vẽ con trỏ (overlay) và thực hiện thao tác bằng
 * dispatchGesture() / ClipboardManager / performGlobalAction(). 
 * Cần bật trong Cài đặt > Trợ năng.
 *
 * Giao thức (mỗi gói UDP):  "<mật khẩu>|<LỆNH> <tham số...>"
 *   PING                 -> trả lời PONG
 *   ENTER <tỉ lệ y>      -> chuột sang điện thoại, xuất hiện ở mép trái
 *   LEAVE                -> ẩn con trỏ
 *   MOVE dx dy           -> di chuyển con trỏ
 *   BTN L|R|M 1|0 [dur dist] -> nhấn/nhả nút (L = chạm/kéo, R = Back, M = Home). 
 *                               Optional params for L release: duration_ms, drag_distance_px.
 *   SCROLL v             -> cuộn dọc (v > 0: cuộn xuống)
 *   HSCROLL v            -> cuộn ngang (v > 0: vuốt sang trái/cuộn phải)
 *   CLIP <base64_text>   -> dán text vào Clipboard Android (Remote Typing)
 *   NAV BACK|HOME|...    -> mô phỏng phím điều hướng hệ thống
 *   KEY ENTER|TAB|BS     -> (Chưa hỗ trợ inject trực tiếp, chỉ log)
 * Điện thoại gửi lại laptop:  RETURN <tỉ lệ y>  khi con trỏ bị kéo ra mép trái.
 */
class MouseService : AccessibilityService() {

    private val main = Handler(Looper.getMainLooper())
    private lateinit var wm: WindowManager
    private var cursor: CursorView? = null

    @Volatile private var running = false
    @Volatile private var socket: DatagramSocket? = null
    private var peerAddr: InetAddress? = null
    private var peerPort = 0

    @Volatile private var active = false
    private var x = 0f
    private var y = 0f
    private var screenW = 1080
    private var screenH = 1920

    private var leftDown = false
    private var downTime = 0L
    private var downX = 0f
    private var downY = 0f

    private var scrollAcc = 0f
    private var scrollScheduled = false

    override fun onServiceConnected() {
        super.onServiceConnected()
        wm = getSystemService(WINDOW_SERVICE) as WindowManager
        updateScreenSize()
        addOverlay()
        AirState.reset()
        AirState.serviceRunning = true
        startNetwork()
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {}
    override fun onInterrupt() {}

    override fun onUnbind(intent: Intent?): Boolean {
        shutdown()
        return super.onUnbind(intent)
    }

    override fun onDestroy() {
        shutdown()
        super.onDestroy()
    }

    private fun shutdown() {
        AirState.serviceRunning = false
        AirState.reset()
        running = false
        socket?.close()
        socket = null
        cursor?.let {
            try { wm.removeView(it) } catch (_: Exception) {}
        }
        cursor = null
    }

    // ---------- overlay ----------
    private fun addOverlay() {
        cursor?.let { try { wm.removeView(it) } catch (_: Exception) {} }
        val v = CursorView(this)
        val lp = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE or
                WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN or
                WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        )
        lp.gravity = Gravity.TOP or Gravity.START
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            lp.layoutInDisplayCutoutMode =
                WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES
        }
        wm.addView(v, lp)
        cursor = v
    }

    private fun updateScreenSize() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            val b = wm.maximumWindowMetrics.bounds
            screenW = b.width()
            screenH = b.height()
        } else {
            val dm = DisplayMetrics()
            @Suppress("DEPRECATION")
            wm.defaultDisplay.getRealMetrics(dm)
            screenW = dm.widthPixels
            screenH = dm.heightPixels
        }
    }

    private fun syncCursor() {
        cursor?.let {
            it.cx = x.coerceAtLeast(0f)
            it.cy = y
            it.invalidate()
        }
    }

    private fun setShown(show: Boolean) {
        cursor?.let {
            it.shown = show
            it.invalidate()
        }
    }

    // ---------- mạng ----------
    private fun secret(): String =
        getSharedPreferences(Config.PREFS, MODE_PRIVATE)
            .getString(Config.KEY_SECRET, Config.DEFAULT_SECRET) ?: Config.DEFAULT_SECRET

    private fun startNetwork() {
        if (running) return
        running = true
        thread(name = "airmouse-udp", isDaemon = true) {
            try {
                val s = DatagramSocket(Config.PORT)
                s.soTimeout = 3000
                socket = s
                val buf = ByteArray(512)
                while (running) {
                    val p = DatagramPacket(buf, buf.size)
                    try {
                        s.receive(p)
                    } catch (_: SocketTimeoutException) {
                        // Laptop im lặng quá lâu (tắt máy, mất Wi-Fi...) -> ẩn con trỏ, tránh kẹt overlay
                        if (active && SystemClock.elapsedRealtime() - AirState.lastSeen > LINK_LOST_MS) {
                            main.post { dropRemote() }
                        }
                        continue
                    }
                    val text = String(p.data, 0, p.length)
                    val bar = text.indexOf('|')
                    if (bar < 0 || text.substring(0, bar) != secret()) continue
                    AirState.touch(p.address?.hostAddress)
                    val cmd = text.substring(bar + 1).trim()
                    val addr = p.address
                    val port = p.port
                    main.post {
                        peerAddr = addr
                        peerPort = port
                        handle(cmd)
                    }
                }
            } catch (ex: Exception) {
                if (running) Log.e("AirMouse", "UDP lỗi", ex)
            }
        }
    }

    private fun reply(msg: String) {
        val a = peerAddr ?: return
        val s = socket ?: return
        val port = peerPort
        val data = "${secret()}|$msg".toByteArray()
        thread(isDaemon = true) {
            try {
                s.send(DatagramPacket(data, data.size, a, port))
            } catch (_: Exception) {}
        }
    }

    // ---------- xử lý lệnh ----------
    private fun handle(cmd: String) {
        val t = cmd.split(' ')
        when (t[0]) {
            "PING" -> reply("PONG")
            "ENTER" -> {
                updateScreenSize()
                val ratio = (t.getOrNull(1)?.toFloatOrNull() ?: 0.5f).coerceIn(0f, 1f)
                x = 0f
                y = ratio * (screenH - 1)
                active = true
                leftDown = false
                AirState.remote = true
                setShown(true)
                syncCursor()
            }
            "LEAVE" -> dropRemote()
            "MOVE" -> if (active) {
                val dx = t.getOrNull(1)?.toFloatOrNull() ?: 0f
                val dy = t.getOrNull(2)?.toFloatOrNull() ?: 0f
                move(dx, dy)
            }
            "BTN" -> if (active) {
                val name = t.getOrNull(1) ?: ""
                val down = t.getOrNull(2) == "1"
                // Nhận thêm thông tin drag nếu có (từ bản update mới của script Python)
                val durMs = t.getOrNull(3)?.toLongOrNull()
                val distPx = t.getOrNull(4)?.toFloatOrNull()
                button(name, down, durMs, distPx)
            }
            "SCROLL" -> if (active) {
                scroll(t.getOrNull(1)?.toFloatOrNull() ?: 0f)
            }
            "HSCROLL" -> if (active) {
                hscroll(t.getOrNull(1)?.toFloatOrNull() ?: 0f)
            }
            "CLIP" -> {
                // Nhận text base64 từ laptop, giải mã và set vào Clipboard
                val b64 = t.getOrNull(1) ?: return
                try {
                    val bytes = Base64.decode(b64, Base64.DEFAULT)
                    val text = String(bytes, Charsets.UTF_8)
                    val cm = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                    cm.setPrimaryClip(ClipData.newPlainText("AirMouse Remote", text))
                    Toast.makeText(this, "📋 Đã copy: \"$text\"", Toast.LENGTH_SHORT).show()
                } catch (ex: Exception) {
                    Log.e("AirMouse", "Lỗi decode CLIP", ex)
                }
            }
            "NAV" -> {
                // Xử lý phím điều hướng hệ thống
                when (t.getOrNull(1)) {
                    "BACK" -> performGlobalAction(GLOBAL_ACTION_BACK)
                    "HOME" -> performGlobalAction(GLOBAL_ACTION_HOME)
                    "RECENTS" -> performGlobalAction(GLOBAL_ACTION_RECENTS)
                    "NOTIFICATIONS" -> performGlobalAction(GLOBAL_ACTION_NOTIFICATIONS)
                    "QUICK_SETTINGS" -> performGlobalAction(GLOBAL_ACTION_QUICK_SETTINGS)
                }
            }
            "KEY" -> {
                // Xử lý phím nhập liệu đặc biệt (Enter, Tab, Backspace)
                // Lưu ý: Accessibility Service không thể inject KeyEvent trực tiếp vào app khác 
                // trừ khi dùng dispatchGesture mô phỏng chạm nút ảo hoặc yêu cầu quyền đặc biệt.
                // Với Enter/Tab/Backspace, cách phổ biến nhất là giả lập hành vi tương đương 
                // nếu đang focus vào EditText (rất phức tạp để parse tree).
                // Giải pháp thay thế an toàn: Chỉ hỗ trợ NAV keys ở trên. 
                // Các KEY còn lại sẽ được log ra để debug hoặc bỏ qua.
                Log.d("AirMouse", "Nhận KEY ${t.getOrNull(1)} - Chưa hỗ trợ inject trực tiếp, vui lòng dùng Clipboard cho text.")
            }
        }
    }

    private fun move(dx: Float, dy: Float) {
        if (dx > 0f && x < 0f) x = 0f
        x = (x + dx).coerceAtMost(screenW - 1f)
        y = (y + dy).coerceIn(0f, screenH - 1f)
        // Tắt cơ chế tự động trả về khi chạm mép trái để tuân thủ cấu hình "--no-edge" từ PC
        // if (x < -EXIT_OVERSHOOT) {
        //     giveBack()
        //     return
        // }
        syncCursor()
    }

    private fun dropRemote() {
        active = false
        leftDown = false
        AirState.remote = false
        setShown(false)
    }

    private fun giveBack() {
        dropRemote()
        reply("RETURN ${(y / screenH).coerceIn(0f, 1f)}")
    }

    private fun button(name: String, down: Boolean, remoteDurMs: Long? = null, remoteDistPx: Float? = null) {
        when (name) {
            "L" -> {
                val cx = x.coerceAtLeast(0f)
                if (down) {
                    cursor?.pulse()
                    leftDown = true
                    downTime = SystemClock.uptimeMillis()
                    downX = cx
                    downY = y
                } else if (leftDown) {
                    leftDown = false
                    // Ưu tiên dùng thời lượng và quãng đường thực tế từ laptop gửi sang nếu có
                    val localHeld = SystemClock.uptimeMillis() - downTime
                    val finalDuration = remoteDurMs ?: localHeld
                    val finalDistance = remoteDistPx ?: hypot(cx - downX, y - downY)
                    
                    gesture(downX, downY, cx, y, finalDuration, finalDistance.toFloat())
                }
            }
            "R" -> if (down) {
                cursor?.pulse()
                performGlobalAction(GLOBAL_ACTION_BACK)
            }
            "M" -> if (down) {
                cursor?.pulse()
                performGlobalAction(GLOBAL_ACTION_HOME)
            }
        }
    }

    /**
     * Khi nhả chuột trái, phát lại thao tác: chạm (ngắn), nhấn giữ (giữ lâu, không di chuyển)
     * hoặc vuốt/kéo (có di chuyển).
     * @param remoteDistPx Quãng đường di chuyển thực tế trên laptop (pixel vật lý), dùng để tính velocity chính xác hơn.
     */
    private fun gesture(x1: Float, y1: Float, x2: Float, y2: Float, heldMs: Long, remoteDistPx: Float? = null) {
        val path = Path()
        path.moveTo(x1, y1)
        
        // Tính khoảng cách hiển thị trên màn hình Android
        val screenDist = hypot(x2 - x1, y2 - y1)
        
        // Nếu có dữ liệu từ laptop, dùng nó để quyết định xem là drag hay tap/long-press
        // Vì đôi khi di chuột ít nhưng vẫn muốn coi là drag (ví dụ kéo icon nhỏ)
        val effectiveDist = remoteDistPx ?: screenDist
        
        val duration: Long
        if (effectiveDist > DRAG_THRESHOLD || screenDist > DRAG_THRESHOLD) {
            path.lineTo(x2, y2)
            
            // Cải thiện cảm giác kéo: 
            // Thay vì chỉ dùng heldMs, ta tính vận tốc trung bình.
            // Người dùng thường kéo nhanh -> thời lượng ngắn. Kéo chậm -> thời lượng dài.
            // Tuy nhiên, nếu gửi quá nhiều gói tin MOVE liên tục trong lúc drag, 
            // việc chờ đến lúc RELEASE mới dispatch sẽ gây lag rõ rệt.
            
            // Giải pháp tốt nhất cho trải nghiệm "như tay trượt":
            // Chia nhỏ hành động drag thành các segment ngắn nếu tổng thời gian lớn,
            // HOẶC đơn giản là ép thời lượng về mức tối thiểu để hệ thống Android xử lý mượt mà 
            // dựa trên quỹ đạo đã được cập nhật qua lệnh MOVE trước đó.
            
            // Ở đây, ta giữ logic cũ nhưng nới lỏng ngưỡng dưới (min duration) 
            // để tránh bị cắt cụt khi người dùng kéo rất nhanh.
            duration = heldMs.coerceIn(80L, 3000L) 
        } else {
            duration = if (heldMs >= LONG_PRESS_MS) heldMs.coerceAtMost(4000L) else 50L
        }
        dispatch(path, duration)
    }

    private fun scroll(v: Float) {
        scrollAcc += v
        if (scrollScheduled) return
        scrollScheduled = true
        main.postDelayed({
            val amt = scrollAcc
            scrollAcc = 0f
            scrollScheduled = false
            if (amt == 0f || !active) return@postDelayed
            val density = resources.displayMetrics.density
            val dist = (amt * 120f * density).coerceIn(-screenH * 0.6f, screenH * 0.6f)
            val cy = y
            // v > 0: cuộn nội dung xuống -> ngón tay vuốt lên
            val startY = (cy + dist / 2).coerceIn(20f, screenH - 20f)
            val endY = (cy - dist / 2).coerceIn(20f, screenH - 20f)
            if (kotlin.math.abs(endY - startY) < 10f) return@postDelayed
            val path = Path()
            path.moveTo(x.coerceAtLeast(0f), startY)
            path.lineTo(x.coerceAtLeast(0f), endY)
            dispatch(path, 200L)
        }, 80L)
    }

    /**
     * Cuộn ngang (Horizontal Scroll) mô phỏng vuốt trái/phải.
     * @param v Giá trị từ laptop (> 0: cuộn sang phải/nội dung dịch trái; < 0: ngược lại).
     */
    private fun hscroll(v: Float) {
        val density = resources.displayMetrics.density
        // Hệ số chuyển đổi tương tự như dọc nhưng dùng chiều rộng màn hình làm giới hạn
        val dist = (v * 150f * density).coerceIn(-screenW * 0.4f, screenW * 0.4f)
        
        val cx = x.coerceAtLeast(0f)
        // Vuốt từ giữa ra ngoài theo hướng mong muốn
        // Nếu v > 0 (cuộn phải): Start ở bên phải tâm, End ở bên trái tâm (ngón tay đi từ phải qua trái)
        // Wait, standard gesture for "scroll right" (content moves left) is swipe LEFT.
        // Let's align with typical behavior: Positive value usually means "forward/right".
        // To see content to the right, you swipe finger to the LEFT.
        
        val startX = (cx + dist / 2).coerceIn(20f, screenW - 20f)
        val endX = (cx - dist / 2).coerceIn(20f, screenW - 20f)
        
        if (kotlin.math.abs(endX - startX) < 10f) return
        
        val path = Path()
        path.moveTo(startX, y)
        path.lineTo(endX, y)
        dispatch(path, 200L)
    }

    private fun dispatch(path: Path, durationMs: Long) {
        try {
            val g = GestureDescription.Builder()
                .addStroke(GestureDescription.StrokeDescription(path, 0L, durationMs))
                .build()
            dispatchGesture(g, null, null)
        } catch (ex: Exception) {
            Log.e("AirMouse", "dispatchGesture lỗi", ex)
        }
    }

    companion object {
        private const val LINK_LOST_MS = 15_000L
        private const val EXIT_OVERSHOOT = 60f   // kéo qua mép trái bao nhiêu px thì trả chuột về laptop
        private const val DRAG_THRESHOLD = 15f
        private const val LONG_PRESS_MS = 450L
    }
}
