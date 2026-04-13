# SUR-GEN
### Unified Gender Violence Incident Registry System
*Sistema Unificado de Registros en Violencia de Género*

> A web-based case management platform designed to prevent the
> re-victimization of gender violence victims by giving them and
> judicial operators unified, persistent access to case records.

---

## The problem

When gender violence victims seek help from authorities, they are
frequently required to recount their situation from scratch — each time,
to a different institution. This repeated retelling is a recognized form
of re-victimization. It happens because case information is fragmented
across institutions, inaccessible to victims, and not preserved in a
single unified record.

## What SUR-GEN does

SUR-GEN centralizes all documents, judicial proceedings, incidents, and
actions relevant to a gender violence case into a single persistent
profile. It provides two interfaces for two distinct user roles:

**Judicial operators (agents)** can:
- Register victims as system users
- Open and manage IPPs (preliminary investigation records)
- Record aggressors and their relationship to the victim
- Log judicial proceedings, concurrences, and attach documents
- Track case status (active / archived)
- Access a full audit trail of all changes — deletion is not permitted

**Victims** can:
- Log in and view their own IPPs and associated documents
- Download case documents
- Edit their contact information and emergency contacts
- View aggressor data linked to their cases
- Access a curated list of support resources

**Data analysis module** — generates reports and visualizations on
case patterns, incident types, geographic distribution, and timelines.

## Architecture

Two-role Django web application with mobile and desktop views,
deployed on a Linux VM hosted at Universidad FASTA (Mar del Plata).

**Database schema** — 8 core models:

| Model | Description |
|---|---|
| `casos_victima` | Victim profile and user account |
| `casos_caso` | IPP (case record) with status and metadata |
| `casos_agresor` | Aggressor profile linked to a case |
| `casos_domicilio` | Address records (victims and aggressors) |
| `casos_incidencia` | Judicial proceedings / incidents |
| `casos_documento` | Uploaded documents linked to cases |
| `casos_concurrencia` | Victim visits to official institutions |
| `casos_contacto` | Emergency contacts per victim |

## Stack

Python · Django · PostgreSQL · SQLite · HTML · CSS · Bootstrap ·
Pandas · Seaborn · Matplotlib · Folium · Ubuntu

## Screenshots

> All data shown in screenshots is fictitious and for illustrative
> purposes only. / Todos los datos mostrados son ficticios con
> propósito ilustrativo.

![LOGIN](https://github.com/user-attachments/assets/c5ae79c6-4710-4b5f-a2cc-4d4014a78e24)
![HOME](https://github.com/user-attachments/assets/8c72b803-5d5c-4ddc-9f73-c15510a07713)
![Captura de pantalla 2024-11-18 164058](https://github.com/user-attachments/assets/ea159e13-b25e-47b4-8f33-f46abed33c6e)

## Deployment note

This system was designed for institutional deployment in a controlled
environment with real victim data. It is not intended to be run locally
without proper environment configuration and data privacy safeguards.

- Valentina Fernández — valen.fernandez.montenegro@gmail.com

Developed at **Info-Lab** · Laboratorio de Investigación y Desarrollo
de Tecnología en Informática Forense


## Español

Surgen es un sistema pensado para que las víctimas de violencia de
género puedan tener accesible y en línea los datos de sus casos,
procurando evitar la revictimización ocurrida cuando recurren a las
autoridades. Unifica, historiza y da acceso inmediato a documentos,
incidencias y acciones relevantes para la asistencia de personas en
situación de violencia de género.

Ver documentación completa en `/docs`.
