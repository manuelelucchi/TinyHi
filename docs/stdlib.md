## Stdlib

Scritta interamente in C e senza dipendenze, consiste in una libreria dinamica contenente una serie di metodi esposti. Quasi tutti i metodi hanno una signature simile a

```c
void nome(tiny_hi_object* output, tiny_hi_object* input1, tiny_hi_object* input2, /*Etc*/)
```

in quanto da LLVM passo gli indirizzi delle strutture allocate nello stack. Ogni oggetto e' formato da una parte di dati (una union che permette di discriminare tra `int`, `char*` e `{int, int*}`) e un byte per indicare il tipo (0 per `int`, 1 per `vector`, 2 per `string`, qualsiasi altro numero verra' interpretato come `null`).

Ogni assegnazione e' fatta per valore.

I principali metodi esposti sono

### Assignment

- assign\_{int|string|vector}

### Math

- sum/sub/mul/div

Queste operazioni sono valide sia tra scalari, che tra vettori della stessa dimensioni, che tra uno scalare e un vettore (broadcasting).

### Comparison

- lt
- leq
- mt
- meq
- eq
- neq

Le funzioni effettivamente implementate sono `mt` e `eq`, le altre sono varianti delle due precedenti.

Dati due oggetti `A` e `B`, `A>B` se e solo se `max(A) > max(B)`. Mentre `A=B` se e solo se ogni elemento di `A` e' uguale al corrispettivo di `B`. Queste due regole si applicano sia alle stringhe, che ai vettori che agli interi, trattati come un vettore lungo 1.

### Enumeration

- subscript

Il subscripting e' valido solo se gli indici sono tutti interi e vettori. Nel caso di un vettore, verranno considerati come degli interi separati dati in sequenza.

### I/O

- input

L'input salva semplicemente una stringa in una variabile

- output

L'output fa il print di un oggetto come stringa, cosi' com'e' se e' effettivamente una stringa, oppure con uno spazio tra un elemento e l'altro se e' un vettore.

### Memory Management

- activate
- collect
- copy
- return_and_collect
- alloc

Spiegato nella sezione Memory Management

### Global Variables Management

- alloc_global
- collect_globals

Spiegato nella sezione Memory Management

## Motivazioni

E' stato scelto il C per il suo ABI stabile e la semplicita' di interfacciamento con un ambiente a basso livello come LLVM. La compilazione crea una libreria dinamica i cui singoli vengono caricati durante l'esecuzione nella virtual machine LLVM. Il compilatore di default e' il Clang in quanto LLVM based a sua volta e multipiattaforma.

## Possibili implementazioni alternative

Un'alternativa sarebbe stata farlo in Rust, per avere una migliore qualita' di codice, un'organizzazione di file migliore e avere a dispoizione
librerie piu' performanti per le strutture dati.
