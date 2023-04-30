# SKILL WORKER -- SW

#### ALL THE NECESSARY ENVIRONMENTS ARE PROVIDED IN THE FINAL REPORT

### HOW TO RUN THE APPLICATION 
1. Git clone ```git clone https://github.com/kofnet002/SW.git```

2. cd to the project directory

3. Install the necessary dependencies ```pip install requirements.txt```

4. Create ".env" file in the project directory and configure the following environment.

a. SCRETE_KEY = "any secret you want/ example: any random strings of words"

b. TWILIO_ACCOUNT_SID = "will be provided in the report"

c. TWILIO_AUTH_TOKEN = "will be provided in the report"

d. TWILIO_PHONE_NUMBER = "will be provided in the report"

e. COUNTRY_CODE = "+233"

5. The application is configured with PostgreSQL from [railway platform](https://railway.app)

6. Time to make migrations, ```python manage.py makemigrations```

7. Apply the migration ```python manage.py migrate``` 

### Point 6 and 7 will get the database ready. 

8. APPLICATION END POINTS 
+ 'client-register/' - To register clients
+ 'worker-register/' - To register workers
+ 'verify-otp/' - To verify users
+ 'clients/' - To show all clients
+ 'workers/' - To show all workers
+ 'services/' - To show all services provided by the workers
+ 'mybookings/' - To show all the available bookings by the clients
