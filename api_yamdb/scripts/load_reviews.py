from django.contrib.auth import get_user_model
# python3 manage.py runscript scripts.{file_name}
import csv

from api.models import Review, Title
from api.exceptions import UserNotFoundError

User = get_user_model()


def run():
    fhand = open('static/data/review.csv')
    reader = csv.reader(fhand)
    next(reader)

    Review.objects.all().delete()

    for row in reader:
        print(row)
        title, created = Title.objects.get_or_create(id=row[1])
        try:
            author = User.objects.get(id=row[3])
        except Exception as ex:
            raise UserNotFoundError

        review = Review(
            id=row[0],
            title_id=title.id,
            text=row[2],
            author=author,
            score=row[4],
            pub_date=row[5]
            )
        review.save()
