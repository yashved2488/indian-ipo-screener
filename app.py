import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import math
from dateutil.relativedelta import relativedelta, TH

# --- CONFIGURATION ---
st.set_page_config(page_title="Indian IPO Blog | Ironclad Risk Screener", layout="wide", page_icon="🛡️")

# Cleaned F&O Universe (Removed historically illiquid/banned names)
FO_STOCKS = {
    'AARTIIND.NS': 1000, 'ABB.NS': 250, 'ABBOTINDIA.NS': 40, 'ABCAPITAL.NS': 5400, 'ABFRL.NS': 2600, 'ACC.NS': 300, 'ADANIENT.NS': 300, 'ADANIPORTS.NS': 800, 'ALKEM.NS': 200, 'AMBUJACEM.NS': 1800, 'APOLLOHOSP.NS': 125, 'APOLLOTYRE.NS': 1700, 'ASHOKLEY.NS': 5000, 'ASIANPAINT.NS': 200, 'ASTRAL.NS': 275, 'ATUL.NS': 75, 'AUBANK.NS': 1000, 'AUROPHARMA.NS': 1000, 'AXISBANK.NS': 625, 'BAJAJ-AUTO.NS': 125, 'BAJAJFINSV.NS': 500, 'BAJFINANCE.NS': 125, 'BALKRISIND.NS': 300, 'BALRAMCHIN.NS': 1600, 'BANDHANBNK.NS': 2500, 'BANKBARODA.NS': 5850, 'BATAINDIA.NS': 375, 'BEL.NS': 3800, 'BERGEPAINT.NS': 1100, 'BHARATFORG.NS': 500, 'BHARTIARTL.NS': 950, 'BHEL.NS': 5250, 'BIOCON.NS': 2500, 'BOSCHLTD.NS': 50, 'BPCL.NS': 1800, 'BRITANNIA.NS': 200, 'CANBK.NS': 2700, 'CANFINHOME.NS': 975, 'CHAMBLFERT.NS': 1900, 'CHOLAFIN.NS': 1250, 'CIPLA.NS': 650, 'COALINDIA.NS': 4200, 'COFORGE.NS': 150, 'COLPAL.NS': 350, 'CONCOR.NS': 1000, 'COROMANDEL.NS': 700, 'CROMPTON.NS': 1800, 'CUB.NS': 5000, 'CUMMINSIND.NS': 300, 'DABUR.NS': 1250, 'DALBHARAT.NS': 250, 'DEEPAKNTR.NS': 300, 'DIVISLAB.NS': 200, 'DIXON.NS': 100, 'DLF.NS': 1650, 'DRREDDY.NS': 125, 'EICHERMOT.NS': 175, 'ESCORTS.NS': 275, 'EXIDEIND.NS': 3600, 'FEDERALBNK.NS': 5000, 'GAIL.NS': 9150, 'GLENMARK.NS': 700, 'GNFC.NS': 1300, 'GODREJCP.NS': 500, 'GODREJPROP.NS': 475, 'GRANULES.NS': 2000, 'GRASIM.NS': 475, 'GUJGASLTD.NS': 1250, 'HAL.NS': 300, 'HAVELLS.NS': 500, 'HCLTECH.NS': 700, 'HDFCAMC.NS': 150, 'HDFCBANK.NS': 550, 'HDFCLIFE.NS': 1100, 'HEROMOTOCO.NS': 300, 'HINDALCO.NS': 1400, 'HINDCOPPER.NS': 4300, 'HINDPETRO.NS': 2700, 'HINDUNILVR.NS': 300, 'ICICIBANK.NS': 700, 'ICICIGI.NS': 500, 'ICICIPRULI.NS': 1500, 'IDFCFIRSTB.NS': 15000, 'IEX.NS': 3750, 'IGL.NS': 1375, 'INDHOTEL.NS': 2000, 'INDIACEM.NS': 2900, 'INDIAMART.NS': 150, 'INDIGO.NS': 300, 'INDUSINDBK.NS': 500, 'INDUSTOWER.NS': 3400, 'INFY.NS': 400, 'IOC.NS': 9750, 'IPCALAB.NS': 650, 'IRCTC.NS': 875, 'ITC.NS': 1600, 'JINDALSTEL.NS': 1250, 'JKCEMENT.NS': 250, 'JSWSTEEL.NS': 675, 'JUBLFOOD.NS': 1250, 'KOTAKBANK.NS': 400, 'L&TFH.NS': 4462, 'LALPATHLAB.NS': 250, 'LAURUSLABS.NS': 1700, 'LICHSGFIN.NS': 2000, 'LT.NS': 300, 'LTIM.NS': 150, 'LTTS.NS': 200, 'LUPIN.NS': 850, 'M&M.NS': 350, 'M&MFIN.NS': 4000, 'MANAPPURAM.NS': 6000, 'MARICO.NS': 1200, 'MARUTI.NS': 50, 'MCX.NS': 400, 'METROPOLIS.NS': 400, 'MFSL.NS': 800, 'MGL.NS': 800, 'MOTHERSON.NS': 7100, 'MPHASIS.NS': 275, 'MRF.NS': 10, 'MUTHOOTFIN.NS': 550, 'NATIONALUM.NS': 7500, 'NAUKRI.NS': 150, 'NAVINFLUOR.NS': 150, 'NESTLEIND.NS': 400, 'NMDC.NS': 4500, 'NTPC.NS': 3000, 'OBEROIRLTY.NS': 700, 'OFSS.NS': 200, 'ONGC.NS': 3850, 'PAGEIND.NS': 15, 'PEL.NS': 750, 'PERSISTENT.NS': 175, 'PETRONET.NS': 3000, 'PFC.NS': 3875, 'PIDILITIND.NS': 250, 'PIIND.NS': 250, 'PNB.NS': 8000, 'POLYCAB.NS': 100, 'POWERGRID.NS': 3600, 'PVRINOX.NS': 407, 'RAMCOCEM.NS': 850, 'RBLBANK.NS': 2500, 'RECLTD.NS': 2000, 'RELIANCE.NS': 250, 'SAIL.NS': 8000, 'SBICARD.NS': 800, 'SBILIFE.NS': 750, 'SBIN.NS': 1500, 'SHREECEM.NS': 25, 'SHRIRAMFIN.NS': 300, 'SIEMENS.NS': 150, 'SRF.NS': 375, 'SUNTV.NS': 1500, 'SYNGENE.NS': 1000, 'TATACHEM.NS': 550, 'TATACOMM.NS': 500, 'TATACONSUM.NS': 900, 'TATAMOTORS.NS': 1425, 'TATAPOWER.NS': 3375, 'TATASTEEL.NS': 5500, 'TCS.NS': 175, 'TECHM.NS': 600, 'TITAN.NS': 175, 'TORNTPHARM.NS': 250, 'TRENT.NS': 400, 'TVSMOTOR.NS': 700, 'UBL.NS': 400, 'ULTRACEMCO.NS': 100, 'UPL.NS': 1300, 'VEDL.NS': 2000, 'VOLTAS.NS': 600, 'WIPRO.NS': 1500, 'ZYDUSLIFE.NS': 900
}

ULTRA_LIQUID_STOCKS = ['RELIANCE', 'HDFCBANK', 'ICICIBANK', 'INFY', 'TCS', 'SBIN', 'ITC', 'TATAMOTORS', 'AXISBANK', 'KOTAKBANK', 'LT', 'BAJFINANCE', 'BHARTIARTL']

# --- FORMATTERS & REAL-WORLD STRIKE MAPPING ---
def fmt_inr(number): return f"₹{int(number):,}" if pd.notna(number) else "₹0"
def fmt_inr_dec(number): return f"₹{number:,.2f}" if pd.notna(number) else "₹0.00"

def get_upcoming_expiries():
    """Calculates upcoming expiries, strictly ignoring anything within 5 days to avoid Gamma Risk."""
    today = datetime.date.today()
    min_safe_date = today + datetime.timedelta(days=5)
    expiries = []
    
    for i in range(4): # Check up to 4 months out to ensure we find valid dates
        target_month = today.replace(day=1) + relativedelta(months=i)
        last_day_of_month = target_month + relativedelta(months=1, days=-1)
        expiry = last_day_of_month + relativedelta(weekday=TH(-1))
        if expiry >= min_safe_date: 
            expiries.append(expiry)
            
    return expiries[:3] # Return the next 3 safe options

def get_sector(symbol):
    banks_fin = ['HDFCBANK', 'ICICIBANK', 'SBIN', 'AXISBANK', 'KOTAKBANK', 'BAJFINANCE', 'CHOLAFIN', 'PFC', 'RECLTD']
    it = ['TCS', 'INFY', 'HCLTECH', 'WIPRO', 'TECHM', 'LTIM']
    auto = ['TATAMOTORS', 'M&M', 'MARUTI', 'BAJAJ-AUTO', 'HEROMOTOCO', 'ASHOKLEY']
    pharma = ['SUNPHARMA', 'CIPLA', 'DRREDDY', 'DIVISLAB', 'LUPIN', 'AUROPHARMA']
    fmcg = ['ITC', 'HINDUNILVR', 'NESTLEIND', 'BRITANNIA', 'DABUR', 'MARICO']
    metals = ['TATASTEEL', 'JSWSTEEL', 'HINDALCO', 'VEDL', 'COALINDIA']
    clean_sym = symbol.replace('.NS', '')
    if clean_sym in banks_fin: return "Banking & Finance"
    if clean_sym in it: return "IT & Tech"
    if clean_sym in auto: return "Automobile"
    if clean_sym in pharma: return "Pharma"
    if clean_sym in fmcg: return "FMCG"
    if clean_sym in metals: return "Metals & Mining"
    return "Others"

def estimate_liquidity(symbol, upside_pct):
    base_score = 3 if symbol in ULTRA_LIQUID_STOCKS else 2
    if upside_pct >= 15: base_score -= 2
    elif upside_pct >= 10: base_score -= 1
    if base_score >= 3: return "🟢 High"
    elif base_score == 2: return "🟡 Med"
    else: return "🔴 Low"

def get_real_strike(cmp, raw_target):
    if cmp <= 250: step = 2.5
    elif cmp <= 500: step = 5
    elif cmp <= 1000: step = 10
    elif cmp <= 3000: step = 20
    elif cmp <= 10000: step = 50
    elif cmp <= 30000: step = 100
    else: step = 500
    return math.ceil(raw_target / step) * step

# --- QUANT ENGINE ---
def norm_cdf(x): return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
def norm_pdf(x): return math.exp(-x**2 / 2.0) / math.sqrt(2.0 * math.pi)

def black_scholes_metrics(S, K, days_to_expiry, hv_annualized):
    T = max(days_to_expiry / 365.0, 0.002) 
    r = 0.07 
    sigma = max(hv_annualized / 100.0, 0.1) 
    
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    delta = norm_cdf(d1)
    theta_annual = -(S * norm_pdf(d1) * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm_cdf(d2)
    
    return max(call_price, 0.1), delta, theta_annual / 365.0

@st.cache_data(ttl=3600)
def fetch_market_data(tickers_dict):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=3*365)
    tickers_list = list(tickers_dict.keys())
    try:
        return yf.download(tickers_list, start=start_date, end=end_date, progress=False)
    except Exception:
        return None

def calculate_rsi(data, periods=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def process_screener_data(historical_data, tickers_dict, margin_available, call_type, days_to_expiry, target_upside):
    if historical_data is None: return None, None
    
    close_prices = historical_data['Close']
    high_prices = historical_data['High']
    low_prices = historical_data['Low']
    trading_days_to_expiry = max(int(days_to_expiry * (252/365)), 1)
    
    main_table_data = []
    global_recommendation_pool = {}

    for ticker, lot_size in tickers_dict.items():
        if ticker not in close_prices.columns: continue
        
        stock_close = close_prices[ticker].dropna()
        stock_high = high_prices[ticker].dropna()
        if stock_close.empty or len(stock_close) < 252: continue
            
        cmp = stock_close.iloc[-1].item()
        high_52w = stock_high.tail(252).max().item()
        low_52w = low_prices[ticker].dropna().tail(252).min().item()
        
        daily_returns = stock_close.pct_change()
        hv = daily_returns.tail(252).std().item() * np.sqrt(252) * 100 
        rsi_14 = calculate_rsi(stock_close).iloc[-1].item()
        
        clean_symbol = ticker.replace('.NS', '')
        sector = get_sector(ticker)
        
        rolling_returns = stock_close.pct_change(periods=trading_days_to_expiry) * 100
        total_periods = len(rolling_returns.dropna())
        
        best_stock_rank = (-999, -999) 
        best_stock_trade = None
        
        # Recommendation Engine Loop
        for up in [10, 12, 15, 18, 20]:
            raw_target_p = cmp * (1 + (up / 100))
            real_target_p = get_real_strike(cmp, raw_target_p)
            actual_up_pct = ((real_target_p - cmp) / cmp) * 100
            
            prob = (len(rolling_returns[rolling_returns >= actual_up_pct]) / total_periods) * 100 if total_periods > 0 else 0
            bs_price, delta, theta = black_scholes_metrics(cmp, real_target_p, days_to_expiry, hv)
            days_above_target_3m = len(stock_high.tail(63)[stock_high.tail(63) >= real_target_p])
            
            veto_reason = None
            if call_type == "Naked (Uncovered)":
                if actual_up_pct < 10.0: veto_reason = f"Upside < 10%"
                elif prob > 8.0: veto_reason = f"Hist. Breach > 8%"
                elif delta > 0.12: veto_reason = f"Delta > 0.12"
                elif days_above_target_3m > 0: veto_reason = f"Resistance Risk"
            else:
                if actual_up_pct < 7.0: veto_reason = f"Upside < 7%"
                elif prob > 15.0: veto_reason = f"Hist. Breach > 15%"
                elif delta > 0.20: veto_reason = f"Delta > 0.20"
            
            prof_per_lot = bs_price * lot_size
            cont_value = cmp * lot_size
            
            if call_type == "Naked (Uncovered)":
                marg_req = cont_value * 0.20 
                lots = int(margin_available // marg_req) if marg_req > 0 else 0
            else:
                lots = int(margin_available // cont_value) if cont_value > 0 else 0
            
            tot_prof = prof_per_lot * lots
            liq = estimate_liquidity(clean_symbol, actual_up_pct)
            
            if lots == 0: veto_reason = "Capital Insufficient"
            if liq == "🔴 Low": veto_reason = "Illiquid"

            if veto_reason is None:
                safety_score = 100 - (prob * 2.0) - (hv / 2.0)
                if real_target_p > high_52w: safety_score += 10
                if rsi_14 > 70: safety_score += 10  
                elif rsi_14 < 40: safety_score -= 15 
                safety_score += min(abs(theta) * 3, 10) 
                safety_score = max(0, min(100, safety_score))

                score_breakdown = {
                    "Veto Status": "✅ Passed",
                    f"Actual Upside": f"{actual_up_pct:.1f}%",
                    f"Historical Breach": f"{prob:.1f}%",
                    f"Theo. Delta": f"{delta:.2f}",
                    "Final Safety Score": round(safety_score, 1)
                }

                rank_tuple = (safety_score, tot_prof) 
                if rank_tuple > best_stock_rank:
                    best_stock_rank = rank_tuple
                    best_stock_trade = {
                        'Stock': clean_symbol, 'Sector': sector, 'Upside': f"{actual_up_pct:.1f}", 'Target': real_target_p,
                        'Lots': lots, 'Total_Profit': tot_prof, 'Risk': prob, 'Safety_Score': safety_score,
                        'HV': hv, 'Delta': delta, 'Margin': marg_req * lots if call_type == "Naked (Uncovered)" else cont_value * lots,
                        'Breakdown': score_breakdown
                    }
        
        if best_stock_trade:
            global_recommendation_pool[clean_symbol] = best_stock_trade

        # --- Process Main UI Table ---
        raw_target_p = cmp * (1 + (target_upside / 100))
        real_target_p = get_real_strike(cmp, raw_target_p)
        actual_up_pct = ((real_target_p - cmp) / cmp) * 100
        
        prob = (len(rolling_returns[rolling_returns >= actual_up_pct]) / total_periods) * 100 if total_periods > 0 else 0
        bs_price, delta, theta = black_scholes_metrics(cmp, real_target_p, days_to_expiry, hv)
        days_above_target_3m = len(stock_high.tail(63)[stock_high.tail(63) >= real_target_p])
        
        table_veto = None
        if call_type == "Naked (Uncovered)":
            if actual_up_pct < 10.0: table_veto = "⛔ Upside < 10%"
            elif prob > 8.0: table_veto = f"⛔ Breach > 8%"
            elif delta > 0.12: table_veto = f"⛔ High Delta"
            elif days_above_target_3m > 0: table_veto = f"⛔ Resistance"
        else:
            if actual_up_pct < 7.0: table_veto = "⛔ Upside < 7%"
            elif prob > 15.0: table_veto = f"⛔ Breach > 15%"
            elif delta > 0.20: table_veto = f"⛔ High Delta"
            
        status_msg = "✅ Pass" if table_veto is None else table_veto

        premium_per_lot = bs_price * lot_size
        contract_value = cmp * lot_size
        
        if call_type == "Naked (Uncovered)":
            margin_req_per_lot = contract_value * 0.20 
            max_lots = int(margin_available // margin_req_per_lot) if margin_req_per_lot > 0 else 0
        else:
            max_lots = int(margin_available // contract_value) if contract_value > 0 else 0
            
        total_profit = premium_per_lot * max_lots
        liquidity_status = estimate_liquidity(clean_symbol, actual_up_pct)

        main_table_data.append({
            'Stock': clean_symbol,
            'Sector': sector,
            'CMP': fmt_inr_dec(cmp),
            'Real Strike': fmt_inr_dec(real_target_p),
            'Veto Status': status_msg,
            'Lot Size': f"{lot_size:,}",
            'Theo. Delta': f"{delta:.2f}",
            'Premium / Lot': fmt_inr_dec(premium_per_lot), 
            'Margin / Lot': fmt_inr(margin_req_per_lot if call_type == "Naked (Uncovered)" else contract_value),
            'Max Lots': max_lots,
            'Total Profit': fmt_inr(total_profit),
            'Hist. Breach': f"{prob:.0f}%",
            'Liquidity': liquidity_status,
            '_raw_profit': total_profit # Hidden column for accurate sorting
        })

    # Sort data by Raw Numeric Profit descending
    main_table_data.sort(key=lambda x: x['_raw_profit'], reverse=True)
    
    # Remove hidden column before passing to DataFrame
    for row in main_table_data:
        del row['_raw_profit']

    main_df = pd.DataFrame(main_table_data)
    sorted_recs = sorted(global_recommendation_pool.values(), key=lambda x: (x['Safety_Score'], x['Total_Profit']), reverse=True)[:5]
    
    return main_df, sorted_recs

# --- UI LAYOUT ---
st.title("🛡️ Indian IPO Blog: Ironclad Risk Screener")
st.markdown("Enforcing institutional hard-limits. High yield cannot compensate for structural risk.")

with st.sidebar:
    st.header("Trade Parameters")
    margin_input = st.number_input("Capital Available (₹)", min_value=100000, value=1000000, step=100000, format="%d")
    
    expiries = get_upcoming_expiries()
    expiry_options = {e.strftime("%d %b %Y"): e for e in expiries}
    
    if not expiry_options:
        st.error("No safe expiry dates found. Please try again later.")
        st.stop()
        
    selected_expiry_str = st.selectbox("Target Expiry Date", list(expiry_options.keys()))
    selected_expiry_date = expiry_options[selected_expiry_str]
    days_to_expiry = (selected_expiry_date - datetime.date.today()).days
    
    call_type = st.radio("Strategy Type", ["Naked (Uncovered)", "Covered (Hold underlying shares)"])
    
    st.markdown("---")
    st.header("Screener Filters")
    sector_filter = st.selectbox("Filter by Sector", ["All Sectors", "Banking & Finance", "IT & Tech", "Automobile", "Pharma", "FMCG", "Metals & Mining", "Others"])
    target_upside = st.selectbox("Target Upside Base (%)", [10, 12, 15, 18, 20], index=0)

historical_data = fetch_market_data(FO_STOCKS)
main_df, top_5_recs = None, None

with st.spinner("Enforcing Veto Limits (Max 8% Breach, Gamma Shield, Zero Resistance Touches)..."):
    main_df, top_5_recs = process_screener_data(historical_data, FO_STOCKS, margin_input, call_type, days_to_expiry, target_upside)

if main_df is not None and not main_df.empty:
    if sector_filter != "All Sectors":
        main_df = main_df[main_df['Sector'] == sector_filter]

    tab1, tab2 = st.tabs(["📊 Main Screener Matrix", "🏆 Top 5 Ironclad Setups"])
    
    with tab1:
        st.subheader(f"Showing Options near {target_upside}% OTM (Sorted by Total Profit)")
        st.dataframe(main_df.style.apply(lambda x: ['color: red; font-weight: bold' if '⛔' in str(v) else 'color: green' if '✅' in str(v) else '' for v in x], subset=['Veto Status']), use_container_width=True, hide_index=True)

    with tab2:
        st.success(f"🎯 **Target Expiry Strategy:** Selling options expiring on **{selected_expiry_str}** ({days_to_expiry} Days to Expiry).")
        st.subheader("The Playbook: Only Trades That Passed All Vetoes")
        st.markdown(f"The algorithm rejects any Naked Call with a historical breach > 8%, Delta > 0.12, or any resistance touches in the last 3 months.")
        
        if top_5_recs:
            for idx, rec in enumerate(top_5_recs, 1):
                with st.container():
                    st.markdown(f"### {idx}. {rec['Stock']} ({rec['Sector']}) | 🛡️ Safety Score: {rec['Safety_Score']:.1f}/100")
                    st.markdown(f"> **Action:** Sell **{rec['Lots']} lot(s)** of the **{rec['Target']} Call** (Actual Upside: {rec['Upside']}%)")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Profit", fmt_inr(rec['Total_Profit']))
                    col2.metric("Capital Required", fmt_inr(rec['Margin']))
                    col3.metric("Theo. Delta (Δ)", f"{rec['Delta']:.2f}")
                    col4.metric("Historical Breach", f"{rec['Risk']:.0f}%")
                    
                    with st.expander("🔍 View Ironclad Audit Trail"):
                        for factor, score in rec['Breakdown'].items():
                            color = "green" if "Passed" in str(score) else "black"
                            st.markdown(f"* **{factor}:** <span style='color:{color}'>{score}</span>", unsafe_allow_html=True)
                            
                    st.markdown("---")
        else:
            st.warning("No trades found matching the Ironclad safety criteria. The strict limits correctly prevented taking on excess risk in current market conditions.")
else:
    st.error("Failed to process market data. Please check connection.")
