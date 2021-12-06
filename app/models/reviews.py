from flask import current_app as app


class ProdReviews:
    def __init__(self, firstname, lastname, uid, pid, rating, numVotes, review, DateTime):
        self.firstname = firstname
        self.lastname = lastname
        self.uid = uid
        self.pid = pid
        self.rating = rating
        self.numVotes = numVotes
        self.review = review
        self.DateTime = DateTime

    @staticmethod
    def get_all(pid):
       
        rows = app.db.execute('''
SELECT firstname, lastname, uid, pid, rating, numVotes, review, DateTime
FROM ProductReview, Users
WHERE ProductReview.uid = Users.id AND ProductReview.pid = :pid
ORDER BY DateTime DESC
''',pid=pid)
        return [ProdReviews(*row) for row in rows]
    
    @staticmethod
    def NewProdReview(
        uid, pid, rating, review
    ):
        try:
            rows = app.db.execute(
                """
INSERT INTO ProductReview(uid, pid, rating, numVotes, review, DateTime)
VALUES(:uid, :pid, :rating, 0, :review, LOCALTIMESTAMP(0))
""",
                uid=uid, 
                pid=pid, 
                rating= rating, 
                review= review, 
            )
         
            return None
        except Exception:
            # likely id already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    def upVotes(pid, numVotes, uid):
        try: rows = app.db.execute('''
UPDATE ProductReview
SET numVotes = :numVotes + 1
WHERE pid = :pid AND uid = :uid
''',pid=pid, numVotes = numVotes, uid = uid)
        except Exception:
            return None

    @staticmethod
    def downVotes(pid, numVotes, uid):
        try: rows = app.db.execute('''
UPDATE ProductReview
SET numVotes = :numVotes - 1
WHERE pid = :pid AND uid = :uid
''',pid=pid, numVotes = numVotes, uid = uid)
        except Exception:
            return None

class SellerReviews:
    def __init__(self, uid, sid, rating, numVotes, review, DateTime):
        self.uid = uid
        self.pid = sid
        self.rating = rating
        self.numVotes = numVotes
        self.review = review
        self.DateTime = DateTime

    @staticmethod
    def get_user_reviews(sid):
        try: rows = app.db.execute('''
SELECT uid, sid, rating, numVotes, review, DateTime
FROM SellerReview
WHERE sid = :sid
ORDER BY DateTime DESC
''',sid=sid)
        except Exception:
            return None
        if rows:
            return [SellerReviews(*row) for row in rows]
        else:
            return None