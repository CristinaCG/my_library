# My Library

Es una aplicación para lanzar una biblioteca local y poder manejar.

## Instalación

Describe los pasos para instalar tu proyecto. Por ejemplo, si tu proyecto es una aplicación Django, podrías incluir los siguientes pasos:

1. Clona el repositorio:
    ```
    git clone https://github.com/CristinaCG/tokio_project.git

    ```
2. Crea un entorno virtual e instala las dependencias:
    ```
    python -m venv env
    source env/bin/activate  # En Windows, usa `env\Scripts\activate`
    pip install -r requirements.txt
    ```
3. Realiza las migraciones de la base de datos:
    ```
    python manage.py migrate
    ```
4. Importa los datos
    ```
    python tools/delete_all.py
    python tools/create_users.py
    python manage.py loaddata media/data/languages.json
    python manage.py loaddata media/data/genres.json
    python manage.py loaddata media/data/authors.json
    python manage.py loaddata media/data/booksagas.json
    python manage.py loaddata media/data/author-*
    python tools/reading.py 
    ```

## Uso

Explica cómo usar tu proyecto. Por ejemplo:

```
python manage.py runserver
```
Luego, abre un navegador y ve a `http://localhost:8000`.

## Tests
```
python manage.py test
```

### Test con cobertura
```
coverage run --source='.' manage.py test
coverage report
coverage html
open htmlcov/index.html
```

## Datos de algunos usuarios
- User: admin, password: 1234
- User: teresa, password: teresa
- User: staff1, password: staff1