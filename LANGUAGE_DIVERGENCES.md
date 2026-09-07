# LANGUAGE

## LANGUAGE NOTES

### **Keywords and language equivalents**
#### Keyword Types
Variables:
- To determine a variable's function in a line, variables must be marked with grammatical cases.
- A Cuneiform sign phonetically ending with "um" must be used for variables intended as being used in a nominative context.
- Valid Cuneiform signs for the nominative case for example include: 𒌝 (um), 𒌈 (tum), 𒈝 (lum), etc.

Verbs:
- Most of the time determines what function is being called internally in Python.

#### Var Declaration
𒋗 (šu) - A copula that declares a variable's value. The copula can also be dropped when declaring with two nominative case named variables.

**AK**
```c
𒅅𒋢𒌝 𒋗 𒉿𒌝 (ek-su-um šu yu-um)

𒅅𒋢𒌝 𒉿𒌝 (ek-su-um yu-um)  # without the copula
```
**C**
```c
x = y;
```

#### Math
𒍣𒅁 (ṣi-ib) - A verb that adds values.

**AK**
```c
// x is 1 and y is 2.
// z is x and y added.
// Output: z is 3.

𒅅𒋢𒌝 𒋗 1 𒅇 𒉿𒌝 𒋗 2 (ek-su-um šu 1 u yu-um šu 2)
𒍣𒌝 𒋗 𒅅𒊓𒄠 𒅇 𒉿𒄠 𒍣𒅁 (zi-um šu ek-sa-am u ya-am ṣi-ib)
    # Output: 𒍣𒌝 𒋗 3 (zi-um šu 3)
```
**C**
```c
int x = 1, y = 2;
int z = x + y;
    // Output: z = 3
```

## DIVERGENCES FROM CONVERTING INTO A PROGRAMMING LANGUAGE

### **Forgivable**
 - Variable grammar case markers are completely regular.

### **Egregious**
 - Akkadian Cuneiform signs can represent multiple phonetic values. However, in this language phonetic values for all Cuneiform signs are completely regular and singular, having only one Latin transliteration.