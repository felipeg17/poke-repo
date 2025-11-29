# Módulos de Combate
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
Dentro de este módulo se encuentran tres clases principales: Trainer, Field, y Battle.

Trainer representa a un entrenador de Pokémon con un equipo seleccionable. Sus responsabilidades son:

- Almacenar el nombre del entrenador y su lista de Pokémon
- Gestionar la disponibilidad de Pokémon (cuáles ya fueron usados)
- Permitir que el entrenador elija su equipo inicial desde la Pokédex mediante choose_pokemon()
- Mostrar páginas de la Pokédex mediante print_dex()

Field es la clase central que gestiona el campo de batalla y mantiene sincronizado el estado completo de la batalla entre dos entrenadores. Su funcionamiento se divide en tres niveles:

1. Creación y gestión de equipos:
- __init__() — inicializa ambos equipos, establece el primer Pokémon activo de cada entrenador, y crea diccionarios para rastrear HP y estadísticas en combate de cada Pokémon
- get_team1() / get_team2() — retorna la lista completa de Pokémon de cada entrenador
- get_active1() / get_active2() — retorna el Pokémon actualmente en batalla

2. Gestión de estadísticas de combate (getters y setters):
- get/set_combat_hp(), get/set_combat_attack(), get/set_combat_defense(), get/set_combat_sp_attack(), get/set_combat_sp_defense(), get/set_combat_speed() — obtienen y establecen las estadísticas modificadas por buffs/debuffs
- reduce_hp() — resta daño; mod_combat_*() — suma o resta valores a estadísticas
- pokemon_available() — retorna Pokémon vivos y no activos disponibles para cambiar

4. Lógica de combate y ejecución de turnos:
- resolve_turn() — orquesta todo un turno: recibe las acciones de ambos entrenadores (atacar, cambiar, rendirse), determina el orden basado en velocidad, y ejecuta los ataques llamando a execute_attack()
- execute_attack() — llama a CombatEngine.calculate_damage() para obtener el daño, aplica los efectos secundarios del movimiento mediante Move_Effect(), reduce HP del defensor, y retorna mensajes
- Move_Effect() — implementa todos los efectos especiales de cada movimiento (curaciones, cambios de estadísticas, estados de condición, movimientos multi-golpe, etc.)
- status_damage() — aplica daño pasivo por estado (quemadura, envenenamiento, etc.)

5. Gestión de condiciones de victoria y cambios forzados:
- end_battle() — retorna True si ambos equipos tienen al menos un Pokémon vivo
- winner_game() — retorna el entrenador ganador o None si la batalla continúa
- switch_defeat() — verifica si el Pokémon activo fue derrotado y hay reemplazos disponibles
- switch_pokemon() — cambia el Pokémon activo de un entrenador
- remove_defeated_pokemon() — elimina Pokémon con HP ≤ 0 del equipo y marca si es necesario cambio forzado

6. Visualización:
- health_bar() — genera una barra de vida visual en texto
- get_number_turn() — retorna el número de turno actual

El flujo general es:
1. Battle.action_py() solicita acciones de ambos entrenadores (atacar, cambiar, rendirse)
2. Field.resolve_turn() recibe ambas acciones y las ejecuta en orden de velocidad
3. Para cada ataque, Field.execute_attack() llama a CombatEngine.calculate_damage() para obtener daño base, después aplica Move_Effect() para efectos especiales
4. Field actualiza HP y estadísticas usando sus diccionarios internos
5. Field.remove_defeated_pokemon() verifica derrotas y marca cambios necesarios
6. Battle muestra mensajes y repite hasta que Field.end_battle() retorne True

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

Dentro de la función main, la cuál será ejecutada al correr el programa directamente, se deben instanciar ambos entrenadores, los cuales se agregan a un "field" y de ahí este se agrega a un "battle",
del que se debe usar la función battle(), sin embargo, es mejor usar el código ya creado en el archivo "main.py" que ya se encuentra en este repositorio, ya que cuenta con su propia interfaz y puedes repetir combates indefinidamente.
```python
from combat.field import Battle, Field, Trainer

if __name__ == "__main__":
        """Main game loop with restart menu"""
    print("=" * 60)
    print("POKÉMON BATTLE SIMULATOR")
    print("=" * 60)

    while True:
        print("\n" + "=" * 60)
        trainer1_name = input("Trainer 1 name: ")
        trainer2_name = input("Trainer 2 name: ")
        trainer1 = Trainer(trainer1_name)
        trainer2 = Trainer(trainer2_name)

        print("\n" + "=" * 60)
        trainer1.choose_pokemon()

        print("\n" + "=" * 60)
        trainer2.choose_pokemon()

        print("\n" + "=" * 60)
        print("BATTLE START!")
        print("=" * 60)
        field = Field(trainer1, trainer2)
        batalla = Battle(field)
        batalla.battle()

        print("\n" + "=" * 60)
        print("BATTLE END")
        print("=" * 60)

        while True:
            option = input(
                "\nWhat do you want to do?\n(1) Play again\n(2) Exit\n> "
            ).strip()

            if option == "1":
                print("\n" + "=" * 60)
                print("NEW BATTLE")
                print("=" * 60)
                break
            elif option == "2":
                print("\nThanks for playing! See you later!")
                break
            else:
                print("Invalid option. Choose 1 or 2.")
        if option == "2":
            break

```
