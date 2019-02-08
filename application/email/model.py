class sent_email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_addr_list = db.Column(db.String(80), unique=True, nullable=False)
    cc_addr_list = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(80), unique=True, nullable=False)
    message = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self):
        return '<Email %r>' % self.message
