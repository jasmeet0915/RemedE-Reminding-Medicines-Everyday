package com.example.remede.model

data class
Medicine(
    var name: String = "",
    var dose: Int = 0,
    var remaining_stock: Int = 0,
    //var times: Map<String, Boolean> = mapOf<String, Boolean>()
    var times: MutableMap<String, Boolean> = mutableMapOf<String, Boolean>()
)

{
    fun putTime(key: String, value: Boolean): Unit{
        times.put(key, value)
    }

}