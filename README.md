## Disease & Pest Alarm
> Disease and Pest Forecasting Service based on SMS Alarm
### How to use
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
* Container
  * Docker
### Documents
* [ERD](https://001forecasting.blob.core.windows.net/image/v1_forecasting_erd.png)
* [API Document](https://disease-pest-alarming.azurewebsites.net/swagger/)
* [Project in detail](https://studynote.oopy.io/projects/6/)
