# scrappingecom

**Scrapping Fundrazr website using scrapy https://fundrazr.com/find?category=Health**


## Developer guide

Install requirements:

```
pip install -r requirements.txt

```
Run the spider :

```
scrapy crawl fundrazr -a category=Health

```
if you eant to ave data into a file

```
scrapy crawl fundrazr -o fundrize.csv -a category=Health

```

this spider is inspired by this tutorial https://www.youtube.com/watch?v=O_j3OTXw2_E
