from sqlmodel import Session

from .database import engine, create_db_and_tables, create_default_data
from .models import *


def main():
    create_db_and_tables()
    create_default_data()


if __name__ == "__main__":
    main()
