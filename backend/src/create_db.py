# backend/src/create_db.py
from .utils.db import engine, Base
from .models.sales_model import Sale

def main():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    main()
