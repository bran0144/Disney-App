# Disney Touring Plans App

## Created by Matthew Tassone & Katherine Gott

### For CS340 Intro to Databases at Oregon State University

 
### Our app.py code borrowed significantly from the flask starter app code
### https://github.com/osu-cs340-ecampus/flask-starter-app
### We used the skeleton code for connecting to the db and used the same style for routing and templates.
### We updated the code to match our columns and added routes for out M:N relationships
### between Touring Plans and Restaurants and Touring Plans and Rides. We followed a similar pattern
### for add/delete/update/get operations for each of our tables the routing and templating. 

### We also used the course materials in the Explorations to add route 
### handling capabilities, and to use gunicorn.
### Source URL: https://canvas.oregonstate.edu/courses/1967354/pages/exploration-developing-in-flask?module_item_id=24460849

### Original work: We added pages for our M:N relationship to display in a separate plan_view.j2. Some of the code within plan_view.j2 comes from the above flask-starter-app.