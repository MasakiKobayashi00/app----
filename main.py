import streamlit as st
import numpy as np
import pandas as pd

from PIL import Image #画像使うときいる

st.title('streamlit入門')

st.write('data frame')#テキスト

df = pd.DataFrame({
    '1列目':[1,2,3,4],
    '2列目':[10,20,30,40]

})

st.dataframe(df.style.highlight_max(axis = 0))#axis= 0は行、1は列を蛍光に
#st.dataframeは動的、ウェブ上で動かせる
st.table(df.style.highlight_max(axis = 0))#axis= 0は行、1は列を蛍光に
#st.tableはstatic(静的)


#マジックコマンド(テキストの書き方)
"""
#章
##節
###項

```python
import streamlit as st
import numpy as np
import pandas as pd
```

"""

#チャートの書き方

graph = pd.DataFrame(
    np.random.rand(20,3),#ランダム20*3
    columns = ['a','b','c']#行列生成
)
st.line_chart(graph)#折れ線
st.area_chart(graph)#色塗り
st.bar_chart(graph)#棒グラフ

map = pd.DataFrame(
    np.random.rand(100,2)/[50,50] + [35.69,139.70],#ランダム20*3 /50,50] + [35.69,139.70]は東京付近の座標
    columns = ['lat','lon']#行列生成   緯度経度
)

st.map(map)#地図描画

st.write('Display Image')

img = Image.open('anpanman.jpg')
st.image(img,caption='anpanman',use_container_width = True)#use_container_width = Trueは実際のレイアウトの横幅に合わせる

st.write('Interactive Widgets')
if st.checkbox('画像を表示する'): #チェックボックスの作成
    img = Image.open('anpanman.jpg')
    st.image(img,caption='anpanman',use_container_width = True)#use_container_width = Trueは実際のレイアウトの横幅に合わせる

option = st.selectbox( #セレクトボックスの作成
    'あなたが好きな数字を教えてください',#ラベル
    list(range(1,11))#１から１１の配列
)

'あなたが好きな数字は',option,'です。'

text = st.text_input('あなたの趣味を教えてください')#テキストボックスの作成
'あなたの趣味は',text,'です。'

condision = st.slider('あなたの今の調子は？',0,100,50)#スライダーによる値の動的変化(最小,最大,初期値)
'コンディション',condision
    
#レイアウトを整える(サイドバー)
text = st.sidebar.text_input('今日の種目を教えてください')#テキストボックスの作成 st.sidebarでサイドバー表示
'今日の種目は',text
condision = st.sidebar.slider('何キロ上げましたか？',0,100,50)#スライダーによる値の動的変化(最小,最大,初期値)
condision,'kg'
    
#レイアウトを整える(２カラムレイアウト)
left_column,right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')#.buttonはボタン,左カラムはボタン
if button:
    right_column.write('ここは右カラム')#右カラムはテキスト

#レイアウトを整える(エキスパンダー)
expander = st.expander('問い合わせ')  
expander.write('問い合わせ内容を書く')
expander1 = st.expander('問い合わせ1')
expander1.text_input('問い合わせ1を書く')

#プログレスバーの表示
st.write('プログレスバーの表示')
'Start!'

latest_interation = st.empty() #空の要素
bar = st.progress(0)

import time 

for i in range(100):
    latest_interation.text(f'Iteration{i+1}')
    bar.progress(i + 1) #進捗バー
    time.sleep(0.1) #0.秒静止して次に行く←これがないと進まん

'Done!!!'#for文が回り終わったら下のコードが表示

