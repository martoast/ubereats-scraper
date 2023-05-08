# ubereats-scraper


# Uber Eats Web Scraper

A web scraper for Uber Eats that allows the user to enter a location and an optional food type to focus on. The scraper will output a csv of  of restaurant data and menu items and identify popular menu items in the specified location.

## Usage

To use the web scraper, follow the steps below:

1. Run the `get_urls.py` file, passing it a location and a search query (optional). This will retrieve all the URLs for the restaurants that match the search criteria. Here's an example of how to run the script:

    ```
    python3 get_urls.py --location New York City --query Pizza
    ```

2. Once you have the URLs, run the `main.py` file to scrape the restaurant data. This script requires a CSV file containing the URLs as input. Here's an example of how to run the script:

    ```
    python3 main.py --location New York
    ```
## Installation

To install the necessary dependencies, run the following command:

  ```
  pip install -r requirements.txt
  ```


## Contributing

If you'd like to contribute to the project, please fork the repository and create a new branch. Pull requests are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

