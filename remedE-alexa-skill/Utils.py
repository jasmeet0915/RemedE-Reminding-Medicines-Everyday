from firebase_admin import db, credentials
import firebase_admin
import json
from datetime import datetime, time


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


def get_med_json_data(medicine_name):
    with open('assets/med_data.json', 'r') as f:
        data = json.load(f)
    f.close()
    return data[medicine_name]


def get_user_medicine_data(med_name):
    with open("assets/user_key.json") as file:
        data = json.load(file)

    print(data['key'])
    db_ref = db.reference("Patients/" + str(data['key']))
    snapshot = db_ref.get()
    print(snapshot)
    for med in snapshot['medicines']:
        print(snapshot['medicines'][med]['name'])
        if snapshot['medicines'][med]['name'] == med_name:
            return snapshot['medicines'][med]


def get_next_dose(med_name):
    med_data_dict = get_user_medicine_data(med_name)
    print(med_data_dict)
    times = med_data_dict['times']
    print(times)
    time_now = datetime.now().time()
    print(time_now)
    for dose_time, taken in times.items():
        print(dose_time)
        print(taken)
        dose_time_iso = time.fromisoformat(dose_time)
        if dose_time_iso > time_now and not taken:
            return dose_time


def get_remaining_stock(med_name):
    med_data_dict = get_user_medicine_data(med_name)
    print(med_data_dict)
    remaining_stock = med_data_dict['remaining_stock']
    print(remaining_stock)
    return remaining_stock
