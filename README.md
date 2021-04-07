# django ecommerce

    Recommendation System for E-Commerce using Collaborative Filtering



## Environment

```sh
$  pip install -r requirements.txt
```


## Run


```python
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## ToDo
  - UI 
  - Errors List Out
  
  
## Algorithm
### Collabortive Filtering (Recommender Algorithm)
	- Collaborative filtering filters information by using the interactions and data collected by the system from other users.
	- There are two types of collaborative filtering
		  User-based, which measures the similarity between target users and other users.
		  Item-based, which measures the similarity between the items that target users rate or interact with and other items.


I have used user based collaborative filtering.	