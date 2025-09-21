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

Se agregó la lógica de los 18 tipos de Pokémon mediante herencia en el archivo `pokemon.py`.

- Se creó la clase base `PokemonType` que hereda de `Pokemon`.
- Se implementaron las resistencias, debilidades e inmunidades de cada tipo.
- Se añadieron 18 clases (una por tipo de Pokémon).
- Se agregó el método `receive_attack` para la efectividad de los ataques.



