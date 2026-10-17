plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.airmouse"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.airmouse"
        minSdk = 26
        targetSdk = 34
        versionCode = 2
        versionName = "2.0"
    }

    // Khoá ký release: dùng airmouse-debug.keystore (đặt cạnh thư mục app) nếu có,
    // nếu không có thì tự dùng khoá debug để vẫn build được.
    val releaseKeystore = file("../airmouse-debug.keystore")
    signingConfigs {
        if (releaseKeystore.exists()) {
            create("release") {
                storeFile = releaseKeystore
                storePassword = "password"
                keyAlias = "airmouse"
                keyPassword = "password"
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.findByName("release") ?: signingConfigs.getByName("debug")
        }
    }

    applicationVariants.all {
        outputs.all {
            val outputImpl = this as com.android.build.gradle.internal.api.BaseVariantOutputImpl
            if (name.contains("release")) {
                outputImpl.outputFileName = "AirMouse.apk"
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}
