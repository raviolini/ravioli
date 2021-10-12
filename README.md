# Ravioli
A startup script and an automation service made with Python.

Current automation modules:
- siakad-auto-attendance: `pasta/siakad_auto_attendance`
- trello-up-next: `pasta/trello_up_next` (up next)

## How To Use
Install dependencies:
```sh
$ pip install -r requirements.txt
```
Run ravioli:
```sh
$ python3 ravioli.py
```
Then you'll be asked for siakad user credentials and preferred web browser (only used when signing in).

You may want to use python venv before installing the dependencies (optional):
```sh
# This assumes ravioli is the directory where ravioli.py is stored
$ cd ravioli
$ python3 -m venv .
```

### or if you don't want to bother you can download the release <a href = "https://github.com/cowdingus/ravioli/releases/latest">here</a>

## Big ToDo
- [ ] Turn ravioli into a windows service on windows.
