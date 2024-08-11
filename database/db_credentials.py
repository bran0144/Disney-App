# Our app.py code borrowed significantly from the flask starter app code
# https://github.com/osu-cs340-ecampus/flask-starter-app
# We used the skeleton code for connecting to the db and used the same style for routing and templates.
# We updated the code to match our columns and added routes for out M:N relationships
# between Touring Plans and Restaurants and Touring Plans and Rides. We followed a similar pattern
# for add/delete/update/get operations for each of our tables the routing and templating. 

# We also used the course materials in the Explorations to add route 
# handling capabilities, and to use gunicorn.
# Source URL: https://canvas.oregonstate.edu/courses/1967354/pages/exploration-developing-in-flask?module_item_id=24460849

# Original work: We added pages for our M:N relationship to display in a separate Plan View. 

# For Local Devlelopment
# host = 'localhost'
# user = 'root'                                   # can be different if you set up another username in your MySQL installation
# passwd = 'nottellingyou'                        # set accordingly
# db = 'bsg'


# For OSU Flip Servers

host = 'classmysql.engr.oregonstate.edu'      # MUST BE THIS
user = 'cs340_gottk'       # don't forget the cs340_ prefix
passwd = ''               # should only be 4 digits if default
db = 'cs340_gottk'                                  
