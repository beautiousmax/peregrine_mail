# Peregrine Mail

Demo email service

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

