# Módulos de Combat
En esta sección se explican de forma general las funcionalidades de los módulos
- Engine
- Field

Encargados de los combates pokemon, utilizando la lógica de Pokemon Stadium
## Engine
Dentro de este módulo únicamente se encuentra la clase "CombatEngine", la cuál recibe la información de el pokemon que ataca y el que recibe el ataque,
esto incluye sus atributos, el movimiento usado, una lista con movimientos usados, y las estadísticas de combate.

Posee cinco métodos, de los cuales "Calculate_damage" es el principal y del que se llaman los demás:
- Status_Changes
- Hit_Accuracy
- Attack_Defense
- Critical_Hit

En conjunto, todos estos se encargan del cálculo del daño realizado en una "instancia de ataque",
en donde primero se verifica si el atacante tiene algún problema de estado (Quemadura, Envenenamiento, etc.) y dependiendo del caso, puede anularse el ataque, cambiar el objetivo o el daño inflingido.
luego se hace el cálculo para ver si el movimiento falla o no, para que, en caso de que no, se obtengan todos los valores necesarios para el cálculo del daño inflingido al pokemon receptor.

Estos incluyen:
- Nivel del Atacante
- Ataque del atacante
- Defensa del receptor
- Tipos del atacante
- Tipo del movimiento
- Debilidades, resistencias e inmunidades del receptor

Además se calcula si el golpe es crítico o no, ya que eso aumenta levemente el daño inflingido, y finalmente se entregan tres valores, el daño como entero y si es critico y si falló como booleanos.
## Field

## Aplicación
Para poder utilizar estos módulos, y todos aquellos que se importan para su funcionamiento,
es necesario crear un archivo "main.py", el cual se debe encontrar en la misma carpeta raíz donde están las carpetas "combat" y "pokemon".

De modo que se parezca a la estructura de archivos de este repositorio.
```
Poke_repo/
├── .github
├── combat
├── pokemon
├── tests
├── .gitignore
├── Readme.md
├── git_commands.md
├── requirements.txt
└── main.py
```
Así pues, el archivo main.py deberá importar la clase "Battle", que es donde se crea un campo "Field" y se llama al Engine, Pokemones, Movimientos y Estadísticas.

Dentro de la función main, la cuál será ejecutada al correr el programa directamente, solo hay que escribir un comando, y es llamar a la función "main_menu()" de Battle, eso iniciará directamente el combate.
```python
from combat.field import Battle

if __name__ == "__main__":
    # Launch interactive main menu
    Battle.main_menu()
```
