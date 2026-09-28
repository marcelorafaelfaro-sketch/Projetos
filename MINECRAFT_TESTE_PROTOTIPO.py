from ursina import *
from ursina.color import orange
from ursina.prefabs import sky
from ursina.prefabs.first_person_controller \
    import FirstPersonController



aplicativo = Ursina()
Sky()
"""
AQUI FICA A CAMERA
"""
for x in range(16):
    for z in range(16):
        Entity(model="cube", color=color.lime,
               texture= "white_cube",
               position=(x,0,z), collider="box")

jogador_doido = FirstPersonController(position=(8,1,2))

"""
AQUI FICAM AS CORES
"""
cores = {"1": color.gray, "2": color.orange,
         "3": color.azure, "4": color.yellow}
cor = color.gray

"""
AREA DOS COMANDOS DO TECLADO
"""
def input(key):
    if key == "escape":
        application.quit()
    global cor
    if key in cores:
        cor = cores[key]
    alvo_bisonho = mouse.hovered_entity
    if not alvo_bisonho:
        return
    if key == "right mouse down":
        Entity(model="cube", color=cor,
               texture="white_cube",
               position=alvo_bisonho.position + mouse.normal,
               collider="box")
    if key == "left mouse down":
            destroy(alvo_bisonho)

aplicativo.run()