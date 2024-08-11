# My Library

`My Library` es una aplicación web que permite organizar y gestionar una biblioteca personal. Permite la gestión de usuarios, gestión de la base de datos, grupos de usuarios, gestión de puntuación y reseñas, etc.

## Características principales
• Facilitar la organización de la lectura personal: Permitir a los usuarios registrar los libros en su librería personal, categorizarlos y gestionarlos de forma ordenada y accesible.
• Proveer una plataforma para la creación y compartición de reseñas: Fomentar la comunidad lectora mediante la posibilidad de escribir y compartir reseñas detalladas de los libros leídos, así como puntuaciones.
• Mejorar la experiencia de lectura: A partir de las reseñas escritas por otros usuarios, facilitar la búsqueda de la próxima lectura para cada usuario.
• Asegurar accesibilidad y usabilidad: Diseñar una interfaz que sea intuitiva y sencilla, evitando la sobrecarga de información en la pantalla.

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
## Características a añadir
1. Recomendaciones Personalizadas. Implementar un sistema de recomendación basado en las preferencias y el historial de lectura del usuario. Utilizar algoritmos de filtrado colaborativo o modelos de aprendizaje automático para sugerir libros que podrían interesar al usuario, basados en sus marcaciones y las de usuarios similares.
2. Integración con APIs de Información de Libros. Conectar con APIs externas como Open Library, Google Books o Goodreads para obtener información detallada sobre los libros, incluyendo sinopsis, reseñas, y portadas. Esto enriquecerá la experiencia del usuario al ofrecer datos más completos sobre los libros.
3. Lista de Lectura Compartida. Introducir una funcionalidad para que los usuarios puedan crear listas de lectura compartidas con amigos o miembros de la familia. Estas listas pueden ser colaborativas, permitiendo que varios usuarios agreguen y comenten libros.
4. Recordatorios y Notificaciones. Desarrollar un sistema de notificaciones para recordar a los usuarios cuándo han comenzado a leer un libro o cuándo deben continuar con la lectura. Esto puede ayudar a mantener el hábito de lectura y la organización de la biblioteca personal.
5. Retos de lectura o clubes de lectura. Desarrollar secciones donde los usuarios puedan participar en retos de lectura o clubes de lectura organizados por otros usuarios o por el staff. Los retos pueden incluir metas de lectura, temas específicos o eventos de discusión.
6. Optimización para Dispositivos Móviles. Desarrollar una versión optimizada para dispositivos móviles o una aplicación móvil complementaria para que los usuarios puedan gestionar su biblioteca desde sus teléfonos y tabletas con facilidad.
7. Soporte Multilingüe. Descripción: Agregar soporte para múltiples idiomas, permitiendo a los usuarios de diferentes regiones utilizar la aplicación en su idioma preferido y ampliar la accesibilidad del proyecto.
8. Ampliación de la plataforma a otro contenido de media.
