package com.example.airmouse

import android.os.SystemClock

/** Trạng thái chia sẻ giữa MouseService (ghi) và MainActivity (đọc để hiển thị). */
object AirState {
    private const val LINK_TIMEOUT_MS = 12_000L

    @Volatile var serviceRunning = false
    @Volatile var remote = false
    @Volatile var peer: String? = null
    @Volatile var lastSeen = 0L

    fun touch(from: String?) {
        lastSeen = SystemClock.elapsedRealtime()
        if (from != null) peer = from
    }

    fun connected(): Boolean =
        serviceRunning && lastSeen != 0L && SystemClock.elapsedRealtime() - lastSeen < LINK_TIMEOUT_MS

    fun reset() {
        remote = false
        peer = null
        lastSeen = 0L
    }
}
