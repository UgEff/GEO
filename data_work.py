import pandas as pd


class DataWork:
    def __init__(self,file_path):
        self.file_path = file_path

    def read_json(self):
        with open(self.file_path, "r") as f:
            data = json.load(f)
        return data
    
    def converte_to_df(self):
        data = self.read_json()
        df = pd.DataFrame(data)
        return df
    
    def save_to_excel(self,df,file_path):
        df.to_excel(file_path, index=False)
    

if __name__ == "__main__":
    file_path = "json_prd/sportcomplex_prd.json"
    



