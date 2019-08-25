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
5. Set up config file
    - Copy config.json.example to config.json
    - Modify to use you own smtp settings 
6. Run
```
python main.py
```

## API METHODS
- add some swagger / raml api documentation
### POST api/v1/
send email, get back id
- retry up to 3 times with 10 minute interval in case of failure

### GET api/v1/<id> 
see status of specific email

### GET api/v1/
see status of all email



## Web-based user interface

- Page to send emails
- Index of statuses

Maybe use bootstrap

