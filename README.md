# heartbeat
Web app to check availability of urls

## Structure

### Tools

* Django 4.1
* Celery 5.2.7
* DRF 3.14
* Flower 1.2
* Redis 4.5.1
* Postgres 14

Project is fully containerized using docker.

#### To build
```bash
docker compose build
```

#### To run
```bash
docker compose up
```

#### To stop
```bash
docker compose down
```

