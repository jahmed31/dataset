# Dataset
This project is in Django. Two main components in this application
1. migration for csv data in database
2. api endpoint 

## Installation
```bash
pip install -r requirements.txt
```
 
## Custom Command
To load the dataset.csv into database, needs to run the following command
```bash
python manage.py migrate_dataset (path to dataset.csv)
```
above command will load the csv and enter all it's rows in database 

#Testing URLs
## Use Case: 1 
http://localhost:8000/api/filter_data?date_to=2017-06-01&sort=clicks&order=desc&group_by=country&group_by=channel

## Use Case: 2 
http://localhost:8000/api/filter_data?date_from=2017-05-01&date_to=2017-05-31&os=ios&sort=date&group_by=date

## Use Case: 3  
http://localhost:8000/api/filter_data?date_from=2017-06-01&date_to=2017-06-01&sort=revenue&order=desc&group_by=os&country=US

## Use Case: 4 
http://localhost:8000/api/filter_data?date_from=2017-06-01&date_to=2017-06-01&sort=CPI&order=desc&group_by=channel&country=CA
