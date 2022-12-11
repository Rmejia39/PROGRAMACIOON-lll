import mysql.connector 

class Registro_datos():

    def __init__(self):
        self.conexion = mysql.connector.connect( host='localhost',
                                            database ='app_musical', 
                                            user = 'root',
                                            password ='Lukavida19')
    def busca_users(self, users):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM login WHERE usuario = {}".format(users)
        cur.execute(sql)
        usersx = cur.fetchall()
        cur.close()     
        return usersx 

    def busca_password(self, password):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM login WHERE contrasena = {}".format(password) #
        cur.execute(sql)
        passwordx = cur.fetchall()
        cur.close()     
        return passwordx