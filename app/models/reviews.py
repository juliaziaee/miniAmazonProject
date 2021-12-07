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
    def hasReviewed(uid,pid):
       
        if app.db.execute('''
SELECT uid, pid
FROM ProductReview
WHERE ProductReview.uid = :uid AND ProductReview.pid = :pid
''',uid=uid, pid=pid):
            return False
        else:
            return True

    def getAvgReview(pid):
        avg = app.db.execute('''
SELECT AVG(rating)
FROM ProductReview
WHERE ProductReview.pid = :pid
''',
pid=pid)    
        data = []
        for row in avg:
            data.append(str(str(row)[1:-2]))
        return data[0]

    
    @staticmethod
    def NewProdReview(uid, pid, review, rating):
        rows = app.db.execute("""
INSERT INTO ProductReview(uid, pid, rating, numVotes, review)
VALUES(:uid, :pid, :rating, 0, :review)
RETURNING uid
""",
                uid=uid,
                pid=pid,
                review= review,
                rating= rating
            )
        return ProdReviews.get_all(pid)

    @staticmethod
    def updateProdReview(uid, pid, review, rating):
        rows = app.db.execute("""
UPDATE ProductReview
SET review = :review, rating = :rating
WHERE uid = :uid and pid = :pid
RETURNING uid
""",
                uid=uid,
                pid=pid,
                review= review,
                rating= rating
            )
        return ProdReviews.get_all(pid)

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
    def __init__(self, firstname, lastname, uid, sid, rating, numVotes, review, DateTime):
        self.firstname = firstname
        self.lastname = lastname
        self.uid = uid
        self.sid = sid
        self.rating = rating
        self.numVotes = numVotes
        self.review = review
        self.DateTime = DateTime

    @staticmethod
    def get_user_reviews(sid):
        rows = app.db.execute('''
SELECT firstname, lastname, uid, sid, rating, numVotes, review, DateTime
FROM SellerReview, Users
WHERE SellerReview.uid = Users.id AND SellerReview.sid = :sid
ORDER BY DateTime DESC
''',sid=sid)
    
        return [SellerReviews(*row) for row in rows]
      
    @staticmethod
    def hasReviewedS(uid,sid):
       
        if app.db.execute('''
SELECT uid, sid
FROM SellerReview
WHERE SellerReview.sid = :sid AND SellerReview.uid = :uid
''',uid=uid, sid=sid):
            return False
        else:
            return True

    @staticmethod
    def NewSellerReview(uid, sid, review, rating):
        rows = app.db.execute("""
INSERT INTO SellerReview(uid, sid, rating, numVotes, review)
VALUES(:uid, :sid, :rating, 0, :review)
RETURNING uid
""",
                uid=uid,
                sid=sid,
                review= review,
                rating= rating
            )
        return SellerReviews.get_user_reviews(sid)

    @staticmethod
    def updateSellerReview(uid, sid, review, rating):
        rows = app.db.execute("""
UPDATE SellerReview
SET review = :review, rating = :rating
WHERE uid = :uid and sid = :sid
RETURNING uid
""",
                uid=uid,
                sid=sid,
                review= review,
                rating= rating
            )
        return SellerReviews.get_user_reviews(sid)

    @staticmethod
    def upVotesS(sid, numVotes, uid):
        try: rows = app.db.execute('''
UPDATE SellerReview
SET numVotes = :numVotes + 1
WHERE sid = :sid AND uid = :uid
''',sid=sid, numVotes = numVotes, uid = uid)
        except Exception:
            return None

    @staticmethod
    def downVotesS(sid, numVotes, uid):
        try: rows = app.db.execute('''
UPDATE SellerReview
SET numVotes = :numVotes - 1
WHERE pid = :pid AND uid = :uid
''',sid=sid, numVotes = numVotes, uid = uid)
        except Exception:
            return None