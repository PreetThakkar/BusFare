# BusFare

This project is specifically to learn the Python framework *Scrapy*. The aim of the spider is to execute several requests and gather bus fares for a route.

### Set up the project
- Install python framework scrapy using ``` pip install scrapy ``` .
- To run the spider, navigate to the ``` spiders ``` folder and run the following command ``` scrapy runspider Abhibus.py -o seatfare.json ``` .
- You can terminate the process midway or wait for it's completion, in either case you will see data in the mentioned json file.
- You are all set.

### Output Data
The output data will be list of dictionaries of the format
```json
{
    "timestamp": "2021-03-09 16:44:15.092785", 
    "date": "2021-03-09", 
    "rid": "797805572", 
    "travelerAgentName": "Xyz Travels", 
    "seat": [
        {"13": "1799"}, 
        {"17": "1799"}, 
        {"21": "1799"}, 
        {"29": "1799"}, 
    ]
}
```