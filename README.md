# Car Website Project
<img width="960" alt="p1" src="https://github.com/Munkh09/cs157a-car-market/assets/143208888/291892bb-5a55-4638-be71-e68118d965f7">
<img width="960" alt="p2" src="https://github.com/Munkh09/cs157a-car-market/assets/143208888/bd4d19d3-2526-429f-9a08-6cae039a503a">
<img width="960" alt="p3" src="https://github.com/Munkh09/cs157a-car-market/assets/143208888/1edf0eb6-570f-4e43-a83f-efdc1d5c99d2">
<img width="960" alt="p4" src="https://github.com/Munkh09/cs157a-car-market/assets/143208888/577034de-51b0-44af-8841-a47b3deda471">
<img width="960" alt="p5" src="https://github.com/Munkh09/cs157a-car-market/assets/143208888/5c0f8461-2122-40ef-b278-bcbdfcdeb100">
<img width="960" alt="p6" src="https://github.com/Munkh09/cs157a-car-market/assets/143208888/ab592b67-f36a-4199-94e8-842cfccf1506">
<img width="959" alt="p7" src="https://github.com/Munkh09/cs157a-car-market/assets/143208888/98004255-d9fa-4a65-8606-d7f0913dbf40">
<img width="960" alt="p8" src="https://github.com/Munkh09/cs157a-car-market/assets/143208888/eed3aab3-79c3-45c0-9cc8-52a8923cc885">

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
  
- **Database Design, Normalization, DDL, Management**: Munkh-Erdene

- **Database Population and Java Integration**: Munkh-Erdene

- **Documentation**: All team members



