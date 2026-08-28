import streamlit as st
import math
import streamlit.components.v1 as components
import urllib.parse

# --- မျှော်မှန်းဂိုး (xG) တွက်ချက်သည့် ဖော်မြူလာ ---
def calculate_advanced_xg(avg_goals, big_chance, sot, corners, pos, own_h2h_wins, opp_h2h_wins):
    # DA နေရာတွင် Possession (pos) ကို အစားထိုး အသုံးပြုထားပါသည်
    base_xg = (avg_goals * 0.35) + (big_chance * 0.25) + (sot * 0.1) + (corners * 0.03) + (pos * 0.003)
    h2h_diff = own_h2h_wins - opp_h2h_wins
    h2h_modifier = h2h_diff * 0.05
    final_xg = max(0.1, base_xg + h2h_modifier)
    return round(final_xg, 2)

def poisson_probability(xg, goals):
    return round(((math.exp(-xg) * (xg ** goals)) / math.factorial(goals)) * 100, 2)

# ==========================================
# Translation Dictionary
# ==========================================
text = {
    "မြန်မာ": {
        "menu_title": "🛠️ စနစ်များ",
        "menu_1": "📊 ရလဒ်ခန့်မှန်းရန်",
        "menu_2": "📝 ပျမ်းမျှဒေတာ တွက်ချက်ရန်",
        "menu_3": "🌐 တိုက်ရိုက်ဂိုးရလဒ်နဲ့ဒေတာများရယူရန်",
        "p1_title": "⚽ Football Master Pro",
        "p1_desc": "ဤ App သည် ဘောလုံးအသင်းများ၏ အရေးကြီးသော ပျမ်းမျှဒေတာများကို ပေါင်းစပ်တွက်ချက်ပြီး ရလဒ်ခန့်မှန်းပေးသော App ဖြစ်ပါသည်။",
        "team_a_header": "🏠 အိမ်ကွင်းအသင်း",
        "team_b_header": "✈️ အဝေးကွင်းအသင်း",
        "team_a_name": "အိမ်ကွင်း",
        "team_b_name": "အဝေးကွင်း",
        "avg_goals": "ပျမ်းမျှသွင်းဂိုး",
        "bc": "အပိုင်အခွင့်အရေး",
        "sot": "ဂိုးပေါက်တည့်မှု",
        "cor": "ထောင့်ကန်ဘော",
        "pos": "ဘောလုံးပိုင်ဆိုင်မှု (%)",
        "h2h": "ထိပ်တိုက်တွေ့ဆုံမှု နိုင်ပွဲ",
        "btn_calc": "📊 ရလဒ် တွက်ချက်မည်",
        "xg_res": "🎯 မျှော်မှန်းဂိုး (xG) :",
        "prob_title": "⚽ ဂိုးရနိုင်ခြေ ရာခိုင်နှုန်းများ",
        "top_scores": "🏆 အဖြစ်နိုင်ဆုံး ဂိုးရလဒ်များ (ထိပ်ဆုံး ၃ ခု)",
        "p2_title": "📝 ပျမ်းမျှဒေတာ တွက်ချက်ခြင်း",
        "btn_avg": "ပျမ်းမျှဒေတာ တွက်မည်",
        "p3_title": "🌐 တိုက်ရိုက်ဂိုးရလဒ်နဲ့ဒေတာများရယူရန်",
        "p3_desc": "ယနေ့ကစားမည့် တိုက်ရိုက်ပွဲစဉ်များကို ကြည့်ရှုနိုင်ပြီး၊ အသင်းများ၏ အသေးစိတ် Data ကိုလည်း အလွယ်တကူ ရှာဖွေကြည့်ရှုနိုင်ပါသည်။",
        "warning": "⚠️ **သတိပေးချက်** - ဤ App သည် သင်္ချာနည်းကျ ဒေတာခန့်မှန်းတွက်ချက်မှု သက်သက်သာ ဖြစ်ပါသည်။ လောင်းကစားပြုလုပ်ရန်အတွက် အသုံးပြုမည်ဆိုပါက သေချာသော ငွေကြေးစီမံခန့်ခွဲမှု ပြုလုပ်ရန် တိုက်တွန်းအပ်ပါသည်။"
    },
    "English": {
        "menu_title": "🛠️ Tools",
        "menu_1": "📊 Predictor",
        "menu_2": "📝 Data Calculator",
        "menu_3": "🌐 Live Scores & Fetch Data",
        "p1_title": "⚽ Football Master Pro",
        "p1_desc": "This app predicts results by calculating and combining important average data of football teams.",
        "team_a_header": "🏠 Home Team",
        "team_b_header": "✈️ Away Team",
        "team_a_name": "Home",
        "team_b_name": "Away",
        "avg_goals": "Average Goals",
        "bc": "Big Chances",
        "sot": "Shots on Target",
        "cor": "Corners",
        "pos": "Possession (%)",
        "h2h": "H2H Wins",
        "btn_calc": "📊 Calculate Result",
        "xg_res": "🎯 Expected Goals (xG):",
        "prob_title": "⚽ Goal Probabilities",
        "top_scores": "🏆 Top 3 Most Likely Correct Scores",
        "p2_title": "📝 Data Calculator (Averages)",
        "btn_avg": "Calculate Averages",
        "p3_title": "🌐 Live Scores & Fetch Data",
        "p3_desc": "View today's live matches and easily generate quick links to find detailed team statistics.",
        "warning": "⚠️ **DISCLAIMER:** This app provides purely mathematical estimations. Strict bankroll management is recommended if used for betting."
    }
}

# ==========================================
# Web App UI & Sidebar Navigation
# ==========================================
st.set_page_config(page_title="Football Master Pro", layout="wide")

lang = st.sidebar.selectbox("🌐 Language / ဘာသာစကား", ["မြန်မာ", "English"])
t = text[lang]

st.sidebar.title(t["menu_title"])
menu = st.sidebar.radio("", [t["menu_1"], t["menu_2"], t["menu_3"]])

st.sidebar.divider()
st.sidebar.warning(t["warning"])

# ---------------------------------------------------------
# စာမျက်နှာ ၁ - Predictor
# ---------------------------------------------------------
if menu == t["menu_1"]:
    st.title(t["p1_title"])
    st.markdown(t["p1_desc"])
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.header(t["team_a_header"])
        a_avg_goals = st.number_input(f"{t['team_a_name']} - {t['avg_goals']}", min_value=0.0, value=1.50, step=0.01, format="%.2f")
        a_big_chance = st.number_input(f"{t['team_a_name']} - {t['bc']}", min_value=0.0, value=2.00, step=0.01, format="%.2f")
        a_sot = st.number_input(f"{t['team_a_name']} - {t['sot']}", min_value=0.0, value=5.00, step=0.01, format="%.2f")
        a_corners = st.number_input(f"{t['team_a_name']} - {t['cor']}", min_value=0.0, value=6.00, step=0.01, format="%.2f")
        # Possession ကို ၅၀% ဟု Default ပေးထားသည်
        a_pos = st.number_input(f"{t['team_a_name']} - {t['pos']}", min_value=0.0, value=50.00, step=0.01, format="%.2f")
        a_h2h = st.number_input(f"{t['team_a_name']} - {t['h2h']}", min_value=0.0, value=2.00, step=0.01, format="%.2f")

    with col2:
        st.header(t["team_b_header"])
        b_avg_goals = st.number_input(f"{t['team_b_name']} - {t['avg_goals']}", min_value=0.0, value=1.20, step=0.01, format="%.2f")
        b_big_chance = st.number_input(f"{t['team_b_name']} - {t['bc']}", min_value=0.0, value=1.00, step=0.01, format="%.2f")
        b_sot = st.number_input(f"{t['team_b_name']} - {t['sot']}", min_value=0.0, value=3.00, step=0.01, format="%.2f")
        b_corners = st.number_input(f"{t['team_b_name']} - {t['cor']}", min_value=0.0, value=4.00, step=0.01, format="%.2f")
        # Possession ကို ၅၀% ဟု Default ပေးထားသည်
        b_pos = st.number_input(f"{t['team_b_name']} - {t['pos']}", min_value=0.0, value=50.00, step=0.01, format="%.2f")
        b_h2h = st.number_input(f"{t['team_b_name']} - {t['h2h']}", min_value=0.0, value=1.00, step=0.01, format="%.2f")

    st.divider()

    if st.button(t["btn_calc"], type="primary"):
        a_xg = calculate_advanced_xg(a_avg_goals, a_big_chance, a_sot, a_corners, a_pos, a_h2h, b_h2h)
        b_xg = calculate_advanced_xg(b_avg_goals, b_big_chance, b_sot, b_corners, b_pos, b_h2h, a_h2h)
        
        st.success(f"{t['xg_res']} {t['team_a_name']} (**{a_xg}**) vs (**{b_xg}**) {t['team_b_name']}")
        
        st.subheader(t["prob_title"])
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            for i in range(4): st.write(f"- **{i}** ဂိုး: {poisson_probability(a_xg, i)}%")
        with res_col2:
            for i in range(4): st.write(f"- **{i}** ဂိုး: {poisson_probability(b_xg, i)}%")
            
        st.divider()
        st.subheader(t["top_scores"])
        
        scores = []
        for a_goals in range(4):
            for b_goals in range(4):
                prob_a = poisson_probability(a_xg, a_goals) / 100
                prob_b = poisson_probability(b_xg, b_goals) / 100
                total_prob = round(prob_a * prob_b * 100, 2)
                scores.append({"score": f"{t['team_a_name']} ({a_goals} - {b_goals}) {t['team_b_name']}", "probability": total_prob})
        
        sorted_scores = sorted(scores, key=lambda x: x['probability'], reverse=True)
        for idx in range(3):
            st.info(f"**{idx+1}**. {sorted_scores[idx]['score']} : **{sorted_scores[idx]['probability']}%**")

# ---------------------------------------------------------
# စာမျက်နှာ ၂ - Data Calculator (Manual)
# ---------------------------------------------------------
elif menu == t["menu_2"]:
    st.title(t["p2_title"])
    matches = st.number_input("Matches / ပွဲအရေအတွက်", min_value=1, max_value=20, value=5)
    
    total_goals, total_bc, total_sot, total_corners, total_pos = 0.0, 0.0, 0.0, 0.0, 0.0
    for i in range(matches):
        with st.expander(f"Match / ပွဲစဉ် {i+1}"):
            c1, c2, c3, c4, c5 = st.columns(5)
            total_goals += c1.number_input("Goals", value=0.0, step=0.01, format="%.2f", key=f"g_{i}")
            total_bc += c2.number_input("Big Chances", value=0.0, step=0.01, format="%.2f", key=f"bc_{i}")
            total_sot += c3.number_input("SoT", value=0.0, step=0.01, format="%.2f", key=f"sot_{i}")
            total_corners += c4.number_input("Corners", value=0.0, step=0.01, format="%.2f", key=f"c_{i}")
            total_pos += c5.number_input("Possession (%)", value=0.0, step=0.01, format="%.2f", key=f"pos_{i}")

    if st.button(t["btn_avg"], type="primary"):
        st.success("✅ Success / ပြီးစီးပါပြီ")
        r1, r2, r3, r4, r5 = st.columns(5)
        r1.metric("Avg Goals", f"{total_goals / matches:.2f}")
        r2.metric("Avg BC", f"{total_bc / matches:.2f}")
        r3.metric("Avg SoT", f"{total_sot / matches:.2f}")
        r4.metric("Avg Corners", f"{total_corners / matches:.2f}")
        r5.metric("Avg Possession", f"{total_pos / matches:.2f}")

# ---------------------------------------------------------
# စာမျက်နှာ ၃ - Live Scores & Quick Search Links
# ---------------------------------------------------------
elif menu == t["menu_3"]:
    st.title(t["p3_title"])
    st.markdown(t["p3_desc"])
    
    st.subheader("1️⃣ အသင်းများ၏ အသေးစိတ် Data ကို ရှာရန်")
    team_search = st.text_input("🔍 အသင်းနာမည် ရိုက်ထည့်ပါ (ဥပမာ - Arsenal, Chelsea, Real Madrid)")
    
    if st.button("ရှာဖွေရန်လင့်ခ်များ ထုတ်ပေးပါ", type="primary") and team_search:
        encoded_team = urllib.parse.quote(team_search)
        st.info(f"**{team_search}** ၏ Data များကို အောက်ပါ ဝက်ဘ်ဆိုက်များတွင် အလွယ်တကူ နှိပ်၍ ကြည့်နိုင်ပါသည် -")
        
        link1, link2, link3 = st.columns(3)
        with link1:
            st.markdown(f"[📊 **Sofascore** တွင်ရှာရန်](https://www.sofascore.com/search?q={encoded_team})")
            st.caption("(Data အစုံဆုံးနှင့် ကြည့်ရအလွယ်ဆုံး)")
        with link2:
            st.markdown(f"[📈 **FotMob** တွင်ရှာရန်](https://www.fotmob.com/search?q={encoded_team})")
            st.caption("(Big Chances ရှာရန် ကောင်းမွန်သည်)")
        with link3:
            st.markdown(f"[⚽ **Flashscore** တွင်ရှာရန်](https://www.flashscore.com/search/?q={encoded_team})")
            st.caption("(Live Scores အတွက် ကောင်းမွန်သည်)")
            
    st.divider()
    st.subheader("2️⃣ 🔴 Live Scores (တိုက်ရိုက်ပွဲစဉ်များ)")
    components.iframe("https://www.scorebat.com/embed/livescore/", height=700, scrolling=True)