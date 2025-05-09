import sys
from main import main

if __name__ == "__main__":
    # Collect arguments passed to app.py
    args = sys.argv[1:]

    # Pass the parsed query parameters to the main function
    main(args)
    