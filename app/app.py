from sqlmodel import Session

from .database import (
    engine,
    create_db_and_tables,
    create_default_data,
    create_test_data,
    create_test_select,
)
from .models import *


def main():
    # create_db_and_tables()
    # create_default_data()
    # create_test_data()
    create_test_select()


if __name__ == "__main__":
    main()
