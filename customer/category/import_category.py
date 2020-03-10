
import xmlrpc.client
import ssl
import csv


url = "http://localhost:8069/xmlrpc/object"
db = 'pricepaper'
pwd = 'confianzpricepaper'


socket = xmlrpc.client.ServerProxy(url,context=ssl._create_unverified_context())

categs = socket.execute(db, 2, pwd, 'res.partner.category', 'search_read', [], ['id','code'])
categories = {categ['code']: categ['id'] for categ in categs}

print (categories)

input_file = csv.DictReader(open("rclclas1.csv"))

with open("Catg_upd_ERROR.csv", "wb") as f:

    for line in input_file:
        try:
            vals = {'code': line.get('CLASS-CODE          ').strip(),
                    'name': line.get('CLASS-DESC          ').strip()
                    }
            if line.get('CLASS-CODE          ').strip() in categories:
                id = categories.get(line.get('CLASS-CODE          ').strip())
                status = socket.execute(db, 2, pwd, 'res.partner.category', 'write', id, vals)
                print (status)
            else:
                status = socket.execute(db, 2, pwd, 'res.partner.category', 'create', vals)
                print(status)
        except:
            f.write(line.get('CLASS-CODE          ').strip())
            f.write('\n')
