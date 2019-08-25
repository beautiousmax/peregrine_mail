# Peregrine Mail

Demo email service

## How to Setup and Run
1. Clone the repository
```
git clone --single-branch --branch development git@github.com:beautiousmax/peregrine_mail.git
```
2. Move into the project
```
cd peregrine_mail
```
3. Create a python 3.6+ virtual environment and activate it
```
python -m venv venv
source venv/bin/activate
```
4. Install requirements
```
pip install -r requirements
```
5. Run
```
python main.py
```

## API METHODS
- add some swagger / raml api documentation
### POST api/v1/
send email, get back id
- retry 3 times with 10 minute interval in case of failure
- log delivery status to database??? "with some retention policy"

### GET api/v1/<id> 
see status of specific email

### GET api/v1/
see status of all email



## Web-based user interface

- Page to send emails
- Index of statuses

Maybe use bootstrap


