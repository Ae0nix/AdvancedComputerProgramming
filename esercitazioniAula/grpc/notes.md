return al posto di yield genera due errori, lato client si aspetta di iterare su un qualcosa che non è iterabile.

Lato server genera uno stream ma non tramite generator (tipo)