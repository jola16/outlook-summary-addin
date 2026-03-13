# 1. Registrera på Office.context.mailbox, inte på item
I en pinnad panel byts Office.context.mailbox.item ut när du klickar runt, men det ursprungliga item‑objektet du fångar i Office.onReady blir ”stale”.

Microsofts docs registrerar därför ItemChanged så här:

```js
Office.onReady(() => {
  const item = Office.context.mailbox.item;

  document.getElementById("meta").textContent =
    (item.from ? item.from.displayName + " - " : "") +
    (item.to   ? item.to.length + " " + t.recipients : "");

  document.getElementById("subject").textContent = item.subject || t.noSubject;

  item.loadCustomPropertiesAsync(onPropsLoaded);

  // Registrera ItemChanged på mailbox, inte på item
  Office.context.mailbox.addHandlerAsync(
    Office.EventType.ItemChanged,
    onItemChanged
  );
});
```

# 2. Uppdatera mer än bara custom properties vid byte
Just nu uppdaterar onItemChanged bara custom properties, men inte din övriga UI (subject, meta).
Jag skulle därför flytta din init‑logik till en separat updateUIForCurrentItem och återanvända den:

```js
Office.onReady(() => {
  updateUIForCurrentItem();

  Office.context.mailbox.addHandlerAsync(
    Office.EventType.ItemChanged,
    onItemChanged
  );
});

function updateUIForCurrentItem() {
  const item = Office.context.mailbox.item;
  if (!item) return;

  document.getElementById("meta").textContent =
    (item.from ? item.from.displayName + " - " : "") +
    (item.to   ? item.to.length + " " + t.recipients : "");

  document.getElementById("subject").textContent = item.subject || t.noSubject;

  item.loadCustomPropertiesAsync(onPropsLoaded);
}

function onItemChanged(event) {
  updateUIForCurrentItem();
}
```
Då får du:

Rätt koppling (på mailbox‑nivå) så att eventet fortsätter fungera när taskpanen är pinnad.

En enda kodpath för både första load och efterföljande item‑byten, vilket minimerar drift mellan fallen.

# Nästa steg
Fundera även på hur du bäst hanterar fall där item saknas (t.ex. när inga meddelanden är markerade eller UI:et fladdrar vid reload).

---

# 2026-03-13 Result: ItemChanged Implementation

## Status: ✓ COMPLETED

Denna plan implementerades i version 1.4.4 och är nu fullt funktionell.

### Vad implementerades:
1. **ItemChanged event handler** registrerad på `Office.context.mailbox` (inte på item)
2. **updateUIForCurrentItem()** funktion som hanterar både initial load och item-byten
3. **UI uppdateras** när användaren byter mellan mejl medan taskpanen är pinnad
4. **Korrekt koppling** på mailbox-nivå för att undvika "stale" item-objekt

### Filer som ändrades:
- `src/taskpane/taskpane.html` – Implementerade ItemChanged-handler och updateUIForCurrentItem()
- `manifest.xml` – Lade till SupportsPinning för pinnad taskpane-stöd
- `CHANGELOG.md` – Dokumenterade ändringar i version 1.4.3 och 1.4.4

### Resultat:
Taskpanen uppdateras nu korrekt när användaren navigerar mellan mejl medan taskpanen är pinnad. Ingen "stale" item-data längre.