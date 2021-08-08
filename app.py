from flask import Flask,request,jsonify
from os import name
import ldap3
from ldap3 import Server, Connection
import base64

app = Flask(__name__)

@app.route('/api/AD/',methods=['POST', 'GET'])
def hello_world():
    return 'Hey, we have Flask in a Docker container!'

@app.route('/api/AD/ad_2000',methods=['POST', 'GET'])
def connexion_ad2000():
    if request.method == 'POST':
        server = Server('10.10.10.11', get_info=ldap3.ALL)
        data = request.json
        email_util = data["ad_2000"]
        passw_util = data["password"]
        try:
            email_util = 'GROUPE-HASNAOUI\\' + email_util
            conn = Connection(server, email_util, passw_util, auto_bind=True)
            if (conn):
                ad_2000 = email_util.split('GROUPE-HASNAOUI\\')[1]
                conn.search(search_base="dc=groupe-hasnaoui,dc=local",
                            search_filter='(sAMAccountName=' + ad_2000 + ')',
                            attributes=('sAMAccountName', 'mail',
                                        'title', 'displayName','thumbnailPhoto')
                            )

                mail = conn.entries[0].mail.value
                title = conn.entries[0].title.value
                name = conn.entries[0].displayName.value                                                 
                thumbnailPhoto = conn.entries[0].thumbnailPhoto.value     
                dict = {'name': name, 'mail': mail, 'ad_2000': ad_2000, 'title': title,"thumbnailPhoto":base64.encodebytes(thumbnailPhoto).decode()}
                
                msg = dict

            
                return {"response": True, "message": msg}
                

            else:
                return {"response": True, "message": "Disconnected"}
        
        except Exception as e:
            return {"response": True, "message": str(e)}

@app.route('/api/AD/email_conn',methods=['POST', 'GET'])
def connexion_email():
    if request.method == 'POST':
        server = Server('10.10.10.11', get_info=ldap3.ALL)
        data = request.json
        email_util = data["email"]
        passw_util = data["password"]
        try:
            conn = Connection(server, email_util, passw_util, auto_bind=True)
            if (conn):
                conn.search(search_base="dc=groupe-hasnaoui,dc=local",
                            search_filter='(mail=' + email_util + ')',
                            attributes=['sAMAccountName',
                                        'mail', 'title', 'displayName','thumbnailPhoto']
                            )
                ad_2000 = conn.entries[0].sAMAccountName.value
                title = conn.entries[0].title.value
                name = conn.entries[0].displayName.value                                                 
                thumbnailPhoto = conn.entries[0].thumbnailPhoto.value

                dict = {'name': name, 'mail': email_util, 'ad_2000': ad_2000, 'title': title,'thumbnailPhoto': base64.encodebytes(thumbnailPhoto).decode()}
                msg = dict
                return {"response": True, "message": msg}
            else:
                return {"response": False, "message": "Disconnected"}

        except Exception as e:
            return {"response": True, "message": str(e)}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

#docker build -t flask-tutorial:latest .
#docker run -d -p 5000:5000 flask-tutorial