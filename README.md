# Poke-repo
Repositorio para aprender POO usando la teoria de pokemon

## Definición 

Creaturas ficticias que viven en un mundo alternativo junto a humanos. La palabra Pokemon es el acronimo de *Pokcet Monsters*. 

### Características
- Nombre
- No en el pokedex
- Tipo principal
- Tipo Secundario
- Sexo
- Peso
- Altura
- Color
- Habilidad
- Habilidad Oculta
- Naturaleza
- Estadisticas
- Ataques
- Evoluciones

### Comportamientos
- Atacar
- Evolucionar

## Diagram

```mermaid
classDiagram
direction TB

class Pokemon {
    - _name: str
    - _pokedex_num: int
    - _type: str
    - _color: str
    - _sex: str
    - _level: int
    - _stats: Stats
    - _weaknesses: list
    - _resistances: list
    - _immunities: list
    + attack()
    + level_up()
    + receive_attack()
    + get_stats()
    + get_attribute()
    + can_evolve()
    + evolve()
    + evolution_hint()
    + __str__()
    - _get_row()
    - _resolve_evolution_target()
}

note for Pokemon "Evolución (desde CSV):\n- evolves_once: int\n- evolves_twice: int\n- evolves_by_stone: int\n- evolves_by_trade: int\n- evolution_level: int"

class Stats {
    - HP: int
    - Attack: int
    - Defense: int
    - Sp_Atk: int
    - Sp_Def: int
    - Speed: int
    - base_hp: int
    - base_attack: int
    - base_defense: int
    - base_spatk: int
    - base_spdef: int
    - base_speed: int
    + combat_stats()
    + __str__()
}

class Normal
class Fire
class Water
class Grass
class Electric
class Ice
class Fighting
class Poison
class Ground
class Flying
class Psychic
class Bug
class Rock
class Ghost
class Dragon
class Dark
class Steel
class Fairy

Pokemon <|-- Normal
Pokemon <|-- Fire
Pokemon <|-- Water
Pokemon <|-- Grass
Pokemon <|-- Electric
Pokemon <|-- Ice
Pokemon <|-- Fighting
Pokemon <|-- Poison
Pokemon <|-- Ground
Pokemon <|-- Flying
Pokemon <|-- Psychic
Pokemon <|-- Bug
Pokemon <|-- Rock
Pokemon <|-- Ghost
Pokemon <|-- Dragon
Pokemon <|-- Dark
Pokemon <|-- Steel
Pokemon <|-- Fairy
Pokemon *-- Stats


```

## Running 

Crear un entorno virtual e instalar las dependencias.

### Linux

Crear un `venv` 
```sh
python -m venv v_pokemon 
source v_pokemon/bin/activate
pip install -r requirements.txt
```

### Windows

Crear un `venv` 
```sh
## Use cmd/powershell
python -m venv v_pokemon
v_pokemon\Scripts\activate
pip install -r requirements.txt
```

**Note:** Si se obtiene un error de permisos en powershell, ejecutar como administrador y correr el siguiente comando:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```


## Testing

Requiere `pytest`

En el directorio raíz ejecutar

```sh
pytest tests/test_types.py -v
```

<img src="resources/tests-results.png" alt="testing" width=800 height=auto>


