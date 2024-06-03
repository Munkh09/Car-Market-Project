CREATE TABLE UserAccount (
    email VARCHAR(200) PRIMARY KEY,
    firstName VARCHAR(200) NOT NULL,
    lastName VARCHAR(200) NOT NULL,
    userName VARCHAR(200) UNIQUE NOT NULL,
    pass VARCHAR(200) UNIQUE NOT NULL,
    CONSTRAINT passFormat CHECK(CHAR_LENGTH(pass) >= 8),
    CONSTRAINT emailFormat CHECK(email LIKE '%@%.com')
);

CREATE TABLE CarPost(
    plateNumber VARCHAR(100),
    ownerEmail VARCHAR(200),
    model VARCHAR(200) NOT NULL,
    mpg INT(2) NOT NULL,
    fuel VARCHAR(200) NOT NULL,
    carYear INT(4) NOT NULL,
    mileage INT(6) NOT NULL,
    city VARCHAR(300) NOT NULL,
    price INT(6) NOT NULL,
    postDate VARCHAR(200) NOT NULL,
    outerColor VARCHAR(200) NOT NULL,
    bookmarkedBy VARCHAR(10000) NOT NULL,
    CONSTRAINT mpgFormat CHECK(mpg >= 0),
    CONSTRAINT yearFormat CHECK(carYear >= 1885),
    CONSTRAINT mileageFormat CHECK(mileage >= 0),
    CONSTRAINT priceFormat CHECK(price >= 0),
    PRIMARY KEY(plateNumber, ownerEmail),
    FOREIGN KEY(ownerEmail) REFERENCES useraccount(email)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE CarInfo(
    model VARCHAR(200) PRIMARY KEY,
    bodyStyle VARCHAR(200) NOT NULL,
    manufacturerName VARCHAR(200) NOT NULL
);

CREATE TABLE Cities(
    city VARCHAR(200) PRIMARY KEY,
    carState CHAR(2) NOT NULL
);

CREATE TABLE PhoneNumber(
    ownerEmail VARCHAR(200),
    phoneNumber VARCHAR(200),
    PRIMARY KEY(ownerEmail, phoneNumber),
    FOREIGN KEY(ownerEmail) REFERENCES UserAccount(email)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Issue(
    issuerEmail VARCHAR(200),
    issueId INT,
    issueDate DATE NOT NULL,
    issueText VARCHAR(400) NOT NULL,
    PRIMARY KEY(issuerEmail, issueId),
    FOREIGN KEY(issuerEmail) REFERENCES UserAccount(email)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Purchases(
    purchaserEmail VARCHAR(200),
    plateNumber VARCHAR(100),
    purchasePrice INT NOT NULL,
    sellerEmail VARCHAR(200) NOT NULL,
    purchaseDate DATE NOT NULL,
    PRIMARY KEY(purchaserEmail, plateNumber),
    FOREIGN KEY(purchaserEmail) REFERENCES UserAccount(email)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Sales(
    sellerEmail VARCHAR(200),
    plateNumber VARCHAR(100),
    purchaserEmail VARCHAR(200),
    salesPrice INT NOT NULL,
    sellDate DATE NOT NULL,
    PRIMARY KEY(sellerEmail, plateNumber),
    FOREIGN KEY(sellerEmail) REFERENCES UserAccount(email)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);




