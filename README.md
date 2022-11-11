# Pdxparser.py
Every Pdx Modder desired to make a parser to parse pdx's strange language, so do I.

This python file desired to parse the paradox language into dict to automatically process.
Recommend to Use it in a Jupyter Notebook to process your paradox text file interactively.

## Parse
```Python
    TEST = "some_trigger = { AND = {a>b a<=c a!=d a = e a >= f a !=g} } "
    PP = PdxParser(TEST)
    pdx_dict = PP.parse() 
    # Output: {'some_trigger': {'AND': {'a': [['>', 'b'], ['<=', 'c'], ['!=', 'd'], 'e', ['>=', 'f'], ['!=', 'g']]}}}
```

## Write
Pdxparser.py delivers many low level apis to write, and a high level api to write, inspired by [Jomini.js](https://github.com/nickbabcock/jomini)
```Python
    pdxwriter = Pdxwriter()
    dump_test = pdxwriter.dump(pdx_dict,PP.ambigouous) ## in Dict is ok
    dump_PP_test = pdxwriter.dump(PP) ## in PP
    print(dump_test)
    """Output:
    some_trigger={
      AND={
        a<=c
        a!=d
        a=e
        a>=f
        a!=g
      }
    }
    """
```
