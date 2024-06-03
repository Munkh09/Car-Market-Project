# Car Website Project

## Team members: Abel Seno, Jared Soliven, Jugraj Pandher, Brian Blockmon, Munkh-Erdene Khuderbaatar

## Overview

The Car Website Project is a web application designed to facilitate the buying and selling of cars online. Users can register, browse listings, post listings, and interact with other users to complete transactions. This README provides instructions on how to set up and compile the project, as well as details on the division of work among team members.

## Setup and Compilation

### Prerequisites
- Python
- Flask
- Java Development Kit (JDK) version 8 or higher
- MySQL Database Server
- Maven (for Java dependency management)

### Steps to Set Up the Project

1. Clone the repository to your local machine:

https://github.com/jaredsoliven/cs157a-car-market.git

2. Set up the MySQL database:
- Create a new database named `cars`.
- Import the provided SQL schema file `CREATE.sql` to create the necessary tables.

3. Populate Database:
- Import the project into your preferred Java IDE (e.g., IntelliJ IDEA, Eclipse).
- Configure MySQL Database:
  - Create a MySQL database named `cars`.
  - Adjust the database connection details in the `Populate.java` file:
    - Set the `url` variable to your MySQL database URL.
    - Set the `mySQLuserName` and `mySQLpassword` variables to your MySQL username and password.
- Compile and run the `Populate.java` file to populate the database.
- Ensure that the necessary MySQL connector JAR file is included in your project's dependencies.

4. Install Dependencies

Navigate to the project directory and install the required Python packages using pip:

pip install Flask jaydebeapi


## Setup Flask Environment

To set up the Flask environment for the Car Website Project, follow these steps:

1. Create a virtual environment for your Flask project. Navigate to your project directory in the terminal and run the following command:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment. Depending on your operating system, the commands to activate the virtual environment may vary:

    - For Windows:

        ```bash
        venv\Scripts\activate
        ```

    - For macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

3. Install Flask and other dependencies. While the virtual environment is activated, use pip to install Flask and any other required packages listed in your project's requirements.txt file:

    ```bash
    pip install -r requirements.txt
    ```

4. Once the dependencies are installed, you can run the Flask application. Ensure that you are in the project directory and the virtual environment is activated, then execute the following command:

    ```bash
    flask run
    ```

    This command will start the Flask development server, and you should see output indicating that the server is running. By default, the Flask application will be accessible at http://localhost:5000 in your web browser.

5. You can now access the Car Website Project in your web browser and test its functionality.

## Division of Work

The division of work among team members is as follows:

- **Frontend Development**: Jared, Brian
  
- **Backend Development**: Abel, Jugraj, Jared, Munkh-Erdene
  
- **Database Setup and Management**: Munkh-Erdene

- **Java Integration**: Munkh-Erdene

- **Documentation**: All team members



