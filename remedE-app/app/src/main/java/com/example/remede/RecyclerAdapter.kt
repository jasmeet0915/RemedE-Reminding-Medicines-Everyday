package com.example.remede
import android.content.Intent
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.Switch
import android.widget.TextView
import androidx.appcompat.view.menu.ActionMenuItemView
import androidx.recyclerview.widget.RecyclerView
import com.example.remede.model.User
import com.google.firebase.database.*
import kotlinx.android.synthetic.main.activity_user_acc.*

class RecyclerAdapter(private val medNames: List<String>,
                      private val nextDose: List<String>,
                      private val icons: List<Int>,
                      private val medKeys: List<String>,
                      private val key: String): RecyclerView.Adapter<RecyclerAdapter.ViewHolder>(){

    class ViewHolder(itemView: View, medicineNames: List<String>, userKey: String, medicineKeys: List<String>) : RecyclerView.ViewHolder(itemView){
        val itemName: TextView = itemView.findViewById(R.id.medName)
        val itemNextDose: TextView = itemView.findViewById(R.id.nextDose)
        val pillImage: ImageView = itemView.findViewById(R.id.pillIcon)
        val takenSwitch: Switch = itemView.findViewById(R.id.takenSwitch)

        private var dataReference: DatabaseReference = FirebaseDatabase.getInstance().getReference("Patients")
        private var userReference: DatabaseReference = dataReference.child(userKey.toString())
        private var medicineReference: DatabaseReference = userReference.child("medicines")

        private var userListener: ValueEventListener? = null
        private var medicineListener: ValueEventListener? = null


        init {
            itemView.setOnClickListener{v: View ->
                val intent = Intent(v.context, MedDataActivity::class.java)
                val position = adapterPosition
                intent.putExtra("medicineName", medicineNames[position])
                intent.putExtra("medicineKey", medicineKeys[position])
                intent.putExtra("userKey", userKey)
                v.context.startActivity(intent)
            }
        }
        init{
            takenSwitch.setOnCheckedChangeListener{ _ , isChecked ->
                if (isChecked) {
                    Log.i("RecyclerAdapter", "${medicineNames[position]} taken")
                    var hour: String = itemNextDose.text.toString().split(':')[1].substring(1)
                    var minute: String = itemNextDose.text.toString().split(':')[2]
                    var time = hour + ":" + minute
                    medicineReference.child(medicineKeys[position] + "/times/" + time)
                        .setValue(true)
                    }
                }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val viewLayout = LayoutInflater.from(parent.context).inflate(R.layout.med_layout, parent, false)
        return ViewHolder(viewLayout, medNames, key, medKeys)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.itemName.text = medNames[position]
        holder.itemNextDose.text = nextDose[position]
        holder.pillImage.setImageResource(icons[position])
    }

    override fun getItemCount(): Int {
        return medNames.size
    }
}