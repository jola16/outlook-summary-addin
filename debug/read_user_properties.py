"""Debug script to read Office.js customProperties using correct MAPI format.

Based on Perplexity's win32com example:
- Namespace GUID: {00020329-0000-0000-C000-000000000046}
- Property name: cecp-357113f9-c204-44ca-a3fc-101588af3f49
"""

import win32com.client
import json
from typing import Optional


def get_outlook_app():
    """Get Outlook application instance."""
    try:
        outlook = win32com.client.GetObject(Class="Outlook.Application")
        return outlook
    except Exception as e:
        print(f"Error connecting to Outlook: {e}")
        return None


def read_custom_properties(item) -> Optional[dict]:
    """Read customProperties using the correct MAPI format."""

    try:
        prop_accessor = item.PropertyAccessor

        # Correct format from Perplexity example
        namespace_guid = "{00020329-0000-0000-C000-000000000046}"
        app_id = "357113f9-c204-44ca-a3fc-101588af3f49"

        schema = f"http://schemas.microsoft.com/mapi/string/{namespace_guid}/cecp-{app_id}"

        print(f"    Attempting to read customProperties...")
        print(f"    Schema URL: {schema}\n")

        try:
            json_blob = prop_accessor.GetProperty(schema)

            if json_blob:
                print(f"    ✓ FOUND customProperties!")
                print(f"      Type: {type(json_blob).__name__}")
                print(f"      Size: {len(json_blob) if isinstance(json_blob, (bytes, str)) else 'N/A'} bytes\n")

                # Parse as JSON
                try:
                    if isinstance(json_blob, bytes):
                        decoded = json_blob.decode('utf-8')
                    else:
                        decoded = str(json_blob)

                    json_data = json.loads(decoded)
                    print(f"    ✓ Successfully parsed as JSON:")
                    print(f"    {json.dumps(json_data, indent=6)}\n")

                    return json_data

                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"    ✗ Failed to parse as JSON: {e}")
                    print(f"    Raw value (first 500 chars):")
                    print(f"    {str(json_blob)[:500]}\n")
                    return None
            else:
                print(f"    ✗ Property returned empty/null\n")
                return None

        except Exception as e:
            error_msg = str(e)
            print(f"    ✗ Error reading property: {error_msg}\n")
            return None

    except Exception as e:
        print(f"    Error: {e}\n")
        return None


def scan_inbox_for_target(outlook_app, target_subject: str = "Unna dig något extra") -> None:
    """Scan inbox for a specific email and read its customProperties."""
    try:
        namespace = outlook_app.GetNamespace("MAPI")
        inbox = namespace.GetDefaultFolder(6)  # 6 = olFolderInbox

        items = inbox.Items

        for item in items:
            try:
                if item.Class != 43:  # 43 = olMail
                    continue

                if target_subject.lower() in item.Subject.lower():
                    print(f"\n✓ FOUND TARGET EMAIL: {item.Subject}")
                    print(f"  From: {item.SenderName}")
                    print(f"  Received: {item.ReceivedTime}\n")

                    cecp_data = read_custom_properties(item)

                    if cecp_data:
                        print(f"  ✓ CustomProperties successfully read!")
                        print(f"    Keys: {list(cecp_data.keys())}")
                        for key, value in cecp_data.items():
                            val_str = str(value)[:100]
                            print(f"    - {key}: {val_str}")
                    else:
                        print(f"  ✗ Could not read customProperties")

                    return

            except Exception as e:
                print(f"Error processing item: {e}")

        print(f"\n✗ Target email '{target_subject}' not found in inbox")

    except Exception as e:
        print(f"Error scanning inbox: {e}")


def main():
    """Main entry point."""
    print("Outlook CustomProperties Reader (Correct MAPI Format)")
    print("=" * 70)

    outlook = get_outlook_app()
    if not outlook:
        print("Failed to connect to Outlook")
        return

    print("Connected to Outlook\n")
    print("Searching for target email: 'Unna dig något extra'")
    print("Reading customProperties with correct MAPI format...\n")

    scan_inbox_for_target(outlook)


if __name__ == "__main__":
    main()
