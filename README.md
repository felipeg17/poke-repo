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
	    - __name: str
	    - __pokedex_num: int
	    - __type: str
	    - __color: str
	    - __sex: str
	    - __level: int
	    -__stats : Stats
	    - _weaknesses: list
	    - _resistances: list
	    - _immunities: list
	    + attack()
	    + level_up(hp, attack, defense, spattack, spdefense, speed)
	    + __str__()
	    + receive_attack(attack_type)
	    +stats()
    }
    class Stats {
	    -HP: int
	    -Attack: int
	    -Defense: int
	    -Sp. Atk: int
	    -Sp. Def: int
	    -Speed: int
	    -base_hp: int
	    -base_attack: int
	    -base_defense: int
	    -base_spatk: int
	    -base_spdef: int
	    -base_speed: int
	    +combatstats(evasion, accuracy)
	    +str()
    }

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

### Linux

Create a `venv` 
```sh
python -m venv v_pokemon 
source v_pokemon/bin/activate
pip install -r requirements.txt
```

### Windows



## Testing

En el directorio raíz ejecutar

```sh
python -m test.test_types
```



