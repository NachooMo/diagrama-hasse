# LIBRERÍAS
import streamlit as st
import random
import time
import networkx as nx
import matplotlib.pyplot as plt


# OBTENER DIVISORES
def obt_div(n):
    divisores = []

    for i in range(1, n + 1):
        if n % i == 0:
            divisores.append(i)

    return divisores


# RELACIONES DE DIVISIBILIDAD
def relacion_div(A):
    relaciones = []

    for a in A:
        for b in A:
            if b % a == 0:
                relaciones.append((a, b))

    return relaciones


# RELACIONES REDUNDANTES
def redundante(a, b, A):
    for c in A:
        if c != a and c != b:
            if b % c == 0 and c % a == 0:
                return True

    return False


# RELACIONES DEL DIAGRAMA DE HASSE
def rela_hasse(A):
    hasse = []

    for a in A:
        for b in A:
            if a != b and b % a == 0:
                if not redundante(a, b, A):
                    hasse.append((a, b))

    return hasse


# NIVELES DEL DIAGRAMA
def niveles(A):
    nivel = {}

    for a in A:
        nivel[a] = 0

    cambio = True

    while cambio:
        cambio = False

        for a in A:
            for b in A:
                if a != b and b % a == 0:
                    if not redundante(a, b, A):
                        if nivel[b] <= nivel[a]:
                            nivel[b] = nivel[a] + 1
                            cambio = True

    return nivel


# DIBUJAR DIAGRAMA
def dibujar_hasse(A):

    relaciones = rela_hasse(A)
    niveles_nodos = niveles(A)

    G = nx.DiGraph()

    for nodo in A:
        G.add_node(nodo)

    for a, b in relaciones:
        G.add_edge(a, b)

    pos = {}

    grupos = {}

    for nodo, nivel in niveles_nodos.items():

        if nivel not in grupos:
            grupos[nivel] = []

        grupos[nivel].append(nodo)

    for nivel, nodos in grupos.items():

        cantidad = len(nodos)

        for i, nodo in enumerate(sorted(nodos)):
            x = i - (cantidad - 1) / 2
            y = nivel
            pos[nodo] = (x, y)

    fig, ax = plt.subplots(figsize=(8, 6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        node_color="#67C9D8",
        edgecolors="black",
        linewidths=2,
        font_size=12,
        font_weight="bold",
        width=2.5,
        arrows=False,
        ax=ax
    )

    plt.title(
        "Diagrama de Hasse",
        fontsize=18,
        fontweight="bold"
    )

    plt.axis("off")

    return fig


# INTERFAZ STREAMLIT

st.title("📊 Diagramas de Hasse")

st.write(
    """
Relación de divisibilidad mediante diagramas de Hasse.

Este programa calcula los divisores de un número natural,
construye la relación de divisibilidad y genera el
diagrama de Hasse.
"""
)


# BOTÓN ALEATORIO
if st.button("🎲 Generar número aleatorio"):
    st.session_state.numero = random.randint(1, 1000)


# INPUT
numero = st.number_input(
    "Ingrese un número natural",
    min_value=1,
    max_value=1000,
    value=st.session_state.get("numero", 1),
    step=1
)


# BOTÓN PRINCIPAL
if st.button("🚀 Generar Diagrama"):

    st.subheader("1. Cálculo de divisores")

    st.write(
        """
Se recorren todos los números desde 1 hasta n.
Si el residuo de n % i es 0, entonces i es divisor.
"""
    )

    divisores = obt_div(numero)

    st.success(f"Divisores de {numero}: {divisores}")

    time.sleep(1)

    st.subheader("2. Relación de divisibilidad")

    st.write(
        """
Se comparan todos los divisores entre sí.
Si un número divide exactamente a otro,
se crea un par ordenado.
"""
    )

    relaciones = relacion_div(divisores)

    for a, b in relaciones:
        st.write(f"({a}, {b})")

    time.sleep(1)

    st.subheader("3. Eliminación de relaciones redundantes")

    st.write(
        """
Se eliminan relaciones reflexivas y transitivas
para conservar únicamente las conexiones directas
del diagrama de Hasse.
"""
    )

    time.sleep(1)

    st.subheader("4. Relaciones del diagrama de Hasse")

    hasse = rela_hasse(divisores)

    for a, b in hasse:
        st.write(f"{a} → {b}")

    time.sleep(1)

    st.subheader("5. Visualización gráfica")

    fig = dibujar_hasse(divisores)

    st.pyplot(fig)
