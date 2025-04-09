mig:
	./manage.py makemigrations
	./manage.py migrate

test:
	pytest