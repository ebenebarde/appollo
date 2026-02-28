# 🚀 Projekt-Abgabe: Appollo (Web-Technologies)

Dieses Projekt wurde für die lokale Entwicklung mit **Docker** und **PostgreSQL** optimiert. Für eine einfache Korrektur wurde das Projekt jedoch so vorkonfiguriert, dass es direkt mit der mitgelieferten **SQLite3-Datenbank** gestartet werden kann.

## Voraussetzungen

* **Python 3.10+** (installiert auf dem System)
* **pip** (Python Package Installer)

## Schnellstart-Anleitung (für die Korrektur)

Um den Server ohne Datenbank-Setup zu starten, folgen Sie bitte diesen Schritten:

### 1. Repository vorbereiten
Navigieren Sie im Terminal in den `backend`-Ordner des Projekts:
```bash
cd backend
```

### 2. Virtuelle Umgebung erstellen (Empfohlen)
```bash
python -m venv venv
# Aktivieren unter Windows:
venv\Scripts\activate
# Aktivieren unter macOS/Linux:
source venv/bin/activate
```

### 3. Abhängigkeiten installieren
Die `requirements.txt` ist so vorbereitet, dass alle notwendigen Pakete für den SQLite-Betrieb installiert werden:
```bash
pip install -r requirements.txt
```

### 4. Datenbank platzieren
Kopieren Sie die mitgelieferte Datei `db.sqlite3` direkt in den Ordner `backend/`. 
*(Hinweis: Der Pfad muss `backend/db.sqlite3` lauten, damit die Konfiguration greift.)*

### 5. Server starten
```bash
python manage.py runserver
```
Die Anwendung ist nun unter [http://127.0.0.1:8000](http://127.0.0.1:8000) erreichbar.

---

## Zugangsdaten für die Korrektur

Für das Django-Admin-Interface und passwortgeschützte API-Bereiche wurde bereits ein Superuser in der Datenbank hinterlegt:

* **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* **Benutzername:** `user1`
* **Passwort:** `pass1`

---

## Technische Details
* **Datenbank-Switch:** Das Projekt nutzt `django-environ`. Falls keine `DATABASE_URL` (für Postgres) in der Umgebung gesetzt ist, wechselt das System automatisch auf den SQLite-Fallback (`backend/db.sqlite3`).
* **API-Dokumentation:** Eine Übersicht der Endpunkte finden Sie (bei laufendem Server) unter `/api/docs/` (Swagger UI).
