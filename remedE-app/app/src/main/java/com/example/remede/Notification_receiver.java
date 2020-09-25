package com.example.remede;

import android.app.NotificationChannel;
import android.app.NotificationManager;

import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.util.Log;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

public class Notification_receiver extends BroadcastReceiver {


    @Override
    public void onReceive(Context context, Intent intent) {


        Log.w("prabhnotif", "Chal rha hai kya?");

        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel =
                    new NotificationChannel("MyNotifications","MyNotifications", NotificationManager.IMPORTANCE_DEFAULT);
            NotificationManager notificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
            notificationManager.createNotificationChannel(channel);
        }


        String Medicine_Name=intent.getStringExtra("key");
        String uniqueKey=intent.getStringExtra("user_key");
        if(uniqueKey=="")
            uniqueKey="-MI44N384kav1QggJmk1";
        Log.w("prabhkeyNR",uniqueKey);

        Log.w("Notification",Medicine_Name);



        Intent repeating_intent = new Intent(context, UserAccountActivity.class);

        repeating_intent.putExtra("key",uniqueKey);
        repeating_intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

        PendingIntent pendingIntent = PendingIntent.getActivity(context,100,repeating_intent,PendingIntent.FLAG_UPDATE_CURRENT);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, "MyNotifications")
                .setContentIntent(pendingIntent)
                .setSmallIcon(android.R.drawable.arrow_up_float)
                .setContentTitle("Time to Take your Medicine")
                .setContentText(Medicine_Name)
                .setAutoCancel(true);

        NotificationManagerCompat manager = NotificationManagerCompat.from(context);
        manager.notify(100,builder.build());

    }
}
