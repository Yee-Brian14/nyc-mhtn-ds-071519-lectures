import Yelp_API_helpers as p

try:
    cursor.execute("USE {}".format(db_name))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(db_name))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, db_name)
        print("Database {} created successfully.".format(db_name))
        conn.database = db_name
    else:
        print(err)
        exit(1)


TABLES = {}
# Create a table for the Businesses
TABLES['Businesses'] = (
    "CREATE TABLE Businesses ("
    "  businessId varchar(30) NOT NULL,"
    "  businessName varchar(255),"
    "  price varchar(4),"
    "  rating REAL,"
    "  PRIMARY KEY (businessId)"
    ") ENGINE=InnoDB")
# Create a table for the reviews
TABLES['Reviews'] = ("""
    CREATE TABLE Reviews (
        reviewId varchar(30) NOT NULL,
        businessId varchar(30),
        rating INT,
        text varchar(255),
        time_created DATETIME,
        PRIMARY KEY (reviewId),
        FOREIGN KEY (businessId)
            REFERENCES Businesses(businessId)
            ON DELETE CASCADE
    ) ENGINE=InnoDB
""")

p.create_table(TABLES)
all_businesses = p.all_business_results(url_params)