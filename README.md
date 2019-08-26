# Peregrine Mail

Demo email service

## How to Setup and Run
1. Clone the repository
```
git clone --single-branch --branch development https://github.com/beautiousmax/peregrine_mail.git
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
pip install -r requirements.txt
```
5. Set up config file
    - Copy config.json.example to config.json
    - Modify to use you own smtp settings 
6. Run
```
python -m peregrine_mail
```

## API METHODS
### POST api/v1/
- Use request body to construct email, get back new email id
- Example:
```
{"to": "you@gmail.com", 
"cc": null, 
"bcc": null, 
"sender": "me@hotmail.com", 
"contents": "Thanks for trying peregrine mail!", 
"subject": "test email", 
"html": null}
```
- In case of failure, messages are resent up to 3 times with a 10 minute interval 

### GET api/v1/<id> 
see status of specific email

### GET api/v1/
see status of all email
