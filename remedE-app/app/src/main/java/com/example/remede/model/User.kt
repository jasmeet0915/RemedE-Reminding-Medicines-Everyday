package com.example.remede.model

data class User(
    var name: String = "",
    var isPatient: Boolean = false,
    var age: Int = 0,
    var contact: Long = 0,
    var address: String = "",
    var weight: Int = 0,
    var email: String = "",
    var password: String=""
){
    fun getIsPatient(): Boolean? {
        return isPatient
    }

}