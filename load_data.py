
import csv
from datetime import date, datetime

from elice import db
from elice.models import Book

session = db.session

with open('library.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        published_at = datetime.strptime(
            row['publication_date'], '%Y-%m-%d').date()
        image_path = f"/static/image/{row['id']}"
        try:
            open(f'app/{image_path}.png')
            image_path += '.png'
        except:
            image_path += '.jpg'

        book = Book(
            id=int(row['id']),
            book_name=row['book_name'],
            publisher=row['publisher'],
            author=row['author'],
            publication_date=published_at,
            pages=int(row['pages']),
            isbn=row['isbn'],
            description=row['description'],
            link="",
            img_url=image_path,
            stock=5,
        )
        db.session.add(book)

    db.session.commit()
