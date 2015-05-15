import win32com.client

class Sapi5Handler:
    def __init__(self):
        print(dir(win32com.win32com))
        self.recognizer = win32com.client.Dispatch("SAPI.ISpRecognizer")
        x = self.recognizer.CreateRecoContext()
        x.OnPhraseStart = self.get_lines

    def get_lines(self):
        return []
        # lines = utilities.get_buffer_lines(self.shared_dir)
        # for line in lines:
        #     if self.filter_on:
        #         line = self.filter_duplicate_letters(line)
        #     yield line
