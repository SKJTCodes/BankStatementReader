import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd


class RF:
    def __init__(self, folder_path):
        self.path = Path(folder_path).absolute()

        assert self.path.is_dir(), f"{self.path} is not a folder."

    def read(self, template=None):
        """

        :param template:
        {
            <Bank Name>: {
                "credit": {
                    "regex": "any regex string to identify all files related to this bank.",
                    # https://www.geeksforgeeks.org/python-datetime-strptime-function/
                    "date": "datetime identifier to break down date from file name if any."
                },
                "debit": {}
            }
        }
        :return:
        """
        if template is None:
            template = {
                "OCBC": {
                    "credit": {
                        "regex": r"OCBC 365 CREDIT CARD-\d{4}-[a-zA-Z]{3}-\d{2}.pdf",
                        "date": "OCBC 365 CREDIT CARD-****-%b-%y.pdf"
                    },
                    "debit": {
                        "regex": r"360 ACCOUNT-\d{4}-[a-zA-Z]{3}-\d{2}.pdf",
                        "date": "360 ACCOUNT-****-%b-%y.pdf"
                    }
                }
            }
        else:
            tmp_path = Path(template)
            assert tmp_path.is_file(), f"Template path is not a file. Path: {tmp_path.absolute()}"

            with open(tmp_path, "r") as file:
                template = json.loads(file.read())
                print(template)

        out_data = []
        for d in self.path.iterdir():
            if d.suffix != ".pdf":
                continue

            for bank_name, bank_info in template.items():
                for trans_type, trans_arr in bank_info.items():
                    for trans_info in trans_arr:
                        regex, date_format = trans_info["regex"], trans_info["date"]
                        if re.match(regex, d.name):
                            out_data.append({
                                "bank": bank_name,
                                "trans_type": trans_type,
                                "date": datetime.strptime(d.name, date_format),
                                "f_path": d.absolute()
                            })
        return pd.DataFrame(out_data)
