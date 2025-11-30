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
    - _moveset: Moveset
    - _weaknesses: list
    - _resistances: list
    - _immunities: list
    - _status: str
    + attack()
    + level_up()
    + receive_attack(attack_type)
    + show_moves()
    + get_stats()
    + get_moveset()
    + set_type()
    + apply_status()
}

class Stats {
    - base_hp: int
    - base_attack: int
    - base_defense: int
    - base_sp_attack: int
    - base_sp_defense: int
    - base_speed: int
    + __str__()
}

class Moveset {
    - pokedex_num: int
    - level: int
    - available_moves: list
    - current_moves: list
    + _load_available_moves()
    + _select_current_moves()
    + show_moves()
    + get_moves_names()
}

class Move {
    - id: int
    - name: str
    - type: str
    - power: int
    - accuracy: int
    - pp: int
    - category: str
    + __str__()
}

class Field {
    - trainer1: Trainer
    - trainer2: Trainer
    - __team1: list
    - __team2: list
    - __active1: Pokemon
    - __active2: Pokemon
    - __combat_hp: dict
    - __combat_attack: dict
    - __combat_defense: dict
    - __combat_sp_attack: dict
    - __combat_sp_defense: dict
    - __combat_speed: dict
    - __number_turn: int
    - active1_moves: list
    - active2_moves: list
    + get_team1()
    + get_team2()
    + get_active1()
    + get_active2()
    + set_active1()
    + set_active2()
    + get_number_turn()
    + mod_combat_hp()
    + get_combat_attack()
    + get_combat_defense()
    + get_combat_sp_attack()
    + get_combat_sp_defense()
    + get_combat_speed()
    + set_combat_attack()
    + set_combat_defense()
    + set_combat_sp_attack()
    + set_combat_sp_defense()
    + set_combat_speed()
    + mod_combat_attack()
    + mod_combat_defense()
    + mod_combat_sp_attack()
    + mod_combat_sp_defense()
    + mod_combat_speed()
    + end_battle()
    + winner_game()
    + pokemon_available()
    + switch_defeat()
    + switch_pokemon()
    + remove_defeated_pokemon()
    + health_bar()
    + Move_Effect()
    + status_damage()
    + get_combat_hp()
    + set_combat_hp()
    + reduce_hp()
    + execute_attack()
    + resolve_turn()
}

class Battle {
    - field : Field
    + display_battle_header()
    + display_turn_header()
    + display_battle_status()
    + action_py()
    + choice_attack()
    + choice_switch()
    + choice_surrender()
    + switch_after_defeat()
    + display_messages()
    + battle()
}

class CombatEngine {
    - attacker: Pokemon
    - defender: Pokemon
    - move : Move
    - attacker_moves: list
    - defender_moves: list
    + calculate_damage()
    + critical_hit()
    + attack_defense()
    + Hit_Accuracy()
    + status_changes()
}

class Trainer {
    - name: str
    - pokemon : list
    + pokemon_available()
    + create_pokemon()
    + choose_pokemon()
    + print_dex()
}

class Normal {}
class Fire {}
class Water {}
class Grass {}
class Electric {}
class Ice {}
class Fighting {}
class Poison {}
class Ground {}
class Flying {}
class Psychic {}
class Bug {}
class Rock {}
class Ghost {}
class Dragon {}
class Dark {}
class Steel {}
class Fairy {}

Pokemon *-- Stats
Pokemon *-- Moveset
Moveset *-- Move

Battle *-- Field
Field *-- Trainer
Trainer *-- Pokemon
Field --> CombatEngine: usa
CombatEngine *-- Pokemon
CombatEngine *-- Move

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


