# Klient bazy danych
## Projekt z Języków symbolicznych
### Anna Krasowska GL 31

---

# Temat projektu
Projektem jest aplikacja okienkowa do zarządzania danymi przedstawionymi w na wzór bazy danych, zatem istnieją:
* Tabele
* Kolumny
* Wiersze

Można również wykonywać operacje na powyższych obiektach, czyli:
* **Tabele** - dodawanie, usuwanie
* **Kolumny** - dodawanie
* **Wiersze** - dodawanie, usuwanie, filtrowanie (wyszukiwanie)

Stan bazy jest odczytywany z pliku oraz przy wyjściu zapisywany do pliku JSON.

# Funkcjonalność
#### Sekcja tabel:
* Przycisk Dodaj tabele, który wyświetla okienko pozwalające na dodanie tabeli wraz z kolumnami (lub bez)
* Tabela tabel z kolumnami Nazwa, Wiersze (ilość wierszy w tabeli) i Akcja (możliwa akcja, czyli Usuń)
* Naciśnięcie na nazwę powoduje podświetlenie pola i wybranie tabeli

#### Okienko dodania nowej tabeli
* Pola tekstowe z nazwą tabeli i kolumny do dodania
* Przycisk typu radio z typem dodawanej kolumny
* Tabela z aktualnie dodanymi kolumnami
* Możliwość powrotu przyciskiem Wróć, co nie powoduje żadnych zmian

#### Sekcja dodania kolumny:
Po wybraniu tabeli jest możliwość dodania kolejnej kolumny, wprowadzając nazwę i wybierając typ elementu typu radio

#### Sekcja wierszy:
* Nazwa tabeli
* Tabela z wierszami wybranej tabeli z kolumnami Wiersz (numer wiersza), [kolumny tabeli], Akcje (Usuń przy istniejących, dodaj przy wierszu wprowadzania nowego wiersza)
* Wiersz dodania nowego wiersza - jako placeholder/hint jest wyświetlany typ danej kolumny z możliwością szybkiego dodania nowego wiersza przyciskiem Dodaj
* Pole tekstowe do filtrowania wierszy, razem z przyciskiem Szukaj (inicjuje akcję filtrowania) i Reset (wraca do oryginalnego stanu). W polu tekstowym
jest możliwość wpisania poprawnego wyrażenia lambda, które zostanie wykonane na wierszach i wynik zostanie wyświetlony zamiast aktualnych danych
  
#### Odczyt i zapis do pliku .json
Na start programu jest wyszukiwany plik `db.json`, jeżeli jest znaleziony to dane z niego są wczytywane przez aplikację.
Po zakończeniu działania programu (zamknięcie okna) jest wykonywany zapis do pliku `db.json`.
  
---

# Pakiety
## application
### Klasa TableService
Służy jako interfejs do operacji na logice programu, a zatem wykonywanie operacji dodawania kolumn, dodawania wierszy.

## infrastructure
### Klasa Decoder
Odczytuje plik .json korzystając z metody `object_hook` używanej przez klasę bazową `JSONDecoder`. Korzysta z dodatkowych
pól, by móc odróżnić różne typy od siebie.

### Klasa Encoder
Zapisuje dane do pliku .json korzystając z metody `default` używanej przez klasę bazową `JSONEncoder`. Tworzy
wpisy pomocnicze celem późniejszego łatwiejszego odczytu.

## lib
### Klasa BaseObservable
Pozwala na łatwiejsze bindowanie danych między modelami, a widokami. Przetrzymuje słownik z funkcjami, które potem klasa
dziedzicząca może wykonać przy pomocy metody `_doCallbacks`.

### Klasa Observable
Podobnie jak klasa `BaseObservable`, tylko bardziej jako wrapper na pojedyncze dane.

### SingletonMeta
Metaklasa pozwalająca na łatwą implementację wzorca projektowego Singleton. Klasy dziedziczące mogą mieć tylko jedną
instancję.

## model

### Klasa Repository

### Klasa Row

### Klasa Table

## model/column

### Klasa FloatColumn

### Klasa IntegerColumn

### Klasa TextColumn

### Klasa ColumnTypeError
Własny wyjątek zwracany, kiedy występuje problem z wprowadzanym typem danych, a typem danych kolumny.

## ui/root

## ui/table

## ui/widgets
