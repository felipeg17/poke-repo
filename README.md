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
    + level_up(hp, attack, defense, spattack, spdefense, speed)
    + receive_attack(attack_type)
    + get_stats()
    + get_attribute(attr)
    + can_evolve(item=None, trade=False) bool
    + evolve(item=None, trade=False) bool
    + evolution_hint() str
    + __str__()
    - _get_row() DataRow
    - _resolve_evolution_target(item=None, trade=False) int|None
}

%% 👇 el truco es dejar una línea vacía antes del note 👇
note right of Pokemon
Evolución (desde CSV):
- evolves_once: int
- evolves_twice: int
- evolves_by_stone: int
- evolves_by_trade: int
- evolution_level: int | ""
end note

class Stats {
    - HP: int
    - Attack: int
    - Defense: int
    - Sp. Atk: int
    - Sp. Def: int
    - Speed: int
    - base_hp: int
    - base_attack: int
    - base_defense: int
    - base_spatk: int
    - base_spdef: int
    - base_speed: int
    + combat_stats(evasion, accuracy)
    + __str__()
}

class Normal
class Fire
class Water
class Gras


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


