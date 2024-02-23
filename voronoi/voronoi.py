import time
from random import random, seed, randint
from utils import (
    tangentes,
    convex_divide,
    mediatriz,
    interseccionRectas,
    enSegmento,
    areaSignada,
)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.region = {}

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def criba(self):
        # quitamos las mediatrices que se han desconectado por actualizar la mediatriz
        # utilizamos un bucle ya que al quitar una mediatriz puede que se desconecten mas
        criba = True
        while criba:
            criba = False
            conexiones = {}
            for key, value in self.region.items():
                for i in range(2):
                    if value[1][i] == 0:
                        if str(value[0][i]) in conexiones:
                            conexiones[str(value[0][i])].append(key)
                        else:
                            conexiones[str(value[0][i])] = [key]
            for key, value in conexiones.items():
                if len(value) == 1:
                    if value[0] in self.region:
                        self.region.pop(value[0])
                        value[0].region.pop(self)

                        criba = True


class Voronoi:
    def __init__(self, points):
        self.points = [Point(x, y) for x, y in points]
        self.voronoi()

    def __repr__(self):
        return f"Voronoi({self.points})"

    def __str__(self):
        return f"Voronoi({self.points})"

    def actualizada(self, med, med_nueva, lado):
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

    def unir_vor(self, voronoi_A, voronoi_B, A_convex, B_convex, profundidad):

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

            med_actualizada = self.actualizada(
                med_actualizada[0], med_nueva[0], med_actualizada[1]
            )

            # actualizamos el diccionario
            voronoi[pivot_A][pivot_B] = med_nueva
            voronoi[pivot_B][pivot_A] = med_nueva
            voronoi[punto1][punto2] = med_actualizada
            voronoi[punto2][punto1] = med_actualizada

            # criba
            voronoi = self.criba(voronoi, punto1)

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
            voronoi[t_inferior[0]][t_inferior[1]] = [
                [ultima_interseccion, final],
                [0, 1],
            ]
            voronoi[t_inferior[1]][t_inferior[0]] = [
                [ultima_interseccion, final],
                [0, 1],
            ]
        else:
            voronoi[t_inferior[0]][t_inferior[1]] = [
                [final, ultima_interseccion],
                [1, 0],
            ]
            voronoi[t_inferior[1]][t_inferior[0]] = [
                [final, ultima_interseccion],
                [1, 0],
            ]

        # if profundidad==0:
        #     cicatriz.append([ultima_interseccion,final])

        #     for i in cicatriz:
        #         G += line(i,color="black",thickness=4)
        #         slides.append(G)

        return voronoi, convex, slides

    def voronoi(self, profundidad=0, G=None):
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
            voronoi_P1, convex_P1, slides = self.voronoi(P1, profundidad + 1)
            voronoi_P2, convex_P2, slides = self.voronoi(P2, profundidad + 1)
            # if profundidad==0:
            #     G = Graphics()
            # unir_vor
            voronoi_P, convex_P, slides = self.unir_vor(
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
    voronoi_P, convex_P, slides = Voronoi(P)
    fin = time.time()
    print("tiempo:", fin - inicio)
