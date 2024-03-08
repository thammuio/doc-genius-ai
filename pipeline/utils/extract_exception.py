import re

from entities.document import ScrapSchema


class ExtractException:
    EXCEPTION_REs = [{"type": "jdkexception","pat": re.compile(r"(^.*?(?:Exception|Error):.*(?:\n+^\s*at .*)+)",re.MULTILINE)},
                 {"type": "pythonexception", "pat": re.compile(r"Traceback \(most recent call last\):(?:\n.*)+?\n(.*?(?:Exception|Error):)\s*(.+)\n(?:Call stack:\n)?(?:File .*\n.*\n)*",re.MULTILINE)}
                 ]
    no_newline_re = re.compile(r"([^\n ])([ \t]+(?:at|Caused by:)\s+)")
    def extract_exceptions(self, scrap):
        ret = []
        if scrap and scrap.get("scrap_text"):
            for reg in self.EXCEPTION_REs:
                for match in reg["pat"].finditer(scrap["scrap_text"]):
                    text = match.group(0)
                    if len(self.no_newline_re.findall(text))>1:
                        # print(f"found long stack:{text}")
                        text = self.no_newline_re.sub('\\1\n\\2', text)
                        # print(f"replaced: {text}")
                    lines = text.splitlines()
                    if len(lines)>5:
                        new_lines = []
                        n_added = 0
                        for i, line in enumerate(lines):
                            if line.find("Caused by:")>-1:
                                n_added = 0
                            if n_added<3:
                                new_lines.append(line)
                                n_added += 1
                        for i in range(len(lines)-3,len(lines)):
                            new_lines.append(lines[i])
                        text = '\n'.join(new_lines)

                    scrap = ScrapSchema().load({"doc_id": scrap.get("doc_id"),
                                                "type_name": "meta-"+ reg["type"],
                                                "scrap_text": text,
                                                "created_at": scrap.get("created_at"),
                                                "updated_at": scrap.get("updated_at")
                                                })
                    ret.append(scrap)
        return ret