from websites.model import Table
from flask import Blueprint, render_template,redirect,request
from . import db
from .model import Table,IpTable
# import qrcode
views=Blueprint('views',__name__)

# random string generator
import random
import string
def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@views.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        in_url=request.form.get('url')
        # print(in_url)
        table=Table.query.filter_by(in_url=in_url).first()
        if table:
            out_url=table.out_url
        else: 
            out_url=random_string()
            table=Table(in_url=in_url,out_url=out_url)
            db.session.add(table)
            db.session.commit()
        return render_template('index.html',in_url=in_url,out_url=out_url,table=table)
    
    return render_template('index.html')
from urllib.request import urlopen
import re
def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

@views.route('/<string:out_url>')
def redirect_url(out_url):
    table=Table.query.filter_by(out_url=out_url).first()
    if table is None:
        return redirect('/')
    s=getPublicIp()
    print(str(s))
    ip=IpTable(ip=str(s),table_id=table.id)
    db.session.add(ip)
    db.session.commit()
    # import socket
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    # local_ip_address = s.getsockname()[0]
    # print(local_ip_address)

    return redirect(table.in_url)