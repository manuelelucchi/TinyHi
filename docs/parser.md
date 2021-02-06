# Parsing

Il parsing avviene utilizzando ANTLR4 mediato da Liblet. In caso di errore viene terminata l'esecuzione e mostrato un messaggio relativo. La grammatica tiene conto dei return e salta i whitespace e tab.

La concatenazione viene gestita come uno statement che si espande in 2 statement di seguito che, in fase di generazione dell'AST, diventano una lista riempita ricorsivamente.

E' supportato anche l'input di variabili, la terminazione dei blocchi di controllo usando `END` seguito dal nome del blocco

Es.
`WHILE X < 1 END WHILE` invece di `WHILE X < 1 END`
