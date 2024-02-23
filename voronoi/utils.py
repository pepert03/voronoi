from math import sqrt


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
