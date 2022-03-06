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

Students can now hit <IP>/<varname> to get an object:

```
{
    <varname>: [
        {
            "timestamp": yyyy-mm-ddThh:mm:ss.ssssss+00:00,
            "val": some random float shaped by a helper function, faking humidity at the time of writing
        }
    ]
}
```

The array will contain an entry for every minute of the last 24h; the crontab will roll this window forward.
