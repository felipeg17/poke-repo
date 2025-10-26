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
---
config:
  theme: dark
---
classDiagram
direction TB
    class Normal {
    }
    class Fire {
    }
    class Water {
    }
    class Grass {
    }
    class Electric {
    }
    class Ice {
    }
    class Fighting {
    }
    class Poison {
    }
    class Ground {
    }
    class Flying {
    }
    class Psychic {
    }
    class Bug {
    }
    class Rock {
    }
    class Ghost {
    }
    class Dragon {
    }
    class Dark {
    }
    class Steel {
    }
    class Fairy {
    }
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
        + attack()
        + level_up(hp, attack, defense, spattack, spdefense, speed)
        + receive_attack(attack_type)
        + get_stats()
        + show_moves()
        + __str__()
    }
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
    class Moveset {
        - pokedex_num: int
        - level: int
        - moves_path: str
        - pokemon_moves_path: str
        - available_moves: list[Move]
        - current_moves: list[Move]
        + _load_available_moves() list[Move]
        + _select_current_moves() list[Move]
        + get_moves_names() list[str]
        + show_moves()
    }
    class Move {
        - id: int
        - name: str
        - type: str
        - power: int
        - accuracy: int
        - pp: int
        + __str__()
    }
    Pokemon *-- Stats
    Pokemon *-- Moveset
    Moveset *-- Move
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


