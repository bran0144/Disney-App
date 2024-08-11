from flask import Flask, render_template, redirect
from flask_mysqldb import MySQL
from flask import request


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


# Configuration and DB setup

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_gottk'
app.config['MYSQL_PASSWORD'] = '' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_gottk'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes 

# Home page with table descriptions
@app.route("/")
def home():
    return render_template("main.j2")


# route for rides page
@app.route("/rides", methods=["POST", "GET"])
def rides():

    # insert a ride into Rides table
    if request.method == "POST":
        # fire off if user presses the Add Ride button
        if request.form.get("insertRide"):
            # grab user form inputs
            rideName = request.form["rideName"]
            parkID = request.form["parkID"]
            heightRestriction = request.form["heightRestriction"]
            lightningLane = request.form["lightningLane"]
            rideLength = request.form["rideLength"]

          
            query = "INSERT INTO Rides (rideName, parkID, heightRestriction, lightningLane, rideLength) VALUES (%s, %s,%s,%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (rideName, parkID, heightRestriction, lightningLane, rideLength))
            mysql.connection.commit()

            # redirect back to rides page
            return redirect("/rides")

    # Grab Rides data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the rides in Rides
        query = "SELECT rideID, rideName, heightRestriction, if(lightningLane=1, 'Yes', 'No') as lightningLane, rideLength, Parks.parkName AS park FROM Rides LEFT JOIN Parks ON Rides.parkID = Parks.parkID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # render edit_rides page passing our query data and parks data to the edit_rides template
        return render_template("rides.j2", data=data, parks=parks_data)

# route for delete functionality, deleting a ride from Rides,
# we want to pass the 'rideID' value of that ride on button click (see HTML) via the route
@app.route("/delete_ride/<int:rideID>")
def delete_ride(rideID):
    # mySQL query to delete the ride with our passed id
    query = "DELETE FROM Rides WHERE rideID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (rideID,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/rides")


# route for edit functionality, updating the attributes of a ride in Rides
# similar to our delete route, we want to the pass the 'rideID' value of that ride on button click (see HTML) via the route
@app.route("/edit_rides/<int:rideID>", methods=["POST", "GET"])
def edit_rides(rideID):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Rides WHERE rideID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (rideID,))
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # render edit_rides page passing our query data and parks data to the edit_ride template
        return render_template("edit_rides.j2", data=data, parks=parks_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Ride' button
        if request.form.get("edit_rides"):
            # grab user form inputs
            rideID = request.form["rideID"]
            rideName = request.form["rideName"]
            heightRestriction = request.form["heightRestriction"]
            lightningLane = request.form["lightningLane"]
            parkID = request.form["parkID"]
            rideLength = request.form["rideLength"]

     
            query = "UPDATE Rides SET rideName= %s, parkID = %s, lightningLane = %s, heightRestriction = %s, rideLength = %s WHERE rideID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (rideName, parkID, lightningLane, heightRestriction, rideLength, rideID))
            mysql.connection.commit()

            # redirect back to rides page after we execute the update query
            return redirect("/rides")

# route for parks page
@app.route("/parks", methods=["POST", "GET"])
def parks():

    # insert a park into Parks
    if request.method == "POST":
        # fire off if user presses the Add Park button
        if request.form.get("insertPark"):
            # grab user form inputs
            parkName = request.form["parkName"]
            parkHours = request.form["parkHours"]
            nighttimeShow = request.form["nighttimeShow"]

            query = "INSERT INTO Parks (parkName, parkHours, nighttimeShow) VALUES (%s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (parkName, parkHours, nighttimeShow))
            mysql.connection.commit()

            # redirect back to parks page
            return redirect("/parks")

    # Grab Parks data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the parks in Parks
        query = "SELECT parkID, parkName, parkHours, nighttimeShow FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render parks page
        return render_template("parks.j2", data=data)


# route for parks page
@app.route("/restaurants", methods=["POST", "GET"])
def restaurants():

    # insert a Restaurant into the Restaurant entity
    if request.method == "POST":
        # fire off if user presses the Add Restaurant button
        if request.form.get("insertRestaurant"):
            # grab user form inputs
            restaurantName = request.form["restaurantName"]
            parkID = request.form["parkID"]
            reservationsAccepted = request.form["reservationsAccepted"]
            characterDining = request.form["characterDining"]

            query = "INSERT INTO Restaurants (restaurantName, parkID, reservationsAccepted, characterDining) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (restaurantName, parkID, reservationsAccepted, characterDining))
            mysql.connection.commit()

            # redirect back to parks page
            return redirect("/restaurants")

    # Grab Parks data so we send it to our template to display
    if request.method == "GET":
         # mySQL query to grab all the rides in Rides
        query = "SELECT restaurantID, restaurantName, if(reservationsAccepted=1, 'Yes', 'No') as reservationsAccepted, if(characterDining=1, 'Yes', 'No') as characterDining, Parks.parkName AS park FROM Restaurants LEFT JOIN Parks ON Restaurants.parkID = Parks.parkID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # render edit_rides page passing our query data and parks data to the edit_rides template
        return render_template("restaurants.j2", data=data, parks=parks_data)


# route for edit functionality, updating the attributes of a ride in Rides
# similar to our delete route, we want to the pass the 'id' value of that ride on button click (see HTML) via the route
@app.route("/edit_restaurants/<int:restaurantID>", methods=["POST", "GET"])
def edit_restaurants(restaurantID):
    if request.method == "GET":
        # mySQL query to grab the info of the restaurant with our passed id
        query = "SELECT * FROM Restaurants WHERE restaurantID = %s" % (restaurantID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # render edit_rides page passing our query data and parks data to the edit_ride template
        return render_template("edit_restaurants.j2", data=data, parks=parks_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Ride' button
        if request.form.get("edit_restaurants"):
            # grab user form inputs
            restaurantID = request.form["restaurantID"]
            restaurantName = request.form["restaurantName"]
            characterDining = request.form["characterDining"]
            reservationsAccepted = request.form["reservationsAccepted"]
            parkID = request.form["parkID"]
            

            query = "UPDATE Restaurants SET Restaurants.restaurantName = %s, Restaurants.parkID = %s, Restaurants.characterDining = %s, Restaurants.reservationsAccepted = %s WHERE Restaurants.restaurantID = %s"
            print(query)
            cur = mysql.connection.cursor()
            cur.execute(query, (restaurantName, parkID, characterDining, reservationsAccepted, restaurantID))
            mysql.connection.commit()

            # redirect back to rides page after we execute the update query
            return redirect("/restaurants")


# route for Visitors page
@app.route("/visitors", methods=["POST", "GET"])
def visitors():

    # insert a visitor into the Visitor entity
    if request.method == "POST":
        # fire off if user presses the Add Visitor button
        if request.form.get("insertVisitor"):
            # grab user form inputs
            visitorName = request.form["visitorName"]
            height = request.form["height"]
            visitorEmail = request.form["visitorEmail"]

            # account for null height AND visitorEmail
            if height  == "" and visitorEmail == "":
                # mySQL query to insert a new person into Visitors with our form inputs
                query = "INSERT INTO Visitors (visitorName) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (visitorName))
                mysql.connection.commit()
            
            # account for null height
            elif height == "":
                query = "INSERT INTO Visitors (visitorName, visitorEmail) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (visitorName, visitorEmail))
                mysql.connection.commit()

            # account for null visitorEmail
            elif visitorEmail == "":
                query = "INSERT INTO Visitors (visitorName, height) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (visitorName, height))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Visitors (visitorName, height, visitorEmail) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (visitorName, height, visitorEmail))
                mysql.connection.commit()

            # redirect back to visitors page
            return redirect("/visitors")

    # Grab Visitors data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the visitors in Visitors
        query = "SELECT visitorID, visitorName, height, visitorEmail FROM Visitors;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render visitors page
        return render_template("visitors.j2", data=data)

# route for rides page
@app.route("/touring_plans", methods=["POST", "GET"])
def touring_plans():

    # insert a plan into the TouringPlans table
    if request.method == "POST":
        # fire off if user presses the Add Touring Plan button
        if request.form.get("insertTouringPlan"):
            # grab user form inputs
            planName = request.form["planName"]
            parkID = request.form["parkID"]
            visitorID = request.form["visitorID"]
            visitDate = request.form["visitDate"]


            # account for null visitDate AND planName
            if visitDate == "" and planName == "":
                # mySQL query to insert a new plan into TouringPlans with our form inputs
                query = "INSERT INTO TouringPlans (parkID, visitorID) VALUES (%s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkID, visitorID))
                mysql.connection.commit()
            
            # account for null visitDate
            elif visitDate == "":
                query = "INSERT INTO TouringPlans (parkID, visitorID, planName) VALUES (%s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkID, visitorID, planName))
                mysql.connection.commit()

            # account for null planName
            elif planName == "":
                query = "INSERT INTO TouringPlans (parkID, visitorID, visitDate) VALUES (%s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkID, visitorID, visitDate))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO TouringPlans (parkID, visitorID, visitDate, planName ) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkID, visitorID, visitDate, planName ))
                mysql.connection.commit()

            # redirect back to touring_plans page
            return redirect("/touring_plans")

    # Grab Touring PLans data so we send it to our template to display
    if request.method == "GET":

        # mySQL query to grab all the plans in TouringPlans
        query = "SELECT planID, visitDate, planName, Parks.parkName AS park, Visitors.visitorName AS visitorName FROM TouringPlans LEFT JOIN Parks ON TouringPlans.parkID = Parks.parkID LEFT JOIN Visitors on TouringPlans.visitorID = Visitors.visitorID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # mySQL query to grab visitor id/name data for our dropdown
        query3 = "SELECT visitorID, visitorName FROM Visitors;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        visitor_data = cur.fetchall()

        # render touring_plans page passing our query data, parks data, and visitors data to the touring_plans template
        return render_template("touring_plans.j2", data=data, parks=parks_data, visitors=visitor_data)

# route to get and add restaurants to the TouringPlan
@app.route("/touring_plan_restaurants/<int:planID>", methods=["POST", "GET"])
def touring_plan_restaurants(planID):
    
    if request.method == "POST":
        # fire off if user presses the Add Restaurant button
        if request.form.get("insertTouringPlanRestaurant"):
            # grab user form inputs
            planID = request.form["planID"]
            restaurantID = request.form["restaurantID"]


            query = "INSERT INTO TouringPlansHasRestaurants (TouringPlansplanID, RestaurantsrestaurantID ) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (planID, restaurantID ))
            mysql.connection.commit()

            # redirect back to touring_plans page
            return redirect("/touring_plans")

    # Grab Touring Plans data so we send it to our template to display
    if request.method == "GET":

        # mySQL query to grab a Single Touring Plan
        query = "SELECT visitDate, planName, Parks.parkName AS parkName, Visitors.visitorName AS visitorName FROM TouringPlans INNER JOIN Parks ON TouringPlans.parkID = Parks.parkID INNER JOIN Visitors on TouringPlans.visitorID = Visitors.visitorID WHERE planID = %s" % (planID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # mySQL query to grab visitor id/name data for our dropdown
        query3 = "SELECT visitorID, visitorName FROM Visitors;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        visitor_data = cur.fetchall()

        # mySQL query to grab restaurant id/name data for our dropdown
        query4 = "SELECT restaurantID, restaurantName FROM Restaurants;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        restaurant_data = cur.fetchall()

        # mySQL query to grab M:N for our dropdown
        query5 = "SELECT TouringPlansplanID, RestaurantsrestaurantID FROM TouringPlansHasRestaurants;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        restaurant_plan_data = cur.fetchall()

        # render touring_plan_restaurants page passing our query data and parks data to the edit_rides template
        return render_template("touring_plan_restaurants.j2", data=data, parks=parks_data, visitors=visitor_data, restaurants=restaurant_data, restaurant_plan=restaurant_plan_data)

# route to get and add rides to the TouringPlan
@app.route("/touring_plan_rides/<int:planID>", methods=["POST", "GET"])
def touring_plan_rides(planID):
    
    if request.method == "POST":

        # fire off if user presses the Add Ride button
        if request.form.get("insertTouringPlanRide"):
            # grab user form inputs
            planID = request.form["planID"]
            rideID = request.form["rideID"]

            query = "INSERT INTO TouringPlansHasRides (planID, ridetID ) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (planID, rideID ))
            mysql.connection.commit()

            # redirect back to touring_plans page
            return redirect("/touring_plans")

    # Grab Touring Plans data so we send it to our template to display
    if request.method == "GET":

        # mySQL query to grab a Single Touring Plan
        query = "SELECT visitDate, planName, Parks.parkName AS parkName, Visitors.visitorName AS visitorName FROM TouringPlans INNER JOIN Parks ON TouringPlans.parkID = Parks.parkID INNER JOIN Visitors on TouringPlans.visitorID = Visitors.visitorID WHERE planID = %s" % (planID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # mySQL query to grab visitor id/name data for our dropdown
        query3 = "SELECT visitorID, visitorName FROM Visitors;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        visitor_data = cur.fetchall()

        # mySQL query to grab ride id/name data for our dropdown
        query4 = "SELECT rideID, rideName FROM Rides;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        ride_data = cur.fetchall()

        # render edit_rides page passing our query data and parks data to the edit_rides template
        return render_template("touring_plans.j2", data=data, parks=parks_data, visitors=visitor_data, rides=ride_data)

# route to display a single Touring Plan with all restaurants and rides chosen for that Touring Plan
@app.route("/plan_view/<int:planID>", methods=["GET"])
def plan_view(planID):

     # Grab TouringPlan data so we send it to our template to display
    if request.method == "GET":

        # mySQL query to grab a Single Touring Plan
        query = "SELECT visitDate, planName, Parks.parkName AS parkName, Visitors.visitorName AS visitorName FROM TouringPlans INNER JOIN Parks ON TouringPlans.parkID = Parks.parkID INNER JOIN Visitors on TouringPlans.visitorID = Visitors.visitorID WHERE planID = %s" % (planID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # mySQL query to grab visitor id/name data for our dropdown
        query3 = "SELECT visitorID, visitorName FROM Visitors;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        visitor_data = cur.fetchall()

        # mySQL query to grab restaurant id/name data for our dropdown
        query4 = "SELECT restaurantID, restaurantName FROM Restaurants;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        ride_data = cur.fetchall()

        # mySQL query to grab ride id/name data for our dropdown
        query5 = "SELECT * FROM TouringPlansHasRestaurants WHERE RestaurantsRestaurantID = restaurantID;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        ride_plan_data = cur.fetchall()


    return render_template("plan_view.j2", data=data, parks=parks_data, visitors=visitor_data, rides=ride_data, ride_plans=ride_plan_data)
# Listener

if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=9008, debug=True)