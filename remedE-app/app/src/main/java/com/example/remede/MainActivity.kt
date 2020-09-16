package com.example.remede

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {

    val button
        get() = findViewById<Button>(R.id.patient_button)
    val button2
        get() = findViewById<Button>(R.id.subscriber_button)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

//        btnLaunchUserAccountActivity.setOnClickListener(){
////            val intent = Intent(this, UserAccountActivity::class.java)
////            startActivity(intent)
////        }
        button.setOnClickListener{

            val intent = Intent(this, Patient_insertion::class.java)
            startActivity(intent)

        }
        button2.setOnClickListener{

            val intent = Intent(this, SubscriberInfo::class.java)
            startActivity(intent)

        }
    }





}
