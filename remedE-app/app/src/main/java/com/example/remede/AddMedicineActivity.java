package com.example.remede;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import static com.example.remede.Utils.INSTANCE;
import com.example.remede.model.Medicine;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Calendar;
import java.util.HashMap;

public class AddMedicineActivity extends AppCompatActivity {

    Button OpenCamera;
    Medicine push;
    DatabaseReference rootRef, demoRef;
    Button addTime;
    Button addMedicine;
    EditText e1,e2,e3,e4;
    String uniqueKey;
    String previousKey;
    private static final int SECOND_ACTIVITY_REQUEST_CODE = 0;

    HashMap<String, Boolean> times = new HashMap<String, Boolean>();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_medicine);

        OpenCamera = findViewById(R.id.OpenCameraButton);
        OpenCamera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent= new Intent(getApplicationContext(),OcrCameraActivity.class);
//              startActivity(intent);
                startActivityForResult(intent, SECOND_ACTIVITY_REQUEST_CODE);

            }
        });

        Intent intent = getIntent();
        previousKey=intent.getStringExtra("key");

        push = new Medicine();


        e1=findViewById(R.id.MedicineName);
        e2=findViewById(R.id.MedicineDose);
        e3=findViewById(R.id.RemainingStock);
        e4=findViewById(R.id.EnterTime);

        addTime=findViewById(R.id.AddTimeButton);
        addMedicine=findViewById(R.id.AddMedButton);
        addTime.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                //Toast to be added later as well
                Toast.makeText(AddMedicineActivity.this,e4.getText().toString()+" added",Toast.LENGTH_LONG).show();

                push.putTime(e4.getText().toString(),false);
                times.put(e4.getText().toString(),false);
                Log.w("prabhmap", String.valueOf(times));

                e4.setText("");

            }
        });
        rootRef = FirebaseDatabase.getInstance().getReference();
        uniqueKey = rootRef.child("Patients").child(previousKey).child("medicines").push().getKey();
        demoRef = rootRef.child("Patients").child(previousKey).child("medicines").child(uniqueKey);
        insert_data();


    }



    public void insert_data(){

        addMedicine.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.O)
            @Override
            public void onClick(View v) {

                //show toast (to be added)
                Toast.makeText(AddMedicineActivity.this,e1.getText().toString()+" has been added!",Toast.LENGTH_LONG).show();

                push.setName(e1.getText().toString());
                push.setDose(Integer.parseInt(e2.getText().toString()));
                push.setRemaining_stock(Integer.parseInt(e3.getText().toString()));
                demoRef.setValue(push);

//                Utils obj=null;

                String CurrentTime="04:20";

                if(times!=null)
                    CurrentTime=INSTANCE.getNextDose(times);
                Log.w("prabhtime",CurrentTime);
                String Hour=CurrentTime.substring(0,2);
                String Minutes=CurrentTime.substring(3);

                Calendar calendar = Calendar.getInstance();

                calendar.set(Calendar.HOUR_OF_DAY,Integer.parseInt(Hour));
                calendar.set(Calendar.MINUTE,Integer.parseInt(Minutes));
                calendar.set(Calendar.SECOND,15);
                Intent intent2 = new Intent(getApplicationContext(), Notification_receiver.class);
                intent2.putExtra("key",e1.getText().toString());
                intent2.putExtra("user_key",previousKey);
                Log.w("prabhkeyAMA",previousKey);

                PendingIntent pendingIntent = PendingIntent.getBroadcast(getApplicationContext(),100,intent2,PendingIntent.FLAG_UPDATE_CURRENT );

                AlarmManager alarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
                alarmManager.setRepeating(AlarmManager.RTC_WAKEUP,calendar.getTimeInMillis(),AlarmManager.INTERVAL_DAY,pendingIntent);

                Intent intent= new Intent(getApplicationContext(),UserAccountActivity.class);
                finish();

            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        // Check that it is the SecondActivity with an OK result
        if (requestCode == SECOND_ACTIVITY_REQUEST_CODE) {
            if (resultCode == RESULT_OK) {
                // Get String data from Intent
                String returnString = data.getStringExtra("key");


                // Set text view with string
                e1.setText(returnString);
            }
        }
    }
}