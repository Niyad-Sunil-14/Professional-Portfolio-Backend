set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py makemigrations
python manage.py migrate

python manage.py management/commands/createsuperuserauto.py

# if [[$CREATE_SUPERUSER]];
# then
#     python manage.py createsuperuser --no-input
# fi