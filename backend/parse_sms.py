# backend/parse_sms.py
import xml.etree.ElementTree as ET
import re
import pandas as pd
from datetime import datetime

def classify(body):
    body = body.lower()
    if "received" in body:
        return "incoming_money"
    elif "withdrawn" in body:
        return "withdrawal"
    elif "bank deposit" in body:
        return "bank_deposit"
    elif "airtime" in body:
        return "airtime_payment"
    elif "cash power" in body:
        return "cash_power"
    elif "payment of" in body:
        return "payment"
    elif "transferred to" in body:
        return "transfer"
    elif "otp" in body or "one-time password" in body:
        return "otp"
    return "other"

def extract_sms(sms):
    body = sms.attrib.get("body", "")
    tx_type = classify(body)

    amount_match = re.search(r'([0-9,]+)\s*RWF', body)
    amount = int(amount_match.group(1).replace(",", "")) if amount_match else None

    datetime_match = re.search(r'at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', body)
    tx_datetime = datetime_match.group(1) if datetime_match else None

    name_match = re.search(r'from ([\w\s]+) \(|to ([\w\s]+) \d+', body)
    name = name_match.group(1) if name_match and name_match.group(1) else name_match.group(2) if name_match else None

    return {
        "tx_type": tx_type,
        "amount": amount,
        "name": name,
        "datetime": tx_datetime,
        "body": body
    }

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    messages = []

    with open("backend/unprocessed.log", "w") as log:
        for sms in root.findall("sms"):
            data = extract_sms(sms)
            if data["tx_type"] == "other" or data["amount"] is None:
                log.write(data["body"] + "\n")
                continue
            messages.append(data)

    return pd.DataFrame(messages)

if __name__ == "__main__":
    df = parse_xml("data/modified_sms_v2.xml")
    df.to_csv("backend/cleaned_data.csv", index=False)
    print("✅ Done. Cleaned data saved to backend/cleaned_data.csv")

