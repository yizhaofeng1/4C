import pandas as pd
def clean_csv(file_path, output_path):
    try:
        df = pd.read_csv(file_path)
        df = df.drop_duplicates(subset='name', keep='first')
        df.to_csv(output_path, index=False,encoding="utf-8-sig")
        print(f"清洗后的数据已保存到 {output_path}")
    except FileNotFoundError:
        print("错误：文件未找到！")
    except Exception as e:
        print(f"错误：发生了一个未知错误：{e}")
if __name__ == "__main__":
    input_file_path = 'shanhaijin.csv'
    output_file_path = 'shanhaijin.csv'
    clean_csv(input_file_path, output_file_path)
