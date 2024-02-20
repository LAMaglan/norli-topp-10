*Note*: No longer working due to substantial changes in the setup of the norli website.
Seems like data to be extracted is now sent through FETCH (type XHR) via Algolia API, which
requires an account with the latter

Scrapes Norli website for top 10 best novels (of the week).
To run with docker locally, do

```bash
docker build -t <chosen name of container> .
docker run -v $PWD/output:/output <chosen name of container>
```

