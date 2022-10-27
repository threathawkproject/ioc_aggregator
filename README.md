## IOC Aggregator

Periodically Aggregates IOC Feeds so user can easily select the IOC form trusted souces

## Step 1: Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## How to run the server
```bash
python manage.py runserver
```

## How to run the consumer
```bash
python manage.py ioc_feeds_consumer_job
```

## How to run the producer
```bash
python manage.py ioc_feeds_job
```


## Tutorial to follow
[Aggregator 101](https://realpython.com/build-a-content-aggregator-python/)


## TODO:
- [x] Darklist
- [ ] Blocklist
- [ ] AbuseIPDB
- [x] Botvrij
