package com.example.airmouse

import android.animation.Animator
import android.animation.AnimatorListenerAdapter
import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.view.View
import android.view.animation.DecelerateInterpolator

/** View trong suốt toàn màn hình, vẽ con trỏ mũi tên có bóng đổ và vòng gợn khi chạm. */
class CursorView(context: Context) : View(context) {
    var cx = 0f
    var cy = 0f
    var shown = false

    private val d = resources.displayMetrics.density

    private val fill = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.WHITE
        style = Paint.Style.FILL
    }
    private val stroke = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = 0xFF0F172A.toInt()
        style = Paint.Style.STROKE
        strokeWidth = 1.6f * d
        strokeJoin = Paint.Join.ROUND
    }
    private val shadow = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = 0x55000000
        style = Paint.Style.FILL
    }
    private val ring = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = 2.5f * d
    }
    private val dot = Paint(Paint.ANTI_ALIAS_FLAG).apply { style = Paint.Style.FILL }
    private val arrow = Path()

    private var ringT = -1f
    private var anim: ValueAnimator? = null

    init {
        val s = d * 1.1f
        arrow.moveTo(0f, 0f)
        arrow.lineTo(0f, 20f * s)
        arrow.lineTo(5f * s, 15f * s)
        arrow.lineTo(9f * s, 23f * s)
        arrow.lineTo(12f * s, 21.5f * s)
        arrow.lineTo(8f * s, 14f * s)
        arrow.lineTo(15f * s, 14f * s)
        arrow.close()
    }

    /** Hiệu ứng gợn sóng tại điểm con trỏ mỗi khi bấm chuột. */
    fun pulse() {
        anim?.cancel()
        anim = ValueAnimator.ofFloat(0f, 1f).apply {
            duration = 380
            interpolator = DecelerateInterpolator()
            addUpdateListener {
                ringT = it.animatedValue as Float
                invalidate()
            }
            addListener(object : AnimatorListenerAdapter() {
                override fun onAnimationEnd(animation: Animator) {
                    ringT = -1f
                    invalidate()
                }
            })
            start()
        }
    }

    override fun onDraw(canvas: Canvas) {
        if (!shown) return
        if (ringT >= 0f) {
            val a = ((1f - ringT) * 200).toInt()
            ring.color = Palette.CYAN
            ring.alpha = a
            dot.color = Palette.CYAN
            dot.alpha = (a * 0.25f).toInt()
            val r = (6f + ringT * 26f) * d
            canvas.drawCircle(cx, cy, r, dot)
            canvas.drawCircle(cx, cy, r, ring)
        }
        canvas.save()
        canvas.translate(cx + 1.5f * d, cy + 2f * d)
        canvas.drawPath(arrow, shadow)
        canvas.restore()
        canvas.save()
        canvas.translate(cx, cy)
        canvas.drawPath(arrow, fill)
        canvas.drawPath(arrow, stroke)
        canvas.restore()
    }
}
