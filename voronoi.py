from math import sqrt
import time
from random import random, seed, randint


def areaSignada(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) / 2


def interseccionRectas(r, s):
    x1 = r[1][1] - r[0][1]
    y1 = r[0][0] - r[1][0]
    x2 = s[1][1] - s[0][1]
    y2 = s[0][0] - s[1][0]
    if x1 * y2 - x2 * y1 == 0:
        print("\n* Rectas paralelas. ", end="")
    else:
        z1 = r[0][0] * r[1][1] - r[0][1] * r[1][0]
        z2 = s[0][0] * s[1][1] - s[0][1] * s[1][0]
        x = (z1 * y2 - z2 * y1) / (x1 * y2 - x2 * y1)
        y = (x1 * z2 - x2 * z1) / (x1 * y2 - x2 * y1)
        return [x, y]


def enSegmento(p, s_comp):
    # if round(areaSignada(p,s[0],s[1]),5)!=0:
    #     return False
    s, s_info = s_comp
    # s contiene los puntos del segmento ([x,y],[x,y])
    # s_info contiene informacion de los extremos del segmento [0,0]. 0 es cerrado, 1 es infinito
    if s_info[0] == 0:
        if s_info[1] == 0:
            if s[0][0] <= p[0] and p[0] <= s[1][0]:
                return True
        elif s_info[1] == 1:
            if s[0][0] <= p[0]:
                return True
    elif s_info[0] == 1:
        if s_info[1] == 0:
            if p[0] <= s[1][0]:
                return True
        elif s_info[1] == 1:
            return True
    return False


def mediatriz(p, q):
    k = 4
    m = ((q[0] + p[0]) / 2, (q[1] + p[1]) / 2)
    p = (-(q[1] - p[1]), (q[0] - p[0]))
    med = [[m[0] - k * p[0], m[1] - k * p[1]], [m[0] + k * p[0], m[1] + k * p[1]]]
    # ordenamos de menor a mayor respecto a la x
    if med[0][0] > med[1][0]:
        return [med[1], med[0]]
    else:
        return [med[0], med[1]]


def es_tangente(A, a, B, b):
    x = areaSignada(A[a - 1], A[a], B[b])
    y = areaSignada(A[a], A[(a + 1) % len(A)], B[b])
    if x * y < 0:
        if x < 0 and y > 0:
            return 1
        if x > 0 and y < 0:
            return 2
    elif x == 0 and y == 0:
        print("ERROR: Dos puntos de B son colineales con A")
        return False
    elif x == 0:
        if y < 0:
            return 2
        else:
            return 1
    elif y == 0:
        if x < 0:
            return 1
        else:
            return 2
    else:
        return False


def tangentes_punto(P, q):
    vertices = []
    for i in range(len(P) - 1):
        if areaSignada(P[i - 1], P[i], q) * areaSignada(P[i], P[i + 1], q) < 0:
            vertices.append([P[i], i])
    if areaSignada(P[-2], P[-1], q) * areaSignada(P[-1], P[0], q) < 0:
        vertices.append([P[-1], len(P) - 1])

    # ordenar por max respecto a la y
    # vertices = sorted(vertices,key=lambda x: x[0][1], reverse=True)

    # ordenar respecto a la pendiente y
    dy1 = vertices[0][0][1] - q[1]
    dx1 = abs(vertices[0][0][0] - q[0])
    dy2 = vertices[1][0][1] - q[1]
    dx2 = abs(vertices[1][0][0] - q[0])
    p1 = dy1 / dx1
    p2 = dy2 / dx2
    if p1 > p2:
        return vertices[0][1], vertices[1][1]
    else:
        return vertices[1][1], vertices[0][1]


def tangentes(A, B):
    if len(A) == 1:
        a, b = tangentes_punto(B, A[0])
        return [A[0], B[a]], [A[0], B[b]]
    if len(B) == 1:
        a, b = tangentes_punto(A, B[0])
        return [A[a], B[0]], [A[b], B[0]]
    a = max(range(len(A)), key=lambda x: A[x][0])
    b = min(range(len(B)), key=lambda x: B[x][0])

    # Tangente superior
    a_s, b_s = a, b
    aa, bb = -1, -1
    while aa != a_s or bb != b_s:
        aa, bb = a_s, b_s
        while es_tangente(A, a_s, B, b_s) != 1:
            a_s = (a_s + 1) % len(A)
        while es_tangente(B, b_s, A, a_s) != 2:
            b_s = (b_s - 1) % len(B)
    t_superior = [A[a_s], B[b_s]]

    # Tangente inferior
    a_i, b_i = a, b
    aa, bb = -1, -1
    while aa != a_i or bb != b_i:
        aa, bb = a_i, b_i
        while es_tangente(A, a_i, B, b_i) != 2:
            a_i = (a_i - 1) % len(A)
        while es_tangente(B, b_i, A, a_i) != 1:
            b_i = (b_i + 1) % len(B)
    t_inferior = [A[a_i], B[b_i]]

    return t_superior, t_inferior


def convex_divide(convex_A, convex_B, tangente_superior, tangente_inferior):
    # A es izquierda, B es derecha

    # guardar la parte de la lista que empieza por la tangente superior y acaba por la tangente inferior (modular)
    convex_B2 = []
    i = convex_B.index(tangente_inferior[1])
    j = convex_B.index(tangente_superior[1])
    if i < j:
        convex_B2 = convex_B[i : j + 1]
    elif i > j:
        #  de i a len(A) y de 0 a j
        convex_B2 = convex_B[i:] + convex_B[: j + 1]
    else:
        convex_B2 = [convex_B[i]]

    convex_A2 = []
    i = convex_A.index(tangente_superior[0])
    j = convex_A.index(tangente_inferior[0])
    if i < j:
        convex_A2 = convex_A[i : j + 1]
    elif i > j:
        #  de i a len(A) y de 0 a j
        convex_A2 = convex_A[i:] + convex_A[: j + 1]
    else:
        convex_A2 = [convex_A[i]]

    convex = convex_B2 + convex_A2
    # siendo la lista circular, reordenamos para que empiece por el mas bajo
    y_min = min(convex, key=lambda x: x[1])
    i = convex.index(y_min)
    convex = convex[i:] + convex[:i]

    return convex


def actualizada(med, med_nueva, lado):
    # ordenamos la med_nueva de mayor a menor respecto a la y
    med_nueva = sorted(med_nueva, key=lambda x: x[1], reverse=True)
    dx = abs(med[0][0][0] - med[0][1][0])
    dy = abs(med[0][0][1] - med[0][1][1])
    # si la med está a la izquierda
    if med[0][0][0] < med_nueva[1][0] and med[0][1][0] < med_nueva[1][0]:
        # alargamos el extremo derecho
        # si la med está por encima
        if med[0][0][1] > med_nueva[1][1] and med[0][1][1] > med_nueva[1][1]:
            dy = -dy
        # si la med está por debajo
        med[0][1] = [med_nueva[1][0] + dx, med_nueva[1][1] + dy]

    # si la med está a la derecha
    elif med[0][0][0] > med_nueva[1][0] and med[0][1][0] > med_nueva[1][0]:
        # alargamos el extremo izquierdo
        dx = -dx
        # si la med está por encima
        if med[0][0][1] > med_nueva[1][1] and med[0][1][1] > med_nueva[1][1]:
            dy = -dy
        med[0][0] = [med_nueva[1][0] + dx, med_nueva[1][1] + dy]

    # voronoi A, lado izquierdo
    if lado == 0:
        if areaSignada(med_nueva[0], med_nueva[1], med[0][0]) < 0:
            return [[med[0][0], med_nueva[1]], [med[1][0], 0]]
        else:
            return [[med_nueva[1], med[0][1]], [0, med[1][1]]]
    # voronoi A, lado derecho
    elif lado == 1:
        if areaSignada(med_nueva[0], med_nueva[1], med[0][0]) < 0:
            return [[med_nueva[1], med[0][1]], [0, med[1][1]]]
        else:
            return [[med[0][0], med_nueva[1]], [med[1][0], 0]]


def criba(A, punto):
    # quitamos las mediatrices que se han desconectado por actualizar la mediatriz
    # utilizamos un bucle ya que al quitar una mediatriz puede que se desconecten mas
    criba = True
    while criba:
        criba = False
        conexiones = {}
        for key, value in A[punto].items():
            for i in range(2):
                if value[1][i] == 0:
                    if str(value[0][i]) in conexiones:
                        conexiones[str(value[0][i])].append(key)
                    else:
                        conexiones[str(value[0][i])] = [key]
        for key, value in conexiones.items():
            if len(value) == 1:
                if value[0] in A[punto]:
                    A[punto].pop(value[0])
                    A[value[0]].pop(punto)
                    criba = True
    return A


def unir_vor(voronoi_A, voronoi_B, A_convex, B_convex, profundidad):

    slides = []
    # if profundidad==0:
    #     G = Graphics()
    #     G += points(A,color="black")+points(B,color="black")
    #     slides.append(G)
    #     G += points(A, color="red",size=25)+points(B,color="blue",size=25)
    #     slides.append(G)
    #     G += polygon(A_convex,alpha=0.1,color="red")
    #     G += polygon(B_convex,alpha=0.1,color="blue")
    #     # nos guardamos el plot en un slide
    #     slides.append(G)

    # hallamos las tangentes
    t_superior, t_inferior = tangentes(A_convex, B_convex)

    convex = convex_divide(A_convex, B_convex, t_superior, t_inferior)

    # if profundidad==0:
    #     G +=point(A,color="red")+point(B)+line(t_superior)+line(t_inferior)
    #     slides.append(G)

    # hallamos las mediatrices de las tangentes
    me_superior = mediatriz(t_superior[0], t_superior[1])
    ms = (
        (t_superior[0][0] + t_superior[1][0]) / 2,
        (t_superior[0][1] + t_superior[1][1]) / 2,
    )
    me_inferior = mediatriz(t_inferior[0], t_inferior[1])
    mi = (
        (t_inferior[0][0] + t_inferior[1][0]) / 2,
        (t_inferior[0][1] + t_inferior[1][1]) / 2,
    )

    # if profundidad==0:
    #     G += line(me_superior, color="black", linestyle="dashed",alpha=0.5)
    #     G += line(me_inferior, color="black", linestyle="dashed",alpha=0.5)
    #     G += point(ms,color="black",alpha=0.5,size=20) + point(mi,color="black",alpha=0.5,size=20)
    #     slides.append(G)
    #     G = showVoronoi(voronoi_A,G,'red')
    #     G = showVoronoi(voronoi_B,G,'blue')
    #     slides.append(G)

    #     cicatriz = []

    # juntamos los dos diccionarios
    voronoi = voronoi_A.copy()
    voronoi.update(voronoi_B)

    # iniciamos los pivotes
    pivot_A, pivot_B = t_superior[0], t_superior[1]
    me_pivot = [me_superior, [1, 1]]
    pivot_anterior = (0, 0)
    inicio = max(me_pivot[0], key=lambda x: x[1])
    ultima_interseccion = inicio

    while pivot_A != t_inferior[0] or pivot_B != t_inferior[1]:
        punto1 = (0, 0)  # pivot
        punto2 = (0, 0)  # posible cambio
        med_nueva = [[]]  # nueva mediatriz de voronoi
        med_actualizada = [[], []]  # mediatriz que necesitamos actualizar
        interseccion_mas_alta = (
            -float("inf"),
            -float("inf"),
        )  # para quedarnos con la interseccion mas alta

        for A_key, A_value in voronoi[pivot_A].items():
            if A_key != pivot_anterior:
                interseccion = interseccionRectas(me_pivot[0], A_value[0])
                if not interseccion:
                    continue
                elif interseccion[1] > interseccion_mas_alta[1]:
                    if enSegmento(interseccion, A_value):
                        punto1 = pivot_A
                        punto2 = A_key
                        if interseccion[0] < ultima_interseccion[0]:
                            med_nueva = [
                                [interseccion, ultima_interseccion],
                                [0, int(inicio == ultima_interseccion)],
                            ]
                        else:
                            med_nueva = [
                                [ultima_interseccion, interseccion],
                                [int(inicio == ultima_interseccion), 0],
                            ]
                        med_actualizada = [A_value, 0]
                        interseccion_mas_alta = interseccion

        for B_key, B_value in voronoi[pivot_B].items():
            if B_key != pivot_anterior:
                interseccion = interseccionRectas(me_pivot[0], B_value[0])
                if not interseccion:
                    continue
                elif interseccion[1] > interseccion_mas_alta[1]:
                    if enSegmento(interseccion, B_value):
                        punto1 = pivot_B
                        punto2 = B_key
                        if interseccion[0] < ultima_interseccion[0]:
                            med_nueva = [
                                [interseccion, ultima_interseccion],
                                [0, int(inicio == ultima_interseccion)],
                            ]
                        else:
                            med_nueva = [
                                [ultima_interseccion, interseccion],
                                [int(inicio == ultima_interseccion), 0],
                            ]
                        med_actualizada = [B_value, 1]
                        interseccion_mas_alta = interseccion

        # excepcion de interseccion por encima de la tangente superior
        if ultima_interseccion == inicio:
            i_extremo = max(range(2), key=lambda x: med_nueva[0][x][1])
            if med_nueva[0][i_extremo] != inicio:
                dx = abs(med_nueva[0][i_extremo][0] - inicio[0])
                dy = abs(med_nueva[0][i_extremo][1] - inicio[1])
                if i_extremo == 0:
                    nuevo_extremo = [
                        med_nueva[0][i_extremo][0] - dx,
                        med_nueva[0][i_extremo][1] + dy,
                    ]
                    med_nueva = [[nuevo_extremo, med_nueva[0][i_extremo]], [1, 0]]
                else:
                    nuevo_extremo = [
                        med_nueva[0][i_extremo][0] + dx,
                        med_nueva[0][i_extremo][1] + dy,
                    ]
                    med_nueva = [[med_nueva[0][i_extremo], nuevo_extremo], [0, 1]]

        med_actualizada = actualizada(
            med_actualizada[0], med_nueva[0], med_actualizada[1]
        )

        # actualizamos el diccionario
        voronoi[pivot_A][pivot_B] = med_nueva
        voronoi[pivot_B][pivot_A] = med_nueva
        voronoi[punto1][punto2] = med_actualizada
        voronoi[punto2][punto1] = med_actualizada

        # criba
        voronoi = criba(voronoi, punto1)

        # actualizamos los pivotes
        if punto1 == pivot_A:
            pivot_anterior = pivot_A
            pivot_A = punto2
        else:
            pivot_anterior = pivot_B
            pivot_B = punto2

        # actualizamos la mediatriz
        me_pivot = [mediatriz(pivot_A, pivot_B), [1, 1]]
        ultima_interseccion = interseccion_mas_alta

        # if profundidad == 0:
        #     cicatriz.append(med_nueva[0])

    # excepcion de interseccion por debajo de la tangente inferior
    final = min(me_inferior, key=lambda x: x[1])
    if ultima_interseccion[1] < final[1]:
        dx = abs(me_inferior[1][0] - me_inferior[0][0])
        dy = abs(me_inferior[1][1] - me_inferior[0][1])
        if ultima_interseccion[0] < final[0]:
            final = [ultima_interseccion[0] - dx, ultima_interseccion[1] - dy]
        else:
            final = [ultima_interseccion[0] + dx, ultima_interseccion[1] - dy]

    # añadimos la ultima mediatriz
    if ultima_interseccion[0] < final[0]:
        voronoi[t_inferior[0]][t_inferior[1]] = [[ultima_interseccion, final], [0, 1]]
        voronoi[t_inferior[1]][t_inferior[0]] = [[ultima_interseccion, final], [0, 1]]
    else:
        voronoi[t_inferior[0]][t_inferior[1]] = [[final, ultima_interseccion], [1, 0]]
        voronoi[t_inferior[1]][t_inferior[0]] = [[final, ultima_interseccion], [1, 0]]

    # if profundidad==0:
    #     cicatriz.append([ultima_interseccion,final])

    #     for i in cicatriz:
    #         G += line(i,color="black",thickness=4)
    #         slides.append(G)

    return voronoi, convex, slides


def voronoi(P, profundidad=0, G=None):
    slides = []
    if len(P) == 1:
        voronoi_P = {P[0]: {}}
        # G+=point(P,color="red")
        return voronoi_P, P, slides
    elif len(P) == 2:
        med_p1 = mediatriz(P[0], P[1])
        voronoi_P = {P[0]: {P[1]: [med_p1, [1, 1]]}, P[1]: {P[0]: [med_p1, [1, 1]]}}
        return voronoi_P, P, slides
    else:
        # extremos respecto a la coordenada x
        p_max = max(P)
        p_min = min(P)
        # punto medio
        m = (p_max[0] + p_min[0]) / 2
        # dividimos la lista
        P1 = [p for p in P if p[0] <= m]
        P2 = [p for p in P if p[0] > m]
        # recursivividad
        voronoi_P1, convex_P1, slides = voronoi(P1, profundidad + 1)
        voronoi_P2, convex_P2, slides = voronoi(P2, profundidad + 1)
        # if profundidad==0:
        #     G = Graphics()
        # unir_vor
        voronoi_P, convex_P, slides = unir_vor(
            voronoi_P1, voronoi_P2, convex_P1, convex_P2, profundidad
        )

        # if profundidad==0:
        #     G = Graphics()
        #     G = showVoronoi(voronoi_P,G,'black')
        #     slides.append(G)
        #     G = Graphics()
        #     G = showDelaunay(voronoi_P,G,'black')
        #     slides.append(G)
        return voronoi_P, convex_P, slides


def showVoronoi(v, G, color_v):
    puntos = []
    segmentos = []
    for i in v:
        puntos.append(i)
        for j in v[i]:
            segmentos.append(v[i][j])
    # G += point(puntos,color=color_v)
    # for segmento in segmentos: # grosor de 30
    #     G += line(segmento[0],color=color_v,thickness=2)
    return G


def showDelaunay(v, G, color_v):
    puntos = []
    segmentos = []
    for i in v:
        puntos.append(i)
        for j in v[i]:
            segmentos.append([i, j])
    # G += point(puntos,color=color_v)
    # for segmento in segmentos:
    #     G += line(segmento,color=color_v)
    return G


if __name__ == "__main__":
    seed_prueba = randint(0, 1000)
    seed(seed_prueba)
    print("seed:", seed_prueba)

    P = [(random(), random()) for i in range(1000)]

    inicio = time.time()
    voronoi_P, convex_P, slides = voronoi(P)
    fin = time.time()
    print("tiempo:", fin - inicio)
