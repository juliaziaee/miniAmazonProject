from flask import current_app as app


class ProdReviews:
    def __init__(self, uid, pid, rating, numUpVotes, numDownVotes, review, DateTime):
        self.uid = uid
        self.pid = pid
        self.rating = rating
        self.numUpVotes = numUpVotes
        self.numDownVotes = numDownVotes
        self.review = review
        self.DateTime = DateTime

    @staticmethod
    def get_all(pid):
       
        rows = app.db.execute('''
SELECT uid, pid, rating, numUpVotes, numDownVotes, review, DateTime
FROM ProductReview
WHERE pid = :pid
ORDER BY DateTime DESC
''',pid=pid)
        print(rows)
        return [ProdReviews(*row) for row in rows]
