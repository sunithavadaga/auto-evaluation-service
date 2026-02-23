DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Vijaya%40123",
    "database": "mock_org_db"
}

DATABASE_URL = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
)