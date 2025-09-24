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

## Pull Request Description

**Summary:** 
se han agregado los 18 tipos de pokemon con la logica de la herencia. A la clase de Pokemon se le ha agregado un metodo para recibir daño, para hacerlo acorde al videojuego; en donde ciertos tipos son debiles o resistentes a ciertos tipos de ataques.

### Type of Change
- [ ] 🐛 Bug fix
- [x] ✨ New feature  
- [ ] 💥 Breaking change
- [ ] 📝 Documentation
- [ ] 🔧 Refactoring

### Changes Made
Se ha agregado 18 subclases que heredan de la clase Pokemon, además de agregar un metodo de recibir daño.

### Testing
- [x] Manual testing completed

### Checklist
- [x] Code self-reviewed
- [ ] Code commented where needed
- [x] No new warnings/errors
- [ ] Documentation updated
- [x] Ready for review

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
