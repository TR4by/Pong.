# Pong.

Prosta wersja gry Pong (tutaj nazwana "Pong." gdzie "." to piłeczka) stworzona w języku Python przy użyciu biblioteki Pygame w ramach projektu na studia.

## Funkcje

- Gra w Pong gdzie kąt odbicia piłki zależy od miejsca, w które uderzyła na paletce.
- Licznik punktów, gra toczy się do tylu punktów ile wskaże się w `src/config.py`.
- Obsługa trybu pełnoekranowego.

## Sterowanie

### Lewa paletka

- `W` - Góra
- `S` - Dół

### Prawa paletka

- `↑` - Góra
- `↓` - Dół

### Inne

- `ENTER` - Start gry / Restart
- `F` - Fullscreen
- `ESC` - Wyjście z gry

## Uruchamianie gry

1. Upewnij się, że masz zainstalowany Python 3.x.
2. Stwórz wirtualne środowisko:

```bash
python -m venv .venv
```

3. Aktywuj wirtualne środowisko (powershell):

```bash
.venv\Scripts\Activate.ps1
```

4. Zainstaluj wymagane biblioteki:

```bash
pip install -r requirements.txt
```

5. Uruchom skrypt:

```bash
python pong.py
```
