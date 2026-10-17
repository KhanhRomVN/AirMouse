package com.example.airmouse

import android.animation.ValueAnimator
import android.content.Context
import android.content.res.ColorStateList
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.LinearGradient
import android.graphics.Paint
import android.graphics.Path
import android.graphics.RectF
import android.graphics.Shader
import android.graphics.Typeface
import android.graphics.drawable.Drawable
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.RippleDrawable
import android.util.TypedValue
import android.view.Gravity
import android.view.View
import android.view.animation.LinearInterpolator
import android.widget.LinearLayout
import android.widget.TextView

/** Bảng màu dùng chung (khớp với giao diện trên laptop). */
object Palette {
    val BG = 0xFF0B0F1A.toInt()
    val SURFACE = 0xFF131A2A.toInt()
    val SURFACE2 = 0xFF1A2236.toInt()
    val SURFACE3 = 0xFF222C45.toInt()
    val BORDER = 0xFF242E49.toInt()
    val TEXT = 0xFFE8ECF8.toInt()
    val MUTED = 0xFF8A94B0.toInt()
    val FAINT = 0xFF566080.toInt()
    val ACCENT = 0xFF6C7BFF.toInt()
    val ACCENT_SOFT = 0x266C7BFF.toInt()
    val VIOLET = 0xFF8B6CFF.toInt()
    val CYAN = 0xFF22D3EE.toInt()
    val OK = 0xFF34D399.toInt()
    val WARN = 0xFFFBBF24.toInt()
    val ERR = 0xFFF87171.toInt()
}

fun Context.dp(v: Number): Int = (v.toFloat() * resources.displayMetrics.density + 0.5f).toInt()
fun Context.dpf(v: Number): Float = v.toFloat() * resources.displayMetrics.density

fun Context.shape(fill: Int, radiusDp: Float, strokeColor: Int = 0, strokeDp: Float = 0f): GradientDrawable =
    GradientDrawable().apply {
        setColor(fill)
        cornerRadius = dpf(radiusDp)
        if (strokeDp > 0f) setStroke(maxOf(1, dp(strokeDp)), strokeColor)
    }

fun Context.gradient(c1: Int, c2: Int, radiusDp: Float): GradientDrawable =
    GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT, intArrayOf(c1, c2)).apply {
        cornerRadius = dpf(radiusDp)
    }

fun Context.ripple(content: Drawable, radiusDp: Float, color: Int = 0x33FFFFFF): RippleDrawable =
    RippleDrawable(ColorStateList.valueOf(color), content, shape(Color.WHITE, radiusDp))

fun Context.label(
    s: CharSequence,
    sizeSp: Float,
    color: Int,
    bold: Boolean = false,
    mono: Boolean = false,
): TextView = TextView(this).apply {
    text = s
    setTextSize(TypedValue.COMPLEX_UNIT_SP, sizeSp)
    setTextColor(color)
    typeface = when {
        mono -> Typeface.MONOSPACE
        bold -> Typeface.create("sans-serif-medium", Typeface.NORMAL)
        else -> Typeface.create("sans-serif", Typeface.NORMAL)
    }
    includeFontPadding = false
}

fun Context.caption(s: String): TextView = label(s, 11f, Palette.FAINT, bold = true).apply {
    letterSpacing = 0.12f
}

fun lp(w: Int, h: Int, l: Int = 0, t: Int = 0, r: Int = 0, b: Int = 0): LinearLayout.LayoutParams =
    LinearLayout.LayoutParams(w, h).apply { setMargins(l, t, r, b) }

fun Context.card(): LinearLayout = LinearLayout(this).apply {
    orientation = LinearLayout.VERTICAL
    background = shape(Palette.SURFACE, 20f, Palette.BORDER, 1f)
    setPadding(dp(18), dp(16), dp(18), dp(18))
}

enum class BtnKind { PRIMARY, SECONDARY, DANGER }

fun Context.styleButton(v: TextView, kind: BtnKind) {
    val r = 14f
    val bg: Drawable = when (kind) {
        BtnKind.PRIMARY -> gradient(Palette.ACCENT, Palette.VIOLET, r)
        BtnKind.SECONDARY -> shape(Palette.SURFACE2, r, Palette.BORDER, 1f)
        BtnKind.DANGER -> shape(0xFF2A1822.toInt(), r, 0xFF5A2A38.toInt(), 1f)
    }
    v.background = ripple(bg, r)
    v.setTextColor(
        when (kind) {
            BtnKind.PRIMARY -> Color.WHITE
            BtnKind.SECONDARY -> Palette.TEXT
            BtnKind.DANGER -> Palette.ERR
        }
    )
}

fun Context.button(s: String, kind: BtnKind, onClick: () -> Unit): TextView =
    label(s, 15f, Color.WHITE, bold = true).apply {
        gravity = Gravity.CENTER
        minHeight = dp(52)
        setPadding(dp(20), dp(14), dp(20), dp(14))
        isClickable = true
        isFocusable = true
        styleButton(this, kind)
        setOnClickListener { onClick() }
    }

/** Chấm trạng thái, có vòng lan toả khi `pulse` bật. */
class PulseDot(context: Context) : View(context) {
    private var color = Palette.MUTED
    private var pulse = false
    private var t = 0f
    private val core = Paint(Paint.ANTI_ALIAS_FLAG)
    private val halo = Paint(Paint.ANTI_ALIAS_FLAG)
    private val ring = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeWidth = context.dpf(2)
    }
    private val anim = ValueAnimator.ofFloat(0f, 1f).apply {
        duration = 1600
        repeatCount = ValueAnimator.INFINITE
        interpolator = LinearInterpolator()
        addUpdateListener {
            t = it.animatedValue as Float
            invalidate()
        }
    }

    fun set(color: Int, pulse: Boolean) {
        this.color = color
        this.pulse = pulse
        updateAnim()
        invalidate()
    }

    private fun updateAnim() {
        if (pulse && isAttachedToWindow) {
            if (!anim.isStarted) anim.start()
        } else {
            anim.cancel()
            t = 0f
        }
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        updateAnim()
    }

    override fun onDetachedFromWindow() {
        anim.cancel()
        super.onDetachedFromWindow()
    }

    override fun onDraw(canvas: Canvas) {
        val cx = width / 2f
        val cy = height / 2f
        val d = resources.displayMetrics.density
        halo.color = color
        halo.alpha = 36
        canvas.drawCircle(cx, cy, 18f * d, halo)
        if (pulse) {
            ring.color = color
            ring.alpha = ((1f - t) * 200).toInt()
            canvas.drawCircle(cx, cy, (8f + t * 14f) * d, ring)
        }
        core.color = color
        canvas.drawCircle(cx, cy, 8f * d, core)
    }
}

/** Logo ứng dụng: ô bo góc chuyển màu + con trỏ chuột. */
class LogoView(context: Context) : View(context) {
    private val bg = Paint(Paint.ANTI_ALIAS_FLAG)
    private val arrowPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { color = Color.WHITE }
    private val path = Path()

    override fun onDraw(canvas: Canvas) {
        val w = width.toFloat()
        val h = height.toFloat()
        bg.shader = LinearGradient(0f, 0f, w, h, Palette.ACCENT, Palette.VIOLET, Shader.TileMode.CLAMP)
        canvas.drawRoundRect(RectF(0f, 0f, w, h), w * 0.28f, w * 0.28f, bg)
        val s = w / 46f
        path.reset()
        path.moveTo(15f * s, 10f * s)
        path.lineTo(15f * s, 34f * s)
        path.lineTo(21f * s, 28f * s)
        path.lineTo(26f * s, 38f * s)
        path.lineTo(30f * s, 36f * s)
        path.lineTo(25f * s, 27f * s)
        path.lineTo(33f * s, 27f * s)
        path.close()
        canvas.drawPath(path, arrowPaint)
    }
}
