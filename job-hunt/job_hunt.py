import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime,time
from streamlit_calendar import calendar

from PIL import Image

st.title('就活状況管理アプリ')

with st.expander("使い方はこちら"):
    st.write("""
    1. **記録する**: 企業名・フェーズ・日時を入力して「記録する」をタップ。
    2. **更新する**: 同じ企業名を入れると、古いデータは自動的に最新版へ上書きされます。
    3. **保存する**: 最後に「CSVダウンロード」を押して保存してください。
    """)


if 'job_logs' not in st.session_state:
    st.session_state.job_logs = []

with st.sidebar:
    st.header("データ管理")
    uploaded_file = st.file_uploader('前回のCSVを読み込む', type='csv')
    
    # 読み込み処理を1回だけに限定して高速化
    if uploaded_file is not None and 'last_uploaded' not in st.session_state:
        import_df = pd.read_csv(uploaded_file)
        import_data = import_df.to_dict('records')
        
        current_firms = [log['企業名'] for log in st.session_state.job_logs]
        for new_log in import_data:
            if new_log['企業名'] not in current_firms:
                st.session_state.job_logs.append(new_log)
        
        # 読み込み済みフラグを立てて、何度も読み込まないようにする
        st.session_state.last_uploaded = uploaded_file.name
        st.success("読み込み完了！")
        st.rerun()

else_input = ""
start_time = None
end_time = None


firm_name = st.text_input(
    '企業名を入力'
)

phase_menu = ['説明会','エントリーシート提出','１次選考','2次選考','最終選考','その他']
phase = st.selectbox(
    '現在の状況を選択する',
    phase_menu
)
if phase == 'その他':
    else_input = st.text_input(
        '就活状況を入力'
    )

memo = st.text_input(
    'メモ'
)


if phase == 'エントリーシート提出':
    date = st.date_input(
        '提出期限を入力' ,datetime.now()
    )
    
else:
    label = f"{else_input}の日を入力" if phase == 'その他' else f"{phase}の日を入力"#もしその他ならelse_inputの日を入力と表示、じゃなかったらphraseの日を入力と表示
    date = st.date_input(
        label ,datetime.now(),
    )
    start_time = st.time_input(
        '開始時間を入力',
        time(10,0),step = 900
    )
    end_time = st.time_input(
        '終了時間を入力',
        time(11,0),step = 900
    )

if st.button('この内容で記録する'):
    st.session_state.job_logs = [log for log in st.session_state.job_logs if log['企業名'] != firm_name]
    save_phase = else_input if phase == 'その他' else phase
    if firm_name:
        s_time = start_time.strftime('%H:%M') if start_time else ""#スタートタイムがあったs_time = 
        e_time = end_time.strftime('%H:%M') if end_time else ""

        new_data ={
            '企業名':firm_name,
            '就活状況':phase,
            '予定日':date.strftime('%Y/%m/%d'),
            '開始時間':s_time,
            '終了時間':e_time,
            'メモ':memo
        }
        st.session_state.job_logs.append(new_data)
        st.success(f"{firm_name}の記録を保存しました")
    else:
        st.error('企業名を入力')

if st.session_state.job_logs:
    df = pd.DataFrame(st.session_state.job_logs)
    col_del1, col_del2 = st.columns([1, 2])
    
    with col_del1:
        # 1. 直近の1件を削除（筋トレアプリ風）
        if st.button(' 直近の記録を1件削除'):
            st.session_state.job_logs.pop()
            st.success("最新の記録を削除しました")
            st.rerun()

    with col_del2:
        # 2. 特定の企業を選んで削除
        all_firms = [log['企業名'] for log in st.session_state.job_logs]
        delete_target = st.selectbox('削除する企業を選択', ['選択してください'] + all_firms)
        if st.button('選択した企業を削除'):
            if delete_target != '選択してください':
                st.session_state.job_logs = [log for log in st.session_state.job_logs if log['企業名'] != delete_target]
                st.success(f"{delete_target}のデータを削除しました")
                st.rerun()

    calendar_events = []
    for log in st.session_state.job_logs:
        base_date = log['予定日'].replace('/', '-')
        start_val = f"{base_date}T{log['開始時間']}:00" if log['開始時間'] else base_date#開始時間があったら{base_date}T{log['開始時間']}:00" 、なかったら日にちだけ
        end_val = f"{base_date}T{log['終了時間']}:00" if log['終了時間'] else base_date
        
        calendar_events.append({
            "title": f"{log['企業名']} ({log['就活状況']})",
            "groupId":memo,
            "start": start_val,
            "end": end_val,
            "resourceId": "a",
        })

    # 2. カレンダーの設定
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek"
        },
        "initialView": "dayGridMonth",
        "selectable": True,
    }


    calc_result = calendar(events=calendar_events, options=calendar_options, key="job_calendar")

    if calc_result and "eventClick" in calc_result:
        event_data = calc_result["eventClick"]["event"]
        st.info(f"詳細確認: {event_data['title']}")
        
        clicked_firm = event_data['title'].split(' (')[0]
        
        for log in st.session_state.job_logs:
            if log['企業名'] == clicked_firm:
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**予定日:** {log['予定日']}")
                    st.write(f"**時間:** {log['開始時間']} ~ {log['終了時間']}" if log['開始時間'] else "**時間:** 終日")
                with c2:
                    st.write(f"**メモ:** {log['メモ']}")

    csv = df.to_csv(index=False).encode('utf-8-sig') 

    st.download_button(
        label='記録をCSVでダウンロード',
        data=csv,
        file_name=f"job_hunt_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )


