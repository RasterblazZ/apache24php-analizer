from flask import Flask, render_template,request,redirect, url_for, Response
import re
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route("/")
def hello_world():
    print('Todo gucci')
    return render_template('formulario.html')

@app.route("/graf")
def graf():
    return plot(1065644,108657,6800)

def plot(info,warning,error,list,list_detail):
    # Datos para el gráfico
    tipos = ['Notice', 'Warning', 'Error']
    cantidades = [info, warning, error]  # Puedes ajustar estas cantidades según tus datos

    plt.bar(tipos, cantidades, color=['blue', 'orange', 'red', 'purple'])
    plt.xlabel('')
    plt.ylabel('Qty')
    plt.title('ERROR LOG REPORT')

    # Ajustar el eje Y para que muestre los valores completos
    plt.ticklabel_format(axis='y', style='plain')

    # Agregar etiquetas de texto debajo de cada barra
    for i, v in enumerate(cantidades):
        plt.text(i, v + 50, str("{:,.2f}".format(v)), ha='center', va='bottom', fontsize=10)


    # Convertir el gráfico a una imagen en formato base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    buffer = base64.b64encode(img.getvalue()).decode()

    plt.close()

    # print(list)
    return render_template('plot.html',plot=buffer,errolist=list,errorlist_detail=list_detail)

@app.route('/cargarDatos',methods=['POST'])
def fileReader():
    archivo = request.files['archivo']
    # Abre el archivo en modo lectura ('r')
    # archivo = open('archivo.txt', 'r')

    # Lee todo el contenido del archivo y lo almacena en una lista de líneas
    lineas = archivo.readlines()

    # Cierra el archivo después de leerlo
    archivo.close()

    cnotice = 0
    cwarning = 0
    cerror = 0
    error_list_headers = []
    error_list = []
    # Itera a través de las líneas e imprime cada una
    for linea in lineas:
        # Expresión regular para capturar diferentes partes del registro de log
        patron = r'\[(.*?)\] \[(.*?)\] \[pid (.*?):tid (.*?)\] \[client (.*?):(.*?)\] (.*)'

        # stringmistico = linea.strip()
        # La línea de texto con el formato a analizar
        resultado = re.match(patron,linea.decode('utf-8'))

        # break
        if resultado:
            fecha = resultado.group(1)
            nivel = resultado.group(2)
            if(nivel == 'php7:notice'):
                cnotice = cnotice + 1
            if(nivel == 'php7:warn'):
                cwarning = cwarning + 1
            if(nivel == 'php7:error'):
                cerror = cerror + 1
                patron2 = r'in\s+([A-Za-z]:\\.*?)(?=\s|$)'
                resultadoRutas = re.findall(patron2,mensaje)
                rutas=''
                if resultadoRutas:
                    rutas = resultadoRutas[0]
                    # print(rutas)
                try:
                    index = error_list_headers.index(rutas)
                except ValueError:
                    error_list_headers.append(rutas)
                    index = error_list_headers.index(rutas)
                
                try:
                    index = error_list.index([rutas,mensaje])
                except ValueError:
                    error_list.append([rutas,mensaje])
                
                
            pid = resultado.group(3)
            tid = resultado.group(4)
            cliente_ip = resultado.group(5)
            cliente_puerto = resultado.group(6)
            mensaje = resultado.group(7)

            # print(cnotice)
            # print(cwarning)
            # print(cerror)
        else:
            print("No se encontró una coincidencia.")

        
        # print(linea.strip())  # strip() elimina los caracteres de nueva línea al final
    print(f"infos : {cnotice}, warning : {cwarning}, errors : {cerror}")
    return plot(cnotice,cwarning,cerror,error_list_headers,error_list)
    # return 'Im uploading a file'