import pyvista as pv
import numpy as np
import os
import ipywidgets as widgets
from IPython.display import display



#nombre de los archivos
archivos_juntar= ["Border Zone Surface.vtk","Core Surface.vtk", "ventricle_Tagged.vtk"] 


plotter = pv.Plotter(shape=(3, 3))

# colores 
colores=['red','blue','green']
Nombres=['Borde', 'Nucleo', 'Ventrículo']

plotter.subplot(0, 0)
mallas_1=[]
for i,archivo in enumerate(archivos_juntar):
    archivo="ventriculos/p2/"+archivo
    malla = pv.read(archivo)
    if i==2:
        v_1=malla
    malla = plotter.add_mesh(malla, color=colores[i], opacity=0.5)
    mallas_1.append(malla)


plotter.add_text("Ventrículo paciente 2 con sus partes", font_size=10)

def toggle_borde_1(show):
    global plotter
    plotter.subplot(0, 0)
    mallas_1[0].SetVisibility(show)

def toggle_nucleo_1(show):
    global plotter
    plotter.subplot(0, 0)
    mallas_1[1].SetVisibility(show)

def toggle_ventriculo_1(show):
    global plotter
    plotter.subplot(0, 0)
    mallas_1[2].SetVisibility(show)

plotter.add_checkbox_button_widget(toggle_borde_1, value=True, position=(30, 20), size=20, color_on='red', background_color='white')
plotter.add_text("Borde", position=(55, 20), font_size=8, color='red')
plotter.add_checkbox_button_widget(toggle_nucleo_1, value=True, position=(30, 40), size=20, color_on='blue', background_color='white')
plotter.add_text("Nucleo", position=(55, 40), font_size=8, color='blue')
plotter.add_checkbox_button_widget(toggle_ventriculo_1, value=True, position=(30, 60), size=20, color_on='green', background_color='white')
plotter.add_text("Ventriculo", position=(55, 60), font_size=8, color='green')

plotter.subplot(0, 1)
mallas_2=[]
for i,archivo in enumerate(archivos_juntar):
    archivo="ventriculos/p5/"+archivo
    malla = pv.read(archivo)
    if i==2:
        v_2=malla
    malla = plotter.add_mesh(malla, color=colores[i], opacity=0.5)
    mallas_2.append(malla)


plotter.add_text("Ventrículo paciente 5 con sus partes", font_size=10)

def toggle_borde_2(show):
    global plotter
    plotter.subplot(0, 1)
    mallas_2[0].SetVisibility(show)

def toggle_nucleo_2(show):
    global plotter
    plotter.subplot(0, 1)
    mallas_2[1].SetVisibility(show)

def toggle_ventriculo_2(show):
    global plotter
    plotter.subplot(0, 1)
    mallas_2[2].SetVisibility(show)

plotter.add_checkbox_button_widget(toggle_borde_2, value=True, position=(30, 20), size=20, color_on='red', background_color='white')
plotter.add_text("Borde", position=(55, 20), font_size=8, color='red')
plotter.add_checkbox_button_widget(toggle_nucleo_2, value=True, position=(30, 40), size=20, color_on='blue', background_color='white')
plotter.add_text("Nucleo", position=(55, 40), font_size=8, color='blue')
plotter.add_checkbox_button_widget(toggle_ventriculo_2, value=True, position=(30, 60), size=20, color_on='green', background_color='white')
plotter.add_text("Ventriculo", position=(55, 60), font_size=8, color='green')




plotter.subplot(0, 2)
mallas_3=[]
for i,archivo in enumerate(archivos_juntar):
    archivo="ventriculos/p36/"+archivo
    malla = pv.read(archivo)
    if i==2:
        v_3=malla
    malla = plotter.add_mesh(malla, color=colores[i], opacity=0.5)
    mallas_3.append(malla)

plotter.add_text("Ventrículo 36 con sus partes", font_size=10)

def toggle_borde_3(show):
    global plotter
    plotter.subplot(0, 2)
    mallas_3[0].SetVisibility(show)

def toggle_nucleo_3(show):
    global plotter
    plotter.subplot(0, 2)
    mallas_3[1].SetVisibility(show)

def toggle_ventriculo_3(show):
    global plotter
    plotter.subplot(0, 2)
    mallas_3[2].SetVisibility(show)

plotter.add_checkbox_button_widget(toggle_borde_3, value=True, position=(30, 20), size=20, color_on='red', background_color='white')
plotter.add_text("Borde", position=(55, 20), font_size=8, color='red')
plotter.add_checkbox_button_widget(toggle_nucleo_3, value=True, position=(30, 40), size=20, color_on='blue', background_color='white')
plotter.add_text("Nucleo", position=(55, 40), font_size=8, color='blue')
plotter.add_checkbox_button_widget(toggle_ventriculo_3, value=True, position=(30, 60), size=20, color_on='green', background_color='white')
plotter.add_text("Ventriculo", position=(55, 60), font_size=8, color='green')


colores = ['pink', 'yellow', 'brown']



plotter.subplot(1, 0)

celulas_1=[]


for i, color in enumerate(colores):
    malla_tipo = v_1.extract_points(list(v_1['Cell_type']==i))
    malla=plotter.add_mesh(malla_tipo, color=color, opacity=0.5)
    celulas_1.append(malla)

plotter.add_text("Células del ventrículo 1", font_size=10)

def celulas_1_0(show):
    global plotter
    plotter.subplot(1, 0)
    celulas_1[0].SetVisibility(show)

def celulas_1_1(show):
    global plotter
    plotter.subplot(1, 0)
    celulas_1[1].SetVisibility(show)

def celulas_1_2(show):
    global plotter
    plotter.subplot(1, 0)
    celulas_1[2].SetVisibility(show)

plotter.add_checkbox_button_widget(celulas_1_0, value=True, position=(30, 20), size=20, color_on='pink', background_color='white')
plotter.add_text("Celulas 0", position=(55, 20), font_size=8, color='pink')
plotter.add_checkbox_button_widget(celulas_1_1, value=True, position=(30, 40), size=20, color_on='yellow', background_color='white')
plotter.add_text("Celulas 1", position=(55, 40), font_size=8, color='yellow')
plotter.add_checkbox_button_widget(celulas_1_2, value=True, position=(30, 60), size=20, color_on='brown', background_color='white')
plotter.add_text("Celulas 2", position=(55, 60), font_size=8, color='brown')


plotter.subplot(1, 1)

celulas_2=[]


for i, color in enumerate(colores):
    malla_tipo = v_2.extract_points(list(v_2['Cell_type']==i))
    malla=plotter.add_mesh(malla_tipo, color=color, opacity=0.5)
    celulas_2.append(malla)

plotter.add_text("Células del ventrículo 2", font_size=10)

def celulas_2_0(show):
    global plotter
    plotter.subplot(1, 1)
    celulas_2[0].SetVisibility(show)

def celulas_2_1(show):
    global plotter
    plotter.subplot(1, 1)
    celulas_2[1].SetVisibility(show)

def celulas_2_2(show):
    global plotter
    plotter.subplot(1, 1)
    celulas_2[2].SetVisibility(show)

plotter.add_checkbox_button_widget(celulas_2_0, value=True, position=(30, 20), size=20, color_on='pink', background_color='white')
plotter.add_text("Celulas 0", position=(55, 20), font_size=8, color='pink')
plotter.add_checkbox_button_widget(celulas_2_1, value=True, position=(30, 40), size=20, color_on='yellow', background_color='white')
plotter.add_text("Celulas 1", position=(55, 40), font_size=8, color='yellow')
plotter.add_checkbox_button_widget(celulas_2_2, value=True, position=(30, 60), size=20, color_on='brown', background_color='white')
plotter.add_text("Celulas 2", position=(55, 60), font_size=8, color='brown')


plotter.subplot(1, 2)

celulas_3=[]


for i, color in enumerate(colores):
    malla_tipo = v_3.extract_points(list(v_3['Cell_type']==i))
    malla=plotter.add_mesh(malla_tipo, color=color, opacity=0.5)
    celulas_3.append(malla)

plotter.add_text("Células del ventrículo 3", font_size=10)

def celulas_3_0(show):
    global plotter
    plotter.subplot(1, 2)
    celulas_3[0].SetVisibility(show)

def celulas_3_1(show):
    global plotter
    plotter.subplot(1, 2)
    celulas_3[1].SetVisibility(show)

def celulas_3_2(show):
    global plotter
    plotter.subplot(1, 2)
    celulas_3[2].SetVisibility(show)

plotter.add_checkbox_button_widget(celulas_3_0, value=True, position=(30, 20), size=20, color_on='pink', background_color='white')
plotter.add_text("Celulas 0", position=(55, 20), font_size=8, color='pink')
plotter.add_checkbox_button_widget(celulas_3_1, value=True, position=(30, 40), size=20, color_on='yellow', background_color='white')
plotter.add_text("Celulas 1", position=(55, 40), font_size=8, color='yellow')
plotter.add_checkbox_button_widget(celulas_3_2, value=True, position=(30, 60), size=20, color_on='brown', background_color='white')
plotter.add_text("Celulas 2", position=(55, 60), font_size=8, color='brown')




# Esto es para la de abajo, información sobre conectividad con slider

def slider_conectividad_1(value):
    global c1
    global plotter
    global v_1
    malla_tipo = v_1.extract_points(list(v_1['scalars']<value))
    plotter.subplot(2, 0)
    plotter.remove_actor(c1)
    c1=plotter.add_mesh(malla_tipo, show_scalar_bar=False)



plotter.subplot(2, 0)
c1=plotter.add_mesh(v_1)
plotter.add_slider_widget(callback=slider_conectividad_1, rng=[0,3000], title="Conectividad del ventrículo 1")


def slider_conectividad_2(value):
    global c2
    global plotter
    global v_2
    malla_tipo = v_2.extract_points(list(v_2['scalars']<value))
    plotter.subplot(2, 1)
    plotter.remove_actor(c2)
    c2=plotter.add_mesh(malla_tipo, show_scalar_bar=False)



plotter.subplot(2, 1)
c2=plotter.add_mesh(v_2)
plotter.add_slider_widget(callback=slider_conectividad_2, rng=[0,3000], title="Conectividad del ventrículo 2")



def slider_conectividad_3(value):
    global c3
    global plotter
    global v_3
    malla_tipo = v_3.extract_points(list(v_3['scalars']<value))
    plotter.subplot(2, 2)
    plotter.remove_actor(c3)
    c3=plotter.add_mesh(malla_tipo, show_scalar_bar=False)



plotter.subplot(2, 2)
c3=plotter.add_mesh(v_3)
plotter.add_slider_widget(callback=slider_conectividad_3, rng=[0,3000], title="Conectividad del ventrículo 3")


plotter.show()