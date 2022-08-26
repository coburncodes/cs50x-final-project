**Welcome to High Desert Hiker!**

This is a companion app for oregonhikers.org. Use this app to track your Central Oregon hikes!

**Video Demo:**
https://youtu.be/PjFtkmPspZY

**Technologies Used:**

HTML5, CSS3, Bootstrap, Python, Jinja, Flask

**Overview:**

With over 135 hikes listed on oregonhikers.org for the Central Oregon area alone, keeping track of your progress through each one can be difficult. That's why I created this app. With High Desert Hiker, users can login to access their account, view information about each of these hikes, add any one of these hikes to their completed list, and leave a review and a rating for each. Users can also edit their reviews, ratings, usernames and passwords, and delete hikes from their completed list.

**Instructions:**

- Click "Register" if you're a new user.
- Input your information.
- Input your login info on the "Login" page.
- From the main page, click the image or navigation links.
- "My Hikes" displays hikes that you've completed, with sort functionality.
- "All Hikes" displays all hikes in the database, with sort functionality.
- "Add Hike" allows you to input a hike, date, rating, and review.
- From the "My Hikes" page, you can also add, edit, and delete hikes.
- Edit your information from the "Account" navigation link.
- Click "Log Out" to end your session.

**Process:**
I began by copying the data from oregonhikers.org and creating a CSV file using Excel. Then, I used this CSV file to create a table in SQLite. This allows the potential to expand the database with more hikes quickly and easily. I chose to use Flask and Python to build the app based on the projects completed in CS50. Using these two technologies, I wrote functionality into the controller to display the view, which I created using HTML and Jinja. These pages were styled using Bootstrap and CSS.

**Functionality:**

- Allows users to register, login, and logout.
- Handles all errors with messages and codes.
- Populates SQLite table with users' registration information.
- Displays multiple pieces of information for each hike including distance, difficulty, name, region, review, and rating.
- Displays dynamically-rendered URLs to each hike's in-depth oregonhikers.org page.
- Allows users to sort "All Hikes" and "My Hikes" by region, name, difficulty, distance and more.
- Allows users to add, edit, and delete hikes from their completed list.
- Allows users to update password, username, and first name using SQL queries.
- Responsive across all devices.

**Files:**

- App.py is the main controller. It contains all 14 routes to each webpage, and allows the users' changes to manipulate the model.
- Hiker.db is the model, where the SQL tables exist for hikes, users, and completed. This file is manipulated by the user when they interact with the view via the controller.
- The templates folder contains all the HTML files that comprise the view. These pages also include Jinja for dynamic rendering, and bootstrap classes that provide styling for the majority of the pages.
- Styles.css contains additional styling.
- Helpers.py includes functions intended to assist app.py such as requiring login for certain HTML pages and rendering error messages.
- Requirements.txt contains the dependencies required for the project.

**Expanding Functionality:**

- Replace relative links to photos with absolute links.
- Pre-populate "Edit" screen based on dropdown selections.
- Allow users to add photos.
- Require stricter password format.
- Reformat "All Hikes" page to display information more cleanly.
