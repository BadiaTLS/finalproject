# Dining Hall Behavior Analysis and Prediction using Machine Learning and Statistics

This project aims to analyze and predict the ordering behavior of customers in a cafeteria using machine learning and statistical methods. By analyzing historical data on orders, we will develop predictive models to forecast future demand for different meal sessions and menu items. Additionally, we will use classification techniques to group customers based on their ordering behavior and provide personalized recommendations. This project will provide valuable insights into customer behavior and help optimize the cafeteria’s operations

## Installation

Make sure that you have python 3 installed, then you can just run the `setup.bat` file to install all needed requirements like environment and database

## Usage

1. After you run the `setup.bat`, you can just use the `run.bat` or use this command in command line the project directory to run the server

```bash
python manage.py runserver
```

2. After you run the server, you can open your favorite browser and go to http://127.0.0.1:8000/admin to check the available users, the username is `admin` and the password is `admin`

3. There will be 3 user with 3 roles, one is Admin, the other is the user that use this main site. (SAS and DiningHall)
- SAS has the role to input users and classes from excel file
- Dining Hall has the role to input menu for that sessions and bookings/live bookings from excel
- You can check the `dummy_gen` to see how the data looks like, try to run each one of them. Start from user, session and then class, booking, live booking.

4. If you already input all the users, you can access the main site http://127.0.0.1:8000/ to login to every users that you registered with sas or with admin

5. That's all you need.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Contributors

[BadiaTLS](https://github.com/BadiaTLS)\
[ElsonPRS](https://github.com/elsonsutrisno)