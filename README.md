# pamiw-projekt

## Co udało się zrobić
- Hosting API - strona i API są udostępniane na chmurze AZURE pod adresem [http://172.160.248.2](http://172.160.248.2)
- Kompatybilność aplikacji mobilnej (plik .apk znajduje się w repozytorium)
- Interfejs
  - Jednolite kolory, czcionki i przyciski
  - Wysokiej jakości ikony (css.gg)
  - Odpowiedź interfejsu (długie operacje są sygnalizowane ikoną ładowania)
  - Wykorzystanie gotowych szablonów (minstyle.io)
  - Walidacja danych (komunikaty w obu językach zwracane przez API <<widać na screenshotach niżej>>)
- Ustawienia użytkownika
  - Wielojęzyczność: angielski i polski
  - tryby ciemny i jasny
- Warstwa wspólnych serwisów

## Czego się nie udało zrobić
- Dostęp do zasobów sprzętowych
- Opcje logowania i rejestracji przez google, facebook, etc.

## Zakładanie konta
Aby założyć konto, należy kliknąć na przycisk "register". Następnie należy wpisać email i hasło oraz jego powtórzenie.
![register_page](https://github.com/ThinCan/pamiw-projekt/assets/20555497/cd0bbf65-f10f-4d45-be3c-4ea97763fc8c)

### Przykładowe komunikaty, informujące użytkownika o błędnie wypełnionym formularzu:
### *Jeśli użytkownik wpisał już zajęty email*
![bad_register](https://github.com/ThinCan/pamiw-projekt/assets/20555497/6809a39f-fc48-49b1-97ca-622272b3454c)
### *Jeśli hasła nie są identyczne*
![bad_password_register](https://github.com/ThinCan/pamiw-projekt/assets/20555497/3eba42ea-7d11-440f-87c2-ba9c44b19c4f)

## Logowanie się
Po utworzeniu konta, zostaniemy ponownie przeniesieni na stronę logowania, gdzie trzeba podać poprawne dane.
![login_page](https://github.com/ThinCan/pamiw-projekt/assets/20555497/d6628f4e-8c53-41cd-bfb0-bbb13e1977e9)

## Notatki
Po zalogowaniu się, otrzymujemy dostęp do naszych notatek, utworzonych z zalogowanego konta.
Póki co lista jest pusta. Na górze widzimy dwie opcje: lista notatek i dodawanie notatek.\
![notes_page](https://github.com/ThinCan/pamiw-projekt/assets/20555497/df075ea6-af30-4145-a5ca-835f1abf0a08)

## Dodawanie notatki
Aby dodać notatkę, należy wybrać prawą opcje na gorze "Add notes". Pojawi się formularz, w którym możemy wpisać tytuł notatki i jej treść.\
![addnote_page](https://github.com/ThinCan/pamiw-projekt/assets/20555497/22a554bf-c0ea-4431-97b9-1de6419249f8)

## Zmiana stylu kolorów i języka
Na dole strony są dwa guziki: jeden zmienia język, drugi zmienia styl kolorów\
![theme_language_change](https://github.com/ThinCan/pamiw-projekt/assets/20555497/8d5b0375-5865-444d-813c-2c20487be04d)

## Znak ładowania
Podczas dodawania, aktualizowania, udostępniania i ładowania strony z notatkami, widoczny jest kółko, które sygnalizuje, że trwa ładowanie.\
![adding_note_loading](https://github.com/ThinCan/pamiw-projekt/assets/20555497/b8e5ecb2-9e4d-4c23-acc2-6bc9f9b1e3d1)

## Wyświetlona notatka
![notes_page_node_added](https://github.com/ThinCan/pamiw-projekt/assets/20555497/97af50d9-9e8b-4765-919a-fa5a6f39c5da)
### Jeśli treść notatki jest wystarczająco długa, pojawi się dodatkowy guzik, który pozwala na pokazanie jej w całości; domyślnie treść jest przycięta do około 50 słów.
![note_collapse](https://github.com/ThinCan/pamiw-projekt/assets/20555497/6b12d21a-556c-42b7-a4d7-d2beb30a49e4)\
![note_expand](https://github.com/ThinCan/pamiw-projekt/assets/20555497/a5562a95-38be-4120-98b3-c112dd489c3a)

## Przeglądanie starszych notatek
Jeśli notatek jest więcej niż 10, wprowadzony jest mechanizm paginacji. Pozwala on na przewijanie stron notatek.\
![page_picker](https://github.com/ThinCan/pamiw-projekt/assets/20555497/8056d5e5-cca8-407c-b95f-2f1a90c77597)

### Strona druga
![page_2](https://github.com/ThinCan/pamiw-projekt/assets/20555497/09087182-1926-48b3-86fb-0a0443bf985a)

## Usuwanie notatek
Aby usunąć notatkę, należy nacisnąć przycisk z czerwonym tłem "Usuń". Następnie pojawi się prośba o potwierdzenie operacji lub jej anulowanie.
Podczas usuwania - po potwierdzeniu - widać kółko, które sygnalizuje przetwarzanie żądania.\
![delete](https://github.com/ThinCan/pamiw-projekt/assets/20555497/19b7de96-b067-4c4e-92d1-39bf9a3b38c7)

## Aktualizowanie notatek
Aby zaktualizować notatkę, należy nacisnąć przycisk z ciemno niebieskim tłem. Po wciśnieciu otworzy się formularz z wypełnionymi polami na tytuł i treść oryginalną treścią i pozwoli on na zmodyfikowanie tych pól.
Operacje możemy anulować albo potwierdzić.\
![update](https://github.com/ThinCan/pamiw-projekt/assets/20555497/bc000c23-1ce9-472f-aeec-528f5764eff8)

### Po zatwierdzeniu aktualizacji
Po zatwierdzeniu pojawi się kółko oznaczające przetwarzanie żądania, po czym strona załaduje notatki jeszcze raz, tym razem z nową treścią i tytułem.\
![update_spinner](https://github.com/ThinCan/pamiw-projekt/assets/20555497/4e426f30-6994-4f0b-8925-111e256ffeab)







