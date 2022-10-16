## Disease & Pest Alarm [![Django CI](https://github.com/MJbae/disease-pest-alarming/actions/workflows/django_ci.yml/badge.svg)](https://github.com/MJbae/disease-pest-alarming/actions/workflows/django_ci.yml)
> Disease and Pest Forecasting Service based on SMS Alarm
### How to work
* Get SMS Alarm When it occurs

   * SMS Example
    ~~~text
    [Web발신] 
    2021-11-16, 가평군의 포도에서 갈색무늬병 피해 발생
    ~~~

### Technologies Used
* Application Framework
  * Django, Django REST Framework
* SMS API
  * SENS(by NAVER CLOUD PLATFORM)
* RDBMS & ORM 
  * MySQL
  * Django's ORM
* Async Distributed Process
  * Celery, Celery Beat
  * AWS SQS
* Test Framework
  * PyTest
  * Model Bakery
### Deployment Environment
* Cloud Infra
  * Microsoft Azure
### Documents
* [Flow Chart](https://github.com/MJbae/disease-pest-alarming/wiki/Flow-Cart)
* [Project in detail](https://studynote.oopy.io/projects/6/)
