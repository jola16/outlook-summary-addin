# Linting Compliance vs Functionality Examples

When linting rules conflict with functionality requirements, prioritize functionality and document the deviation. Below are common scenarios where this applies.

## Example 1: Dynamic imports for plugin systems

**Rule:** `PLC0415` – Import outside toplevel
**Reason for exception:** Plugin system requires runtime import based on configuration

```python
def load_plugin(plugin_name: str):
    """Load plugin dynamically based on configuration."""
    if plugin_name == "outlook":
        from plugins import outlook  # noqa: PLC0415
        return outlook
    # Plugin name determines which module to import at runtime
```

## Example 2: Broad exception handling for COM objects

**Rule:** `BLE001` – Broad exception catch
**Reason for exception:** COM objects can raise various Windows-specific exceptions that are difficult to predict

```python
def get_outlook_item(entry_id: str):
    """Fetch item from Outlook via COM."""
    try:
        outlook_item = outlook.GetItemFromID(entry_id)
        return outlook_item
    except Exception as e:  # noqa: BLE001
        # COM errors are unpredictable; must catch all and log for debugging
        print(f"Failed to retrieve item {entry_id}: {e}")
        return None
```

## Example 3: Long lines in inline CSS/HTML

**Rule:** `E501` – Line too long
**Reason for exception:** Inline CSS strings are more maintainable as single lines than split across multiple lines

```python
STYLE = '<style>body { font-family: "Segoe UI", sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }</style>'  # noqa: E501
```

## Example 4: Magic values in test fixtures

**Rule:** `PLR2004` – Magic value used in comparison
**Reason for exception:** Test data uses specific values for reproducibility and clarity

```python
def test_parse_email():
    """Test email parsing with known fixture."""
    items = parse_email_fixture()
    assert len(items) == 42  # noqa: PLR2004
    # 42 is the exact count in test fixture, not arbitrary
```

## Example 5: Assert for critical business invariants

**Rule:** `S101` – Use of assert detected
**Reason for exception:** Critical invariant that must never be violated in production

```python
def process_payment(amount: float):
    """Process payment with validation."""
    assert amount > 0, "Payment amount must be positive"  # noqa: S101
    # This is a critical business rule, not a test assertion
    # Failure indicates a bug in the calling code
```

## Example 6: Print for CLI user feedback

**Rule:** `T201` – print() found
**Reason for exception:** CLI tool requires direct stdout output for user feedback

```python
def refresh_inbox():
    """Refresh inbox with progress feedback."""
    print("Fetching inbox items...")  # noqa: T201
    # Logging would require extra configuration for CLI users
    # Direct print is appropriate for command-line tools
```

## Common Pattern

All examples share a common theme:
- The linting rule is **technically correct** but **contextually inappropriate**
- The functionality **requires** the deviation
- The alternative would make the code **worse or more complex**
- The deviation is **documented** with a comment explaining why

## When to use this approach

1. **Functionality cannot be achieved otherwise** – no reasonable refactoring exists
2. **The deviation is localized** – not a systemic problem
3. **The reason is documented** – future maintainers understand the trade-off
4. **User approval is obtained** – never add disable comments without asking first
