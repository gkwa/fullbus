## Summary

just like `find` but with a friendly timespan option



## cli

```log
root@ip-172-30-1-139:~# fullbus  --help
usage: fullbus [-h] [-t TIMESPAN] [-d DIRECTORY] [-e EXT] [-x EXCLUDE] [-i INCLUDE]

Find recently modified files.

optional arguments:
  -h, --help            show this help message and exit
  -t TIMESPAN, --timespan TIMESPAN
                        Timespan for modification (e.g., 5m, 1h, 3.2m, 10s, 2d). If not specified, no timespan limit is applied.
  -d DIRECTORY, --directory DIRECTORY
                        Starting directory for the search (default: /)
  -e EXT, --ext EXT     File extensions to search for
  -x EXCLUDE, --exclude EXCLUDE
                        Paths to exclude from the search
  -i INCLUDE, --include INCLUDE
                        Paths to include in the search (case-insensitive)
root@ip-172-30-1-139:~#
```

## examples

```bash
# help
fullbus --help

# show all files
fullbus

# filter by log files
fullbus --ext log
fullbus -e log

# filter by txt ext
fullbus --ext txt

# both log and txt
fullbus --ext log --ext txt

# filter by directory
fullbus --ext log -d /tmp

# text files modified within the last 20m
fullbus --ext txt -t 20m

# duration is flexible filter by files modified within last 0.2h
fullbus -e log -t 0.2h

# log files modified within last 1h
fullbus -e log -t 1h

# show only paths that contain substring trash
fullbus -i trash

# limit filter by directory
fullbus -t 20m --ext txt --ext log -d /var/snap/lxd/
```

## Install

```bash
pip install git+https://github.com/taylormonacelli/fullbus
```
