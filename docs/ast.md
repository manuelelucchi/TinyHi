# AST

La generazione dell'AST avviene tramite due dispatch table (una per i token, l'altra per le regole). In questa implementazione del linguagio l'AST viene ricostruito da zero basandosi sul parsing tree, in particolare si fa uso dell'interfaccia creata per semplificare la creazione dei nodi (in tinyhi.generation).

In questa fase avvengono i controlli sulla legalita' della chiamate a funzione (sulla base di scope, globalita') e si riconoscono alcune operazioni non esplicite nella grammatica (ad esempio la concatenazione)

L'AST viene poi attraversato ricorsivamente per generare l'LLVM IR.
Nell'LLVM IR non esiste il concetto di funzioni annidate, quindi ogni funzione viene messa sullo stesso livello, per poi essere ordinate e chiamati secondo la stessa logica con cui sarebbe legale che si possano chiamare tra di loro.

## Ottimizzazioni

Il compilatore ottimizza le seguenti situazioni:

- Operazioni binarie tra interi letterali (Es X <- 3 + 4 diventa in fase di generazione X <- 7)
- Operazioni unarie in interi e stringhe letterali (Es #"ABACO" diventa 5, #5 diventa 1)
- Concatenazione tra stringhe (Es X <- "A" "B" diventa X <- "AB")

## Motivazioni

La scelta della ricorsione rispetto all'iterazione con code threading deriva dalla necessita', a differenza di un interprete, di eseguire la generazione in ordine di dichiarazione, invece che di esecuzione, di conseguenza la capacita' di "saltare tra i nodi" risultava non necessaria.
