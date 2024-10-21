from flask import Flask, render_template, request, redirect, url_for, session, flash, json, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import time # To simulate time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234@Saikiran'
app.config['MYSQL_DB'] = 'emp'

mysql = MySQL(app)

@app.route('/')
def index():  
    return render_template('sign-up.html')

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/temp')
def temp():
    return render_template('temp.html')

# profile update
def generate_empid() -> str:
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT value FROM counters WHERE name = 'latest_empid'")
    result = cursor.fetchone()
    latest_empid = result[0] if result else 0
    new_empid = latest_empid + 1
    cursor.execute("UPDATE counters SET value = %s WHERE name = 'latest_empid'", (new_empid,))
    mysql.connection.commit()
    return f"BA{new_empid:03d}"

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    username = session.get('username')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email_address = request.form['email_address']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        date_of_birth = request.form['date_of_birth']
        designation = request.form['designation']
        joining_date = request.form['joining_date']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        postal_code = request.form['postal_code']
        uan = request.form['uan']
        pan = request.form['pan']
        bname = request.form['bname']
        branch = request.form['branch']
        account_number = request.form['account_number']
        user_role = request.form['user_role']
        
        
       
        empid = generate_empid()
        
        cursor = mysql.connection.cursor()
        try:
            #Inseting data into Profile table
            cursor.execute('INSERT INTO profile (empid, username, password, email_address, first_name, last_name, phone_number, date_of_birth, designation, joining_date, address, city, country, postal_code,uan,pan,bname,branch,account_number, user_role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                       (empid, username, password, email_address, first_name, last_name, phone_number, date_of_birth, designation, joining_date, address, city, country, postal_code,uan,pan,bname,branch,account_number, user_role))
            
            #Inserting data into users table
            cursor.execute('''
                INSERT INTO users (id, username, password, designation, employed_on) 
                VALUES (%s, %s, %s, %s, %s)
            ''', 
            (empid, username, password, designation, joining_date))
        
            mysql.connection.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            mysql.connection.rollback()
            print(f"Error occurred: {e}")
            return f"Error occurred: {e}"
        finally:
            # Close the cursor
            cursor.close()
        return redirect(url_for('userprofile'), user_role=user_role)
    
    return render_template('adduser.html', user_role=user_role)


# profile display
@app.route('/userprofile')
def userprofile():
    username = session.get('username')
    
     # Ensure username is a string
    if 'username':
        cur = mysql.connection.cursor()
        sql = "SELECT * FROM profile WHERE username=%s"  # Use prepared statement
        cur.execute(sql, (session['username'],))
        profile = cur.fetchone()
        cur.close()
        print(profile)
    return render_template('userprofile.html', profile=profile)

# calendar


@app.route('/calendar', methods=['GET', 'POST', 'PUT', 'DELETE'])
def calendar():
    if request.method == 'GET':
        # Retrieve all events
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM events")
        data = cur.fetchall()
        cur.close()
        return jsonify({'events': data})

    elif request.method == 'POST':
        # Add a new event
        data = request.json
        title = data.get('title')
        time_from = data.get('time_from')
        time_to = data.get('time_to')
        day = data.get('day')
        month = data.get('month')
        year = data.get('year')

        if not (title and time_from and time_to and day and month and year):
            return jsonify({'error': 'Missing data'}), 400

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO events (title, time_from, time_to, day, month, year) VALUES (%s, %s, %s, %s, %s, %s)", (title, time_from, time_to, day, month, year))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Event added successfully'})

    elif request.method == 'PUT':
        # Update an event
        data = request.json
        event_id = data.get('id')
        title = data.get('title')
        time_from = data.get('time_from')
        time_to = data.get('time_to')
        day = data.get('day')
        month = data.get('month')
        year = data.get('year')

        if not (event_id and title and time_from and time_to and day and month and year):
            return jsonify({'error': 'Missing data'}), 400

        cur = mysql.connection.cursor()
        cur.execute("UPDATE events SET title = %s, time_from = %s, time_to = %s, day = %s, month = %s, year = %s WHERE id = %s", (title, time_from, time_to, day, month, year, event_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Event updated successfully'})

    elif request.method == 'DELETE':
        # Delete an event
        event_id = request.json.get('id')

        if not event_id:
            return jsonify({'error': 'Missing event id'}), 400

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Event deleted successfully'})

      
        

# payroll
@app.route('/payroll',methods=['GET', 'POST'])
def payroll():
    username = session.get('username')
    
    if 'username':
       cur = mysql.connection.cursor()
       sql = "SELECT * FROM profile WHERE username=%s"  # Use prepared statement
       cur.execute(sql, (session['username'],))
       user = cur.fetchone()
       cur.close()
       curs = mysql.connection.cursor()
       sql1 = "SELECT * FROM payslip WHERE username=%s"  # Use prepared statement
       curs.execute(sql1, (session['username'],))
       payslip = curs.fetchone()
       curs.close()
       return render_template('payroll.html', user=user, payslip= payslip)

from datetime import datetime

# payrollmanager
@app.route('/payrollmanager', methods=['GET', 'POST'])
def payrollmanager():
    username = session.get('username')
    empid = session.get('empid')
    user_role = session.get('user_role')

    if not username or user_role in ['Employee', 'Trainee']:
        return '''
            <script type="text/javascript">
                alert("Access denied. You do not have permission to view this page.");
                window.location.href = "/dashboard";  // Redirect to the desired page after alert
            </script>
        '''
   
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profile")
    data = cur.fetchall()
    cur.close()
    
    empid = session.get('empid')

    cur = mysql.connection.cursor()
    # Query to fetch the logged-in user's details
    cur.execute("SELECT empid, username FROM profile WHERE empid = %s", (empid,))
    user = cur.fetchone()  # Fetch a single user's data (empid, username)
    cur.close()

    if request.method == 'POST':
        employee_id = request.form.get('emp_id')
        username = request.form.get('emp_name')  # Fetching username from the form
        pay_period_input = request.form.get('pay_period')
        pay_date = request.form.get('pay_date')
        bp = request.form.get('bp')
        hra = request.form.get('hra')
        ma = request.form.get('ma')
        ca = request.form.get('ca')
        oa = request.form.get('oa')
        pt = request.form.get('pt')
        pf = request.form.get('pf')

        # Convert pay_period to a complete date
        pay_period = datetime.strptime(pay_period_input + '-01', '%Y-%m-%d').date()

        ge = float(bp) + float(hra) + float(ma) + float(ca) + float(oa)
        td = float(pt) + float(pf)
        net_payable = ge - td

        # Insert into payslip table
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO payslip (employee_id, username, pay_period, pay_date, bp, hra, ma, ca, oa, ge, pt, pf, td, net_payable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (employee_id, username, pay_period, pay_date, bp, hra, ma, ca, oa, ge, pt, pf, td, net_payable)
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('payrollmanager'))

    return render_template('payrollmanager.html', users=data, user=user,user_role=user_role)


#employeeleavemanaement--for emp
@app.route('/empleave', methods=['GET', 'POST'])
def leavemanagement():
    username = session.get('username')  # Get username from session
   

    # Open the cursor at the start of the function
    cursor = mysql.connection.cursor()

    # Fetch leave requests for the logged-in user based on username
    cursor.execute('SELECT * FROM empleave WHERE username = %s', (username,))
    data = cursor.fetchall()

    if request.method == 'POST':
        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']
        
        # Initialize an empty error message
        error_message = None

        # Server-side validation
        if not leave_type or not start_date or not end_date or not reason:
            error_message = "All fields are required. Please fill in all the details."
        elif start_date > end_date:  # Check if start date is before end date
            error_message = "Start date must be before end date."

        if error_message is None:
            try:
                # Convert date formats from DD/MM/YYYY to YYYY-MM-DD
                start_date = datetime.strptime(start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%d/%m/%Y').strftime('%Y-%m-%d')

                # Insert into the database
                cursor.execute('INSERT INTO empleave (username, leave_type, start_date, end_date, reason, status) VALUES (%s, %s, %s, %s, %s, %s)', 
                               (username, leave_type, start_date, end_date, reason, 'Pending'))
                mysql.connection.commit()

                # After successful insertion, fetch the updated leave requests
                cursor.execute('SELECT * FROM empleave WHERE username = %s', (username,))
                data = cursor.fetchall()

                #return render_template('leaverequest.html', leaves=data)  # Redirect to updated data view
                return redirect(url_for('leavemanagement'))
            except ValueError:
                error_message = "There was an error processing the date. Please check your input."

        # If validation fails, return the error message to the template
        return render_template('leaverequest.html', leaves=data, error_message=error_message)

    # Close the cursor after all operations
    cursor.close()
    
    return render_template('leaverequest.html', leaves=data)
   



@app.route('/managerleave', methods=['GET', 'POST'])
def managerleave():
    username = session.get('username')
    user_role = session.get('user_role')

    if not username or user_role in ['Employee', 'Trainee']:
        return '''
            <script type="text/javascript">
                alert("Access denied. You do not have permission to view this page.");
                window.location.href = "/dashboard";  // Redirect to the desired page after alert
            </script>
        '''
    
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        leave_type = data['leave_type']
        start_date = data['start_date']
        status = data['status']

        # Updating the leave status for the selected username, leave_type, and start_date
        cur.execute("""
            UPDATE empleave 
            SET status = %s 
            WHERE username = %s AND leave_type = %s AND start_date = %s
        """, (status, username, leave_type, start_date))

        mysql.connection.commit()
        cur.close()

        return jsonify({'message': f'Status updated to {status} successfully'})

    # Fetch and display the leave requests
    cur.execute("SELECT * FROM empleave")
    data = cur.fetchall()
    cur.close()
    
    return render_template('managerleave.html', employees=data,user_role=user_role)


# project
@app.route('/project', methods=['GET', 'POST']) 
def project():
    username = session.get('username')
    user_role = session.get('user_role')

    if not username or user_role in ['Employee', 'Trainee']:
        return '''
            <script type="text/javascript">
                alert("Access denied. You do not have permission to view this page.");
                window.location.href = "/dashboard";  // Redirect to the desired page after alert
            </script>
        '''
    if request.method == 'POST':
        project_title = request.form['project_title']
        description= request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO project VALUES (NULL, %s, %s, %s, %s)', (project_title, description, start_date, end_date))
        mysql.connection.commit()
        return render_template('project.html',user_role=user_role)
    return render_template('project.html',user_role=user_role)

# duplicateproject
@app.route('/pr0ject')
def pr0ject():
    username = session.get('username')
    user_role = session.get('user_role')

    # if not username or user_role in ['Employee', 'Trainee']:
    #     return '''
    #         <script type="text/javascript">
    #             alert("Access denied. You do not have permission to view this page.");
    #             window.location.href = "/dashboard";  // Redirect to the desired page after alert
    #         </script>
    #     '''    
    if 'username':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM project")
        data = cur.fetchall()
        cur.close()
        print(data)
        return render_template('projectlist.html', project=data,user_role=user_role)
    else:
        return redirect(url_for('index'))



@app.route('/workreport', methods=['GET', 'POST'])
def workreport():
    empid = session.get('empid')  # Get empid from session
    username = session.get('username')
    user_role = session.get('user_role')

    if not username or user_role in ['Employee', 'Trainee']:
        return '''
            <script type="text/javascript">
                alert("Access denied. You do not have permission to view this page.");
                window.location.href = "/dashboard";  // Redirect to the desired page after alert
            </script>
        '''
    
    
    # Fetch profile data based on empid
    profile = None
    if empid:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM profile WHERE empid = %s", (empid,))
        profile = cursor.fetchone()  # Fetch the first row
        cursor.close()

    # Fetch all usernames to populate the dropdown
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM profile")  # Fetch all usernames
    usernames = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        date = request.form['date']
        time = request.form['Timings']
        work_done = request.form['workdone']
        selected_username = request.form.get('usernameFilter')  # Get selected username from form

        # Fetch empid of the selected user
        if selected_username:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT empid FROM profile WHERE username = %s", (selected_username,))
            selected_profile = cursor.fetchone()
            cursor.close()

            if selected_profile:
                selected_empid = selected_profile[0]  # Get empid of the selected user

                cursor = mysql.connection.cursor()
                cursor.execute(
                    'INSERT INTO workreport (empid, date, time, work_done) VALUES (%s, %s, %s, %s)', 
                    (selected_empid, date, time, work_done)
                )
                mysql.connection.commit()
                cursor.close()

                return redirect(url_for('workreportlist'))  # Redirect to work report list after saving

    return render_template('workreport.html', profile=profile, usernames=[u[0] for u in usernames], user_role=user_role)  # Pass profile and usernames to the template


#workreport-list
@app.route('/workreportlist', methods=['GET', 'POST'])
def workreportlist():
    empid = session.get('empid')  # Get empid from session
    username = session.get('username')
    user_role = session.get('user_role')
    
    
    if 'username' in session:  # Check if user is logged in
        empid = session['empid']  # Get empid from session
        username = session.get('username') #get username from session
        
        cursor = mysql.connection.cursor()
        
        # Fetch distinct usernames for the filter
        cursor.execute("SELECT DISTINCT username FROM profile")  # Adjust the query as needed
        usernames = [row[0] for row in cursor.fetchall()]  # Extract usernames into a list
        
        # Fetch user role based on the logged-in empid
        cursor.execute("SELECT user_role FROM profile WHERE empid = %s", (empid,))
        user_role = cursor.fetchone()[0]  # Assuming 'user_role' is the first column in the fetched result
        
        # Fetch the logged-in user's time data from the workreport
        cursor.execute("SELECT time FROM workreport WHERE empid = %s", (empid,))
        time_result = cursor.fetchone()  # Fetch one result

        # Handle case where no time data is found
        if time_result is None:
            
            time = None  # Handle as needed (set time to None or use a default value)
        else:
            time = time_result[0]  # Access the first column if the result is not None

        # Fetch filter parameters from the request (POST or GET)
        selected_username = request.form.get('usernameFilter')  # From filter dropdown
        selected_date = request.form.get('dateFilter')  # From date input
        
        # If no date is selected, default to today's date
        if not selected_date:
            selected_date = datetime.today().strftime('%Y-%m-%d')  # Default to today's date
        
        # If no username is selected, treat it as None for filtering
        if not selected_username:
            selected_username = None

        # If the user is the CEO, allow filtering by username and date
        if user_role == "CEO":
            # Prepare query with filters
            query = """
                SELECT wr.*, p.username 
                FROM workreport wr 
                JOIN profile p ON wr.empid = p.empid
                WHERE (%s IS NULL OR p.username = %s)  -- If no username selected, get all
                AND wr.date = %s
            """
            cursor.execute(query, (selected_username, selected_username, selected_date))
            disable_filter = False  # CEO can use the filter
        else:
            # If not the CEO, only retrieve the work reports for the logged-in empid
            query = """
                SELECT wr.*, p.username 
                FROM workreport wr 
                JOIN profile p ON wr.empid = p.empid 
                WHERE wr.empid = %s 
                AND wr.date = %s
            """
            cursor.execute(query, (empid, selected_date))
            disable_filter = True  # Non-CEO cannot use the filter
        
        # Fetch the result
        data = cursor.fetchall()
        cursor.close()
        
        # Check if there's no data found
        no_data = not data  # True if no data, False otherwise
        
        # Initialize timer_status, pause_reason, and check_reason
        timer_status, pause_reason, check_reason = None, None, None
        
        # Handle timer updates (assuming the data comes in as JSON)
        if request.method == 'POST' and request.is_json:
            data = request.get_json()
            action = data.get('action')
            work_done = data.get('work_done')
            pause_reason = data.get('pause_reason')
            check_reason = data.get('check_reason')

            cursor = mysql.connection.cursor()

            # Check if a work report for the empid, date, and work_done already exists
            cursor.execute("""
                SELECT COUNT(*) 
                FROM workreport 
                WHERE empid = %s AND date = %s AND work_done = %s
            """, (empid, selected_date, work_done))
            report_exists = cursor.fetchone()[0]  # Gets the count

            if report_exists == 0:
                # Insert the default "yet to start" status if this is a new work report
                cursor.execute("""
                    INSERT INTO workreport (empid, time, date, work_done, timer_status) 
                    VALUES (%s, %s, %s, %s, 'yet to start')
                """, (empid, time, selected_date, work_done,work_done))
                mysql.connection.commit()

            # Update the timer_status based on the action
            if action == 'play':
                # Update the work report's timer status to "running"
                cursor.execute("""
                    UPDATE workreport 
                    SET timer_status = 'running'
                    WHERE empid = %s AND work_done = %s AND date = %s
                """, (empid, work_done, selected_date))
                timer_status= 'running'
            elif action == 'pause':
            # Update the work report's timer status to 'paused' and record the pause reason
                cursor.execute("""
                    UPDATE workreport 
                    SET timer_status = 'paused', pause_reason = %s
                    WHERE empid = %s AND work_done = %s AND date = %s
                """, (pause_reason, empid, work_done, selected_date))
                timer_status = 'paused'
            elif action == 'check':
            # Update the work report's timer status to 'done' and record the check reason
                cursor.execute("""
                    UPDATE workreport 
                    SET timer_status = 'done', check_reason = %s
                    WHERE empid = %s AND work_done = %s AND date = %s
                """, (check_reason, empid, work_done, selected_date))
                timer_status = 'done'

            mysql.connection.commit()
            cursor.close()
        
            cursor = mysql.connection.cursor()
            # Fetch the timer_status data from the workreport
            cursor.execute("SELECT timer_status, pause_reason, check_reason FROM workreport WHERE empid = %s AND date = %s AND work_done = %s", (empid,selected_date,work_done))
            work_report_data = cursor.fetchone()
            cursor.close()
        
            if work_report_data:
                timer_status, pause_reason, check_reason = work_report_data
            else:
                timer_status, pause_reason, check_reason = None, None, None
        
            # Render the workreportlist template with the filtered data
        return render_template('workreportlist.html', project=data, usernames=usernames, 
                               disable_filter=disable_filter, selected_username=selected_username,
                               selected_date=selected_date, no_data=no_data, timer_status=timer_status,
                               pause_reason=pause_reason,check_reason=check_reason, username=username, user_role=user_role)
    else:
        return redirect(url_for('index'))


# tables
@app.route('/tables')
def tables():
    username = session.get('username')
    user_role = session.get('user_role')

    if not username or user_role in ['Employee', 'Trainee']:
        return '''
            <script type="text/javascript">
                alert("Access denied. You do not have permission to view this page.");
                window.location.href = "/dashboard";  // Redirect to the desired page after alert
            </script>
        '''
   
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM profile")
        data = cur.fetchall()
        cur.close()
        print(data)
        return render_template('tables.html', users=data,user_role=user_role)
    else:
        return redirect(url_for('index'))
    

    
#userworkallocation
@app.route('/userworkallocation')
def userworkallocation():
    username = session.get('username')
    
    
    if not username:
        return redirect(url_for('index'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM workallocation WHERE username = %s", (username,))
    data = cursor.fetchall()
    cursor.close()

    return render_template('userworkallocation.html', work=data)

#workallocation
@app.route('/workallocation', methods=['GET', 'POST'])
def workallocation():
    username = session.get('username')
    user_role = session.get('user_role')

    if not username or user_role in ['Employee', 'Trainee']:
        return '''
            <script type="text/javascript">
                alert("Access denied. You do not have permission to view this page.");
                window.location.href = "/dashboard";  // Redirect to the desired page after alert
            </script>
        '''
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM project")
    project_title1=cursor.fetchall()
    cursor.execute("SELECT * FROM users")
    username1=cursor.fetchall()
    if request.method == 'POST':
       project_title=request.form['project_title']
       username=request.form['username']
       work_date = request.form['work_date']
       work_time = request.form['work_time']
       work_description = request.form['work_description']
       cursor.execute('INSERT INTO workallocation VALUES (NULL, %s, %s, %s, %s, %s)', (project_title, username, work_date, work_time, work_description))
       mysql.connection.commit()
       return redirect(url_for('workallocation'))
    return render_template('workallocation1.html', project=project_title1, users=username1, user_role=user_role )


@app.route('/migrate_users')
def migrate_users():
    cursor = mysql.connection.cursor()

    try:
        # Fetch all necessary fields from the 'profile' table
        cursor.execute('''
            SELECT empid, username, password, designation, joining_date 
            FROM profile
        ''')
        profiles = cursor.fetchall()

        # Fetch existing usernames from the 'users' table to avoid duplicates
        cursor.execute('SELECT username FROM users')
        existing_users = [row[0] for row in cursor.fetchall()]

        # Loop through the profiles and insert into 'users' table where username does not already exist
        for profile in profiles:
            empid, username, password, designation, joining_date = profile

            # Check if the username already exists in the users table
            if username not in existing_users:
                cursor.execute('''
                    INSERT INTO users (id, username, password, designation, employed_on)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (empid, username, password, designation, joining_date))

        # Commit the changes to the database
        mysql.connection.commit()

        return "Migration completed successfully!"

    except Exception as e:
        # Rollback in case of an error
        mysql.connection.rollback()
        print(f"Error occurred during migration: {e}")
        return f"Error occurred during migration: {e} An error occurred during migration."

    finally:
        cursor.close()





# newdashboard
@app.route('/newdashboard')
def newdashboard():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM profile")
        data = cur.fetchall()
        cur.close()
        return render_template('dashboard.html', users=data)
    else:
        return redirect(url_for('index'))



# login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profile WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['username'] = username
        session['empid'] = user[1]  # Set empid in session
        session['user_role'] = user[20]
        return redirect(url_for('dashboard'))
    else:
        flash('Incorrect username or password', 'error')
        return redirect(url_for('index'))

#change-password
@app.route('/change-password', methods=['POST'])
def change_password():
    empid = session.get('empid')
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    
    if new_password != confirm_password:
        flash('New password and confirm password do not match', 'new_password_error')
        return redirect('/userprofile')

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT password FROM profile WHERE empid = %s", (empid,))
        result = cursor.fetchone()
        
        if result and result[0] == old_password:
            cursor.execute("UPDATE profile SET password = %s WHERE empid = %s", (new_password, empid))
            mysql.connection.commit()
            flash('Password changed successfully', 'success')
        else:
            flash('Current password is incorrect', 'old_password_error')  # Use flash for incorrect password

    except mysql.connector.Error as err:
        flash(f"Error: {err}", 'danger')

    return redirect('/userprofile')

@app.route('/validate-password', methods=['POST'])
def validate_password():
    empid = session.get('empid')
    old_password = request.json.get('old_password')  # Get the old password from the request

    # Connect to the database and check the password
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT password FROM profile WHERE empid = %s", (empid,))
    result = cursor.fetchone()

    # Check if the password matches
    if result and result[0] == old_password:
        return jsonify({'is_valid': True})  # Password is correct
    else:
        return jsonify({'is_valid': False})  # Password is incorrect
     
    

# dashboard
@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    user_role = session.get('user_role')
    
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM profile")
        data = cur.fetchall()
        cur.close()
        return render_template('newone.html', users=data, user_role=user_role)
    else:
        return redirect(url_for('index'))


# logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# to-do
@app.route('/todo', methods=['GET'])
def todo():
    username = session.get('username')
    user_role = session.get('user_role')

    
    user_id= session.get('username') 
    category= request.args.get('category')
    username=request.args.get('username')
    print(category)
    print(username)
    cur = mysql.connection.cursor()
    print(user_id)
    if 'username' in session :
            cur.execute("SELECT * FROM todo WHERE username = %s  ", (user_id,))  
    
    # else:
    #     cur.execute(("SELECT * FROM todo WHERE category = 'business'", ))
    todos = cur.fetchall()
    cur.close()
    return render_template('todo1.html', todos=todos, user_role=user_role)
   

@app.route('/add_todo', methods=['POST'])
def add_todo():
    if request.method == 'POST':
        content = request.form['content']
        category = request.form['category']
        username = session.get('username')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO todo (content, category, completed, username) VALUES (%s, %s, %s, %s)", (content, category, False, username))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('todo'))
    
@app.route('/edit_todo/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    # Retrieve data from the form submission
    content = request.form['content']
    category = request.form['category']
    completed = 'completed' in request.form
    
    # Update the todo item in the database
    cur = mysql.connection.cursor()
    cur.execute("UPDATE todo SET content=%s, category=%s, completed=%s WHERE id=%s", (content, category, completed, todo_id))
    mysql.connection.commit()
    cur.close()
    
    # Return JSON response with the updated todo item
    return jsonify({'success': True, 'message': 'Todo item updated successfully'})


@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM todo WHERE id = %s", (todo_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True, 'message': 'Todo item deleted successfully'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Failed to delete todo item'}), 500
    

# from flask import request

@app.route('/toggle_complete/<int:todo_id>', methods=['POST'])
def toggle_complete(todo_id):
    try:
        # Fetch the current completion status of the todo item
        cur = mysql.connection.cursor()
        cur.execute("SELECT completed FROM todo WHERE id = %s", (todo_id,))
        completed = cur.fetchone()[0]
        
        # Toggle the completion status
        completed = not completed
        
        # Update the completion status in the database
        cur.execute("UPDATE todo SET completed = %s WHERE id = %s", (completed, todo_id))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'success': True, 'message': 'Todo item marked as complete'})
    except ValueError as ve:
        return jsonify({'success': False, 'message': str(ve)}), 400
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Failed to mark todo item as complete'}), 500
    
@app.route('/tasks', methods=['GET', 'POST']) 
def tasks():
    # Fetch profile data based on empid if needed, but we are focusing on usernames
    empid = session.get('empid') 
    usernames = []  # Initialize a list to hold usernames

    # Fetch all usernames from the profile table
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM profile")
    usernames = [row[0] for row in cursor.fetchall()]  # Get usernames
    cursor.close()

    if request.method == 'POST':
        date = request.form['date']
        time = request.form['Timings']
        work_done = request.form['workdone']
        user_name = request.form['usernameFilter']

        if user_name:  # Ensure that a username has been selected
            cursor = mysql.connection.cursor()
            # Insert the work report using the selected username
            cursor.execute(
                'INSERT INTO taskslist (empid, date, time, work_done) VALUES (%s, %s, %s, %s)', 
                (empid, date, time, work_done)
            )
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('taskslist'))  # Redirect to work report list

    return render_template('tasks.html', usernames=usernames)  # Pass usernames to the template

#tasks-list page
@app.route('/taskslist', methods=['GET', 'POST'])
def taskslist():
    if 'username' in session:  # Check if user is logged in
        empid = session['empid']  # Get empid from session
        
        cursor = mysql.connection.cursor()
        
        # Fetch distinct usernames for the filter
        cursor.execute("SELECT DISTINCT username FROM profile")
        usernames = [row[0] for row in cursor.fetchall()]  # Extract usernames into a list
        
        # Fetch user role based on the logged-in empid
        cursor.execute("SELECT user_role FROM profile WHERE empid = %s", (empid,))
        user_role = cursor.fetchone()[0]  # Assuming 'user_role' is the first column in the fetched result

        # Fetch selected username from the request (POST or GET)
        selected_username = request.form.get('usernameFilter')  # From filter dropdown
        
        # If no username is selected, treat it as None for filtering
        if not selected_username:
            selected_username = None

        # If the user is the CEO, allow filtering by username
        if user_role == "CEO":
            # Prepare query with filters based on selected username
            query = """
                SELECT t.*, p.username 
                FROM taskslist t 
                JOIN profile p ON t.empid = p.empid
                WHERE (%s IS NULL OR p.username = %s)  -- If no username selected, get all
            """
            cursor.execute(query, (selected_username, selected_username))
            disable_filter = False  # CEO can use the filter
        else:
            # If not the CEO, only retrieve the tasks for the logged-in empid
            query = """
                SELECT t.*, p.username 
                FROM taskslist t 
                JOIN profile p ON t.empid = p.empid 
                WHERE t.empid = %s
            """
            cursor.execute(query, (empid,))
            disable_filter = True  # Non-CEO cannot use the filter
        
        # Fetch the result
        data = cursor.fetchall()
        cursor.close()
        
        # Check if there's no data found
        if not data:
            no_data = True  # Flag to indicate no data
        else:
            no_data = False

        # Render the taskslist template with the filtered data
        return render_template('taskslist.html', project=data, usernames=usernames, 
                               disable_filter=disable_filter, selected_username=selected_username,
                               no_data=no_data)
    else:
        return redirect(url_for('index'))
    
# Start Timer
@app.route('/start_timer', methods=['POST'])
def start_timer():
    empid = session.get('empid')
    date = request.form['date']
    
    cursor = mysql.connection.cursor()
    start_time = datetime.now()
    
    cursor.execute(
        'INSERT INTO taskslist (empid, date, start_time, status) VALUES (%s, %s, %s, %s)', 
        (empid, date, start_time, 'running')
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({'status': 'success', 'message': 'Timer started', 'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S')})

# Pause Timer
@app.route('/pause_timer/<int:task_id>', methods=['POST'])
def pause_timer(task_id):
    cursor = mysql.connection.cursor()
    pause_time = datetime.now()
    
    cursor.execute(
        'UPDATE taskslist SET pause_time = %s, status = %s WHERE id = %s', 
        (pause_time, 'paused', task_id)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({'status': 'success', 'message': 'Timer paused', 'pause_time': pause_time.strftime('%Y-%m-%d %H:%M:%S')})

# Stop Timer
@app.route('/stop_timer/<int:task_id>', methods=['POST'])
def stop_timer(task_id):
    cursor = mysql.connection.cursor()
    
    # Fetch the start and pause times to calculate total time
    cursor.execute('SELECT start_time, pause_time FROM taskslist WHERE id = %s', (task_id,))
    record = cursor.fetchone()
    
    if record:
        start_time = record[0]
        stop_time = datetime.now()
        total_time = (stop_time - start_time).total_seconds()  # Calculate total seconds
        
        cursor.execute(
            'UPDATE taskslist SET total_time = %s, status = %s WHERE id = %s', 
            (total_time, 'completed', task_id)
        )
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'status': 'success', 'message': 'Timer stopped', 'total_time': total_time})
    else:
        return jsonify({'status': 'error', 'message': 'Task not found'}), 404   
    



if __name__ == '__main__':
    app.run(debug=True)
