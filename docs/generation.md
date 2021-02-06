# Generazione

Ogni nodo che compone l'AST eredita dalla classe `ASTNode`. In particolare, se un nodo ha dei figli, allora ereditera' da `ExpressionNode`. Ogni nodo genera dell'IR usando il `builder` della libreria `llvmlite`. Ogni nodo ha quindi un metodo `codegen(builder, ctx)` che passa ad ogni figlio il builder sopracitato e un contesto condiviso per tutto l'albero.

In questo contesto vi sono informazioni sulla funzione corrente che si sta generando, le variabili registrate (divise per scope), le funzioni registrate fino a quel momento (comprese quelle della stdlib).

Per facilitare lo sviluppo e' stata creata un'interfaccia funzionale completamente context unaware, che permette di creare sottoalberi dell'AST in modo semplice e piu' controllato, gestendo in automatico i riferimenti e trasformando i tipi di python (int, str, list) nei nodi corretti senza doversi porre il problema di quale tipo si stia passando.

## Motivazioni

Le scelte della generazione sono ispirate principalmente al linguaggio Julia. Innanzitutto per rispettare le specifiche iniziali, il linguaggio e' tipizzato solo dinamicamente. In molti casi non e' quindi possibile sapere in fase di compilazione il tipo di ogni variabile (che inoltre puo' cambiare durante l'esecuzione). Nel caso ad esempio di una variabile parametro `A` di cui quindi non si puo' conoscere il tipo a priori, una eventuale operazione `A + 1` non puo' essere gestita come in C/C++ con un'istruzione `add` di LLVM, ma richiede una funzione apposita. Julia, che compila ed esegue le funzioni una alla volta, identifica il tipo di un oggetto tramite la funzione `typeof` e ottiene il puntatore alla funzione corretta attraverso un hash che la identifica. Richiama quindi `julia_apply_generic` a cui passa il puntatore a funzione (`j_value_t*`) e un array di valori (`j_value_t**`) e ovviamente la sua lunghezza come intero. TinyHi ovviamente non ha bisogno di supportare potenzialmente infiniti tipi, quindi wrappa ogni literal (come gli interi e le strighe fisse) in un `tiny_hi_object` che supporta i 3 tipi possibili, per poi scegliere cosa fare chiamando le funzioni della standard lib come `sum` o `concat`. Nel caso `A + 1` detto prima, `A` sara' gia' un `tiny_hi_object` e 1 andra' wrappato usando `assign_int` che restituisce un `tiny_hi_object`, per poter applicare la funzione `sum`.

## Possibili implementazioni alternative

### Typeof

Si potrebbe creare una funzione `typeof` sfruttando la presenza di solo 3 tipi possibili per scegliere come muoversi in modo definito, ma porterebbe ad un IR ancora piu' complesso.

### Type Inferencing

Compilando ed eseguendo una funzione alla volta e controllando i risultati, sarebbe possibile ottenere una definizione statica dei tipi di ogni valore all'interno di una singola funzione.
