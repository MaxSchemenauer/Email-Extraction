import json
import email
import os
from email import policy
from email.parser import BytesParser

from sympy.physics.vector import outer


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

    decoding = msg.get_content_charset()
    if decoding is None:
        decoding = "utf-8"

    # Extract plain text and HTML body, if available
    if msg.is_multipart():
        for part in msg.iter_parts():
            content_type = part.get_content_type()
            content_disposition = part.get("Content-Disposition")
            part_decoding = msg.get_content_charset()
            if part_decoding is None:
                part_decoding = "utf-8"

            # Process the body content
            if content_type == "text/plain" and not content_disposition:
                email_data["body"] += part.get_payload(decode=True).decode(part_decoding, errors="replace")
            elif content_type == "text/html" and not content_disposition:
                email_data["body"] += part.get_payload(decode=True).decode(part_decoding, errors="replace")

            # Process attachments
            if content_disposition and "attachment" in content_disposition:
                attachment = {
                    "filename": part.get_filename(),
                    "content_type": content_type,
                    "size": len(part.get_payload(decode=True))
                }
                email_data["attachments"].append(attachment)
    else:
        email_data["body"] = msg.get_payload(decode=True).decode(decoding, errors="replace")

    # Convert the email data to JSON
    email_json = json.dumps(email_data, indent=4)
    return email_json


def convert_all_to_json():
    input_folder = "emails"
    output_folder = "email_jsons"
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if filename.endswith(".eml") and os.path.isfile(file_path):
            email_json = eml_to_json(file_path)
            output_filename = f"{os.path.splitext(filename)[0]}.json"
            output_path = os.path.join(output_folder, output_filename)
            with open(output_path, "w", encoding="utf-8") as json_file:
                json_file.write(email_json)

            print(f"Saved JSON for {filename} to {output_filename}")

if __name__ == "__main__":
    eml_file_path = "./id000.eml"
    email_json = eml_to_json(eml_file_path)
    print(email_json)

    convert_all_to_json()
