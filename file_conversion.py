import json
import email
from email import policy
from email.parser import BytesParser


def eml_to_json(eml_file_path):
    # Read and parse the .eml file
    with open(eml_file_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)

    # Extract key fields
    email_data = {
        "subject": msg["subject"],
        "from": msg["from"],
        "to": msg.get("to"),
        "cc": msg.get("cc"),
        "bcc": msg.get("bcc"),
        "date": msg.get("date"),
        "body": "",
        "attachments": []
    }

    # Extract plain text and HTML body, if available
    if msg.is_multipart():
        for part in msg.iter_parts():
            content_type = part.get_content_type()
            content_disposition = part.get("Content-Disposition")

            # Process the body content
            if content_type == "text/plain" and not content_disposition:
                email_data["body"] += part.get_payload(decode=True).decode(part.get_content_charset(), errors="replace")
            elif content_type == "text/html" and not content_disposition:
                email_data["body"] += part.get_payload(decode=True).decode(part.get_content_charset(), errors="replace")

            # Process attachments
            if content_disposition and "attachment" in content_disposition:
                attachment = {
                    "filename": part.get_filename(),
                    "content_type": content_type,
                    "size": len(part.get_payload(decode=True))
                }
                email_data["attachments"].append(attachment)
    else:
        email_data["body"] = msg.get_payload(decode=True).decode(msg.get_content_charset(), errors="replace")

    # Convert the email data to JSON
    email_json = json.dumps(email_data, indent=4)
    return email_json


if __name__ == "__main__":
    eml_file_path = "./id000.eml"
    email_json = eml_to_json(eml_file_path)
    print(email_json)