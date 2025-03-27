import mysql.connector
import yaml
import os
import logging

class DatabaseUtils:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.load_config()
        self.setup_logging()

    def load_config(self):
        """Load database configuration from config.yaml"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            self.db_config = config['database']

    def setup_logging(self):
        """Setup logging configuration"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            self.cursor = self.connection.cursor()
            self.logger.info("Successfully connected to database")
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {str(e)}")
            raise e

    def disconnect(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            self.logger.info("Successfully disconnected from database")
        except Exception as e:
            self.logger.error(f"Failed to disconnect from database: {str(e)}")
            raise e

    def execute_query(self, query, params=None):
        """Execute SQL query"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor
        except Exception as e:
            self.logger.error(f"Failed to execute query: {str(e)}")
            raise e

    def fetch_one(self, query, params=None):
        """Fetch single row from query result"""
        try:
            cursor = self.execute_query(query, params)
            return cursor.fetchone()
        except Exception as e:
            self.logger.error(f"Failed to fetch one row: {str(e)}")
            raise e

    def fetch_all(self, query, params=None):
        """Fetch all rows from query result"""
        try:
            cursor = self.execute_query(query, params)
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Failed to fetch all rows: {str(e)}")
            raise e

    def verify_user_exists(self, email):
        """Verify if user exists in database"""
        try:
            query = "SELECT * FROM users WHERE email = %s"
            result = self.fetch_one(query, (email,))
            return result is not None
        except Exception as e:
            self.logger.error(f"Failed to verify user existence: {str(e)}")
            raise e

    def get_user_details(self, email):
        """Get user details from database"""
        try:
            query = "SELECT * FROM users WHERE email = %s"
            return self.fetch_one(query, (email,))
        except Exception as e:
            self.logger.error(f"Failed to get user details: {str(e)}")
            raise e 