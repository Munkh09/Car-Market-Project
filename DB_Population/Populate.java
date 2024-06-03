import java.sql.*;
import java.time.LocalDate;
import java.util.Random;

public class Populate {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/cars";  //localhost bc the todo_db is in my local computer machine and the default port is 3306
        String mySQLuserName = "root";  //to see the username for my Mysql account enter SELECT USER(); in the mysql
        String mySQLpassword = "Munkh2000.";  //my mysql password

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");   //access this class in the project file in External Libraries
            Connection connection = DriverManager.getConnection(url, mySQLuserName, mySQLpassword);  //connect to the db

            Random random = new Random();

            //Names of Current Users
            String[] firstNames = {
                    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas",
                    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
                    "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark", "Paul", "Steven", "Andrew", "Kenneth",
                    "Emily", "Lisa", "Nancy", "Betty", "Dorothy", "Sandra", "Ashley", "Kimberly", "Donna", "Carol",
                    "George", "Joshua", "Kevin", "Brian", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan"
            };
            String[] lastNames = {
                    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
                    "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King",
                    "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
                    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins"
            };

            String[] models = {"prius", "camry", "corolla", "sienna", "rav4", "4runner", "avensis", "fortuner", "highlander", "hilux", "sequioa", "tacoma", "tundra", "venza", "verso", "yaris", "alphard", "avalon", "avanza", "celica"};

            //Populating useraccount (Strong), has dependents, so has to be created at the top
            for(int i = 0; i<models.length; i++) {
                for (int j = 1; j <= 100; j++) {
                    int randomFirstName = random.nextInt(firstNames.length);
                    int randomLastName = random.nextInt(lastNames.length);
                    String firstName = firstNames[randomFirstName];
                    String lastName = lastNames[randomLastName];
                    String username = firstName + lastName.charAt(0) + i + "_" + j;
                    String password = firstName + lastName + i + "_" + j;
                    String query = "INSERT INTO useraccount VALUES(?, ?, ?, ?, ?)";
                    PreparedStatement statement = connection.prepareStatement(query);
                    statement.setString(1, "owner" + i + "_" + j + "@gmail.com");
                    statement.setString(2, firstNames[randomFirstName]);
                    statement.setString(3, lastNames[randomLastName]);
                    statement.setString(4, username);
                    statement.setString(5, password);
                    statement.executeUpdate();
                }
            }

            //Populating PhoneNumber (Weak Entity). Has to be done after populating UserAccount
            String[] areaCodes = {"408", "669", "510", "341", "424", "310", "424","305", "786","727", "656", "212",  "214", "469", "972", "682", "646", "332", "917", "718", "347", "917", "929"};

            for(int i = 0; i<models.length; i++) {
                for (int j = 1; j <= 100; j++) {
                    int randomPhoneArea = random.nextInt(areaCodes.length);
                    int phone2 = random.nextInt(899) + 100;
                    int phone3 = random.nextInt(8999) + 1000;
                    String query = "INSERT INTO phonenumber VALUES(?, ?)";
                    PreparedStatement statement = connection.prepareStatement(query);
                    statement.setString(1, "owner" + i + "_" + j + "@gmail.com");
                    statement.setString(2, areaCodes[randomPhoneArea] + "-" + phone2 + "-" + phone3);
                    statement.executeUpdate();
                }
            }

            int mileageLowerBound = 1000;
            int mileageUpperBound = 200000;
            int yearLowerBound = 1990;
            int yearUpperBound = 2024;
            String[] bodyStyle = {"hatchback", "sedan", "sedan", "minivan", "suv", "suv", "sedan", "suv", "suv", "truck", "suv", "truck", "truck", "suv", "mpv", "hatchback", "hatchback", "minivan", "sedan", "mpv", "coupe"};
            String[] cities = {"Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose", "Buffalo", "Rochester", "Yonkers", "Syracuse", "Albany", "Houston", "Dallas", "Austin", "San Antonio", "Fort Worth", "Miami", "Orlando", "Tampa", "Jacksonville", "St. Petersburg"};
            String[] fuels = {"gas", "hybrid", "electric"};
            String[] outerColors = {"white", "blue", "navy", "black", "red"};
            //Populating CarPost (weak entity).
            for(int i = 0; i<models.length; i++) {
                for (int j = 1; j <= 100; j++) {
                    int randomFuel = random.nextInt(3);
                    int randomMileage = random.nextInt(mileageUpperBound - mileageLowerBound) + mileageLowerBound;
                    int randomCarYear = random.nextInt(yearUpperBound - yearLowerBound) + yearLowerBound;
                    int randomMpg = random.nextInt(50 - 10) + 10;
                    int randomPrice = random.nextInt(40000 - 5000) + 5000;
                    int randomPostYear = random.nextInt(2024-2000) + 2000;
                    int randomPostMonth = random.nextInt(12-1) + 1;
                    int randomPostDay = random.nextInt(31-1) + 1;
                    int randomOuterColor = random.nextInt(outerColors.length);
                    String query = "INSERT INTO carpost VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
                    PreparedStatement statement = connection.prepareStatement(query);
                    statement.setString(1, "PLNUM" + "_" + i + "_" + j);
                    statement.setString(2, "owner" + i + "_" + j + "@gmail.com");
                    statement.setString(3,  models[i]);
                    statement.setInt(4, randomMpg);
                    statement.setString(5, fuels[randomFuel]);
                    statement.setInt(6, randomCarYear);
                    statement.setInt(7, randomMileage);
                    statement.setString(8,  cities[i]);
                    statement.setInt(9, randomPrice);
                    statement.setString(10, randomPostYear + "-" + randomPostMonth + "-" + randomPostDay);
                    statement.setString(11, outerColors[randomOuterColor]);
                    statement.setString(12, "");
                    statement.executeUpdate();
                }
            }
            // Populating Cities (Strong Entity) Table
            String[][] statesCities = getStrings();
            String[] states = {"CA", "NY", "TX", "FL"};
            for(int i = 0; i<states.length; i++){
                for(int j = 0; j<5; j++){
                    String query = "INSERT INTO cities VALUES(?, ?)";
                    PreparedStatement statement = connection.prepareStatement(query);
                    statement.setString(1, statesCities[i][j]);
                    statement.setString(2,  states[i]);
                    statement.executeUpdate();
                }
            }

            // Populating CarInfo (Strong Entity) Table
            for(int i = 0; i<models.length; i++){
                String query = "INSERT INTO carinfo VALUES(?, ?, ?)";
                PreparedStatement statement = connection.prepareStatement(query);
                statement.setString(1, models[i]);
                statement.setString(2,  bodyStyle[i]);
                statement.setString(3,  "Toyota");
                statement.executeUpdate();
            }

            connection.close();
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }

    private static String[][] getStrings() {
        String[] california = {"Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose"};
        String[] newyork = {"Buffalo", "Rochester", "Yonkers", "Syracuse", "Albany"};
        String[] texas = {"Houston", "Dallas", "Austin", "San Antonio", "Fort Worth"};
        String[] florida = {"Miami", "Orlando", "Tampa", "Jacksonville", "St. Petersburg"};
        String[][] states= {california, newyork, texas, florida};
        return states;
    }
}
