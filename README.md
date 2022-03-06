# fake api

A fake API to support simple intro-class exercises

## usage

Set up the 'api':

```
docker image build -t fakepi .
docker container run --rm -d -p 5000:5000 fakepi
```

create a crontab to trigger the api to update every minute:

```
crontab -e
* * * * * curl localhost:5000/update
```
