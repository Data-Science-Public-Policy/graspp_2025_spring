import pandas as pd
import os

def analyze_csv(file_path):
    """
    CSVファイルを分析し、題名とカラム一覧を出力する関数
    """
    # ファイル名を取得
    file_name = os.path.basename(file_path)
    
    # ファイルサイズを取得 (MB)
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    
    print(f"\n{'='*50}")
    print(f"ファイル名: {file_name}")
    print(f"ファイルサイズ: {file_size_mb:.2f} MB")
    print(f"{'='*50}")
    
    # CSVファイルを読み込む（エンコーディングとエラー処理を追加）
    try:
        # まずUTF-8で試す
        df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
    except UnicodeDecodeError:
        # 次にcp932（日本語Windows環境）で試す
        try:
            df = pd.read_csv(file_path, encoding='cp932', on_bad_lines='skip')
        except Exception:
            # それでもダメなら、エンコーディングを推定
            import chardet
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read())
            df = pd.read_csv(file_path, encoding=result['encoding'], on_bad_lines='skip')
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("CSVファイルを最小限の設定で読み込みます")
        df = pd.read_csv(file_path, encoding='utf-8', engine='python', sep=None, on_bad_lines='skip')
    
    # データセットの基本情報
    print("\n【基本情報】")
    print(f"行数: {df.shape[0]}")
    print(f"列数: {df.shape[1]}")
    
    # カラム一覧
    print("\n【カラム一覧】")
    for i, column in enumerate(df.columns, 1):
        print(f"{i}. {column}")
    
    # データセットに固有の列に基づいて題名を推測
    if "Series Name" in df.columns:
        unique_series = df["Series Name"].unique()
        print("\n【データセット内容】")
        print(f"このデータセットには以下の{len(unique_series)}種類の指標が含まれています:")
        for i, series in enumerate(unique_series, 1):
            print(f"{i}. {series}")
    
    # 国または地域の数
    if "Country Name" in df.columns:
        unique_countries = df["Country Name"].unique()
        print(f"\n国/地域の数: {len(unique_countries)}")
    
    # データサンプルを表示
    print("\n【データサンプル】")
    try:
        print(df.head(3).to_string())
    except:
        print(df.head(3))
    
    return df

def main():
    # ファイルパス
    file_path1 = r"C:\Users\kris7\VScode_projects\HW1_NatsukiKonishi\2b63cf6c-2ead-4e13-baab-aa58e0f950ba_Series - Metadata.csv"
    file_path2 = r"C:\Users\kris7\VScode_projects\HW1_NatsukiKonishi\a63b8b46-f6d8-4de1-ac51-7666d978adee_Series - Metadata.csv"
    
    # 各ファイルが存在するか確認
    for path in [file_path1, file_path2]:
        if not os.path.exists(path):
            print(f"エラー: ファイル '{path}' が見つかりません。")
            return
    
    # 各ファイルを分析
    print("\n1つ目のファイルを分析中...")
    df1 = analyze_csv(file_path1)
    
    print("\n2つ目のファイルを分析中...")
    df2 = analyze_csv(file_path2)
    
    print("\n【データ構造の比較】")
    # 両方のデータセットのカラム比較
    df1_cols = set(df1.columns)
    df2_cols = set(df2.columns)
    common_cols = df1_cols.intersection(df2_cols)
    
    print(f"共通のカラム: {', '.join(common_cols)}")
    
    # 共通のカラムがあれば、結合可能性についてアドバイス
    if common_cols:
        print("\n【データ結合の可能性】")
        print("以下の共通カラムをキーとして結合可能です:")
        for col in common_cols:
            print(f"- {col}")
        
        # 国コードや国名がある場合は特に言及
        if "Country Code" in common_cols or "Country Name" in common_cols:
            print("\n国別データとして結合することが推奨されます。")
    
    # 指定されたキーを使用してデータを結合
    # 結合キー
    join_keys = ['Country Name', 'Country Code', 'Series Name', 'Series Code', '2020 [YR2020]']
    
    # 結合前のデータセット識別用に列を追加
    df1['データソース'] = 'データセット1'
    df2['データソース'] = 'データセット2'
    
    # 結合を実行
    print("\n【データ結合の実行】")
    print("指定されたキーを使用してデータを結合します...")
    
    # 結合に使用する実際のキー（両方のデータセットに存在するもののみ）
    valid_keys = [key for key in join_keys if key in common_cols]
    
    if valid_keys:
        print(f"結合に使用するキー: {', '.join(valid_keys)}")
        
        # 結合の実行（outer joinで両方のデータセットのすべての行を保持）
        merged_df = pd.merge(df1, df2, on=valid_keys, how='outer', suffixes=('_dataset1', '_dataset2'))
        
        # 結合結果の基本情報
        print("\n【結合結果】")
        print(f"結合データの行数: {merged_df.shape[0]}")
        print(f"結合データの列数: {merged_df.shape[1]}")
        
        # 結合結果のサンプル
        print("\n【結合データのサンプル】")
        try:
            print(merged_df.head(3).to_string())
        except:
            print(merged_df.head(3))
        
        # 結合結果を保存
        output_path = os.path.join(os.path.dirname(file_path1), "merged_data.csv")
        merged_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n結合データを保存しました: {output_path}")
    else:
        print("指定されたキーが両方のデータセットに存在しないため、結合できません。")

if __name__ == "__main__":
    main()