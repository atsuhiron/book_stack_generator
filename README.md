# book_stack_generator
Generates images of books placed on the bookshelf.

## Requirement
Python >= 3.12

## Configurable values
- height
- width
- base color
- edge size
- edge color
- obi height
- obi color
- shadow strength
- shadow size

## Available Random Distributions
- Uniform Distribution
- Bernoulli Distribution
- Normal Distribution (with and without cutoffs)
- Distributions represented by the product of the above distributions

## Generating Color
Based on the above random distributions, you can specify colors using RGB values.
Furthermore, by mapping the generated colors within the RGB space, you can achieve various effects.
The available mappings are as follows:
- Identity Mapping: Default mapping
- Desaturation Mapping: Mapping to move colors closer to gray
