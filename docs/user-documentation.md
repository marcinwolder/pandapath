# Dokumentacja funkcjonalna

## Czym jest CAPRI

CAPRI to aplikacja pozwalająca użytkownikom na generowanie planu wycieczki w wybranym mieście. CAPRI bierze pod uwagę godziny otwarcia miejsc, pogodę, preferencje finansowe oraz datę wycieczki. CAPRI dobiera atrakcje na podstawie preferencji użytkownika, które może on podać na wiele sposobów np. przez rozmowę z chatbot'em, przez quiz lub przez napisane notatki o sobie.

## Jak działa CAPRI

CAPRI zbiera preferencje użytkownika (np. przez rozmowę z chatbotem, quiz lub notatki), a następnie pobiera listę atrakcji i informacji kontekstowych (m.in. godziny otwarcia i daty wycieczki). Na tej podstawie system wylicza dopasowanie miejsc do profilu użytkownika, dzieli atrakcje na dni, optymalizuje kolejność zwiedzania oraz czasy przejazdów, a na końcu generuje podsumowanie planu przez usługę Llama. Wynikiem jest harmonogram dni z listą miejsc, informacjami o transporcie oraz danymi pogodowymi dla wybranego zakresu dat.

### Algorytm domyślny

Algorytm domyślny opiera się na wieloetapowym procesie planowania. Najpierw dla każdej atrakcji liczona jest łączna ocena dopasowania do preferencji użytkownika, a miejsca z niedodatnią oceną są odrzucane. Następnie pozostałe atrakcje są dzielone na dni przy użyciu constrained k‑means, gdzie cechami są lokalizacja i ocena, a ograniczenia wynikają z dostępności miejsc w konkretnych dniach (godziny otwarcia).

Dla każdego dnia algorytm rozwiązuje problem VRP z oknami czasowymi (OR‑Tools). Koszt przejazdu uwzględnia czas dojazdu i czas zwiedzania, a pominięcie miejsc jest karane proporcjonalnie do ich ocen (z bardzo wysoką karą dla miejsc oznaczonych jako „must see”). Wykorzystywana jest strategia startowa PATH_MOST_CONSTRAINED_ARC.

Czasy przejazdów wyliczane są na podstawie odległości: dla Polski, gdy dostępne, wykorzystywane są dane z OSRM; w innych przypadkach modele regresyjne. Dobierany jest tryb pieszy lub samochodowy zależnie od dystansu. Na końcu generowane jest tekstowe podsumowanie planu przez usługę Llama.

### Algorytm WiBIT

Algorytm WiBIT stosuje heurystykę opartą o punktowe oceny POI (points of interest). Miejsca są mapowane na POI wraz z kategoriami/podkategoriami i szacowanym czasem wizyty. Preferencje użytkownika przekładają się na wagi kategorii, które z czasem ulegają wygaszaniu (decay), a dodatkowe ograniczenie bliskości wzmacnia różnorodność, aby unikać zbyt podobnych lub sąsiadujących atrakcji.

Dla każdego dnia (domyślne okno 9:00–17:00) wybierane są najlepsze POI mieszczące się w czasie zwiedzania. Kolejność odwiedzin wyznaczana jest przez graf odległości, zbudowanie MST, a następnie usprawnienia 2‑opt oraz korektę punktu startowego trasy. Czasy przejazdów są szacowane na podstawie przybliżenia haversine, z rozróżnieniem na marsz i przejazd samochodem, a godziny są zaokrąglane do 5 minut.
