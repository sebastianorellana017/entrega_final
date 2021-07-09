import requests
import sqlite3


def mi_funcion():

    con = sqlite3.connect('C:/Users/sebas/Downloads/ventas_ultima_entrega/Group_ventas-master/db.sqlite3')
    
    cur = con.cursor()

    r = requests.get('http://54.242.117.221:5000/Productos')
    to_db = r.json()

    n = 20

    for i in range(n): 
       slu = to_db[i][1]
       des = to_db[i][1]
       img = to_db[i][10]
       code = to_db[i][6]
       val = to_db[i][4]
       can = to_db[i][5]
       mar = to_db[i][3]
       pes = to_db[i][7]
       tam = to_db[i][8]
       prov = to_db[i][9]
      
       cur.execute("INSERT INTO cart_product (slug, nombre, image,descripcion, valor, peso, tamano, proveedor,cantidad, marca) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", ( slu,des,img,code, val, pes, tam, prov,can, mar))
    
   

    con.commit()

    cur.execute('''SELECT * FROM cart_product''')
    print(cur.fetchall())

    con.close()


print(mi_funcion())