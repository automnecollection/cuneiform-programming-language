# Planning 
Var type declaration
Meaning declaration

**AK**
```c
# variable_meaning_declarations.ak 
alū nisaam have                         // Cities have populations (plural generalisation)
nisuum su number                        // Populations are a number
summa aliim nisuum 25000 gr_than:       // If (a) city's population greater than 25000
    aliim nisuum su large               // The city's population is large
    aliim nisuum su large               // The city is large

# game_code.ak 
akade su alum                           // Akkad is (a) city
akadim nisuum su 30000             
    # Output: akadim nisuum su large

# pseudocode results from variable_meaning_declarations.ak:

# pseudocode results from game_code.ak:
# normal vars dict
akade [
    variables [
        alum [
            nisuum [
                numbers {
                    30000,
                }
                variables [
                large   
            ]
        ]
        large
    ]
]
```

### ANNOTATED:
- Initialises an Alum (city) general var type and an additional general variable type Nisuum (population) that is a struct child of the city type.
- Declares populations a number variable type
- Adds an if_declaration statement var. If a variable of the city type has a population greater than 25000: then the city object's population struct will have the "large" var type initialised.

### NOTES:
Normal var vs General type var.
 - General vars are like a class of var there can be multiple of. Like how there can be multiple cities.
 - Norm vars are singular vars that have the ability to inherit the features of a general type var, or just be its own thing. For example Akkad can be declared a city and inherit the population variable and others.
 - I need to come up with a better term for these terms.