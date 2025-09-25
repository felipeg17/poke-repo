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
    class Pokemon {
        - name: str
        - pokedex_num: int
        - type: str
        - color: str
        - sex: str
        - level: int
        - weaknesses: list
        - resistances: list
        - immunities: list
        + attack()
        + level_up()
        + __str__()
        + receive_attack(attack_type)
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
