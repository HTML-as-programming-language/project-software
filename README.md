# project-software

Deze repository bevat de centrale software en de bijbehorende centrale-clients.


## backend

Backend is de originele centrale. Deze kijkt naar de seriele poorten (/dev/ttyACM op Unix en COM op NT) en initieerd de verbinding met de modules.
Daarnaast exposed het een HTTP API waar clients mee kunnen verbinden.

Het protocol tussen de backend-API en de clients is hier gedocumenteerd: https://etherpad.net/p/timoenremidoendingen

## client

Dit is de Python client, die origneel onderdeel was van de centrale/backend.


## angular

Dit is de webclient geschreven in Angular.

## app

De app is de serverkant van de webapp. Deze verbind met de API van de centrale, en exposed dit als websocket waar de Angular webapplicatie gebruik van maakt.
