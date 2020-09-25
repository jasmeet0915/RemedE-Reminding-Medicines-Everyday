package com.example.remede

import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.widget.Button
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.remede.model.Medicine
import com.example.remede.model.User
import com.google.firebase.database.*
import kotlinx.android.synthetic.main.activity_user_acc.*
import java.util.*


class UserAccountActivity : AppCompatActivity() {

    private lateinit var dataReference: DatabaseReference
    private lateinit var userReference: DatabaseReference
    private lateinit var medicineReference: DatabaseReference

    private var userListener: ValueEventListener? = null
    private var medicineListener: ChildEventListener? = null

    private var medNames = mutableListOf<String>()
    private var nextDose = mutableListOf<String>()
    private var iconsList = mutableListOf<Int>()
    private var medKeys = mutableListOf<String>()

    val button
        get() = findViewById<Button>(R.id.addMedButton)
    val logout
        get() = findViewById<Button>(R.id.logout_button)

    companion object {
        private const val TAG: String = "UserAccountActivity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_user_acc)

        // get user key from previous activity
        val bundle: Bundle? = intent.extras
        var uniqueKey = bundle?.getString("key")
        Log.w("prabhkeyUAA", uniqueKey!!.toString())

        //initialize dataReference, userReference, medicineReference
        dataReference = FirebaseDatabase.getInstance().getReference("Patients")
        userReference = dataReference.child(uniqueKey.toString())
        medicineReference = userReference.child("medicines")

        medRecyclerView.layoutManager = LinearLayoutManager(this)

        logout.setOnClickListener{

            val sharedPreference =  getSharedPreferences("mypref", Context.MODE_PRIVATE)
            var editor = sharedPreference.edit()
            editor.clear()
            editor.commit()
            finish();
        }
        button.setOnClickListener{

            val intent = Intent(this, AddMedicineActivity::class.java)
            intent.putExtra("key", uniqueKey)

            startActivity(intent)

        }


        //add value event listener to listen for changes in database
        val userListener = object : ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {

                if (dataSnapshot.exists()) {
                    val user = dataSnapshot.getValue(User::class.java)

                    userName.text = user?.name
                    userAge.text = user?.age.toString()
                    userWeight.text = user?.weight.toString()
                    userContact.text = user?.contact.toString()
                    userEmail.text = user?.email
                    userAddress.text = user?.address

                }
            }

            override fun onCancelled(error: DatabaseError) {
                Log.i(TAG, "Failed to Read Message!!")
            }
        }

        // add the userListener addValueEventListener created above to userReference
        userReference.addValueEventListener(userListener)
        this.userListener = userListener

        // add ChildEventListener to the medicineListener
        val medicineListener = object : ChildEventListener {
            @RequiresApi(Build.VERSION_CODES.O)
            override fun onChildAdded(snapshot: DataSnapshot, previousChildName: String?) {
                Log.i(TAG, "onChildAdded: function")
                if (snapshot.exists()) {
                    val med = snapshot.getValue(Medicine::class.java)
                    medNames.add(med?.name.toString())
                    nextDose.add("Upcoming dose at: " + Utils.getNextDose(med!!.times))
                    iconsList = Collections.nCopies(medNames.size, R.mipmap.ic_pill)
                    medKeys.add(snapshot.key.toString())
//                    nextDose=Collections.nCopies(medNames.size,"jassu")
                    Log.i(TAG, "${medNames}")
                    Log.i(TAG, "${nextDose}")
                    Log.i(TAG, "${medKeys}")
                    medRecyclerView.adapter = RecyclerAdapter(
                        medNames,
                        nextDose,
                        iconsList,
                        medKeys,
                        uniqueKey.toString()
                    )
                }
            }

            override fun onChildChanged(snapshot: DataSnapshot, previousChildName: String?) {
                TODO("Not yet implemented")
            }

            override fun onChildRemoved(snapshot: DataSnapshot) {
                TODO("Not yet implemented")
            }

            override fun onChildMoved(snapshot: DataSnapshot, previousChildName: String?) {
                TODO("Not yet implemented")
            }

            override fun onCancelled(error: DatabaseError) {
                TODO("Not yet implemented")
            }
        }

        medicineReference.addChildEventListener(medicineListener)
        this.medicineListener = medicineListener

        Log.i(TAG, "onCreate() function")
    }

    override fun onStart() {
        super.onStart()
        Log.i(TAG, "onStart() function")
    }

    override fun onStop() {
        super.onStop()

        // Remove user value event listener
        userListener?.let {
            userReference.removeEventListener(it)
        }

        medicineListener?.let {
            medicineReference.removeEventListener(it)
        }
    }

}

