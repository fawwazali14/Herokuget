from flask import Flask,jsonify,request
import os
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)


db_config = {
    'host': 'dbms.cbj29vmpnvrx.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'password',
    'database': 'carematch'
}


@app.route('/fetch_data', methods = ['GET'])
def fetch_data():
    try:
        table = request.args.get('table')
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        print(table)

        if table == "Notifications":
            x = request.args.get('ID')
            print(x)
            notif_query1 = f"SELECT notif_id, notif_type, degree, Notifications.description, notif_title, Notifications.job_ID FROM Notifications JOIN Job_Listings ON Notifications.job_ID = Job_Listings.job_ID WHERE notif_type = 'Post' AND Job_Listings.ID = '{x}'"
            notif_query2 = f"SELECT * FROM Notifications WHERE job_ID IN (SELECT job_ID FROM Job_Listings WHERE ID = '{x}') AND notif_type = 'Applied'"
            # print("1")
            cursor1 = connection.cursor()
            cursor2 = connection.cursor()
            print("2")
            cursor1.execute(notif_query1)
            print("3")
            cursor2.execute(notif_query2)
            print("4")

            result1 = cursor1.fetchall()
            result2 = cursor2.fetchall()
            final = result1 + result2
            return jsonify({'notification': final}), 200

        if table == "Job_Listings":
            x = request.args.get('ID')
            print("solo")
            print(x)
            job_fetch_query = f"SELECT job_ID, job_title, time_posted, Job_Listings.description, pay_per_hr, duration, cyclic, Job_Listings.ID,is_open,name,email,willing_to_travel,dob,curr_job,gender,phone_number FROM Job_Listings Join Users on Job_Listings.ID = Users.ID WHERE Job_Listings.ID !='{x}' ;"
            cursor.execute(job_fetch_query)
            job_listings = cursor.fetchall()

            cursor.close()
            connection.close()
            print(job_listings)

            # Convert the result to a list of dictionaries for JSON serialization
            jobs = [
                {
                    'job_ID': job[0] if job[0] is not None else None,
                    'job_title': job[1] if job[1] is not None else None,
                    'time_posted': job[2] if job[2] is not None else None,
                    'description': job[3] if job[3] is not None else None,
                    'pay_per_hr': job[4] if job[4] is not None else None,
                    'duration': job[5] if job[5] is not None else None,
                    'cyclic': job[6] if job[6] is not None else None,
                    'ID': job[7] if job[7] is not None else None,
                    'is_open': job[8] if job[8] is not None else None,
                    'username':job[9],
                    'email' : job[10],
                    'travel' : job[11],
                    'dob': job[12],
                    'job': job[12],
                    'gender': job[12],
                    'phone_number': job[12]
                } for job in job_listings
            ]


            return jsonify({'jobs': jobs}), 200
        elif table == "filter":
            print("x")

        elif table == "jobs_myprofile":
            print("yoyo")
            x = request.args.get("ID")
            print(x)
            query = f"Select job_ID, job_title, time_posted, Job_Listings.description, pay_per_hr, duration, cyclic, Job_Listings.ID,is_open from Job_Listings  where ID = '{x}'"
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            cursor.close()
            jobs = [
                {
                    'job_ID': job[0] if job[0] is not None else None,
                    'job_title': job[1] if job[1] is not None else None,
                    'time_posted': job[2] if job[2] is not None else None,
                    'description': job[3] if job[3] is not None else None,
                    'pay_per_hr': job[4] if job[4] is not None else None,
                    'duration': job[5] if job[5] is not None else None,
                    'cyclic': job[6] if job[6] is not None else None,
                    'ID': job[7] if job[7] is not None else None,
                    'is_open': job[8] if job[8] is not None else None,

                } for job in result
            ]
            return jsonify(jobs)

        elif table =="myprofile":
            x = request.args.get("ID")
            print(x)
            query = f"Select  name,email,phone_number,dob,willing_to_travel,curr_job,bio,location from Users where ID = '{x}'"
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            cursor.close()
            connection.close()
            resultnew = [
                {
                    'name': item[0] if item[0] is not None else None,
                    'email': item[1] if item[1] is not None else None,
                    'pno': item[2] if item[2] is not None else None,
                    'dob': item[3],
                    'travel' : item[4],
                    'curr_job':item[5],
                    'bio':item[6],
                    'location':item[7]

                } for item in result
            ]
            return jsonify({'data': resultnew}), 200


        elif table =="Applies":
            x = request.args.get("job_ID")
            query = f"Select name,Users.ID,phone_number,email from Applies Join Users On Applies.ID = Users.ID Where Applies.job_ID = '{x}' "
            cursor.execute(query)
            result = cursor.fetchall()
        elif table =="all":
            query = "SELECT name,email FROM AllUsers"
            cursor.execute(query)
            result = cursor.fetchall()
            resultnew = [
                {
                    'name': item[0] if item[0] is not None else None,
                    'email': item[1] if item[1] is not None else None,


                } for item in result
            ]
            return jsonify({'data': resultnew}), 200



        elif table == "check":
            x = request.args.get("ID")
            check_query = f"SELECT * FROM Users WHERE ID LIKE '{x}';"
            cursor.execute(check_query)
            cq = cursor.fetchall()
            cursor.close()
            connection.close()
            print("yolo")
            # bool = None
            if cq is not None and len(cq) > 0:
                bool = "1"
            else:
                bool = "0"

            return jsonify({"bool":bool}), 200

        return jsonify({'message': 'Table not specified or invalid'}), 400

    except pymysql.Error as e:
        return jsonify({'error': f'Error fetching data: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Use port provided by Heroku or default to 5000
    app.run(host='0.0.0.0', port=port)
