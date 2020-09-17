package com.example.remede

import android.content.Context
import android.os.Build
import androidx.annotation.RequiresApi
import com.example.remede.model.MedData
import com.google.gson.Gson
import com.google.gson.JsonParser
import com.google.gson.reflect.TypeToken
import java.time.LocalTime

object Utils {
    private fun getJsonFromAsset(context: Context, fileName: String): String{
        return context.assets.open(fileName).bufferedReader().use { it.readText() }
    }

    fun getMedNames(context: Context): Set<String>{
        val json = getJsonFromAsset(context, "med_data.json")
        return JsonParser().parse(json).asJsonObject.keySet()
    }

    fun getMedDetails(context: Context, medName: String?): MedData {
        val json = getJsonFromAsset(context, "med_data.json")
        val medJson = JsonParser().parse(json).asJsonObject.get(medName)
        val gson = Gson()
        val medDataType = object : TypeToken<MedData>() {}.type
        return gson.fromJson(medJson, medDataType)
    }

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




