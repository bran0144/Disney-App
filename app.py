from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_gottk'
app.config['MYSQL_PASSWORD'] = '' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_gottk'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes 

@app.route("/")
def home():
    return render_template("main.j2")


# route for rides page
@app.route("/rides", methods=["POST", "GET"])
def rides():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("insertRide"):
            # grab user form inputs
            rideName = request.form["rideName"]
            parkID = request.form["parkID"]
            heightRestriction = request.form["heightRestriction"]
            lightningLane = request.form["lightningLane"]
            rideLength = request.form["rideLength"]

            # account for null heightRestriction AND lightningLane AND rideLength
            if heightRestriction == "" and lightningLane == "" and rideLength == "":
                # mySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Rides (rideName, parkID) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID))
                mysql.connection.commit()
            
            # account for null heightRestriction and null lightningLane
            elif heightRestriction == "" and lightningLane == "":
                query = "INSERT INTO Rides (rideName, parkID, rideLength) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, rideLength))
                mysql.connection.commit()

            # account for null heightRestriction and null rideLength
            elif heightRestriction == "" and rideLength == "":
                query = "INSERT INTO Rides (rideName, parkID, lightningLane) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane))
                mysql.connection.commit()

            # account for null lightningLane and null rideLength
            elif lightningLane == "" and rideLength == "":
                query = "INSERT INTO Rides (rideName, parkID, heightRestriction) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction))
                mysql.connection.commit()

            # account for null heightRestriction
            elif heightRestriction == "":
                query = "INSERT INTO Rides (rideName, parkID, lightningLane, rideLength) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, rideLength))
                mysql.connection.commit()

            # account for null lightningLane
            elif lightningLane == "":
                query = "INSERT INTO Rides (rideName, parkID, heightRestriction, rideLength) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, rideLength))
                mysql.connection.commit()

            # account for null rideLength
            elif rideLength == "":
                query = "INSERT INTO Rides (rideName, parkID, heightRestriction, lightningLane) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, lightningLane))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Rides (rideName, parkID, heightRestriction, lightningLane, rideLength) VALUES (%s, %s,%s,%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, lightningLane, rideLength))
                mysql.connection.commit()

            # redirect back to rides page
            return redirect("/rides")

    # Grab Rides data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the rides in Rides
        query = "SELECT Rides.rideID, rideName, heightRestriction, lightningLane, rideLength, Parks.parkName AS park FROM Rides LEFT JOIN Parks ON Rides.parkID = Parks.parkID;"
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
# we want to pass the 'id' value of that ride on button click (see HTML) via the route
@app.route("/delete_ride/<int:id>")
def delete_ride(id):
    # mySQL query to delete the ride with our passed id
    query = "DELETE FROM Rides WHERE rideID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/rides")


# route for edit functionality, updating the attributes of a ride in Rides
# similar to our delete route, we want to the pass the 'id' value of that ride on button click (see HTML) via the route
@app.route("/edit_ride/<int:id>", methods=["POST", "GET"])
def edit_ride(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Rides WHERE rideID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
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
        if request.form.get("edit_ride"):
            # grab user form inputs
            rideID = request.form["rideID"]
            rideName = request.form["rideName"]
            heightRestriction = request.form["heightRestriction"]
            lightningLane = request.form["lightningLane"]
            parkID = request.form["parkID"]
            rideLength = request.form["rideLength"]

            # account for null heightRestriction AND lightningLane AND rideLength
            if heightRestriction == "" and lightningLane == "" and rideLength == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.heightRestriction = NULL, Rides.lightningLane = NULL, Rides.rideLength = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, rideID))
                mysql.connection.commit()

            # account for null heightRestriction AND lightningLane
            elif heightRestriction == "" and lightningLane == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.rideLength = %s, Rides.heightRestriction = NULL, Rides.lightningLane = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, rideLength, rideID))
                mysql.connection.commit()

            # account for null heightRestriction AND rideLength
            elif heightRestriction == "" and rideLength == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.lightningLane = %s, Rides.heightRestriction = NULL, Rides.rideLength = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, rideID))
                mysql.connection.commit()

            # account for null rideLength AND lightningLane
            elif lightningLane == "" and rideLength == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.heightRestriction = %s, Rides.lightningLane = NULL, Rides.rideLength = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, rideID))
                mysql.connection.commit()
            
            # account for null lightningLane
            elif lightningLane == "" :
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.heightRestriction = %s, Rides.rideLength = %s, Rides.lightningLane = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, rideLength, rideID))
                mysql.connection.commit()

            # account for null heightRestriction
            elif heightRestriction == "" :
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.lightningLane = %s, Rides.rideLength = %s, Rides.heightRestriction = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, rideLength, rideID))
                mysql.connection.commit()

            # account for null rideLength
            elif rideLength == "" :
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.lightningLane = %s, Rides.heightRestriction = %s, Rides.rideLength = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, heightRestriction, rideID))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Rides SET Rides.rideName= %s, Rides.parkID = %s, Rides.lightningLane = %s, Rides.heightRestriction = %s Rides.rideLength = %s WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, heightRestriction, rideLength, rideID))
                mysql.connection.commit()

            # redirect back to rides page after we execute the update query
            return redirect("/rides")

# route for parks page
@app.route("/parks", methods=["POST", "GET"])
def parks():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("insertPark"):
            # grab user form inputs
            parkName = request.form["parkName"]
            parkHours = request.form["parkHours"]
            nighttimeShow = request.form["nighttimeShow"]

            # account for null parkHours AND nighttimeShow
            if parkHours  == "" and nighttimeShow == "":
                # mySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Parks (parkName) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkName))
                mysql.connection.commit()
            
            # account for null parkHours
            elif parkHours == "":
                query = "INSERT INTO Parks (parkName, nighttimeShow) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkName, nighttimeShow))
                mysql.connection.commit()

            # account for null nighttimeShow
            elif nighttimeShow == "":
                query = "INSERT INTO Parks (parkName, parkHours) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkName, parkHours))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Parks (parkName, parkHours, nighttimeShow) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkName, parkHours, nighttimeShow))
                mysql.connection.commit()

            # redirect back to parks page
            return redirect("/parks")

    # Grab Parks data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the parks in Parks
        query = "SELECT Parks.parkID, parkName, parkHours, nighttimeShow;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render parks page
        return render_template("parks.j2", data=data)


# route for parks page
@app.route("/restaurants", methods=["POST", "GET"])
def restaurants():
    # Separate out the request methods, in this case this is for a POST
    # insert a Restaurant into the Restaurant entity
    if request.method == "POST":
        # fire off if user presses the Add Restaurant button
        if request.form.get("insertRestaurant"):
            # grab user form inputs
            restaurantName = request.form["restaurantName"]
            parkID = request.form["parkID"]
            reservationsAccepted = request.form["reservationsAccepted"]
            characterDining = request.form["characterDining"]

            # account for null parkID AND reservationsAccepted AND characterDining
            if parkID  == "None" and reservationsAccepted == "" and characterDining== "":
                # mySQL query to insert a new restaurant into Restaurants with our form inputs
                query = "INSERT INTO Restaurants (restaurantName) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (restaurantName))
                mysql.connection.commit()
            
            # account for null reservationsAccepted AND characterDining
            elif reservationsAccepted == "" and characterDining == "":
                query = "INSERT INTO Restaurants (restaurantName, parkID) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (restaurantName, parkID))
                mysql.connection.commit()

            # account for null parkID AND reservationsAccepted
            elif parkID  == "None" and reservationsAccepted == "":
                query = "INSERT INTO Restaurants (restaurantName, characterDining) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (restaurantName, characterDining))
                mysql.connection.commit()

            # account for null parkID AND characterDining
            elif parkID  == "None" and characterDining == "":
                query = "INSERT INTO Restaurants (restaurantName, reservationsAccepted) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (restaurantName, reservationsAccepted))
                mysql.connection.commit()
            
            # account for null parkID
            elif parkID  == "None":
                query = "INSERT INTO Restaurants (restaurantName, reservationsAccepted, characterDining) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (restaurantName, reservationsAccepted, characterDining))
                mysql.connection.commit()

            # account for null reservationsAccepted
            elif reservationsAccepted == "None":
                query = "INSERT INTO Restaurants (restaurantName, parkID, characterDining) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (restaurantName, parkID, characterDining))
                mysql.connection.commit()

            # account for null characterDining
            elif characterDining == "None":
                query = "INSERT INTO Restaurants (restaurantName, parkID, reservationsAccepted) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (restaurantName, parkID, reservationsAccepted))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Restaurants (restaurantName, parkID, reservationsAccepted, characterDining) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (restaurantName, parkID, reservationsAccepted, characterDining))
                mysql.connection.commit()

            # redirect back to parks page
            return redirect("/restaurants")

    # Grab Parks data so we send it to our template to display
    if request.method == "GET":
         # mySQL query to grab all the rides in Rides
        query = "SELECT Restaurants.restaurantID, restaurantName, reservationsAccepted, characterDining, Parks.parkName AS park FROM Restaurants LEFT JOIN Parks ON Restaurants.parkID = Parks.parkID;"
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

# route for parks page
@app.route("/visitors", methods=["POST", "GET"])
def visitors():
    # Separate out the request methods, in this case this is for a POST
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
        query = "SELECT Visitors.visitorID, visitorName, height, visitorEmail;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render parks page
        return render_template("visitors.j2", data=data)

# route for rides page
@app.route("/touring_plans", methods=["POST", "GET"])
def touring_plans():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("insertTouringPlan"):
            # grab user form inputs
            planName = request.form["planName"]
            parkID = request.form["parkID"]
            visitorID = request.form["visitorID"]
            visitDate = request.form["visitDate"]


            # account for null visitDate AND planName
            if visitDate == "" and planName == "":
                # mySQL query to insert a new plan into TouringPlans with our form inputs
                query = "INSERT INTO TouringPlans (parkID, visitorID) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkID, visitorID))
                mysql.connection.commit()
            
            # account for null visitDate
            elif visitDate == "":
                query = "INSERT INTO TouringPlans (parkID, visitorID, planName) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkID, visitorID, planName))
                mysql.connection.commit()

            # account for null planName
            elif planName == "":
                query = "INSERT INTO TouringPlans (parkID, visitorID, visitDate) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkID, visitorID, visitDate))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO TouringPlans (parkID, visitorID, visitDate, planName ) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (parkID, visitorID, visitDate, planName ))
                mysql.connection.commit()

            # redirect back to rides page
            return redirect("/touring_plans")

    # Grab Rides data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the rides in Rides

        query = "SELECT TouringPlans.planID, visitDate, planName, Parks.parkName AS park, Visitors.visitorName AS visitorName FROM TouringPlans LEFT JOIN Parks ON TouringPlans.parkID = Parks.parkID LEFT JOIN Visitors on TouringPlans.visitorID = Visitors.visitorID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # mySQL query to grab ride id/name data for our dropdown
        query3 = "SELECT visitorID, visitorName FROM Visitors;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        visitor_data = cur.fetchall()

        # render edit_rides page passing our query data and parks data to the edit_rides template
        return render_template("touring_plans.j2", data=data, parks=parks_data, visitors=visitor_data)

# Listener

if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=9001, debug=True)