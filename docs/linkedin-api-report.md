# Informe técnico: APIs de LinkedIn y acceso a datos de perfil

**Fecha de revisión:** 14 de septiembre de 2026  
**Fuentes:** documentación oficial de LinkedIn y Microsoft Learn

## 1. Resumen ejecutivo

Una aplicación Consumer convencional de LinkedIn no puede descargar el perfil completo de un
usuario. Las APIs abiertas permiten autenticar al miembro, obtener datos básicos de identidad y
publicar contenido, pero no recuperar su currículum, recomendaciones, proyectos, preferencias
laborales o red de contactos.

La única opción oficial que cubre casi todos esos datos es **Member Data Portability API**:

- Solo opera sobre el miembro que autoriza expresamente a la aplicación mediante OAuth.
- No permite descargar perfiles arbitrarios a partir de una URL de LinkedIn.
- Está sometida a restricciones geográficas derivadas del Digital Markets Act.
- El EEE está soportado de forma inequívoca.
- La documentación de miembro incluye Suiza, pero la página específica para aplicaciones de
  terceros la omite. El Help Center general sí incluye Suiza. Una integración de terceros debe
  confirmar este caso con LinkedIn.
- La modalidad para terceros requiere revisión de la aplicación y verificación empresarial.
- Devuelve datos por dominios con un esquema JSON genérico, no contratos fuertemente tipados para
  cada categoría.

Resultados principales:

| Información | Resultado |
| --- | --- |
| Perfil completo de cualquier persona | No existe una API Consumer oficial |
| Perfil del miembro que da consentimiento | Sí, mediante Member Data Portability |
| Experiencia, educación, cursos y certificaciones | Sí, mediante dominios de portabilidad |
| Idiomas, recomendaciones y proyectos | Sí, mediante dominios de portabilidad |
| Preferencias laborales | Sí, mediante `JOB_SEEKER_PREFERENCES` |
| Contactos de primer grado | Sí, mediante `CONNECTIONS`, con limitaciones |
| Acerca de | El ejemplo de `PROFILE` contiene `Summary`, sin garantía contractual de equivalencia |
| Destacados | No existe un dominio de portabilidad que preserve esta sección |
| Usuarios fuera de regiones elegibles | Descarga manual del archivo o importación de CV |

## 2. Modelos de acceso

Es esencial diferenciar cuatro modelos que la documentación distribuye entre distintas secciones:

1. **Consumer de autoservicio:** inicio de sesión y publicación.
2. **Verified on LinkedIn:** identidad y señales de verificación; datos profesionales limitados.
3. **Member Data Portability:** descarga amplia de los datos del miembro que consiente.
4. **APIs restringidas:** productos para socios aprobados o programas cerrados.

Que una aplicación Lite o Plus pueda trabajar con “todos los miembros” significa que cualquier
miembro elegible puede autorizarla. No significa que la aplicación pueda enumerar o consultar
personas sin su participación en OAuth.

## 3. Inventario de productos Consumer

El TOC actual contiene más productos que el resumen de la página inicial.

| Producto | Acceso | Endpoints o capacidad principal |
| --- | --- | --- |
| Sign In with LinkedIn mediante OIDC | Autoservicio | `/v2/userinfo` |
| Share on LinkedIn | Autoservicio | `/v2/ugcPosts`, registro y carga de medios |
| Verified on LinkedIn | Development, Lite y Plus | `/identityMe`, `/verificationReport` |
| Verified Plus | Acuerdo comercial | `/validationStatus` y datos adicionales |
| Scores, Reviews and 3P Signals | Beta cerrada, solo invitación | Credibilidad y componentes de perfil |
| Live Events | Beta y sujeto a elegibilidad | Creación y gestión de emisiones en directo |
| Profile API | Desarrolladores aprobados | `/v2/me`, `/v2/people` |
| Add to Profile | Botón estático | Introducción manual de títulos o certificaciones |
| Plugins | Widgets JavaScript | Share, Follow Company y AutoFill |

Member Data Portability está documentada bajo la sección DMA, no bajo el índice Consumer
principal, aunque sea la API determinante para este caso de uso.

### 3.1 Sign In with LinkedIn mediante OIDC

Scopes:

```text
openid
profile
email
```

Petición:

```http
GET https://api.linkedin.com/v2/userinfo
Authorization: Bearer {access_token}
```

Esquema de salida:

```typescript
interface LinkedInUserInfo {
  sub: string;
  name: string;
  given_name: string;
  family_name: string;
  picture: string;
  locale: string;
  email?: string;
  email_verified?: boolean;
}
```

El endpoint no devuelve experiencia, educación, certificaciones, idiomas, proyectos, sumario,
preferencias laborales o contactos. LinkedIn también advierte que OIDC autentica la cuenta, pero
no verifica la identidad real de la persona.

### 3.2 Share on LinkedIn

Scope:

```text
w_member_social
```

Petición principal:

```http
POST https://api.linkedin.com/v2/ugcPosts
X-Restli-Protocol-Version: 2.0.0
Authorization: Bearer {access_token}
Content-Type: application/json
```

Esquema resumido:

```typescript
interface UgcPostRequest {
  author: string;
  lifecycleState: "PUBLISHED";
  specificContent: {
    "com.linkedin.ugc.ShareContent": {
      shareCommentary: { text: string };
      shareMediaCategory: "NONE" | "ARTICLE" | "IMAGE" | "VIDEO";
      media?: ShareMedia[];
    };
  };
  visibility: {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" | "CONNECTIONS";
  };
}
```

Una creación correcta devuelve `201 Created` y el identificador en `X-RestLi-Id`.

Para imágenes o vídeos se registra primero una carga mediante:

```http
POST https://api.linkedin.com/v2/assets?action=registerUpload
```

La respuesta contiene una URL temporal de carga y un `DigitalMediaAsset URN`. Esta API no aporta
datos de perfil.

### 3.3 Verified on LinkedIn

Niveles:

| Nivel | Acceso | Datos |
| --- | --- | --- |
| Development | Automático, solo administradores de la app | Perfil básico y pruebas |
| Lite | Revisión de LinkedIn, producción | Perfil básico de miembros que consientan |
| Plus | Business Development | Empleo actual, educación reciente y metadatos avanzados |

#### Profile Details API

```http
GET https://api.linkedin.com/rest/identityMe
LinkedIn-Version: 202510.03
Authorization: Bearer {access_token}
```

Scopes:

```text
r_profile_basicinfo
r_most_recent_education
r_primary_current_experience
```

Los dos últimos son exclusivos de Plus.

Esquema resumido:

```typescript
interface IdentityMe {
  id: string;
  lastRefreshedAt: number;
  basicInfo: {
    firstName: MultiLocaleString;
    lastName: MultiLocaleString;
    primaryEmailAddress?: string;
    profileUrl: string;
    profilePicture?: ExpiringImage;
  };
  mostRecentEducation?: {
    schoolName?: MultiLocaleString;
    degreeName?: MultiLocaleString;
    schoolLogo?: ExpiringImage;
  };
  primaryCurrentPosition?: {
    title?: MultiLocaleString;
    companyName?: MultiLocaleString;
    companyPageUrl?: string;
    companyLogo?: ExpiringImage;
    startedOn?: { month: number; year: number };
  };
}
```

No devuelve el historial completo: únicamente la posición principal actual y la educación más
reciente, cuando la aplicación tiene nivel Plus y los scopes correspondientes.

#### Verification Report API

```http
GET https://api.linkedin.com/rest/verificationReport
LinkedIn-Version: 202607
```

Parámetros opcionales:

```text
verificationCriteria=IDENTITY
verificationCriteria=WORKPLACE
verifiedWithinDays={integer}
```

Salida principal:

```typescript
interface VerificationReport {
  id: string;
  userId?: string;
  verifications: Array<"IDENTITY" | "WORKPLACE">;
  verificationUrl?: string;
  lastRefreshedAt?: number;
  verifiedDetails?: Array<{
    category: "IDENTITY" | "WORKPLACE";
    lastVerifiedAt: number;
    verifiedName?: {
      firstName?: string;
      middleName?: string;
      lastName?: string;
    };
    verificationMethod?: string;
    organizationInfo?: {
      name: string;
      url: string;
    };
  }>;
}
```

#### Validation Status API

Exclusiva de Plus y autenticada mediante OAuth de dos patas:

```http
POST https://api.linkedin.com/rest/validationStatus?action=retrieve
LinkedIn-Version: 202510
```

Entrada:

```json
{
  "validationQueries": [
    {
      "id": "member-id"
    }
  ]
}
```

Se admiten hasta 500 identificadores.

Salida:

```typescript
interface ValidationStatusResponse {
  value: Array<{
    id: string;
    verificationStatus: {
      identity: "VALID" | "INVALID" | "VALID_WITH_UPDATES";
      workplace: "VALID" | "INVALID" | "VALID_WITH_UPDATES";
    };
    profileInformationStatus: "VALID" | "INVALID";
  }>;
}
```

Verified on LinkedIn no está diseñado para descargar currículums. Su documentación prohíbe usarlo
como herramienta de evaluación de candidatos o para tomar decisiones de contratación.

### 3.4 Scores, Reviews and 3P Signals

Es una beta cerrada, disponible únicamente por invitación. Utiliza el scope:

```text
rw_credibilitySignals
```

Endpoints principales:

```text
/rest/credibilitySignalV2
/rest/profileComponents
/rest/profileImages
/rest/profileDocuments
```

Permite integrar señales de credibilidad, proyectos y medios aportados por aplicaciones asociadas.
No es una API para descargar el perfil de LinkedIn del miembro ni modifica las conclusiones de
este informe.

### 3.5 Live Events

Producto beta para miembros o páginas elegibles para LinkedIn Live. Incluye:

```text
/v2/liveVideos
/v2/liveAssetActions
/v2/contentAccess
/v2/assets
/v2/ugcPosts
```

Permite programar, publicar y finalizar emisiones. Tampoco ofrece acceso a los campos de perfil
objeto de este informe.

### 3.6 Add to Profile y Plugins

[Add to Profile][add-to-profile] sigue activo, pero es un botón o enlace estático. Los valores de
certificaciones y títulos ya no se autocompletan; el miembro los introduce manualmente. No es una
API REST y no tiene esquema de respuesta.

Los plugins disponibles son:

- Share: recibe opcionalmente `data-url`.
- Follow Company: recibe `data-id` y opciones visuales.
- AutoFill: completa formularios, pero el dominio debe estar autorizado por LinkedIn.

## 4. OAuth 2.0 común

### 4.1 Autorización del miembro

```http
GET https://www.linkedin.com/oauth/v2/authorization
    ?response_type=code
    &client_id={client_id}
    &redirect_uri={registered_https_uri}
    &state={csrf_state}
    &scope={space_delimited_scopes}
```

Entrada:

| Parámetro | Obligatorio | Descripción |
| --- | --- | --- |
| `response_type` | Sí | Siempre `code` |
| `client_id` | Sí | Identificador de la aplicación |
| `redirect_uri` | Sí | URI HTTPS registrada exactamente |
| `scope` | Sí | Scopes aprovisionados, separados por espacios |
| `state` | Recomendado | Protección frente a CSRF |

La redirección correcta contiene `code` y `state`. El código expira a los 30 minutos.

### 4.2 Intercambio del código

```http
POST https://www.linkedin.com/oauth/v2/accessToken
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
code={authorization_code}
client_id={client_id}
client_secret={client_secret}
redirect_uri={same_redirect_uri}
```

Salida:

```typescript
interface TokenResponse {
  access_token: string;
  expires_in: number;
  refresh_token?: string;
  refresh_token_expires_in?: number;
  scope: string;
}
```

Los access tokens de miembro duran normalmente 60 días. Los refresh tokens programáticos solo
están disponibles para determinados productos o socios.

## 5. Member Data Portability API

### 5.1 Elegibilidad y acceso

#### Aplicaciones de terceros

Requisitos documentados:

1. Crear una aplicación asociada a una LinkedIn Company Page.
2. Hacer que un superadministrador verifique esa asociación.
3. Solicitar el producto **Member Data Portability API (3rd Party)**.
4. Proporcionar email empresarial, nombre legal, dirección registrada, web y política de
   privacidad.
5. Superar la revisión de LinkedIn.
6. Solicitar consentimiento mediante OAuth.

Scope:

```text
r_dma_portability_3rd_party
```

No se publican criterios completos de aprobación, cuotas generales ni plazos de revisión.

#### Aplicación personal

El miembro puede crear una aplicación que acceda únicamente a sus propios datos usando la página
especial **Member Data Portability (Member) Default Company**.

Existe una inconsistencia oficial:

- El onboarding indica `r_dma_portability_self_serve`.
- La referencia de los endpoints indica `r_dma_portability_member`.

Debe usarse el scope que realmente aparezca aprovisionado en la pestaña Auth del Developer Portal.

### 5.2 Member Snapshot API

Petición:

```http
GET https://api.linkedin.com/rest/memberSnapshotData
    ?q=criteria
    &domain=POSITIONS
    &start=0

Linkedin-Version: 202312
Authorization: Bearer {access_token}
Content-Type: application/json
```

Reglas:

- `q=criteria` es fijo y obligatorio.
- `domain` es opcional.
- Los dominios distinguen mayúsculas y minúsculas.
- Omitir `domain` está documentado como una petición de todos los dominios.
- Es preferible consultar explícitamente cada dominio.
- El endpoint solo acepta `Linkedin-Version: 202312`.
- La vista documental vigente es `2026-08`, pero no cambia la versión del endpoint.

Esquema formal de salida:

```typescript
interface MemberSnapshotResponse {
  paging: {
    start: number;
    count: number;
    total: number;
    links: Array<{
      type: string;
      rel: "next" | "prev";
      href: string;
    }>;
  };
  elements: Array<{
    snapshotDomain: string;
    snapshotData: Array<Record<string, unknown>>;
  }>;
}
```

Ejemplo oficial del dominio `PROFILE`:

```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "links": [],
    "total": 1
  },
  "elements": [
    {
      "snapshotDomain": "PROFILE",
      "snapshotData": [
        {
          "First Name": "Tom",
          "Last Name": "Cruise",
          "Headline": "Marketing Manager",
          "Summary": "",
          "Websites": "",
          "Address": "",
          "Geo Location": "",
          "Zip Code": "",
          "Birth Date": ""
        }
      ]
    }
  ]
}
```

LinkedIn no publica un esquema fuerte para los registros de cada dominio. La descripción del
dominio establece su semántica, pero no garantiza nombres, obligatoriedad o tipos de todos los
campos internos.

Recomendaciones de implementación:

- Conservar el payload original.
- Normalizar cada dominio independientemente.
- Considerar opcionales todos los campos.
- Ignorar de forma segura propiedades desconocidas.
- Seguir los enlaces `next`.
- No confiar exclusivamente en `paging.total`, que puede ser incompleto.
- Continuar hasta recibir la indicación de que no quedan datos.

### 5.3 Member Changelog API

Permite consultar interacciones archivadas después del consentimiento durante un máximo de 28
días:

```http
GET https://api.linkedin.com/rest/memberChangeLogs
    ?q=memberAndApplication
    &startTime={epoch_milliseconds}
    &count=10

Linkedin-Version: 202312
Authorization: Bearer {access_token}
```

`count` admite de 1 a 50. LinkedIn recomienda 10 y consultar aproximadamente una vez por hora por
miembro.

Esquema del evento:

```typescript
interface MemberChange {
  id: string | number;
  activityId: string;
  capturedAt: number;
  processedAt: number;
  configVersion: number;
  owner: string;
  actor: string;
  resourceName: string;
  resourceId: string;
  resourceUri: string;
  method: "CREATE" | "UPDATE" | "PARTIAL_UPDATE" | "DELETE";
  methodName?: string;
  activity: Record<string, unknown>;
  processedActivity: Record<string, unknown>;
  siblingActivities?: unknown[];
  parentSiblingActivities?: unknown[];
  activityStatus: "SUCCESS" | "FAILURE" | "SUCCESSFUL_REPLAY";
}
```

Debe utilizarse el último `processedAt` como siguiente `startTime`. Como el límite es inclusivo, es
necesario deduplicar por `id` o `activityId`.

### 5.4 Estado de la autorización

```http
GET https://api.linkedin.com/rest/memberAuthorizations
    ?q=memberAndApplication
```

Salida:

```typescript
interface MemberAuthorizationResponse {
  elements: Array<{
    memberComplianceAuthorizationKey: {
      developerApplication: string;
      member: string;
    };
    regulatedAt: number;
    memberComplianceScopes: ["DMA"];
  }>;
}
```

El procesamiento puede activarse manualmente, si el registro automático falla:

```http
POST https://api.linkedin.com/rest/memberAuthorizations
Content-Type: application/json

{}
```

## 6. Evaluación de las acciones solicitadas

| # | Acción | Resultado | API, dominio o limitación |
| --- | --- | --- | --- |
| 1 | Descargar el perfil | Sí, condicionado | Snapshot del miembro que consiente; no perfiles arbitrarios |
| 2 | Cursos y certificaciones | Sí | `COURSES`, `CERTIFICATIONS`; `LEARNING` es historial de Learning |
| 3 | Experiencia profesional completa | Sí | `POSITIONS` |
| 4 | Idiomas | Sí | `LANGUAGES` |
| 5 | Recomendaciones | Sí | `RECOMMENDATIONS`, recibidas y emitidas |
| 6 | Proyectos | Sí | `PROJECTS` |
| 7 | Educación | Sí | `EDUCATION` |
| 8 | Destacados | No de forma completa | No existe dominio `FEATURED` |
| 9 | Acerca de | Parcialmente documentado | `PROFILE` contiene `Summary` en el ejemplo |
| 10 | Teléfono, nombre, email y dirección | Sí, del miembro | Varios dominios; no implica que sean públicos |
| 11 | Preferencias de búsqueda de empleo | Sí | `JOB_SEEKER_PREFERENCES` |
| 12 | Red de contactos | Sí, primer grado | `CONNECTIONS`; sin navegación de segundo grado |

### 6.1 Perfil completo

No existe un endpoint equivalente a:

```text
downloadProfile("https://linkedin.com/in/usuario")
```

El Snapshot API solo opera sobre el miembro representado por el token OAuth. Una descarga amplia
requiere combinar `PROFILE` con los dominios profesionales y personales necesarios.

### 6.2 Cursos y certificaciones

Dominios:

```text
COURSES
CERTIFICATIONS
LEARNING
```

`COURSES` representa cursos incluidos en el perfil. `CERTIFICATIONS` representa licencias y
certificaciones. `LEARNING` contiene actividad de LinkedIn Learning y no debe mezclarse con las
otras dos categorías.

La descarga manual describe certificaciones con entidad emisora, fechas y número de licencia,
cuando estén presentes. La API de Snapshot no formaliza esos campos en un esquema estable.

### 6.3 Experiencia profesional

`POSITIONS` incluye los puestos añadidos al perfil, con información como empresa, título,
descripción, ubicación y fechas.

Verified Plus no es equivalente: solo proporciona `primaryCurrentPosition`.

### 6.4 Idiomas

`LANGUAGES` contiene los idiomas declarados por el miembro y su nivel de competencia.

### 6.5 Recomendaciones

`RECOMMENDATIONS` contiene recomendaciones emitidas y recibidas. La descarga manual las separa en:

```text
Recommendations Given
Recommendations Received
```

La documentación de descarga describe nombre, empresa asociada, texto y fecha de publicación.

### 6.6 Proyectos

`PROJECTS` representa los proyectos del perfil. La descarga manual documenta nombre, descripción,
colaboradores, fechas y URLs de medios adjuntos.

### 6.7 Educación

`EDUCATION` incluye instituciones, fechas, titulaciones y actividades. Verified Plus solo devuelve
`mostRecentEducation`, no el historial.

### 6.8 Destacados

No existe un dominio `FEATURED`. Estos dominios pueden contener piezas utilizadas en la sección:

```text
ARTICLES
MEMBER_SHARE_INFO
RICH_MEDIA
PROJECTS
```

Pero no preservan de manera documentada:

- Qué elementos están destacados.
- Su orden.
- Sus etiquetas.
- La asociación entre un elemento y la sección Destacados.

Existe una API restringida denominada Member Rich Content. Su campo `memberRichContents` se
documenta como la sección Featured y puede referenciar posts, artículos, enlaces o medios. Se usa
indirectamente mediante `/v2/me`, pero solo está disponible para desarrolladores aprobados y no
constituye una opción Consumer abierta.

Además, la sección actual permite destacar experiencia, certificaciones, recomendaciones, cursos,
proyectos o educación. La referencia antigua de Member Rich Content no garantiza cobertura de
estas nuevas asociaciones.

### 6.9 Acerca de

El ejemplo oficial del dominio `PROFILE` contiene una propiedad `Summary`. Sin embargo, LinkedIn no
garantiza expresamente que corresponda siempre a la sección actual “Acerca de”. Debe tratarse como
una equivalencia probable y no como un contrato estable.

No debe confundirse con:

```text
PROFILE_SUMMARY
```

Ese dominio contiene un resumen generado por IA para recomendaciones de contactos, no
necesariamente el texto escrito por el miembro.

### 6.10 Datos personales

No existe un único dominio `CONTACT_INFO`. Deben combinarse:

| Dominio | Contenido |
| --- | --- |
| `PROFILE` | Nombre, dirección, ubicación, código postal y otros datos biográficos |
| `EMAIL_ADDRESSES` | Emails actuales e históricos asociados a la cuenta |
| `PHONE_NUMBERS` | Números vinculados a la cuenta |
| `CONTACTS` | Contactos importados por el miembro |

Estos datos son datos de portabilidad de la propia cuenta. No son necesariamente datos publicados
en el perfil. La documentación no garantiza un indicador uniforme que permita saber qué campos son
públicos.

OIDC y `/identityMe` pueden devolver el email primario del miembro autenticado, pero es opcional.
No permiten consultar teléfonos o direcciones de otros miembros.

### 6.11 Preferencias laborales

`JOB_SEEKER_PREFERENCES` puede incluir:

- Tipos de trabajo preferidos.
- Ubicaciones.
- Industrias.
- Tamaños de empresa.
- Empresas deseadas.
- Títulos profesionales.
- Nivel de actividad.

No está disponible mediante OIDC ni mediante `/identityMe`.

### 6.12 Red de contactos

`CONNECTIONS` contiene contactos de primer grado y documenta:

- Nombre.
- Puesto.
- Empresa.
- Fecha de conexión.

La descripción del dominio API no promete emails ni URLs públicas. La descarga manual puede
incluirlos, pero el email solo aparece si el contacto lo permite en su configuración de privacidad.

`CONTACTS` es diferente: representa contactos importados desde otros servicios.

## 7. APIs restringidas e históricas

### 7.1 Profile API

```http
GET https://api.linkedin.com/v2/me
GET https://api.linkedin.com/v2/people/(id:{person_id})
```

Está restringida a desarrolladores aprobados. Los IDs son específicos de la aplicación y no
permiten buscar personas por URL o nombre.

El scope histórico `r_fullprofile` incluía dirección, cursos, certificaciones, educación,
posiciones, proyectos, sumario, teléfono y otros campos, pero su acceso está cerrado.

Las páginas de referencia de esos campos describen un contrato histórico, no una capacidad que una
nueva aplicación Consumer pueda solicitar.

### 7.2 Connections API

```http
GET https://api.linkedin.com/v2/connections
    ?q=viewer
    &start=0
    &count=50
```

Scopes restringidos:

```text
r_1st_connections
r_compliance
```

Salida básica:

```typescript
interface ConnectionsResponse {
  elements: Array<{
    to: string;
  }>;
  paging: {
    start: number;
    count: number;
    total: number;
    links: unknown[];
  };
}
```

La decoración puede añadir ID y nombres. No permite:

- Obtener contactos de segundo grado.
- Consultar los contactos de una conexión.
- Navegar redes de terceros.

Compliance es un programa cerrado a nuevas solicitudes.

## 8. Descarga manual

Fuera del ámbito geográfico o cuando una aplicación no obtiene aprobación, el usuario puede:

```text
LinkedIn
→ Settings & Privacy
→ Data Privacy
→ Download your data
→ Seleccionar categorías
→ Request archive
```

Características:

- Disponible globalmente.
- No es una API.
- LinkedIn envía un enlace por email.
- El enlace permanece disponible durante 72 horas.
- Solo se incluyen categorías aplicables a la cuenta.
- No se incluyen People You May Know ni Who Viewed Your Profile.
- La lista de conexiones solo incluye emails cuando el contacto lo ha permitido.

El archivo manual contempla explícitamente Positions, Education, Certifications, Courses,
Languages, Projects, Recommendations, Job Seeker Preferences, Profile, Phone Numbers, Email
Addresses y Connections.

No existe una categoría específica y garantizada para Featured.

## 9. Inconsistencias documentales relevantes

1. El producto Member personal menciona `r_dma_portability_self_serve`, mientras las referencias
   compartidas usan `r_dma_portability_member`.
2. El Help Center incluye Suiza en la portabilidad para miembros y terceros, pero la página técnica
   específica de terceros solo menciona el EEE.
3. La tabla general de OIDC menciona headline, pero el contrato de `/userinfo` no lo incluye.
4. Algunas páginas de Verified asignan `r_verify` a Development/Lite y `r_verify_details` a Plus,
   mientras la referencia actual acepta o exige combinaciones distintas.
5. La documentación de Share describe la carga binaria como POST, pero su ejemplo con
   `curl --upload-file` utiliza PUT.
6. El índice antiguo de Consumer no refleja todos los productos presentes en el TOC actual.
7. El enlace de Microsoft Learn a Add to Profile puede fallar, aunque el servicio oficial
   independiente continúa activo.

En producción, los scopes efectivamente aprovisionados en Developer Portal y las release notes
vigentes deben considerarse la fuente operativa de verdad.

## 10. Recomendación de arquitectura

### Usuarios elegibles para Member Data Portability

1. Solicitar el producto para terceros.
2. Implementar OAuth con `r_dma_portability_3rd_party`.
3. Verificar `memberAuthorizations`.
4. Consultar explícitamente cada dominio requerido.
5. Recorrer todas las páginas.
6. Guardar el payload original.
7. Normalizar a un modelo interno.
8. Sincronizar cambios mediante Member Changelog.
9. Gestionar revocación, expiración y eliminación de datos.

Modelo de almacenamiento sugerido:

```typescript
interface ImportedLinkedInDomain {
  memberId: string;
  domain: string;
  importedAt: string;
  rawPayload: Record<string, unknown>[];
  normalizedData?: Record<string, unknown>;
}
```

### Usuarios no elegibles

1. Usar OIDC para identidad básica.
2. Solicitar un CV o archivo descargado manualmente.
3. Importar y normalizar ese documento con consentimiento.

No se recomienda scraping de perfiles públicos:

- No es una API oficial.
- No elimina las restricciones de privacidad y consentimiento.
- Es frágil ante cambios de interfaz.
- Puede vulnerar las condiciones de LinkedIn.

## 11. Conclusión

Member Data Portability permite construir una importación amplia del perfil profesional para
miembros elegibles que consientan. Cubre once de las doce categorías total o parcialmente. La
excepción principal es Destacados, cuya selección y orden no están modelados en la API de
portabilidad.

Para una aplicación Consumer global no existe una API oficial que descargue el currículum completo
de un usuario. OIDC y Verified on LinkedIn son complementos de identidad y verificación, no
sustitutos del archivo de datos. La solución debe diseñarse alrededor del consentimiento, la
elegibilidad geográfica y la naturaleza no tipada de los snapshots.

## 12. Fuentes oficiales

- [LinkedIn Consumer Solutions][consumer]
- [Consumer TOC][consumer-toc]
- [Sign In with LinkedIn mediante OIDC][oidc]
- [Share on LinkedIn][share]
- [Verified on LinkedIn][verified]
- [Profile Details API][identity-me]
- [Verification Report API][verification-report]
- [Validation Status API][validation-status]
- [Member Data Portability para terceros][portability-third-party]
- [Member Data Portability para miembros][portability-member]
- [Member Snapshot API][snapshot-api]
- [Member Snapshot Domains][snapshot-domains]
- [Member Changelog API][changelog-api]
- [Member Authorization Management API][authorization-management]
- [OAuth Authorization Code Flow][oauth]
- [Profile API][profile-api]
- [Full Profile Fields, acceso cerrado][full-profile]
- [Connections API][connections-api]
- [Member Rich Content API][rich-content]
- [Descargar datos de LinkedIn][download-data]
- [Exportar conexiones][export-connections]
- [Uso de datos por aplicaciones de terceros][third-party-data]
- [Términos de portabilidad][portability-terms]
- [Scores, Reviews and 3P Signals][signals]
- [Live Events][live-events]

[consumer]: https://learn.microsoft.com/en-us/linkedin/consumer/
[consumer-toc]: https://learn.microsoft.com/en-us/linkedin/consumer/toc.json
[oidc]: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2
[share]: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin
[verified]: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/verified-on-linkedin/overview
[identity-me]: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/verified-on-linkedin/api-reference/identity-me
[verification-report]: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/verified-on-linkedin/api-reference/verification-report
[validation-status]: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/verified-on-linkedin/api-reference/validation-status
[portability-third-party]: https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/member-data-portability-3rd-party/?view=li-dma-data-portability-2026-08
[portability-member]: https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/member-data-portability-member/?view=li-dma-data-portability-2026-08
[snapshot-api]: https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/shared/member-snapshot-api?view=li-dma-data-portability-2026-08
[snapshot-domains]: https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/shared/snapshot-domain?view=li-dma-data-portability-2026-08
[changelog-api]: https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/shared/member-changelog-api?view=li-dma-data-portability-2026-08
[authorization-management]: https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/shared/member-authorization-management-api?view=li-dma-data-portability-2026-08
[oauth]: https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow
[profile-api]: https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/profile-api
[full-profile]: https://learn.microsoft.com/en-us/linkedin/shared/references/v2/profile/full-profile
[connections-api]: https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/connections-api
[rich-content]: https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/member-rich-content-api
[download-data]: https://www.linkedin.com/help/linkedin/answer/a1339364
[export-connections]: https://www.linkedin.com/help/linkedin/answer/a566336
[third-party-data]: https://www.linkedin.com/help/linkedin/answer/a519947
[portability-terms]: https://www.linkedin.com/legal/l/portability-api-terms
[signals]: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/scores-reviews-3p-signals/overview
[live-events]: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/live-video/
[add-to-profile]: https://addtoprofile.linkedin.com/
