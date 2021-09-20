# Ravioli
My i3wm startup script made with python.

Current startup "modules":
- auto-presence-fill: `auto-absen.py`

## Installing
Install required modules:
```sh
$ pip install -r requirements.txt
```
Download firefox and geckodriver

## How to use
### Write your account details
Make a `config.json`
```json
{"email": "<email>", "password": "<password>"}
```
### Run ravioli.py
```
$ python ravioli.py
```

## Roadmap
- [x] Semi-automatic login
- [x] Cookie persistence
- [ ] Cross-webdriver support
