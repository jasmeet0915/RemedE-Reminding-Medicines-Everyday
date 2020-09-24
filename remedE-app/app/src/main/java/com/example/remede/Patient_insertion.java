package com.example.remede;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.example.remede.model.User;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.Calendar;


public class Patient_insertion extends AppCompatActivity {


    DatabaseReference rootRef, demoRef;
    Button insertion;
    User push;        //object to be pushed to firebase
    EditText e1,e2,e3,e4,e5,e6,e7;
    String uniqueKey;
    SharedPreferences sharedPreferences;
    private static final String SHARED_PREF_NAME = "mypref";
    private static final String KEY_NAME = "name";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_patient_insertion);
        sharedPreferences = getSharedPreferences(SHARED_PREF_NAME,MODE_PRIVATE);
        uniqueKey = sharedPreferences.getString(KEY_NAME,null);
        if(uniqueKey!=null)
        {
            Intent intent= new Intent(getApplicationContext(),UserAccountActivity.class);
            intent.putExtra("key", uniqueKey);
            startActivity(intent);
        }
        else
            {
            push = new User();
            rootRef = FirebaseDatabase.getInstance().getReference();
            uniqueKey = rootRef.child("Patients").push().getKey();
            demoRef = rootRef.child("Patients").child(uniqueKey);
            insertion = findViewById(R.id.create_button);
            e1=findViewById(R.id.name_text);
            e2=findViewById(R.id.Age_text);
            e3=findViewById(R.id.Weight_text);
            e4=findViewById(R.id.Phone_text);
            e5=findViewById(R.id.Email_text);
            e6=findViewById(R.id.Address_text);
            e7=findViewById(R.id.Password_text);
            insert_data();
      }
    }

    public void set_data()
    {
        push.setName(e1.getText().toString());
        push.setEmail(e5.getText().toString());
        push.setAddress(e6.getText().toString());
        push.setAge(Integer.parseInt(e2.getText().toString()));
        push.setWeight(Integer.parseInt(e3.getText().toString()));
        push.setContact(Long.parseLong(e4.getText().toString()));
        push.setPassword(e7.getText().toString());
        push.setPatient(true);
    }
    public void insert_data(){

        insertion.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                set_data();
                demoRef.setValue(push);
                SharedPreferences.Editor editor = sharedPreferences.edit();
                editor.putString(KEY_NAME,uniqueKey);
                editor.apply();
                Intent intent= new Intent(getApplicationContext(),UserAccountActivity.class);
                intent.putExtra("key", uniqueKey);
                startActivity(intent);
            }
        });
    }

}