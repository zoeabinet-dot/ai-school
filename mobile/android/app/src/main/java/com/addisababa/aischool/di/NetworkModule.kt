package com.addisababa.aischool.di

import com.addisababa.aischool.data.network.ApiService
import com.addisababa.aischool.data.network.MockApiService
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    
    @Provides
    @Singleton
    fun provideApiService(): ApiService {
        // For now, return mock service
        // TODO: Replace with real Retrofit implementation
        return MockApiService()
    }
}