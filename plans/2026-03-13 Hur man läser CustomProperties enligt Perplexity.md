# 2026-03-13 Plan: Hur man läser CustomProperties enligt Perplexity

## Del 1: Perplexity's förklaring

Det är "korrekt" att Roo Code inte hittar dem via vanliga MAPI‑properties – Outlook‑addins sparar `CustomProperties` i **en enda special‑property som JSON**, inte som vanliga named properties som syns i `UserProperties`/normala MAPI‑fält. [github](https://github.com/OfficeDev/office-js-docs-pr/blob/main/docs/outlook/metadata-for-an-outlook-add-in.md)

### Hur CustomProperties faktiskt lagras

- `Office.js` serialiserar alla dina custom properties till ett JSON‑objekt. [learn.microsoft](https://learn.microsoft.com/en-us/javascript/api/outlook/office.customproperties?view=outlook-js-preview)
- Det JSON:et sparas i **en MAPI‑extended property** vars namn är `cecp-<addinManifestId>` (där `<addinManifestId>` är ditt manifest‑GUID i *lowercase*). [stackoverflow](https://stackoverflow.com/questions/43130810/get-custom-property-set-in-outlook-add-in-via-microsoft-graph)
- Den här extended propertyn ligger i en speciell property set enligt MS‑OXCEXT och syns inte som "fina" per‑nyckel properties, utan som en blob‐sträng. [github](https://github.com/OfficeDev/office-js/issues/1234)

Så om du bara itererar `MailItem.UserProperties`, "custom fields" i Outlook‑UI eller generiska MAPI‑attribut så hittar du dem inte. [support.microsoft](https://support.microsoft.com/en-us/topic/changes-to-custom-properties-in-outlook-f1caa232-60a3-0526-068c-d5eeec8b3752)

### Vad du behöver göra från win32com

Med `win32com`/MAPI måste du:

1. Få tag i rätt MAPI‑objekt (`IMAPIProp`) för mailet (via `CDO/MAPI` eller `mapi.Session.OpenMessageStore` etc).
2. Leta efter **extended propertyn** med rätt namn/ID – typiskt något i stil med:
   - Property‑tag i intervallet för custom props, och
   - Ett namn som matchar `cecp-357113f9-c204-44ca-a3fc-101588af3f49` (din `Id` i manifestet, fast lowercase). [learn.microsoft](https://learn.microsoft.com/en-us/office/client-developer/outlook/mapi/choosing-a-form-s-property-set)
3. När du hittat propertyn: läsa värdet (sträng/bytes), tolka som JSON, och plocka ut dina nycklar.

Det är exakt det Microsoft rekommenderar om du ska läsa dessa via REST/Graph – du expanderar extended property med det här ID/Namnet och parsar JSON:en själv. [learn.microsoft](https://learn.microsoft.com/en-us/office/dev/add-ins/outlook/metadata-for-an-outlook-add-in)
Via `win32com` är det samma princip, bara annan API‑yta.

### Slutsats från Perplexity

- Det är inte ett problem med att `CustomProperties` saknas; de ligger bara i en dold JSON‑blob på en extended property.
- Roo Code måste explicit leta efter den extended propertyn (`cecp-<lowercase-manifest-id>`) och deserialisera innehållet, istället för att loopa vanliga MAPI/named properties. [stackoverflow](https://stackoverflow.com/questions/43130810/get-custom-property-set-in-outlook-add-in-via-microsoft-graph)

### VBA-exempel från Perplexity

```vb
Sub ReadAddinCustomProps()
    Dim mail As Outlook.MailItem
    Dim pa As Outlook.PropertyAccessor
    Dim schema As String
    Dim json As String

    ' Ta t.ex. första mejlet i Inkorgen
    Set mail = Application.Session.GetDefaultFolder(olFolderInbox).Items(1)

    ' cecp-<app-guid> – använd ditt manifest-ID i lowercase
    schema = "http://schemas.microsoft.com/mapi/string/" & _
             "{00020329-0000-0000-C000-000000000046}/" & _
             "cecp-357113f9-c204-44ca-a3fc-101588af3f49"

    Set pa = mail.PropertyAccessor

    On Error Resume Next
    json = pa.GetProperty(schema)
    On Error GoTo 0

    Debug.Print json  ' Här får du JSON-strängen med alla CustomProperties
End Sub
```

### win32com-exempel från Perplexity

```python
import win32com.client as win32

outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # olFolderInbox
mail = inbox.Items[0]

guid = "{00020329-0000-0000-C000-000000000046}"
app_id = "357113f9-c204-44ca-a3fc-101588af3f49"  # lowercase
schema = f"http://schemas.microsoft.com/mapi/string/{guid}/cecp-{app_id}"

pa = mail.PropertyAccessor
json_blob = pa.GetProperty(schema)  # kan kasta COM‑exception om ej finns

print(json_blob)
```

---

## Del 2: Roo Code's implementering och resultat

### Implementering

Baserat på Perplexity's vägledning skapade jag ett Python-skript: **`debug/read_user_properties.py`**

Skriptet använder exakt det format som Perplexity rekommenderade:
- Namespace GUID: `{00020329-0000-0000-C000-000000000046}`
- Property-namn: `cecp-357113f9-c204-44ca-a3fc-101588af3f49`
- URL-format: `http://schemas.microsoft.com/mapi/string/{GUID}/cecp-{APP_ID}`

### Resultat från debug-skriptet

Skriptet fungerar perfekt! Här är den kompletta konsolutmatningen från körningen:

```
✓ FOUND TARGET EMAIL: Unna dig något extra
✓ FOUND customProperties!
Type: str
Size: 267 bytes
✓ Successfully parsed as JSON:
{
  "summary": "<p>Det här är ett exempel på <strong>summary</strong>. Ingen summary hittades i meddelandets customProperties.</p>",
  "actions": "<ul><li>Det här är ett exempel på en <strong>action</strong>. Inga actions hittades i meddelandets customProperties.</li></ul>"
}
```

**Resultat**: Skriptet läste framgångsrikt customProperties från mejlet "Unna dig något extra" och parsade JSON-blobben korrekt.

### Slutsatser från implementeringen

1. **CustomProperties lagras som JSON-blob** i en extended MAPI-property
2. **Rätt namespace GUID** är: `{00020329-0000-0000-C000-000000000046}` (inte cecp-GUID:en!)
3. **Property-namn** är: `cecp-357113f9-c204-44ca-a3fc-101588af3f49`
4. **URL-format** för PropertyAccessor: `http://schemas.microsoft.com/mapi/string/{GUID}/cecp-{APP_ID}`
5. **Fungerar perfekt** från Python via win32com med rätt format

### Tillgängliga debug-verktyg

#### 1. `debug/read_user_properties.py` (REKOMMENDERAD)
- **Typ**: Python-skript
- **Körs från**: Kommandoraden
- **Använder**: `win32com` och MAPI extended properties
- **Status**: ✓ Testad och fungerar perfekt
- **Användning**: `python debug/read_user_properties.py`
- **Fördel**: Läser customProperties direkt från Outlook utan att behöva öppna mejlet i gränssnittet

#### 2. `debug/read_custom_properties.html`
- **Typ**: HTML/Office.js debug-verktyg
- **Körs från**: Outlook (som taskpane eller i webbläsare)
- **Använder**: Office.js API
- **Användning**:
  1. Öppna ett mejl i Outlook
  2. Öppna denna HTML-fil i Outlook's taskpane eller en lokal webbserver
  3. Klicka på "Read Custom Properties"-knappen
  4. Verktyget visar mejlets customProperties (summary, actions, etc.)
- **Fördel**: Testar Office.js API direkt från Outlook-gränssnittet

**Rekommendation**: Använd `debug/read_user_properties.py` för snabb debugging från kommandoraden.
