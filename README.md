# Instalacja

W terminalu, będąc w głównym katalogu projektu:

## Stworzenie środowiska pythona

```cmd
python -m venv env
```

## Aktywacja stworzonego środowiska

```cmd
env\Scripts\activate.bat
```

## Instalacja wymaganych packages

```cmd
pip install -r requirements.txt
```

## Stworzenie bazydanych z migracji

```cmd
flask db upgrade
```

# Development

## Database migrations

### Przed pierwszym uruchomieniem

```cmd
flask db init
```

### Stworzenie migracji

```cmd
flask db migrate -m "opis"
```

### Aktualizacja bazy danych do ostatniej migracji

```cmd
flask db upgrade
```
