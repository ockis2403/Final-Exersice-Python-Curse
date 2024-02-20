from pathlib import Path
from os import system, remove, rmdir
from shutil import rmtree
import os
import msvcrt
import sys

recetario = {'carnes':['Entrecot al Malbec','Matambre a la Pizza'],
             'ensaladas':['Ensalada Griega','Ensalada Mediterranea'],
             'pastas':['Canelones de Espinaca','Ravioles de Ricotta'],
             'postres':['Compota de Manzana','Tarta de Frambuesa']}


def preparar_db():
    lista_carpetas = os.listdir(r"C:\Recetas")
    if len(lista_carpetas) == 0:
        instalar_db()
    else:
        recetario.clear()
        for carpeta in lista_carpetas:
            recetario[carpeta] = []
            ruta = crear_ruta(carpeta)
            lista_archivos = os.listdir(ruta)
            for archivo in lista_archivos:
                a = archivo.replace('.txt', '')
                recetario[carpeta].append(a)


def crear_ruta(*args):
    base = r"C:\Recetas"
    op = len(args)
    match op:
        case 1:
            rutaf = Path(base, args[0])
        case 2:
            rutaf = Path(base, args[0], args[1]+'.txt')
    return rutaf


def grabar_carpeta(rutaf):
    os.mkdir(rutaf)


def grabar_archivo(rutaf, titulof):
    with open(rutaf, "w") as file:
        file.write(titulof + '\n')


def grabar_receta(rutaf, texto):
    with open(rutaf, "a") as rct:
        rct.write(texto)


def instalar_db():
    texto_receta = {'Entrecot al Malbec': 'texto', 'Matambre a la Pizza': 'texto',
                    'Ensalada Griega': 'texto', 'Ensalada Mediterranea': 'texto',
                    'Canelones de Espinaca': 'texto', 'Ravioles de Ricotta': 'texto',
                    'Compota de Manzana': 'texto', 'Tarta de Frambuesa': 'texto'}
    listCarpetas = recetario.keys()
    for carpeta in listCarpetas:
        ruta = crear_ruta(carpeta)
        try:
            grabar_carpeta(ruta)
        except:
            print("Error")
            una_tecla()
            sys.exit()
        listaArchivos = recetario[carpeta]
        for archivo in listaArchivos:
            ruta = crear_ruta(carpeta, archivo)
            try:
                grabar_archivo(ruta, archivo)
            except:
                print("Error")
                una_tecla()
                sys.exit()
            grabar_receta(ruta, texto_receta[archivo])


def menu():
    lista_menupr = ['leer receta', 'agregar receta', 'eliminar receta',
                'agregar categoria', 'eliminar categoria', 'salir']
    opc = seleccion(0,lista_menupr)
    return opc


def encabezados(pos):
    encabezado = ['******Tu recitario 1.0*******',
                   '******Tus categorias*******',
                   '******Tus recetas*******',
                   '******Nuevas recetas*******',
                   '*Esta a punto de eliminar una receta\nDesea Continuar?*',
                   '*Esta a punto de elminar una categoria\nEsto borrara todas las recetas de la misma\nDesea continuar?*']
    return encabezado[pos]


def seleccion(tm, lista_menu):
    while True:
        limpiar_pantalla()
        print(encabezados(tm))
        fila = 1
        for elemento in lista_menu:
            print(f'{fila} {elemento}')
            fila+=1
        try:
            opc = int(input("Selecciona una opcion: "))
            if (opc > 0) and (opc <= len(lista_menu)):
                break
            else:
                print("opcion incorrecta\n")
                una_tecla()
        except:
            print("Error leyendo la opcion\n")
            una_tecla()
    return opc


def una_tecla():
    print("\nPresione una tecla para continuar...")
    msvcrt.getch()


def limpiar_pantalla():
    system('cls')


def leer_receta():
    categoria = pedir_categoria()
    if len(categoria) != 0:
        receta = pedir_receta(categoria)
        if len(receta) != 0:
            ruta = crear_ruta(categoria,receta)
            mostrar_receta(ruta)


def pedir_categoria():
    lista_categorias = list(recetario.keys())
    if len(lista_categorias) == 0:
        limpiar_pantalla()
        print('No hay categorias para mostrar')
        una_tecla()
        return lista_categorias
    else:
        opc = seleccion(1, lista_categorias)
        return lista_categorias[opc-1]


def pedir_receta(llave):
    lista_recetas = list(recetario[llave])
    if len(lista_recetas) == 0:
        limpiar_pantalla()
        print("No hay recetas para mostrar")
        una_tecla()
        return lista_recetas
    else:
        opc = seleccion(2, lista_recetas)
        return lista_recetas[opc - 1]


def mostrar_receta(rutaf):
    limpiar_pantalla()
    with open(rutaf, 'r') as archivo:
        print(archivo.read())
    una_tecla()


def agregar_receta():
    lista_esnueva = ['Categoria  Existente', 'Categoria Nueva']
    sw = 1
    opc = seleccion(3,lista_esnueva)



    if opc == 1:
        categoria = pedir_categoria()
        if len(categoria) != 0:
            texto_receta = pedir_texto_receta()
            while sw:
                try:
                    receta = pedir_titulo_receta()
                    ruta = crear_ruta(categoria,receta)
                    grabar_archivo(ruta, receta)
                    sw = 0
                except:
                    print("Error al guardar archivo, verifique el titulo (caracteres especiales")
                    una_tecla()
            grabar_receta(ruta, texto_receta)
            actualizar_indice_receta(1,categoria, receta)
    else:
        print("Cree la categoria Primero")
        una_tecla()


def pedir_texto_receta():
    textoreceta = []
    limpiar_pantalla()
    print('Instrucciones: \nIntroduzca el texto de su receta, para guardar el texto\n'
          'Coloque en una sola linea la palabra: fin\n')
    while True:
        linea = input()
        textoreceta.append(linea + '\n')
        if 'fin' in linea:
            break
    textoformateado = ''.join(textoreceta)
    return textoformateado


def pedir_titulo_receta():
    limpiar_pantalla()
    print('Introduzca el titulo de su receta. No use caracteres especiales')
    tituloreceta = input()
    return tituloreceta


def actualizar_indice_receta(opc, *args):
    match opc:
        case 1:
            recetario[args[0]].append(args[1])
        case 2:
            lista = list(recetario[args[0]])
            lista.remove(args[1])
            recetario[args[0]] = lista
        case 3:
            recetario[args[0]] = []
        case 4:
            del recetario[args[0]]
    limpiar_pantalla()
    print("\nSe ha actualizado el indice del recetario")
    una_tecla()


def eliminar_receta():
    lista = ['si', 'no']
    opc = seleccion(4, lista)
    if opc == 1:
        categoria = pedir_categoria()
        if len(categoria) != 0:
            receta = pedir_receta(categoria)
            if len(receta) != 0:
                ruta = crear_ruta(categoria, receta)
                borrar_receta(ruta)
                actualizar_indice_receta(2, categoria, receta)


def borrar_receta(rutaf):
    remove(rutaf)


def agregar_categoria():
    while True:
        limpiar_pantalla()
        try:
            print('Introduce la nueva categoria')
            categoria = input("No uses caracteres especiales: ")
            ruta = crear_ruta(categoria)
            grabar_carpeta(ruta)
            break
        except:
            print("Error, verifique el nombre de carpeta")
            una_tecla()
    actualizar_indice_receta(3, categoria)


def eliminar_categoria():
    lista = ['si', 'no']
    opc = seleccion(5, lista)
    if opc == 1:
        categoria = pedir_categoria()
        if len(categoria) != 0:
            ruta = crear_ruta(categoria)
            lista = os.listdir(ruta)
            if len(lista) == 0:
                rmdir(ruta)
            else:
                rmtree(ruta)
            actualizar_indice_receta(4, categoria)


def recetario_exe():
    preparar_db()
    while True:
        opcion = menu()
        match opcion:
            case 1:
                leer_receta()
            case 2:
                agregar_receta()
            case 3:
                eliminar_receta()
            case 4:
                agregar_categoria()
            case 5:
                eliminar_categoria()
            case 6:
                break
    print("Disfrute la cocina")


recetario_exe()