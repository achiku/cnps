# cnps

See who's comming to your event

### Why created

To find assholes.


### Usage

```
Usage: cnps [OPTIONS] COMMAND [ARGS]...

  cnps cli (v0.1.0)

Options:
  --help  Show this message and exit.

Commands:
  dump    dump basic user data
  filter  filter user data
```

#### dump user data

```
Usage: cnps dump [OPTIONS] EVENT_URL

  dump basic user data

Options:
  --help  Show this message and exit.
```


#### filter user data

```
Usage: cnps filter [OPTIONS] FILE_PATH

  filter user data

Options:
  --facebook-link / --no-facebook-link
  --github-link / --no-github-link
  --twitter-link / --no-twitter-link
  --duplicate-event / --no-duplicate-event
  --recent-event-interval INTEGER
  --help                          Show this message and exit.
```
