# Conventional Commits
Es una especificación ampliamente usada para describir commits. Es muy simple, solo se necesita tener clara la estructura de un commit.
```sh
<tipo>[alcance]:<descripción>
```
## tipo
puede ser uno de estos, con base en el contenido del commit.

|<tipo>|Usar para...|
|--|--|
|feat| agregar nuevas características|
|fix|correción de errores|
|build|cambios en el sistema de compilación|
|chore|cambios que no afectan al entorno de producción|
|ci|cambios en la configuración de _Continuos integration_|
|docs|cambios en la documentación|
|perf|mejoras en el rendimiento|
|refactor|procesos de refactoring|
|revert|reversiones a un commit anterior|
|style|cambios en la sintáxis|
|test|agregar o corregir test|
## alcance
provee contexto de cuál fue el ámbito de la aplicación que se modificó, ej:
```sh
refactor(api)!: blah blah
feat(lang)!: blah blah
```
## descripción
menciona el cambio introducido en una frase corta