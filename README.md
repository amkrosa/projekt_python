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

Wykorzystana biblioteka do rysowania okienek to DearPyGui (https://github.com/hoffstadt/DearPyGui).

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
### Klasa TableService ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/application/TableService.py#L11)
Służy jako interfejs do operacji na logice programu, a zatem wykonywanie operacji dodawania kolumn, dodawania wierszy.

## infrastructure
### Klasa Decoder ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/infrastructure/Decoder.py#L13)
Odczytuje plik .json korzystając z metody `object_hook` używanej przez klasę bazową `JSONDecoder`. Korzysta z dodatkowych
pól, by móc odróżnić różne typy od siebie.

### Klasa Encoder ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/infrastructure/Encoder.py#L11)
Zapisuje dane do pliku .json korzystając z metody `default` używanej przez klasę bazową `JSONEncoder`. Tworzy
wpisy pomocnicze celem późniejszego łatwiejszego odczytu.

## lib
### Klasa BaseObservable ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/lib/BaseObservable.py#L4)
Pozwala na łatwiejsze bindowanie danych między modelami, a widokami. Przetrzymuje słownik z funkcjami, które potem klasa
dziedzicząca może wykonać przy pomocy metody `_doCallbacks`.

### Klasa Observable ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/lib/Observable.py#L1)
Podobnie jak klasa `BaseObservable`, tylko bardziej jako wrapper na pojedyncze dane.

### Metaklasa SingletonMeta ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/lib/SingletonMeta.py#L1)
Metaklasa pozwalająca na łatwą implementację wzorca projektowego Singleton. Klasy dziedziczące mogą mieć tylko jedną
instancję.

## model

### Klasa Repository ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/Repository.py#L14)
Singleton przechowujący dane o tabelach. Posiada podstawowe metody do dodawania, usuwania oraz wyszukiwania tabel.
Dziedziczy również po `BaseObservable` celem łatwiejszego zbindowania modelu z UI.

### Klasa Row ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/Row.py#L1)
Model wiersza. Dane przechowywane w postaci słownika, metody pozwalają na dodanie wartości i pozyskanie słownika.

### Klasa Table ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/Table.py#L12)
Model tabeli. Metody umożliwiają dodawanie, usuwanie wierszy, dodawanie kolumn. Operacje dodawania, usuwania są walidowane
i w tej klasie są zdefiniowane walidatory dla tabeli. Dziedziczy również po `BaseObservable`.

## model/column

### Klasa Column ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/Column.py#L3)
Podstawowa klasa po której dziedziczą wszystkie inne klasy `...Column`. Posiada metodę do walidacji nazwy kolumny, udostępnia
`property` z nazwą. Posiada dwie niezaimplementowane metody `cast` i `type`, które powinny być przesłonięte
przez klasy dziedziczące.

### Klasa FloatColumn ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/FloatColumn.py#L8)
Klasa dziedzicząca po `Column`. `type` zwraca `float`, a `cast` rzutuje typ na `float`. W razie błędnego rzutowania jest
wyrzucany wyjątek ColumnTypeError.

### Klasa IntegerColumn ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/IntegerColumn.py#L8)
Klasa dziedzicząca po `Column`. `type` zwraca `int`, a `cast` rzutuje typ na `int`. W razie błędnego rzutowania jest
wyrzucany wyjątek ColumnTypeError.

### Klasa TextColumn ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/TextColumn.py#L8)
Klasa dziedzicząca po `Column`. `type` zwraca `str`, a `cast` rzutuje typ na `str`. W razie błędnego rzutowania jest
wyrzucany wyjątek ColumnTypeError.

### Klasa ColumnTypeError ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/ColumnTypeError.py#L1)
Własny wyjątek zwracany, kiedy występuje problem z wprowadzanym typem danych, a typem danych kolumny.

## ui/root
### Klasa RootView ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/root/RootView.py#L4)
Definiuje wysokość i szerokość okienka, tworzy `viewport` aplikacji. Posiada metody do wyśrodkowywania elementu.

### Klasa RootHandler ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/root/RootViewModel.py#L10)
Inicjalizuje `RootView` oraz wczytuje dane do `Repository` z pliku, jeżeli istnieją. Definiuje również handler
wywoływany w momencie zamknięcia aplikacji.

## ui/table

### Klasa TableView ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/table/TableView.py#L16)
Główna klasa typu `View`, która rysuje lub wywołuje klasy rysujące elementy w interfejsie. Zawiera większość logiki związanej z UI, oprócz funkcji `callback`, które są przekazywane z `TableHandler`.
### Klasa TableHandler ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/table/TableViewModel.py#L16)
Przechowuje wszystkie funkcje do obsługi wydarzeń w zakresie aplikacji. W tym miejscu są one również przekazywane do widoku `TableView` razem z jego
inicjalizacją.

## ui/widgets
W pakiecie znajdują się klasy tworzące podstawowe elementy. 
### Klasa AddTableModal ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/widgets/AddTableModal.py#L6)
Tworzy elementy w interfejsie graficznym odpowiadające za okienko `AddTable`. Udostępnia `property` `form`, które
zczytuje dane z elementów interfejsu.

### Klasa ConfirmationModal ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/widgets/ConfirmationModal.py#L6)
Tworzy elementy w interfejsie graficznym odpowiadające za `ConfirmationModal`, czyli potwierdzenie.

### ErrorPopup ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/widgets/ErrorPopup.py#L4)
Tworzy elementy w interfejsie graficznym odpowiadające za `ErrorPopup`, czyli popup błędu. Element jest tworzony obok wskazanego w konstruktorze
elementu.

### TablesTable ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/widgets/TablesTable.py#L4)
Tworzy elementy w interfejsie graficznym odpowiadające za `TablesTable`, czyli tabelę z obiektami `Table`.

### MainApplication
Główny punkt wejścia programu.
## Funkcja run ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/MainApplication.py#L7)
Wywołuje podstawowe funkcje biblioteki dearpygui.
## Funkcja exit ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/MainApplication.py#L16)
Niszczy kontekst elementów biblioteki dearpygui.

# Testy ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/tests/tests.py#L8)

Po każdym teście jest czyszczony singleton `Repository` w metodzie `tearDown`.

### test_shouldAddValidTableAndColumn
Sprawdza dodawanie tabel wraz z kolumnami.

### test_shouldAddValidRow
Sprawdza dodawanie wierszy do istniejących już tabeli.

### test_shouldNotAddInvalidRowWhenTypeIsIncorrect
Sprawdza negatywny przypadek dodawania wierszy do istniejących już tabeli.

### test_shouldNotAddTableWithEmptyName
Sprawdza negatywny przypadek dodawania nowych tabeli z niepoprawną nazwą.

### test_shouldNotAddColumnWithEmptyField
Sprawdza negatywny przypadek dodawania tabeli z niepoprawnymi kolumnami.

### test_shouldQueryRows
Sprawdza czy filtrowanie poprzez przekazanie funkcji `lambda` działa.

# Konstrukcje

## Wyrażenia lambda
### Pobranie wartości jako callback ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/table/TableView.py#L102)
### Pobranie nazwy aktualnie wybranej tabeli ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/table/TableView.py#L213) 
### Test funkcjonalności filtrowania ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/tests/tests.py#L133) 

## List & dict comprehension
Oba sposoby są używane dość powszechnie w projekcie, poniżej 3 przykłady:
### Rzutowanie wartości w słowniku ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/Table.py#L56)
### Czytanie wartości z elementów UI ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/ui/widgets/AddTableModal.py#L36)
### Filtrowanie wartości na podstawie przekazanej funkcji ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/application/TableService.py#L54)

## Klasy
Projekt został wykonany w większości w paradygmacie OOP. W projekcie znajduje się kilka klas po których dziedziczą inne klasy, z czego jedna to metaklasa. 
Występuje również podział na klasy od logiki i interfejsu. Przykłady poniżej:

### Klasa bazowa Column ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/Column.py#L3)
### Klasa dziedzicząca FloatColumn ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/FloatColumn.py#L8)
### Klasa dziedzicząca IntegerColumn ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/IntegerColumn.py#L8)
### Klasa dziedzicząca TextColumn ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/TextColumn.py#L8)


## Wyjątki
Jest zdefiniowana jedna własna klasa wyjątku. Przy walidacji danych powszechne w projekcie jest łapanie i rzucanie wyjątków.

### Klasa wyjątku ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/ColumnTypeError.py#L1)

### Łapanie wyjątku ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/Table.py#L106)

## Moduły
Za wyjątkiem `MainApplication.py` wszystkie pliki zawierają po jednej klasie i projekt jest uporządkowany według pakietów.

## Metaklasy 
### Singleton ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/lib/SingletonMeta.py#L1)

## Dekoratory
Dekoratory są używane w wielu miejscach ze względu na użycie dekoratora `@property`.

### Rozszerzenie `@property` przez ustawienie settera ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/Repository.py#L31)
### `@abc.abstractmethod` ➔ [link](https://github.com/amkrosa/projekt_python/blob/51d311cb66aac94587584a40a8f0bdb4b67cd2ff/model/column/Column.py#L14)