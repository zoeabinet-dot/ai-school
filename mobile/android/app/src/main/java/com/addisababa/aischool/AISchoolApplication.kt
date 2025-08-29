package com.addisababa.aischool

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class AISchoolApplication : Application() {
    
    override fun onCreate() {
        super.onCreate()
        
        // Initialize any app-wide configurations here
        // TODO: Initialize crash reporting, analytics, etc.
    }
}