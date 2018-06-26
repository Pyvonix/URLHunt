
<h1 align="center">
  <br>
  <a href="https://github.com/TheBuky/URL-Hunt"><img src="https://vignette.wikia.nocookie.net/videogamefan/images/6/6d/Custom_ssb_duck_hunt_by_lisnovski-d7zc13u.png" alt="URL Hunt" width="300"></a>
  <br>
  URL Hunt
  <br>
</h1>


## Introduction

The main goal is to make it easier for analysts to search for URLs where are the downloaded payloads.

For that, the script help to find available URLs on a domain, where files can be accessible. Furthermore, he contains a feature to report found URLs to [URLHaus](https://urlhaus.abuse.ch/).

NB: A part of this script is based on the [URLHaus API script](https://urlhaus.abuse.ch/api/#submit).

## Features

List of features already implemented (checked) and conceived (empty):

* [X]  [URLHaus](https://urlhaus.abuse.ch/) submission
* [ ]  [URLHaus](https://urlhaus.abuse.ch/) search
* [X]  Submit URL from local file
* [X]  Submit URL from Pastebin
* [ ]  Define tag(s) for each URL
* [X]  Light Bruteforce
* [X]  Browse directory
* [ ]  Download files


## Usage

```
usage: urlhunt.py [-h] [-u URL | -f FILE | -p PASTEBIN] [-b | -i] [-s] [-v]
                  [--version]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     process with url in input
  -f FILE, --file FILE  process with local file
  -p PASTEBIN, --pastebin PASTEBIN
                        process with raw page on pastebin
  -b, --bruteforce      basic iterator to find extra files
  -i, --index           list all files in index
  -s, --submit          submit result on URLHaus
  -v, --verbose         increase output verbosity
  --version             show program's version number and exit
```

## Examples

1. Submit all file in a web repertory
```
python3 urlhunt.py -u http://example.org/repertory/1.exe -i -s -v

[Directory] Parent Directory
[File] 1.doc
[File] 1.exe
[File] 10.exe
[File] 2.exe
[File] 20.exe
[File] 3.exe
[File] 4.exe
[File] 5.exe
[File] 6.exe
[File] 7.exe
[File] 8.exe
[File] 9.exe
[Directory] doc/
[Directory] exe/
[Directory] inew/
[Directory] new/
[Directory] newdoc/

[*] Submit...
http://example.org/repertory/1.doc
http://example.org/repertory/1.exe
http://example.org/repertory/10.exe
http://example.org/repertory/2.exe
http://example.org/repertory/20.exe
http://example.org/repertory/3.exe
http://example.org/repertory/4.exe
http://example.org/repertory/5.exe
http://example.org/repertory/6.exe
http://example.org/repertory/7.exe
http://example.org/repertory/8.exe
http://example.org/repertory/9.exe
[!] Done.
```

2. Submit all URL in pastebin page
```
python3 urlhunt.py -p http://pastebin.com/PAGE -s -v

[*] Submit...
http://example.org/1
http://example.org/2
http://example.org/3
http://example.org/4
http://example.org/5
[!] Done.
```

