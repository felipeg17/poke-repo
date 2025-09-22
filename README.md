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

## Descripción de la solución

Este proyecto implementa un modelo básico de Pokémon y sus tipos utilizando composición en lugar de herencia.
La corrección se hace porque en un inicio los tipos (Fire, Grass, etc.) se modelaban como clases hijas de Pokemon, lo cual no es correcto en el diseño orientado a objetos.

Un Pokémon no es un Tipo, sino que tiene uno o más Tipos.
Por eso, ahora cada objeto Pokemon contiene una lista de objetos Type, donde cada Type define sus debilidades, resistencias e inmunidades.

-Cambios realizados
Se eliminó la herencia entre Pokemon y Type.
Se creó la clase Type, que encapsula la información de: Debilidades, resistencias, inmunidades
La clase Pokemon ahora recibe una lista de tipos (composición).
Métodos en Pokemon permiten consultar sus debilidades, resistencias e inmunidades a partir de sus tipos.
Se agregó un diagrama UML actualizado para reflejar la relación de composición.

```text

classDiagram
    class Type {
        +String name
        +List weaknesses
        +List resistances
        +List immunities
    }

    class Pokemon {
        +String name
        +int pokedex_num
        +List types
        +String color
        +String sex
        +int level
        +attack()
        +level_up()
        +show_info()
        +get_weaknesses()
        +get_resistances()
        +get_immunities()
    }

    %% Tipos de Pokémon (subclases conceptuales de Type)
    Type <|-- Normal
    Type <|-- Fire
    Type <|-- Water
    Type <|-- Grass
    Type <|-- Electric
    Type <|-- Ice
    Type <|-- Fighting
    Type <|-- Poison
    Type <|-- Ground
    Type <|-- Flying
    Type <|-- Psychic
    Type <|-- Bug
    Type <|-- Rock
    Type <|-- Ghost
    Type <|-- Dragon
    Type <|-- Dark
    Type <|-- Steel
    Type <|-- Fairy

    %% Relación de composición: un Pokémon tiene uno o varios tipos
    Pokemon --> Type : types



