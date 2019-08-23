# Data storage design 

## Possibilities

- dedicated database
- message queue
- in memory storage
- flat file like json 

## Database structure


#### Email
|field  |description    |
|-------|---------------|
|id     |PRIMARY KEY
|contents|
|to|
|from|
|cc|
|bcc|
|subject|
|attachments|
|type   | html or text|
|created |  timestamp|


#### delivery
|field  |description    |
|-------|---------------|
|id     |PRIMARY KEY|
|email_id | FOREIGN KEY|
|status | success or not|
|server_message |
|attempt | timestamp|


## Theoretical Process

1. New message is created using API POST
    - New email is added to email table
    - Email ID is returned to user
2. ID is sent to message queue
3. Message queue looks to see past delivery attempts
    - if attempts < 3 and last attempt > 10 mins ago (or no attempts made), try sending email
4. Record delivery status in delivery table
    - if delivery fails, put ID back in message queue
    - add wait timestamp / delay to message broker for id??
