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
|sender|
|cc|
|bcc|
|subject|
|attachments|
|html   | 
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
2. Email info is sent to background thread queue
3. New emails waiting in queue are sent to smtp server
4. Thread looks for failed emails that meet criteria to resend
    - Criteria is if attempts < 3 and last attempt > 10 mins ago
