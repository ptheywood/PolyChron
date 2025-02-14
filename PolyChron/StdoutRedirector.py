import re


class StdoutRedirector(object):
    def __init__(self, text_area, pb1):
        """allows us to rimedirect
        output to the app canvases"""
        self.text_area = text_area
        self.pb1 = pb1

    def write(self, str):
        """writes to canvas"""
        #     self.text_area.update_idletasks()
        self.pb1.update_idletasks
        # self.text_area.destroy()
        str1 = re.findall(r"\d+", str)
        if len(str1) != 0:
            self.text_area["text"] = str1[0] + "% complete"
            self.pb1["value"] = int(str1[0])
            self.text_area.update_idletasks()
        #  self.text_area.see(1.0)

    def flush(self):
        pass
