# Data storage design 

## How it works

1. New message is created using API POST
    - New email is added to email table
    - Email ID is returned to user
2. Email info is sent to background thread queue
3. New emails waiting in queue are sent to smtp server
4. Thread looks for failed emails that meet criteria to resend
    - Criteria is if attempts < 3 and last attempt > 10 mins ago
5. Emails older than 3 days are removed from the database


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


## Development Notes

- Production quality attachments would take me more time than a weekend
- Used threads because they have less dependencies than something like RQ or Celery, and it's easier to setup for cross platform usage
- Used sqlalchemy to speed up development. If I had more time, pure SQL would have a speed advantage
