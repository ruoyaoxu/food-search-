# si507

Warning: This project only allows for "food". It is made to search all things but not here. Scraing only allows for restaurants. 


This project accesses the data from website, using Yelp Fusion api source and key	 as well as scraping in the restaurant’s page. After organizing the data, ask users questions to find the rating of the restaurant they want (limit is 50), and show all of the restaurants return. 
Users can also choose as many as areas they want to search. And they can also have an option to choose a specific restaurant. They can choose to go to the website, or they can stay in the program to see some important information about the restaurant by scraping (number of reviews, phone, address)

Other than find the restaurant’s page or information, users can also see the visualization of the data return. The goal of the program is to find the percent of the restaurant that provides delivery service in the area. Users can see the visualization in bar chart if they want to compare all of the areas they search (compare the number of those restaurants) or see the pie chart of the percent of the restaurant provides delivery service in one specific area.


Data source and structure. Data source website https://docs.developer.yelp.com/reference/v3_business_search. Basic api https://api.yelp.com/v3/businesses/search json. Scraping in https://www.yelp.com + all restaurants. (html) Url is returned by the api search.
You can get your private api key here. https://docs.developer.yelp.com/docs/fusion-authentication

Cache codes are at the begining of the project.

Users can choose to display different kinds of graph, and, it is very flexible even though they choose to search a lot of different areas. Using Plotly to display the data.
