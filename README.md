# sdoclib

> sequential document library for building python workflow ide



## environment

python : 3.6.12



## what is purpose ?

...



## how to use ?

...

##### Document Translator

​	document translator class translates sequential document with context handler & instance handler. also, provides built in functions on global context based on variable "built_in_functions".

<b>sequential document format</b>

| key                      | description                      |
| ------------------------ | -------------------------------- |
| id (str)                 | unique instance id               |
| display (str)            | instance display name            |
| expression (str)         | python expression                |
| is_global_context (bool) | execution flag on global context |
| next_id (str)            | next unique instance id          |
| contains (list)          | instances that are contained     |

<b>built in functions</b>

| function name                         | description                                                  |
| ------------------------------------- | ------------------------------------------------------------ |
| _copy_this_context                    | copy current context deeply to other context                 |
| _copy_variable_from_context           | copy variable deeply from other context to current context   |
| _refer_this_context                   | reference current context to other context                   |
| _refer_variable_from_context          | reference variable from other context to current context (mutable object) |
| _globalize_variable_from_this_context | set variable from current context in global context          |
| _raise_exception                      | raise exception with sequential document format              |



##### Instance Handler

​	instance handler class resolves sequential document as instance, handles execution flow sequentially, and also provides essential keys to translate instance



##### Context Handler

​	context handler class handles contexts safely when executing expression, and local context key is based on instance's id (so each instance would be guaranteed independence). but global context key is limited to variable "__global_key". remember! cannot access main context from each sub context (global & locals).

main context : document translation runtime

​	- global context : global context made by context handler from main context

​	- local context 01 : an independent local context made by context handler from main context

  

## example code

##### example executor process

```python
from translator import DocumentTranslator 
from handler import ContextHandler
from handler import InstanceHandler

if __name__ == '__main__':
    with open('example_document.json', mode='r', encoding='utf8') as file:
        serialized_document = file.read()
        translator = DocumentTranslator(ContextHandler, InstanceHandler)
        translator.translate(serialized_document)
```

##### example sequential document

```javascript
{
    "id": "__trigger__",
    "display": "global",
    "expression": "a=1",
    "is_global_context": true,
    "next_id": "",
    "contains": [
        {
            "id": "A",
            "display": "01. sequence",
            "expression": "_refer_this_context('B'); print(a); c=1; cc=2",
            "is_global_context": false,
            "next_id": "B",
            "contains": []
        },
        {
            "id": "B",
            "display": "02. sequence",
            "expression": "print(c); _refer_variable_from_context('A', 'c'); print(cc)",
            "is_global_context": false,
            "next_id": "",
            "contains": []
        }
    ]
}
```

​	the executor process receives the sequential document that is built from your front application. then according to a predefined translate rule, document translator instance would translate (execute) document. 



## next update

1. add decision tree format (if/elif/else) 

