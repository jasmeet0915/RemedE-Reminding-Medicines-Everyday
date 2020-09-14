package com.example.remede

import android.content.Context
import android.os.Build
import androidx.annotation.RequiresApi
//import com.example.remede.model.MedData
//import com.google.gson.Gson
//import com.google.gson.JsonParser
//import com.google.gson.reflect.TypeToken
import java.time.LocalTime

object Utils {
    @RequiresApi(Build.VERSION_CODES.O)
    fun getNextDose(times: Map<String, Boolean>): String {
        val currTime = LocalTime.now()
        var nextDoseKey: String = ""
        for ((key, value) in times) {
            val keyParts = key.split(":")
            val doseTime = LocalTime.of(keyParts[0].toInt(), keyParts[1].toInt(), 0)
            if (doseTime > currTime && !value) {
                nextDoseKey = key
                break
            }
        }
        return nextDoseKey
    }

}




