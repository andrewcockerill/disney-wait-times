from data_acquisition import *
import sys

def main():
    # Create database for all project data
    print('Creating database using API arguments:')
    build_sqlite_db(ncdc_api_key = sys.argv[1], bls_api_key = sys.argv[2])
    
if __name__ == '__main__':
    main()