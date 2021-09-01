from . import db
class Table(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    in_url=db.Column(db.String(4000))
    out_url=db.Column(db.String(4000))
    # relationship with IpTable
    ip_table_id=db.relationship('IpTable', backref='tables', lazy='dynamic')

class IpTable(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ip=db.Column(db.String(40))
    table_id=db.Column(db.Integer,db.ForeignKey('tables.id'))

    
    

    