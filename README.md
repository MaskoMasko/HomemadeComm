# HomemadeComm

## Superuser credentials

massimo_persic
1234

## Prakticni zadatak 1

Admin korisnik: **massimo_persic**

Admin lozinka: **1234**

Obican Korisnik: **MassimoTest**

Obiacn Korisnik lozinka: **te$t1234**

Admin se moze ulogirat na `BASE_URL/accounts/login` ili `BASE_URL/admin`

Admin korisnik moze vidjeti `BASE_URL/admin-only` rutu dok obican korisnik dobije upozorenje da nije autoriziran za pregled te rute

Registracija korisnika se desava na ruti: `BASE_URL/register`
Admin takodjer moze kreirati i brisati korisnika u admin panelu kada se ulogira na `BASE_URL/admin` ruti.

## Prakticni zadatak 2

Za drugi dio zadatka dodao sam endpointe `/products` i `/products/:id`. Na /products vidimo listu kreiranih proizvoda, kategorije, itd., te ih mozemo sortirati prema cijeni i kategoriji. Klikom na ime proizvoda dolazimo na stranicu sa detaljima proizvoda, u kojim narudzbama se nalazio taj proizvod te u kojim kosaricama se nalazi.

## Prakticni zadatak 3

Dodani su button za editiranje i brisanje zasebnih proizvoda i narudzbi

Takodjer je na `/products` i `/orders` dodan link za kreaciju proizvoda i narudzbi. Napravljena je logika za kreaciju, editiranje i brisanje "kosarice", ali je trenutno nepotrebna unutar aplikacije tako da je nema u korisnickom sucelju
