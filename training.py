import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime 

from PIL import Image

st.title('筋トレメニュー管理アプリ')


if 'training_logs' not in st.session_state:
    st.session_state.training_logs = []

st.write('部位の選択')

options = ['胸','背中','二頭筋','三頭筋','肩','足']
target_point = st.selectbox(#部位選択
    '鍛える部位を選択',
    options
)


menu_list = []
if target_point == '胸':#胸のメニュー選択
    menu_list = ['ベンチプレス','インクラインベンチプレス','ダンベルフライ','チェストプレス','ペックフライ']

elif target_point == '背中':#胸のメニュー選択
    menu_list = ['懸垂','ハイプーリー','ロープーリー','シーデットロー','ワンハンドローイング','デッドリフト']

elif target_point == '二頭筋':#二頭のメニュー選択
    menu_list = ['バーベルカール','EZバーカール','ダンベルカール','インクラインカール','ハンマーカール','プリチャーカール']

elif target_point == '三頭筋':#三頭のメニュー選択
    menu_list = ['ナローベンチ','スカルクラッシャー','ケーブルプレスダウン','ディップス']

elif target_point == '肩':#肩のメニュー選択
    menu_list = ['ショルダープレス','フロントレイズ','サイドレイズ','リアレイズ','スミスショルダープレス','アップライトロウ']

else :
    menu_list = ['スミススクワット','レッグエクステンション','レッグカール','レッグプレス','ブルガリアンスクワット']

selected_menu = st.selectbox('メニュー選択',menu_list+['その他'])

if selected_menu == 'その他':
    selected_menu = st.text_input('種目名')


left_column,right_column = st.columns(2)
with left_column:
    weight = st.number_input(
        '重さ入力',
        1,
        200,
        1,
        1
    )


with right_column:
    reps = st.number_input(
        '回数入力',
        1,
        30,
        1,
        1
    )

st.title('インターバルタイマー')

rest_time = st.number_input(
    '休憩時間',
    1,
    300,
    30,
    10
)

if st.button('セット終わり！タイマースタート'):
    new_entry = {
        '部位':target_point,
        '種目':selected_menu,
        '重さ':weight,
        '回数':reps,
    }
    st.session_state.training_logs.append(new_entry)

    st.success(f'記録完了:{selected_menu}{weight}kg * {reps}回')

    latest_interation = st.empty() #空の要素
    bar = st.progress(1)

    for i  in range(rest_time + 1):
        latest_interation.text(f'残り{rest_time-i}秒')
        bar.progress((rest_time-i)/rest_time) #進捗バー
        time.sleep(1) #0.秒静止して次に行く←これがないと進まん
st.write('休憩終わり！')

if st.session_state.training_logs:
    if st.button('前の記録を削除'):
        st.session_state.training_logs.pop()
        st.rerun()
    

    df = pd.DataFrame(st.session_state.training_logs)
    df['日付'] = datetime.now().strftime('%Y/%m/%d')
    df = df[['日付','部位','種目','重さ','回数']]
    st.table(df)

    uploaded_file = st.file_uploader('前回保存したファイルを選択')

    if uploaded_file is not None:
        old_df = pd.read_csv(uploaded_file)
        final_df = pd.concat([old_df,df],ignore_index = True)
    else:
        final_df = df


    csv = final_df.to_csv(index = False,mode = 'a',encoding='utf_8_sig').encode('utf_8_sig')

    st.download_button(
        label = '記録をダウンロード',
        data = csv,
        file_name=f"workout_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )

else:
    st.write("記録なし。トレーニングしよう")