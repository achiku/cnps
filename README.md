# cnps

See who's comming to your event through [connpass](https://connpass.com/)

## Why created

Simply said, it's created to find meetup assholes.


## Usage

```
Usage: cnps [OPTIONS] COMMAND [ARGS]...

  cnps cli (v0.1.0)

Options:
  --help  Show this message and exit.

Commands:
  dump    dump basic event applicants data
  filter  filter applicants data with multiple options
```

### dump applicants data

You should first dump all applicants data in json format. It contains Twitter/Facebook/GitHub links, connpass user id, and event dates that a user recently participated (or applied). This scrapes event page, so just be nice to connpass, they are cool.

```
Usage: cnps dump [OPTIONS] EVENT_URL

  dump basic event applicants data

Options:
  --help  Show this message and exit.
```


```console
# example
cnps dump https://fintech-engineers-drink-up.connpass.com/event/56057/ > user.json
```


### filter user data

Once you dumped applicants data, you can now filter with the following options. You might want to find users with no social links, trying to join more than two events at the same date, etc.

```
Usage: cnps filter [OPTIONS] FILE_PATH

  filter  filter applicants data with multiple options

Options:
  --facebook-link / --no-facebook-link
  --github-link / --no-github-link
  --twitter-link / --no-twitter-link
  --duplicate-event / --no-duplicate-event
  --avg-event-interval INTEGER
  --help                          Show this message and exit.
```

```console
# example to find users trying to participate more than two events in the same date in the latest 10 events
cnps filter ./user.json  --duplicate-event
```
