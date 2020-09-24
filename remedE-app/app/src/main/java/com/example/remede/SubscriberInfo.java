package com.example.remede;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.remede.model.User;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class SubscriberInfo extends AppCompatActivity {

    Button Entering;
    //DatabaseReference rootRef, demoRef;
    DatabaseReference databaseReference;
    String uniqueKey;
    //User push;
    SharedPreferences sharedPreferences;
    private static final String SHARED_PREF_NAME = "mypref";
    private static final String KEY_NAME = "name";
    EditText e1, e2;
    String input_name = "", input_password = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_subscriber_info);

        //sharedPreferences = getSharedPreferences(SHARED_PREF_NAME,MODE_PRIVATE);
        //uniqueKey = sharedPreferences.getString(KEY_NAME,null);
        if (uniqueKey != null) {
            Intent intent = new Intent(getApplicationContext(), UserAccountActivity.class);
            intent.putExtra("key", uniqueKey);
            startActivity(intent);
        }
        else
            {
            //push = new User();
            databaseReference = FirebaseDatabase.getInstance().getReference();
            Entering = findViewById(R.id.UserInformation);
            Entering.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

            Entering = findViewById(R.id.UserInformation);
            e1 = findViewById(R.id.editTextTextPersonName2);
            e2 = findViewById(R.id.editTextTextPassword);
            input_name = e1.getText().toString();
            input_password = e2.getText().toString();
            databaseReference.child("Patients")
                    .orderByChild("name")
                    .equalTo(input_name)
                    .addListenerForSingleValueEvent(new ValueEventListener() {
                        @Override
                        public void onDataChange(DataSnapshot dataSnapshot) {
                            uniqueKey="";

                            for (DataSnapshot childSnapshot : dataSnapshot.getChildren()) {
                                String names = childSnapshot.getKey();
                                String stored_data = (String) childSnapshot.child("name").getValue();
                                String stored_data1 = (String) childSnapshot.child("password").getValue();
                                if (stored_data.equals(input_name) && !stored_data.equals("") && stored_data1.equals(input_password) && !stored_data1.equals("")) {
                                    Log.d("ghgh", names);
                                    Log.d("ghg",input_password);
                                    uniqueKey=names;
                                    break;
                                }
                            }
                            if(uniqueKey!="") {
                                Intent intent = new Intent(getApplicationContext(), UserInfo.class);
                                intent.putExtra("key", uniqueKey);
                                startActivity(intent);
                            }
                            else
                            {
                                //show toast;
                                Toast.makeText(SubscriberInfo.this,"No match found \nTry Again!!",Toast.LENGTH_LONG).show();
                            }

                        }
                        @Override
                        public void onCancelled(@NonNull DatabaseError error) {
                            Log.d("check","the input cannot be read");
                        }

                    });
                }
            });
        }
    }
}