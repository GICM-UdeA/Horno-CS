# Contribuir al proyecto

:+1: Primero que todo, gracias por leer está guía para realizar tus contribuciones! :+1: 

A continuación, se dejan unas pautas generales para realizar sus contribuciones:

#### Tabla de contenidos
1. [¿Encontró algún Bug o tienes alguna pregunta? ](#Bug?)
2. [Lineamiento para resolver un issue](#issue)
3. [Finalizar sus contribuciones](#after)

### <a name="Bug?"></a> ¿Encontró algún Bug o tienes alguna pregunta? 
Abra un `issue` qué describa el problema lo mejor posible y asigne una de las posibles etiquetas https://github.com/GICM-UdeA/Horno-CS/labels/bug, https://github.com/GICM-UdeA/Horno-CS/labels/enhancement, https://github.com/GICM-UdeA/Horno-CS/labels/documentation, https://github.com/GICM-UdeA/Horno-CS/labels/invalid, o https://github.com/GICM-UdeA/Horno-CS/labels/question. Se tratará de dar solución lo antes posible. Incluso, si lo considera pertinente, puede publicar su propia solución al problema mediante un Merge Request. 

### <a name="issue"></a> Lineamiento para resolver un issue
Con base al `issue` relacionado cree una nueva rama, anteponiendo al nombre de la rama la etiqueta correspondiente el tipo de cambio que desea implementar ((feature|bugfix|cleanup)/[branch-name]). No es necesario hacer Fork al repositorio, solo tenga presente:
* No publicar los cambios directamente en la rama principal.
* Comentar apropiadamente sus implementaciones.
* Si sus cambios afectan directamente las aplicaciones existentes, actualice o añada la documentación relevante.
* Publique los commits con mensajes descriptivos, puede consultar [acá](https://cbea.ms/git-commit/) las convenciones generales del tema.
* Si es su primer commit, añada su nombre a la lista [CONTRIBUTORS][contributors].

Eso es todo, ¡Gracias por su contribución!

### <a name="after"></a> Finalizar sus contribuciones
Después de que su pull request sea aceptado y mezclado con la rama principal, su rama sera automáticamente eliminada por el repositorio central.

* Cambie a la rama principal:
```bash
git checkout master -f
```
* Borre la rama localmente:
```bash
git branch -D my-fix-branch
```
* Actualice su rama principal con los últimos cambios del upstream
```bash
git pull --ff origin master
```

[contributors]: CONTRIBUTORS