from firebase_admin import db, credentials
import firebase_admin
import json


creds = credentials.Certificate("/home/singh/Downloads/remede-service-account-key.json")
firebase_admin.initialize_app(creds, {'databaseURL': 'https://remede-b04d1.firebaseio.com/'})


def get_user_key(username):
    db_ref = db.reference("Patients/")
    db_snapshot = db_ref.get()
    keys = list(db_snapshot.keys())
    i = 0
    for user in db_snapshot:
        if db_snapshot[user]['name'] == username:
            user_dict = {'name': username, 'key': keys[i]}
            user_json = json.dumps(user_dict)
            file = open("assets/user_key.json", 'w')
            file.write(user_json)
            file.close()
            break
        i = i + 1

