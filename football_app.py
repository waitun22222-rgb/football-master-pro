import streamlit as st
import math
import streamlit.components.v1 as components
import urllib.parse
import tempfile
import os
from fpdf import FPDF

# ==========================================
# ဘာသာစကား ဒေတာများ (Translation Dictionary)
# ==========================================
text = {
    "မြန်မာ": {
        "menu_title": "🛠️ စနစ်များ",
        "menu_1": "📊 ရလဒ်ခန့်မှန်းရန်",
        "menu_2": "📝 ပျမ်းမျှဒေတာ တွက်ချက်ရန်",
        "menu_3": "🌐 တိုက်ရိုက်ဂိုးရလဒ်နဲ့ဒေတာများရယူရန်",
        "p1_title": "⚽ Football Master Pro",
        "p1_desc": "ဤ App သည် ဘောလုံးအသင်းများ၏ အရေးကြီးသော ပျမ်းမျှဒေတာများကို ပေါင်းစပ်တွက်ချက်ပြီး ရလဒ်နှင့် ပေါက်ကြေးများကို ခန့်မှန်းပေးသော App ဖြစ်ပါသည်။",
        "team_a_header": "🏠 အိမ်ကွင်းအသင်း",
        "team_b_header": "✈️ အဝေးကွင်းအသင်း",
        "team_a_name": "အိမ်ကွင်းအမည်",
        "team_b_name": "အဝေးကွင်းအမည်",
        "home_default": "Home",
        "away_default": "Away",
        "avg_goals": "ပျမ်းမျှသွင်းဂိုး",
        "bc": "အပိုင်အခွင့်အရေး",
        "sot": "ဂိုးပေါက်တည့်မှု",
        "cor": "ထောင့်ကန်ဘော",
        "pos": "ဘောလုံးပိုင်ဆိုင်မှု (%)",
        "h2h_header": "🤝 ထိပ်တိုက်တွေ့ဆုံမှု ရလဒ်များ (H2H)",
        "h2h_wins": "နိုင်ပွဲ",
        "h2h_draws": "သရေပွဲ (Draws)",
        "btn_calc": "📊 ရလဒ် တွက်ချက်မည်",
        "xg_res": "🎯 မျှော်မှန်းဂိုး (xG) :",
        "odds_pred": "📈 ပေါက်ကြေး ခန့်မှန်းချက်",
        "prob_title": "⚽ ဂိုးရနိုင်ခြေ ရာခိုင်နှုန်းများ",
        "top_scores": "🏆 အဖြစ်နိုင်ဆုံး ဂိုးရလဒ်များ (ထိပ်ဆုံး ၃ ခု)",
        "pdf_btn": "📄 PDF ရလဒ်ဖိုင် ဒေါင်းလုဒ်လုပ်ရန်",
        "p2_title": "📝 ပျမ်းမျှဒေတာ တွက်ချက်ခြင်း",
        "matches_input": "Matches / ပွဲအရေအတွက်",
        "match_exp": "Match / ပွဲစဉ်",
        "btn_avg": "ပျမ်းမျှဒေတာ တွက်မည်",
        "success_msg": "✅ Success / ပြီးစီးပါပြီ",
        "p3_title": "🌐 တိုက်ရိုက်ဂိုးရလဒ်နဲ့ဒေတာများရယူရန်",
        "p3_sub1": "1️⃣ အသင်းများ၏ အသေးစိတ် Data ကို ရှာရန်",
        "search_label": "🔍 အသင်းနာမည် ရိုက်ထည့်ပါ (ဥပမာ - Arsenal, Chelsea)",
        "btn_search": "ရှာဖွေရန်လင့်ခ်များ ထုတ်ပေးပါ",
        "search_res": "၏ Data များကို အောက်ပါ ဝက်ဘ်ဆိုက်များတွင် အလွယ်တကူ နှိပ်၍ ကြည့်နိုင်ပါသည် -",
        "p3_sub2": "2️⃣ 🔴 Live Scores (တိုက်ရိုက်ပွဲစဉ်များ)",
        "warning": "⚠️ **သတိပေးချက်** - ဤ App သည် သင်္ချာနည်းကျ ဒေတာခန့်မှန်းတွက်ချက်မှု သက်သက်သာ ဖြစ်ပါသည်။ လောင်းကစားပြုလုပ်ရန်အတွက် အသုံးပြုမည်ဆိုပါက သေချာသော ငွေကြေးစီမံခန့်ခွဲမှု ပြုလုပ်ရန် တိုက်တွန်းအပ်ပါသည်။"
    },
    "English": {
        "menu_title": "🛠️ Tools",
        "menu_1": "📊 Predict Result",
        "menu_2": "📝 Calculate Averages",
        "menu_3": "🌐 Live Scores & Fetch Data",
        "p1_title": "⚽ Football Master Pro",
        "p1_desc": "This app predicts the match result and betting odds by calculating key average statistics.",
        "team_a_header": "🏠 Home Team",
        "team_b_header": "✈️ Away Team",
        "team_a_name": "Home Team Name",
        "team_b_name": "Away Team Name",
        "home_default": "Home",
        "away_default": "Away",
        "avg_goals": "Average Goals",
        "bc": "Big Chances",
        "sot": "Shots on Target",
        "cor": "Corners",
        "pos": "Possession (%)",
        "h2h_header": "🤝 Head-to-Head Results (H2H)",
        "h2h_wins": "Wins",
        "h2h_draws": "Draws",
        "btn_calc": "📊 Calculate Result",
        "xg_res": "🎯 Expected Goals (xG) :",
        "odds_pred": "📈 Predicted Betting Odds",
        "prob_title": "⚽ Goal Probabilities",
        "top_scores": "🏆 Top 3 Most Likely Scores",
        "pdf_btn": "📄 Download PDF Report",
        "p2_title": "📝 Data Calculator (Averages)",
        "matches_input": "Number of Matches",
        "match_exp": "Match",
        "btn_avg": "Calculate Averages",
        "success_msg": "✅ Calculation Successful",
        "p3_title": "🌐 Live Scores & Fetch Data",
        "p3_sub1": "1️⃣ Find Detailed Team Data",
        "search_label": "🔍 Enter Team Name (e.g. Arsenal, Chelsea)",
        "btn_search": "Generate Search Links",
        "search_res": "data can be viewed easily via the following websites:",
        "p3_sub2": "2️⃣ 🔴 Live Scores",
        "warning": "⚠️ **DISCLAIMER:** This app provides purely mathematical estimations. Strict bankroll management is recommended if used for betting."
    }
}

# --- မျှော်မှန်းဂိုး (xG) တွက်ချက်သည့် ဖော်မြူလာ ---
def calculate_advanced_xg(avg_goals, big_chance, sot, corners, pos, own_h2h_wins, opp_h2h_wins, h2h_draws):
    base_xg = (avg_goals * 0.6) + (big_chance * 0.15) + (sot * 0.05) + (corners * 0.02) + ((pos - 50) * 0.005)
    h2h_diff = own_h2h_wins - opp_h2h_wins
    h2h_modifier = (h2h_diff * 0.05) / (1 + (h2h_draws * 0.2))
    final_xg = max(0.1, base_xg + h2h_modifier)
    return round(final_xg, 2)

def poisson_probability(xg, goals):
    return round(((math.exp(-xg) * (xg ** goals)) / math.factorial(goals)) * 100, 2)

# --- ပေါက်ကြေး တွက်ချက်သည့် ဖော်မြူလာ ---
def format_handicap(diff):
    w = int(math.floor(diff))
    f = diff - w
    if f == 0.0: return f"{w} =" if w > 0 else "="
    elif f == 0.25: return f"{w} - 25" if w > 0 else "- 25"
    elif f == 0.50: return f"{w} + 50" if w > 0 else "+ 50"
    elif f == 0.75: return f"{w+1} - 25"
    return str(diff)

def format_total(total):
    w = int(math.floor(total))
    f = total - w
    if f == 0.0: return f"{w} ="
    elif f == 0.25: return f"{w} + 25"
    elif f == 0.50: return f"{w+1} + 100"  
    elif f == 0.75: return f"{w+1} - 25"   
    return str(total)

def calculate_betting_lines(a_xg, b_xg, team_a, team_b):
    diff = round(abs(a_xg - b_xg) * 4) / 4
    total = (round((a_xg + b_xg) * 4) / 4) - 1.0
    if total < 0.5:
        total = 0.5
        
    fav = "Level" if diff == 0 else (team_a if a_xg > b_xg else team_b)
    ah_str = format_handicap(diff)
    ou_str = format_total(total)
    
    return fav, ah_str, ou_str

# --- PDF ဖန်တီးသည့် စနစ် ---
def create_pdf_report(team_a, team_b, a_xg, b_xg, fav, ah_str, ou_str, top_scores):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Football Master Pro - Prediction Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Match: {team_a} vs {team_b}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Expected Goals (xG): {team_a} ({a_xg}) vs ({b_xg}) {team_b}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Predicted Betting Odds:", ln=True)
    pdf.set_font("Arial", '', 12)
    
    if fav == "Level":
        pdf.cell(200, 10, txt=f"Asian Handicap: {team_a} [ = ] {team_b}", ln=True)
    elif fav == team_a:
        pdf.cell(200, 10, txt=f"Asian Handicap: (*) {team_a} [ {ah_str} ] {team_b}", ln=True)
    else:
        pdf.cell(200, 10, txt=f"Asian Handicap: {team_a} [ {ah_str} ] {team_b} (*)", ln=True)
        
    pdf.cell(200, 10, txt=f"Total Goals: Over [ {ou_str} ] Under", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Top 3 Most Likely Scores:", ln=True)
    pdf.set_font("Arial", '', 12)
    for score in top_scores:
        pdf.cell(200, 10, txt=f"{score['eng_score']} - {score['probability']}%", ln=True)
        
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            pdf_bytes = f.read()
    os.remove(tmp.name)
    return pdf_bytes

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
        team_a = st.text_input(t["team_a_name"], value=t["home_default"])
        a_avg_goals = st.number_input(f"{team_a} - {t['avg_goals']}", min_value=0.0, value=1.50, step=0.01, format="%.2f")
        a_big_chance = st.number_input(f"{team_a} - {t['bc']}", min_value=0.0, value=2.00, step=0.01, format="%.2f")
        a_sot = st.number_input(f"{team_a} - {t['sot']}", min_value=0.0, value=5.00, step=0.01, format="%.2f")
        a_corners = st.number_input(f"{team_a} - {t['cor']}", min_value=0.0, value=6.00, step=0.01, format="%.2f")
        a_pos = st.number_input(f"{team_a} - {t['pos']}", min_value=0.0, value=50.00, step=0.01, format="%.2f")

    with col2:
        st.header(t["team_b_header"])
        team_b = st.text_input(t["team_b_name"], value=t["away_default"])
        b_avg_goals = st.number_input(f"{team_b} - {t['avg_goals']}", min_value=0.0, value=1.20, step=0.01, format="%.2f")
        b_big_chance = st.number_input(f"{team_b} - {t['bc']}", min_value=0.0, value=1.00, step=0.01, format="%.2f")
        b_sot = st.number_input(f"{team_b} - {t['sot']}", min_value=0.0, value=3.00, step=0.01, format="%.2f")
        b_corners = st.number_input(f"{team_b} - {t['cor']}", min_value=0.0, value=4.00, step=0.01, format="%.2f")
        b_pos = st.number_input(f"{team_b} - {t['pos']}", min_value=0.0, value=50.00, step=0.01, format="%.2f")

    st.divider()
    
    st.header(t["h2h_header"])
    h2h_1, h2h_2, h2h_3 = st.columns(3)
    with h2h_1:
        a_h2h = st.number_input(f"{team_a} {t['h2h_wins']}", min_value=0.0, value=2.00, step=1.0, format="%.2f")
    with h2h_2:
        h2h_draws = st.number_input(t["h2h_draws"], min_value=0.0, value=1.00, step=1.0, format="%.2f")
    with h2h_3:
        b_h2h = st.number_input(f"{team_b} {t['h2h_wins']}", min_value=0.0, value=1.00, step=1.0, format="%.2f")
        
    st.divider()

    if st.button(t["btn_calc"], type="primary"):
        a_xg = calculate_advanced_xg(a_avg_goals, a_big_chance, a_sot, a_corners, a_pos, a_h2h, b_h2h, h2h_draws)
        b_xg = calculate_advanced_xg(b_avg_goals, b_big_chance, b_sot, b_corners, b_pos, b_h2h, a_h2h, h2h_draws)
        
        st.success(f"{t['xg_res']} {team_a} (**{a_xg}**) vs (**{b_xg}**) {team_b}")
        
        fav, ah_str, ou_str = calculate_betting_lines(a_xg, b_xg, team_a, team_b)
        
        st.markdown(f"### {t['odds_pred']}")
        a_color = "#39ff14" if fav == team_a else "white"
        b_color = "#39ff14" if fav == team_b else "white"
        if fav == "Level": a_color = b_color = "white"

        st.markdown(
            f"""
            <div style="background-color: #444444; padding: 15px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #777;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px; font-size: 18px;">
                    <div style="width: 40%; text-align: left; color: {a_color};">
                        {'★ ' if fav == team_a else ''}{team_a}
                    </div>
                    <div style="width: 20%; text-align: center; color: #ffcc00; font-weight: bold;">
                        {ah_str}
                    </div>
                    <div style="width: 40%; text-align: right; color: {b_color};">
                        {team_b}{' ★' if fav == team_b else ''}
                    </div>
                </div>
                <hr style="border-top: 1px dashed #777; margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; font-size: 18px;">
                    <div style="width: 40%; text-align: left; color: white;">
                        Over
                    </div>
                    <div style="width: 20%; text-align: center; color: #ffcc00; font-weight: bold;">
                        {ou_str}
                    </div>
                    <div style="width: 40%; text-align: right; color: white;">
                        Under
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        
        st.divider()
        st.subheader(t["prob_title"])
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            for i in range(4): st.write(f"- **{i}** Goals: {poisson_probability(a_xg, i)}%")
        with res_col2:
            for i in range(4): st.write(f"- **{i}** Goals: {poisson_probability(b_xg, i)}%")
            
        st.divider()
        st.subheader(t["top_scores"])
        
        scores = []
        for a_goals in range(4):
            for b_goals in range(4):
                prob_a = poisson_probability(a_xg, a_goals) / 100
                prob_b = poisson_probability(b_xg, b_goals) / 100
                total_prob = round(prob_a * prob_b * 100, 2)
                scores.append({
                    "score": f"{team_a} ({a_goals} - {b_goals}) {team_b}", 
                    "eng_score": f"{team_a} {a_goals}-{b_goals} {team_b}",
                    "probability": total_prob
                })
        
        sorted_scores = sorted(scores, key=lambda x: x['probability'], reverse=True)
        top_3 = sorted_scores[:3]
        for idx in range(3):
            st.info(f"**{idx+1}**. {top_3[idx]['score']} : **{top_3[idx]['probability']}%**")
            
        pdf_bytes = create_pdf_report(team_a, team_b, a_xg, b_xg, fav, ah_str, ou_str, top_3)
        st.download_button(
            label=t["pdf_btn"],
            data=pdf_bytes,
            file_name=f"Prediction_{team_a}_vs_{team_b}.pdf",
            mime="application/pdf",
            type="primary"
        )

# ---------------------------------------------------------
# စာမျက်နှာ ၂ - Data Calculator 
# ---------------------------------------------------------
elif menu == t["menu_2"]:
    st.title(t["p2_title"])
    matches = st.number_input(t["matches_input"], min_value=1, max_value=20, value=5)
    
    total_goals, total_bc, total_sot, total_corners, total_pos = 0.0, 0.0, 0.0, 0.0, 0.0
    for i in range(matches):
        with st.expander(f"{t['match_exp']} {i+1}"):
            c1, c2, c3, c4, c5 = st.columns(5)
            total_goals += c1.number_input("Goals", value=0.0, step=0.01, format="%.2f", key=f"g_{i}")
            total_bc += c2.number_input("Big Chances", value=0.0, step=0.01, format="%.2f", key=f"bc_{i}")
            total_sot += c3.number_input("SoT", value=0.0, step=0.01, format="%.2f", key=f"sot_{i}")
            total_corners += c4.number_input("Corners", value=0.0, step=0.01, format="%.2f", key=f"c_{i}")
            total_pos += c5.number_input("Possession (%)", value=0.0, step=0.01, format="%.2f", key=f"pos_{i}")

    if st.button(t["btn_avg"], type="primary"):
        st.success(t["success_msg"])
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
    
    st.subheader(t["p3_sub1"])
    team_search = st.text_input(t["search_label"])
    
    if st.button(t["btn_search"], type="primary") and team_search:
        encoded_team = urllib.parse.quote(team_search)
        st.info(f"**{team_search}** {t['search_res']}")
        
        link1, link2, link3 = st.columns(3)
        with link1:
            st.markdown(f"[📊 **Sofascore**](https://www.sofascore.com/search?q={encoded_team})")
        with link2:
            st.markdown(f"[📈 **FotMob**](https://www.fotmob.com/search?q={encoded_team})")
        with link3:
            st.markdown(f"[⚽ **Flashscore**](https://www.flashscore.com/search/?q={encoded_team})")
            
    st.divider()
    st.subheader(t["p3_sub2"])
    components.iframe("https://www.scorebat.com/embed/livescore/", height=700, scrolling=True)
