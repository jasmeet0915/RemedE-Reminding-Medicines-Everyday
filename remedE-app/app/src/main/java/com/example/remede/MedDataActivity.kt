package com.example.remede

import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.annotation.RequiresApi
import com.example.remede.model.Medicine
import com.example.remede.model.User
import com.google.firebase.database.*
import kotlinx.android.synthetic.main.activity_med_data.*
import kotlinx.android.synthetic.main.activity_user_acc.*
import java.util.*


class MedDataActivity : AppCompatActivity() {

    private lateinit var dataReference: DatabaseReference
    private lateinit var userReference: DatabaseReference
    private lateinit var medicineReference: DatabaseReference

    private var medicineListener: ValueEventListener? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_med_data)

        val bundle: Bundle? = intent.extras
        var medName = bundle?.getString("medicineName")
        var userKey = bundle?.getString("userKey")
        var medKey = bundle?.getString("medicineKey")
        val medData = Utils.getMedDetails(baseContext, medName)

        val dataReference = FirebaseDatabase.getInstance().getReference("Patients")
        val userReference = dataReference.child(userKey.toString())
        var medicineReference = userReference.child("medicines").child(medKey.toString())

        MedName.text = medName
        genName.text = medData.generic_name
        description.text = medData.description
        sideEffects.text = medData.side_effects

        // add ChildEventListener to the medicineListener
        val medicineListener = object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {

                if (dataSnapshot.exists()) {
                    val med = dataSnapshot.getValue(Medicine::class.java)
                    dose.text = med?.dose.toString()
                    stock.text = med?.remaining_stock.toString()
                    medTimes.text = med?.times?.keys.toString()
                }
            }

            override fun onCancelled(error: DatabaseError) {
                Log.i("MedDataActivity", "Failed to Read Message!!")
            }
        }

        medicineReference.addValueEventListener(medicineListener)
        this.medicineListener = medicineListener

    }
}