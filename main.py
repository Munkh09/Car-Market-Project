import datetime

from flask import Flask, render_template, request, session, redirect, url_for

import jaydebeapi

conn = jaydebeapi.connect("com.mysql.cj.jdbc.Driver", # class name of the JDBC driver class for MySQL
                              "jdbc:mysql://localhost:3306/cars", # jdbc:mysql://<hostname>:<port>/<database_name>
                              ["root", "jumanji23"], # [username, pass] MySQL username, password
                              "lib/mysql-connector-j-8.4.0.jar",) # already in file

curs = conn.cursor()

app = Flask(__name__)

app.secret_key = b'secretSessionKey123' # session key

'''
REGULAR FUNCTIONS HERE
'''
def checkSession(user):
    errMsg = ''
    if user == None:
        errMsg = 'Please log in'
        return redirect(url_for('logout'))

'''
START OF RENDERING PAGES
'''
### Login Page
@app.route('/', methods=['POST', 'GET'])  
@app.route('/login', methods=['POST', 'GET'])
def login():
    errMsg = ''
    # user uses login
    if request.method == 'POST' and 'loginEmail' in request.form and 'loginPW' in request.form:
        user = request.form['loginEmail']
        pw = request.form['loginPW']
        # check if input was valid
        if user == '' or pw == '':
            errMsg = 'Please fill out all fields'
            return render_template('login.html', errMsg = errMsg)
        
        
        curs.execute("SELECT email FROM UserAccount WHERE email = ?", (user,))
        user_data = curs.fetchone()
        if not user_data:
            errMsg = 'User not in database'
            return render_template('login.html', errMsg=errMsg)
        else:
            curs.execute("SELECT * FROM UserAccount WHERE email = ? AND pass = ?", (user, pw))
            user_data = curs.fetchone()
            if not user_data: 
                errMsg = 'Invalid email or password'
                return render_template('login.html', errMsg=errMsg)
            else:
                session['user'] = user_data[0]
                return render_template('bookmarks.html', user = session['user'])
                
                
    # user uses registration
    elif request.method == 'POST' and 'signupEmail' in request.form and 'signupPW' in request.form and 'confPW' in request.form:
        # got here, all fields filled out
        # gather data from form
        user = request.form['signupEmail']
        pw = request.form['signupPW']
        confPW = request.form['confPW']
        fn = request.form['signupFN']
        ln = request.form['signupLN']
        # check if form was filled out
        if user == '' or pw == '' or confPW == '' or fn == '' or ln == '':
            errMsg = 'Please fill out all fields'
            return render_template('login.html', errMsg = errMsg)
        
        curs.execute("SELECT email FROM UserAccount WHERE email = ?", (user,))
        user_data = curs.fetchone()
        
        if user_data:
            errMsg = 'User already in database'
            return render_template('login.html', errMsg=errMsg)
        
        if pw != confPW:
            errMsg = 'Passwords do not match'
            return render_template('login.html', errMsg = errMsg)
        
        else:
            print(user)
            curs.execute("INSERT INTO UserAccount (email, pass, firstName, lastName, userName) VALUES (?, ?, ?, ?, ?)", (user, pw, fn, ln, user))
            return render_template('bookmarks.html', user=session['user'])
    return render_template('login.html')
  

### Profile
@app.route('/profile', methods=['POST', 'GET'])  
def profile():
    checkSession(session['user'])

    errMsg = ''

    user = session['user']

    curs.execute("SELECT * FROM UserAccount WHERE email = ?", (user,))
    user_data = curs.fetchone()
    if not user_data:
        errMsg = 'User not in database'


    if request.method == 'POST' and request.form.get('delete_account') == 'true':
        print("deleting account")
        # Check if the request is for deleting the account
            
        #curs.execute("DELETE FROM UserAccount WHERE email = ?", (user,))

        # conn.commit()

        # After deletion, you may want to redirect the user to a different page
        return redirect(url_for('login'))  # Redirect to the home page after deletion
        
    elif request.method == 'POST' and 'pwSignup' in request.form and 'confPW' in request.form and request.form.get('saveChange') == 'save':
        print('updating password')
        newPW = request.form['pwSignup']
        confNewPW = request.form['confPW']
        if newPW != confNewPW:
            errMsg = "Passwords do not match"
            render_template('profile.html', user=user_data, errMsg=errMsg)
        if len(newPW) < 8:
            errMsg = "Password length not long enough"
            render_template('profile.html', user=user_data, errMsg=errMsg)

        query = f"UPDATE UserAccount SET pass='{newPW}' WHERE email='{user}'"
        # Execute the SQL query
        curs.execute(query)
        errMsg = "successfully changed pw"
        print("pw changed")

    return render_template('profile.html', user = user_data, errMsg=errMsg)


## your_post
@app.route('/your_posts', methods=['POST', 'GET'])
def your_posts():
    checkSession(session['user'])
    user = session['user']
    try:

        # on load, SELECT * FROM car_table;
        # Retrieve all car posts except those belonging to the current user
        query = f"SELECT * FROM CarPost WHERE ownerEmail = '{user}'"
        curs.execute(query)
        car_posts = curs.fetchall()
        # conn.close()

        # Search bar function here
        if request.method == 'POST' and 'postSearch' in request.form:
            # Get the search input from the form
            search_input = request.form['postSearch']

            # Construct the SQL query to search across multiple attributes
            query = """
                SELECT * FROM CarPost 
                WHERE ownerEmail != ? AND (
                    plateNumber = ? OR
                    ownerEmail = ? OR
                    model = ?
                )
            """ # add more if needed

            # Execute the SQL query with placeholders for user input
            curs.execute(query, (user, search_input, search_input, search_input))
            car_posts = curs.fetchall()

            # Render the template with the search results
            return render_template('your_posts.html', posts=car_posts, user=user)

            # if user searches for car, SELECT * FROM car_table WHERE carname = ?;


        # filter function here
        elif request.method == 'POST':
            filterList = []

            # Check if color is filled out
            if 'yourpostColor' in request.form:
                color = request.form['yourPostColor']
                if color:  # Check if color is not empty
                    filterList.append(f"outerColor = '{color}'")
            
            # Check if year is filled out
            if 'yourPostYear' in request.form:
                year = request.form['yourPostYear']
                if year:  # Check if color is not empty
                    filterList.append(f"carYear = '{year}'")

            # Check if minMiles and maxMiles are filled out
            if 'yourPostMinMiles' in request.form:
                minMiles = request.form['yourPostMinMiles']
                if minMiles:  # Check if minMiles is not empty
                    filterList.append(f"yourMileage >= {minMiles}")

            if 'yourPostMaxMiles' in request.form:
                maxMiles = request.form['yourPostMaxMiles']
                if maxMiles:  # Check if maxMiles is not empty
                    filterList.append(f"mileage <= {maxMiles}")

            # Check if minPrice and maxPrice are filled out
            if 'yourPostMinPrice' in request.form:
                minPrice = request.form['yourPostMinPrice']
                if minPrice:  # Check if minPrice is not empty
                    filterList.append(f"price >= {minPrice}")

            if 'yourPostMaxPrice' in request.form:
                maxPrice = request.form['yourPostMaxPrice']
                if maxPrice:  # Check if maxPrice is not empty
                    filterList.append(f"price <= {maxPrice}")

            # Check if energyType is filled out
            if 'yourPostEnergyType' in request.form:
                energyType = request.form['yourPostEnergyType']
                if energyType:  # Check if energyType is not empty
                    filterList.append(f"fuel = '{energyType}'")

            # Check if city is filled out
            if 'yourPostCity' in request.form:
                city = request.form['yourPostCity']
                if city:  # Check if city is not empty
                    filterList.append(f"city = '{city}'")

            # Construct the SQL query
            condition = " AND ".join(filterList)
            query = f"SELECT * FROM CarPost WHERE {condition}"

            # Execute the SQL query
            curs.execute(query)
            car_posts = curs.fetchall()
            print(car_posts)
            return render_template('your_posts.html', posts=car_posts, user=user)
        
        elif request.method == 'POST' and 'plateNumber' in request.form:
            seller = request.form['plateNumber']
            query = f"SELECT * FROM CarPost WHERE plateNumber = '{seller}'"
            # Execute the SQL query
            curs.execute(query)
            car_posts = curs.fetchall()

        return render_template('your_posts.html', posts=car_posts, user=user)
        

    except jaydebeapi.Error as e:
        # Handle database errors
        print("Database error:", e)
        return "An error occurred while retrieving car posts. Please try again later."


## Bookmarks
@app.route('/bookmarks', methods=['POST', 'GET'])
def bookmarks():
    checkSession(session['user'])
    user = session['user']

    # on load, SELECT * FROM car_table;
    curs.execute("SELECT * FROM CarPost WHERE bookmarkedBy LIKE ?", ('%' + user + '%',))
    posts = curs.fetchall()
    print("current user", user)
    print("bookmarked amount:", len(posts))

    # Search bar function here
    if request.method == 'POST' and 'bookmarkSearch' in request.form:
        print("search details:", request.form['bookmarkSearch'])
        # if user searches for car, SELECT * FROM car_table WHERE carname = ?;


    # filter function here
    # appends all data into a list. list looks like this filter prefs: ['', '', '', '', '', '', '', '', '', '']
    elif request.method == 'POST' and 'bookmarkColor' in request.form and 'bookmarkMinMiles' in request.form and 'bookmarkMaxMiles' in request.form:
        filterList = list()
        color = request.form['bookmarkColor']
        filterList.append(color)
        minMiles = request.form['bookmarkMinMiles']
        filterList.append(minMiles)
        maxMiles = request.form['bookmarkMaxMiles']
        filterList.append(maxMiles)
        minPrice = request.form['bookmarkMinPrice']
        filterList.append(minPrice)
        maxPrice = request.form['bookmarkMaxPrice']
        filterList.append(maxPrice)
        energyType = request.form['bookmarkEnergyType']
        filterList.append(energyType)
        condition = request.form['bookmarkCondition']
        filterList.append(condition)
        zipCode = request.form['bookmarkZip']
        filterList.append(zipCode)
        city = request.form['bookmarkCity']
        filterList.append(city)
        state = request.form['bookmarkState']
        filterList.append(state)
        print('filter prefs:', filterList)
        # SELECT * FROM car_table WHERE ?,?,?,?,etc
    
    return render_template('bookmarks.html', posts = posts)


@app.route('/bookmarks/<car_id>', methods=['POST', 'GET'])
def removeBookmark(car_id):
    checkSession(session['user'])
    user = session['user']

    print("bookmarking car", car_id)

    if(car_id == None):
        print("made it here")
        pass # redirect or don't do anthingn with useless value
    else: # remove bookmark
        # check if user already bookmarked
        query = f'SELECT * FROM CarPost WHERE bookmarkedBy LIKE "%{user}%" AND plateNumber = "{car_id}"'
        curs.execute(query)
        alreadyIn = curs.fetchall()
        if len(alreadyIn) > 0: # if user did not bookmark this car
            query = f'UPDATE CarPost SET bookmarkedBy = REPLACE(bookmarkedBy, "{user}", "") WHERE plateNumber="{car_id}"'
            curs.execute(query)
            print("query successful")
        else:
            print("user already bookmarked this post")
        #print("bookmarked?", alreadyIn)



    # on load, SELECT * FROM car_table;
    curs.execute("SELECT * FROM CarPost WHERE bookmarkedBy LIKE ?", ('%' + user + '%',))
    posts = curs.fetchall()
    print("current user", user)
    print("bookmarked amount:", len(posts))

    # Search bar function here
    if request.method == 'POST' and 'bookmarkSearch' in request.form:
        print("search details:", request.form['bookmarkSearch'])
        # if user searches for car, SELECT * FROM car_table WHERE carname = ?;


    # filter function here
    # appends all data into a list. list looks like this filter prefs: ['', '', '', '', '', '', '', '', '', '']
    elif request.method == 'POST' and 'bookmarkColor' in request.form and 'bookmarkMinMiles' in request.form and 'bookmarkMaxMiles' in request.form:
        filterList = list()
        color = request.form['bookmarkColor']
        filterList.append(color)
        minMiles = request.form['bookmarkMinMiles']
        filterList.append(minMiles)
        maxMiles = request.form['bookmarkMaxMiles']
        filterList.append(maxMiles)
        minPrice = request.form['bookmarkMinPrice']
        filterList.append(minPrice)
        maxPrice = request.form['bookmarkMaxPrice']
        filterList.append(maxPrice)
        energyType = request.form['bookmarkEnergyType']
        filterList.append(energyType)
        condition = request.form['bookmarkCondition']
        filterList.append(condition)
        zipCode = request.form['bookmarkZip']
        filterList.append(zipCode)
        city = request.form['bookmarkCity']
        filterList.append(city)
        state = request.form['bookmarkState']
        filterList.append(state)
        print('filter prefs:', filterList)
        # SELECT * FROM car_table WHERE ?,?,?,?,etc
    
    return render_template('bookmarks.html', posts = posts)

## Bought Cars
@app.route('/bought_cars', methods=['POST', 'GET'])
def bought_cars():
    checkSession(session['user'])
    user = session['user']
    # Retrieve all car posts except those belonging to the current user
    query = "SELECT * FROM Purchases WHERE purchaserEmail = ?"
    curs.execute(query, (user,))
    bought_cars = curs.fetchall()

    # on load, SELECT * FROM car_table;

    if request.method == 'POST' and 'boughtSearch' in request.form:
        boughtSearch = request.form["boughtSearch"]
        query = """
            SELECT * FROM Sales 
            WHERE (sellerEmail = ? OR plateNumber = ?)"""
        
        curs.execute(query, (boughtSearch, boughtSearch))

        bought_filter = curs.fetchall()

        return render_template('bought_cars.html', user=user, posts=bought_filter)

    elif request.method == 'POST' and 'boughtMinPrice' in request.form and 'boughtMaxPrice' in request.form:
        filterList = list()
        minPrice = request.form['boughtMinPrice']
        if minPrice:  # Check if minPrice is not empty
            filterList.append(f"purchasePrice >= {minPrice}")
        
        maxPrice = request.form['boughtMinPrice']
        if maxPrice:  # Check if maxPrice is not empty
            filterList.append(f"purchasePrice <= {maxPrice}")

        date = request.form['boughtDate']
        if date:  # Check if maxPrice is not empty
            filterList.append(f"purchaseDate = '{date}'")

        # Construct the SQL query
        condition = " AND ".join(filterList)
        query = f"SELECT * FROM Purchases WHERE {condition}"

        return render_template('bought_cars.html', user=user, posts=bought_filter)

    elif request.method == 'POST':
        plate_number = request.form['plateNumber']
        owner_email = request.form['ownerEmail']
        print(plate_number, owner_email)

        # SELECT CarPost
        curs.execute("SELECT * FROM CarPost WHERE plateNumber = ? AND ownerEmail = ?", (plate_number, owner_email))
        purchased_car = curs.fetchall()

        # INSERT to purchase table
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        curs.execute("INSERT INTO Purchases (purchaserEmail, plateNumber, purchasePrice, sellerEmail, purchaseDate) VALUES (?, ?, ?, ?, ?)", (user, purchased_car[0][0], purchased_car[0][8], purchased_car[0][1], current_date))
        # conn.commit() # Set to true already

        # DELETE POST (post is not available anymore)
        curs.execute("DELETE FROM CarPost WHERE plateNumber = ? AND ownerEmail = ?", (plate_number, owner_email))

        # Need to insert into sales
        curs.execute("INSERT INTO Sales (sellerEmail, plateNumber, purchaserEmail, salesPrice, sellDate) VALUES (?, ?, ?, ?, ?)", (purchased_car[0][1], purchased_car[0][0], user, purchased_car[0][8], current_date))
        # conn.commit() # Set to true already

        # Get all purchase post
        curs.execute("SELECT * FROM  Purchases WHERE purchaserEmail = ?", (user,))
        posts = curs.fetchall()

        return render_template('bought_cars.html', user=user, posts=posts)

    return render_template('bought_cars.html', posts=bought_cars, user=user)
## Owned Cars
@app.route('/owned_cars', methods=['POST', 'GET'])
def owned_cars():
    checkSession(session['user'])
    try:
        # Fetch data from CarPost table where ownerEmail matches current user session email
        curs.execute("""
            SELECT plateNumber, price, CURDATE() AS currentDate
            FROM CarPost
            WHERE ownerEmail = ?
        """, (session['user'],))
        carpost_data = curs.fetchall()

        # Fetch data from Purchases table
        curs.execute("""
            SELECT plateNumber, purchasePrice, purchaseDate
            FROM Purchases
            WHERE purchaserEmail = ?
        """, (session['user'],))
        purchases_data = curs.fetchall()

        # Combine data from CarPost and Purchases tables
        posts = carpost_data + purchases_data

        curs.execute("""
            SELECT plateNumber, salesPrice, sellDate, purchaserEmail
            FROM Sales
            WHERE sellerEmail = ?
        """, (session['user'],))

        previousCars = curs.fetchall()

        # Search bar function here
        if request.method == 'POST' and 'ownedSearch' in request.form:
            search_term = request.form['ownedSearch']
            filtered_posts = [post for post in posts if search_term in post[0]]  # Assuming the search term matches the plateNumber
            filtered_previous = [car for car in previousCars if search_term in car[0]]
            return render_template('owned_cars.html', posts=filtered_posts, prevPosts=filtered_previous)

        # Filter function here
        elif request.method == 'POST' and ('ownedMinPrice' in request.form or 'ownedMaxPrice' in request.form):
            min_price = request.form.get('ownedMinPrice', None)
            max_price = request.form.get('ownedMaxPrice', None)

            filtered_previous = []

            # Apply filters based on provided price range
            if min_price is not None and max_price is not None:
                filtered_posts = [post for post in posts if min_price <= post[1] <= max_price]
                filtered_previous = [car for car in previousCars if min_price <= car[1] <= max_price]
            elif min_price is not None:
                filtered_posts = [post for post in posts if post[1] >= min_price]
                filtered_previous = [car for car in previousCars if car[1] >= min_price]
            elif max_price is not None:
                filtered_posts = [post for post in posts if post[1] <= max_price]
                filtered_previous = [car for car in previousCars if car[1] <= max_price]
            else:
                filtered_posts = posts  # If no price range is provided, return all posts
                filtered_previous = previousCars

            return render_template('owned_cars.html', posts=filtered_posts, prevPosts=filtered_previous)

        return render_template('owned_cars.html', posts=posts, prevPosts=previousCars)

    except jaydebeapi.Error as e:
        # Handle database errors
        print("Database error:", e)
        # Redirect the user to an error page or any other relevant page
        return redirect(url_for('error_page'))




## Post
@app.route('/post', methods=['POST', 'GET'])
def post():
    checkSession(session['user'])
    user = session['user']
    try:

        # on load, SELECT * FROM car_table;
        # Retrieve all car posts except those belonging to the current user
        query = f"SELECT * FROM CarPost WHERE ownerEmail != '{user}' LIMIT 30"
        curs.execute(query)
        car_posts = curs.fetchall()
        # conn.close()

        # Search bar function here
        if request.method == 'POST' and 'postSearch' in request.form:
            # Get the search input from the form
            search_input = request.form['postSearch']

            # Construct the SQL query to search across multiple attributes
            query = """
                SELECT * FROM CarPost 
                WHERE ownerEmail != ? AND (
                    plateNumber = ? OR
                    ownerEmail = ? OR
                    model = ?
                )
            """ # add more if needed

            # Execute the SQL query with placeholders for user input
            curs.execute(query, (user, search_input, search_input, search_input))
            car_posts = curs.fetchall()

            # Render the template with the search results
            return render_template('post.html', posts=car_posts, user=user)

            # if user searches for car, SELECT * FROM car_table WHERE carname = ?;


        # filter function here
        elif request.method == 'POST':
            filterList = []

            # Check if color is filled out
            if 'postColor' in request.form:
                color = request.form['postColor']
                if color:  # Check if color is not empty
                    filterList.append(f"outerColor = '{color}'")
            
            # Check if year is filled out
            if 'postYear' in request.form:
                color = request.form['postYear']
                if color:  # Check if color is not empty
                    filterList.append(f"carYear = '{color}'")

            # Check if minMiles and maxMiles are filled out
            if 'postMinMiles' in request.form:
                minMiles = request.form['postMinMiles']
                if minMiles:  # Check if minMiles is not empty
                    filterList.append(f"mileage >= {minMiles}")

            if 'postMaxMiles' in request.form:
                maxMiles = request.form['postMaxMiles']
                if maxMiles:  # Check if maxMiles is not empty
                    filterList.append(f"mileage <= {maxMiles}")

            # Check if minPrice and maxPrice are filled out
            if 'postMinPrice' in request.form:
                minPrice = request.form['postMinPrice']
                if minPrice:  # Check if minPrice is not empty
                    filterList.append(f"price >= {minPrice}")

            if 'postMaxPrice' in request.form:
                maxPrice = request.form['postMaxPrice']
                if maxPrice:  # Check if maxPrice is not empty
                    filterList.append(f"price <= {maxPrice}")

            # Check if energyType is filled out
            if 'postEnergyType' in request.form:
                energyType = request.form['postEnergyType']
                if energyType:  # Check if energyType is not empty
                    filterList.append(f"fuel = '{energyType}'")

            # Check if city is filled out
            if 'postCity' in request.form:
                city = request.form['postCity']
                if city:  # Check if city is not empty
                    filterList.append(f"city = '{city}'")

            # Construct the SQL query
            condition = " AND ".join(filterList)
            query = f"SELECT * FROM CarPost WHERE {condition} LIMIT 30"

            # Execute the SQL query
            curs.execute(query)
            car_posts = curs.fetchall()
            print(car_posts)
            return render_template('post.html', posts=car_posts, user=user)

        return render_template('post.html', posts=car_posts, user=user)
        

    except jaydebeapi.Error as e:
        # Handle database errors
        print("Database error:", e)
        return "An error occurred while retrieving car posts. Please try again later."

@app.route('/post/<car_id>', methods=['POST', 'GET'])
def addPostToBookMarks(car_id):
    checkSession(session['user'])
    user = session['user']
    print("bookmarking car", car_id)

    if(car_id == None):
        print("made it here")
        pass # redirect or don't do anthingn with useless value
    else: # add bookmark
        # check if user already bookmarked
        query = f'SELECT * FROM CarPost WHERE bookmarkedBy LIKE "%{user}%" AND plateNumber = "{car_id}"'
        curs.execute(query)
        alreadyIn = curs.fetchall()
        if len(alreadyIn) == 0: # if user did not bookmark this car
            query = f'UPDATE CarPost SET bookmarkedBy = CONCAT(bookmarkedBy, "{user}") WHERE plateNumber="{car_id}"'
            curs.execute(query)
            print("query successful")
        else:
            print("user already bookmarked this post")
        #print("bookmarked?", alreadyIn)
    try:

        # on load, SELECT * FROM car_table;
        # Retrieve all car posts except those belonging to the current user
        query = f"SELECT * FROM CarPost WHERE ownerEmail != '{user}' LIMIT 30"
        curs.execute(query)
        car_posts = curs.fetchall()
        # conn.close()

        # Search bar function here
        if request.method == 'POST' and 'postSearch' in request.form:
            # Get the search input from the form
            search_input = request.form['postSearch']

            # Construct the SQL query to search across multiple attributes
            query = """
                SELECT * FROM CarPost 
                WHERE ownerEmail != ? AND (
                    plateNumber = ? OR
                    ownerEmail = ? OR
                    model = ?
                )
            """ # add more if needed

            # Execute the SQL query with placeholders for user input
            curs.execute(query, (user, search_input, search_input, search_input))
            car_posts = curs.fetchall()

            # Render the template with the search results
            return render_template('post.html', posts=car_posts, user=user)

            # if user searches for car, SELECT * FROM car_table WHERE carname = ?;


        # filter function here
        elif request.method == 'POST':
            filterList = []

            # Check if color is filled out
            if 'postColor' in request.form:
                color = request.form['postColor']
                if color:  # Check if color is not empty
                    filterList.append(f"outerColor = '{color}'")

            # Check if year is filled out
            if 'postYear' in request.form:
                color = request.form['postYear']
                if color:  # Check if color is not empty
                    filterList.append(f"carYear = '{color}'")

            # Check if minMiles and maxMiles are filled out
            if 'postMinMiles' in request.form:
                minMiles = request.form['postMinMiles']
                if minMiles:  # Check if minMiles is not empty
                    filterList.append(f"mileage >= {minMiles}")

            if 'postMaxMiles' in request.form:
                maxMiles = request.form['postMaxMiles']
                if maxMiles:  # Check if maxMiles is not empty
                    filterList.append(f"mileage <= {maxMiles}")

            # Check if minPrice and maxPrice are filled out
            if 'postMinPrice' in request.form:
                minPrice = request.form['postMinPrice']
                if minPrice:  # Check if minPrice is not empty
                    filterList.append(f"price >= {minPrice}")

            if 'postMaxPrice' in request.form:
                maxPrice = request.form['postMaxPrice']
                if maxPrice:  # Check if maxPrice is not empty
                    filterList.append(f"price <= {maxPrice}")

            # Check if energyType is filled out
            if 'postEnergyType' in request.form:
                energyType = request.form['postEnergyType']
                if energyType:  # Check if energyType is not empty
                    filterList.append(f"fuel = '{energyType}'")

            # Check if city is filled out
            if 'postCity' in request.form:
                city = request.form['postCity']
                if city:  # Check if city is not empty
                    filterList.append(f"city = '{city}'")

            # Construct the SQL query
            condition = " AND ".join(filterList)
            query = f"SELECT * FROM CarPost WHERE {condition} LIMIT 30"

            # Execute the SQL query
            curs.execute(query)
            car_posts = curs.fetchall()
            print(car_posts)
            return render_template('post.html', posts=car_posts, user=user)

        return render_template('post.html', posts=car_posts, user=user)


    except jaydebeapi.Error as e:
        # Handle database errors
        print("Database error:", e)
        return "An error occurred while retrieving car posts. Please try again later."

## Sales
@app.route('/sales', methods=['POST', 'GET'])
def sales():
    checkSession(session['user'])
    userEmail = session['user']
    try:
        # on load, SELECT * FROM car_table;
        curs.execute("SELECT * FROM Sales WHERE sellerEmail = ?", (userEmail,))
        posts = curs.fetchall()
        # Search bar function here
        if request.method == 'POST' and 'soldSearch' in request.form:
            print("search details:", request.form['soldSearch'])
            # if user searches for car, SELECT * FROM car_table WHERE carname = ?;
            search_term = request.form['soldSearch']
            # Search within the user's bought cars for the provided model name
            curs.execute("SELECT * FROM Sales WHERE sellerEmail = ? AND plateNumber = ?", (userEmail, f'%{search_term}%'))
            posts = curs.fetchall()
            return render_template('sales.html', posts=posts)
        # filter function here
        # appends all data into a list. list looks like this filter prefs: ['', '', '', '', '', '', '', '', '', '']
        elif request.method == 'POST' and 'soldColor' in request.form and 'soldMinMiles' in request.form and 'soldMaxMiles' in request.form:
            filterList = list()
            color = request.form['soldColor']
            filterList.append(color)
            minMiles = request.form['soldMinMiles']
            filterList.append(minMiles)
            maxMiles = request.form['soldMaxMiles']
            filterList.append(maxMiles)
            minPrice = request.form['soldMinPrice']
            filterList.append(minPrice)
            maxPrice = request.form['soldMaxPrice']
            filterList.append(maxPrice)
            energyType = request.form['soldEnergyType']
            filterList.append(energyType)
            condition = request.form['soldCondition']
            filterList.append(condition)
            zipCode = request.form['soldZip']
            filterList.append(zipCode)
            city = request.form['soldCity']
            filterList.append(city)
            state = request.form['soldState']
            filterList.append(state)
            print('filter prefs:', filterList)
            # SELECT * FROM car_table WHERE ?,?,?,?,etc
            query = "SELECT * FROM Sales WHERE sellerEmail = ?"
            conditions = []
            params = [userEmail]
            if color:
                conditions.append("outerColor = ?")
                params.append(color)
            if minMiles:
                conditions.append("mileage >= ?")
                params.append(minMiles)
            if maxMiles:
                conditions.append("mileage <= ?")
                params.append(maxMiles)
            if minPrice:
                conditions.append("price >= ?")
                params.append(minPrice)
            if maxPrice:
                conditions.append("price <= ?")
                params.append(maxPrice)
            if energyType:
                conditions.append("fuel = ?")
                params.append(energyType)
            # if condition:
            # conditions.append("condition = ?")
            # params.append(condition)
            # if zipCode:
            #    conditions.append("zipCode = ?")
            #    params.append(zipCode)
            if city:
                conditions.append("city = ?")
                params.append(city)
            # if state:
            # conditions.append("state = ?")
            # params.append(state)

            if conditions:
                query += " AND " + " AND ".join(conditions)

            curs.execute(query, params)
            posts = curs.fetchall()
            return render_template('sales.html', posts=posts)
        # Now perform the database query here
        # For example:
        # curs.execute("SELECT * FROM CarTable WHERE ...")
        # car_data = curs.fetchall()

        return render_template('sales.html', posts = posts)

    except jaydebeapi.Error as e:
        # Handle database errors
        print("Database error:", e)
        # Redirect the user to an error page or any other relevant page
        return redirect(url_for('error_page'))


@app.route('/issue', methods=['POST', 'GET'])
def issue():
    checkSession(session['user'])
    user = session['user']
    errMsg = ''

    curs.execute("SELECT * FROM UserAccount WHERE email = ?", (user,))
    user_data = curs.fetchone()
    if not user_data:
        errMsg = 'User not in database'

    curs.execute("SELECT count(*) FROM Issue")
    issueCount = curs.fetchall()
    print(issueCount)
    print(issueCount[0])
    print(issueCount[0][0])
    issueNum = issueCount[0][0] + 2
    print("issue num:", issueNum)


    if request.method == 'POST' and request.form.get('issueBtn') == 'Send':
        print("attempting to submit issue")
        if request.form.get('issueDate') == '' or request.form.get('issueText') == '':
            errMsg = "Please fillout all areas"
            render_template('issue.html', user=user, issueNum=issueNum, errMsg=errMsg)
        else:
            date = request.form.get('issueDate')
            print("date", date)
            issueText = request.form.get('issueText')
            curs.execute("INSERT INTO Issue (issuerEmail, issueId, issueDate, issueText) VALUES (?, ?, ?, ?)", (user, issueNum, date, issueText))
            print("successful issue insert")



    return render_template('issue.html', user=user, issueNum=issueNum, errMsg=errMsg)

## Logout
@app.route('/logout')
def logout():
    errMsg = 'Thanks for using The CS157A Car Market'
    session.pop('user', None)
    session['user'] = None
    return render_template('login.html', errMsg = errMsg)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
