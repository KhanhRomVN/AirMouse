package com.example.airmouse

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.view.View

/** View trong suốt toàn màn hình, chỉ vẽ một con trỏ chuột hình mũi tên. */
class CursorView(context: Context) : View(context) {
    var cx = 0f
    var cy = 0f
    var shown = false

    private val fill = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.WHITE
        style = Paint.Style.FILL
    }
    private val stroke = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.BLACK
        style = Paint.Style.STROKE
        strokeWidth = 3f
    }
    private val arrow = Path()

    init {
        val s = resources.displayMetrics.density
        arrow.moveTo(0f, 0f)
        arrow.lineTo(0f, 20f * s)
        arrow.lineTo(5f * s, 15f * s)
        arrow.lineTo(9f * s, 23f * s)
        arrow.lineTo(12f * s, 21.5f * s)
        arrow.lineTo(8f * s, 14f * s)
        arrow.lineTo(15f * s, 14f * s)
        arrow.close()
    }

    override fun onDraw(canvas: Canvas) {
        if (!shown) return
        canvas.save()
        canvas.translate(cx, cy)
        canvas.drawPath(arrow, fill)
        canvas.drawPath(arrow, stroke)
        canvas.restore()
    }
}
