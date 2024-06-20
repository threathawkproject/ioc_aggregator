## IOC Aggregator

Periodically Aggregates IOC Feeds so user can easily select the IOC form trusted souces

Note: **Try to do this in a virutalenv!**

## Step 1: Install the required dependencies
```bash
cd aggregator
pip install -r requirements.txt 

```


## Step 2: Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Run the server
```bash
python manage.py runserver 8004
```

### Exposed Endpoints
- `/api/ioc_feeds`

## Step 4: Run the consumer
```bash
python manage.py ioc_feeds_consumer
```

## Step 5: Run the producer
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
