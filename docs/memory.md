# Memory

Essendo un linguaggio tipizzato dinamicamente, ogni variabile e' tracciata anche a runtime e liberata alla fine dello scope in cui e' stata creata. Quando viene creata con `assign_*`, viene registrata in uno stack globale nella stdlib che viene parzialmente svuotato ad ogni richiamo di `collect`. Per registrare l'inizio di un nuovo scope viene utilizzata la funzione `activate`.

Alla fine di una funzione, per restituirne il valore, viene chiamata la funzione `return_and_collect`, che crea una copia della variabile e la assegna allo scope della funzione chiamante.

## Variabili Globali

Le variabili globali vengono allocate la prima volta in cui sono riferite usando `alloc_global`, che restituisce un `tiny_hi_object*` e che viene salvato in una variabile globale definita dall'LLVM IR. A quel punto sono accessibili in qualsiasi funzione. Vengono liberate dal metodo `collect_globals` chiamato alla fine del metodo di ingresso.

## Motivazioni

Gli assegnamenti sono tutti per valore, di conseguenza, avendo una variabile `K`, `F <- K` non puo' sfruttare il SSA (Single Static Assignment), in quanto successive modifiche ad `F` si rispecchierebbero anche su `K`. Viene quindi usato il metodo `copy` che crea una copia di `K` nel caso `F` esista gia', oppure `assign_object` nel caso `F` non esista, e verra' registrata in quel momento.

Non essendoci il concetto di riferimento ed essendo immutabili i parametri, l'eliminazione delle variabili non utilizzate avviene alla fine dello scope in cui vengono create, in modo da non occupare piu' memoria del necessario senza aver bisongno di un garbage collector.

## Possibili Implementazioni Alternative

Con il supporto all'assegnamento per reference (come ad esempio in Python e Julia) si sarebbe potuto sfruttare al massimo il SSA e i nodi Phi.
