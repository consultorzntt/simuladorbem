import streamlit as st
import time
import random

st.set_page_config(
    page_title="BEM | Simulador de Comissões",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BEM_BLUE = "#0877B9"
BEM_BLUE_DARK = "#055F96"
BEM_CYAN = "#00AEEF"
BEM_GREEN = "#53C58B"
WHITE = "#FFFFFF"
OFF_WHITE = "#F6F8FA"
TEXT = "#24313B"
MUTED = "#6B7780"
LINE = "#DCE4E8"
SOFT_BLUE = "#EAF5FB"
SOFT_GREEN = "#EEF9F3"

PRODUCTS = {
    "Empréstimo Consignado": {"avg": 10.0, "max": 14.0, "full_payout": True},
    "Seguros": {"avg": 23.0, "min": 10.0, "max": 50.0, "full_payout": False},
    "Consórcio": {"avg": 4.0, "max": 6.5, "full_payout": False},
    "Empréstimo Pessoal": {"avg": None, "max": 11.0, "full_payout": True},
    "Fin./Refin. Automóvel": {"avg": 4.0, "max": 6.0, "full_payout": False},
    "Financiamento Imobiliário": {"avg": 2.0, "max": 2.0, "full_payout": False},
    "Refinanciamento Imobiliário": {"avg": 5.0, "max": 8.0, "full_payout": False},
    "Agro": {"avg": None, "max": 1.0, "full_payout": False},
    "Fintech": {"avg": None, "max": 1.0, "full_payout": False},
}

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {OFF_WHITE};
        color: {TEXT};
    }}
    .block-container {{
        max-width: 1380px;
        padding-top: 1.1rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3 {{
        color: {BEM_BLUE_DARK};
    }}
    .bem-header {{
        background: {BEM_BLUE};
        padding: 22px 28px;
        border-radius: 18px;
        color: white;
        margin-bottom: 20px;
    }}
    .bem-title {{
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.05;
    }}
    .bem-subtitle {{
        color: #DDF3FD;
        margin-top: 8px;
        font-size: 1.02rem;
    }}
    .commission-card {{
        background: white;
        border: 1px solid {LINE};
        border-radius: 16px;
        padding: 18px;
        min-height: 150px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }}
    .commission-card .name {{
        font-weight: 700;
        color: {TEXT};
        font-size: 1.03rem;
        min-height: 44px;
    }}
    .commission-card .big {{
        color: {BEM_BLUE_DARK};
        font-size: 1.65rem;
        font-weight: 800;
        margin-top: 8px;
    }}
    .commission-card .small {{
        color: {MUTED};
        font-size: .9rem;
        margin-top: 4px;
    }}
    .green-badge {{
        display: inline-block;
        background: {SOFT_GREEN};
        color: {BEM_BLUE_DARK};
        padding: 5px 9px;
        border-radius: 8px;
        font-size: .77rem;
        font-weight: 700;
        margin-top: 10px;
    }}
    .result-box {{
        background: white;
        border: 2px solid {BEM_CYAN};
        border-radius: 18px;
        padding: 26px;
        text-align: center;
        margin: 14px 0;
    }}
    .result-label {{
        color: {MUTED};
        font-weight: 700;
        font-size: .9rem;
    }}
    .result-value {{
        color: {BEM_BLUE_DARK};
        font-size: 3rem;
        font-weight: 900;
        margin-top: 4px;
    }}
    .note {{
        color: {MUTED};
        font-size: .85rem;
    }}
    div[data-testid="stMetric"] {{
        background: white;
        border: 1px solid {LINE};
        padding: 14px;
        border-radius: 14px;
    }}
    div.stButton > button {{
        background: {BEM_BLUE};
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
    }}
    div.stButton > button:hover {{
        background: {BEM_BLUE_DARK};
        color: white;
        border: none;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

def pct(v):
    if abs(v - round(v)) < 1e-9:
        return f"{int(round(v))}%"
    return f"{v:.3f}".rstrip("0").rstrip(".").replace(".", ",") + "%"

def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"

def share_for(product, model):
    if PRODUCTS[product]["full_payout"]:
        return 1.0
    return 0.75 if model == "HOME" else 0.80

def rate_selector(product, key_prefix):
    data = PRODUCTS[product]
    modes = ["MÉDIA", "MÁXIMA", "PERSONALIZADA"]
    if data["avg"] is None:
        modes = ["MÁXIMA", "PERSONALIZADA"]

    mode = st.radio(
        "Comissão utilizada",
        modes,
        horizontal=True,
        key=f"{key_prefix}_mode"
    )

    if mode == "MÉDIA":
        return data["avg"], mode

    if mode == "MÁXIMA":
        return data["max"], mode

    min_rate = data.get("min", 0.1)
    rate = st.slider(
        "Percentual personalizado",
        min_value=float(min_rate),
        max_value=float(data["max"]),
        value=float(data["avg"] if data["avg"] is not None else data["max"]),
        step=0.1,
        key=f"{key_prefix}_rate"
    )
    return rate, mode

def reveal_amount(final_value, label):
    placeholder = st.empty()
    low = max(final_value * 0.2, 10)
    high = max(final_value * 1.35, 100)

    for i in range(18):
        if i > 13:
            value = final_value * (1 + (random.random() - .5) * .02)
        else:
            value = random.uniform(low, high)
        placeholder.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">{label}</div>
                <div class="result-value">{brl(value)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.045)

    placeholder.markdown(
        f"""
        <div class="result-box">
            <div class="result-label">{label}</div>
            <div class="result-value">{brl(final_value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="bem-header">
        <div class="bem-title">BEM | Simulador de Comissões</div>
        <div class="bem-subtitle">Apresente as comissões e simule quanto uma ou várias vendas podem gerar para o franqueado.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs([
    "💼 Comissões por Produto",
    "📊 Simulação Individual",
    "🚀 Cenário de Vendas",
])

with tab1:
    st.subheader("Comissões por Produto")
    st.caption("Os percentuais abaixo são os percentuais dos produtos. O repasse Home/Office é aplicado somente depois da comissão ser gerada.")

    items = list(PRODUCTS.items())
    for start in range(0, len(items), 3):
        cols = st.columns(3)
        for col, (name, data) in zip(cols, items[start:start+3]):
            if name == "Seguros":
                big = "10% a 50%"
                small = "Comissão média: 23%"
            elif data["avg"] is None:
                big = f"Até {pct(data['max'])}"
                small = "Comissão média não informada"
            else:
                big = f"Média {pct(data['avg'])}"
                small = f"Até {pct(data['max'])}"

            badge = '<div class="green-badge">100% da comissão para o franqueado</div>' if data["full_payout"] else ""

            with col:
                st.markdown(
                    f"""
                    <div class="commission-card">
                        <div class="name">{name}</div>
                        <div class="big">{big}</div>
                        <div class="small">{small}</div>
                        {badge}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("---")
    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        st.metric("MODELO HOME", "75%", "da comissão gerada")
    with c2:
        st.metric("MODELO OFFICE", "80%", "da comissão gerada")
    with c3:
        st.info("Consignado e Empréstimo Pessoal têm repasse de 100% da comissão gerada, independentemente do modelo.")

with tab2:
    st.subheader("Simulação Individual")
    st.caption("Simule uma única venda e veja o valor que fica com o franqueado.")

    c1, c2 = st.columns([1.2, 1])

    with c1:
        product = st.selectbox("Produto", list(PRODUCTS.keys()), key="single_product")
        sale = st.number_input(
            "Valor da venda",
            min_value=0.0,
            value=500000.0,
            step=1000.0,
            format="%.2f",
            key="single_sale"
        )
        rate, mode = rate_selector(product, "single")

    with c2:
        model = st.radio(
            "Modelo de negócio",
            ["HOME", "OFFICE"],
            horizontal=True,
            key="single_model"
        )

        share = share_for(product, model)
        gross = sale * rate / 100
        net = gross * share

        st.metric("Comissão do produto", pct(rate))
        st.metric("Comissão gerada nesta venda", brl(gross))
        st.metric(
            "Repasse ao franqueado",
            "100%" if share == 1 else pct(share * 100)
        )

        if PRODUCTS[product]["full_payout"]:
            st.success("Neste produto, 100% da comissão gerada fica com o franqueado.")

    if st.button("REVELAR COMISSÃO", use_container_width=True, key="single_reveal"):
        reveal_amount(net, "VALOR QUE FICA COM O FRANQUEADO NESTA VENDA")

with tab3:
    st.subheader("Cenário de Vendas")
    st.caption("Combine vários produtos no mesmo cenário e veja o resultado total.")

    model = st.radio(
        "Modelo de negócio",
        ["HOME", "OFFICE"],
        horizontal=True,
        key="scenario_model"
    )

    if "rows" not in st.session_state:
        st.session_state.rows = [
            {"product": "Empréstimo Consignado", "sale": 20000.0, "mode": "MÉDIA", "custom": 10.0},
            {"product": "Seguros", "sale": 30000.0, "mode": "MÉDIA", "custom": 23.0},
        ]

    top_a, top_b = st.columns([1, 4])
    with top_a:
        if st.button("+ ADICIONAR PRODUTO"):
            if len(st.session_state.rows) < 8:
                st.session_state.rows.append(
                    {"product": "Consórcio", "sale": 10000.0, "mode": "MÉDIA", "custom": 4.0}
                )
                st.rerun()

    breakdown = []

    for i, row in enumerate(list(st.session_state.rows)):
        with st.container(border=True):
            cols = st.columns([2.0, 1.3, 1.3, 1.0, .55])

            with cols[0]:
                product = st.selectbox(
                    "Produto",
                    list(PRODUCTS.keys()),
                    index=list(PRODUCTS.keys()).index(row["product"]),
                    key=f"p_{i}"
                )
            with cols[1]:
                sale = st.number_input(
                    "Valor da venda",
                    min_value=0.0,
                    value=float(row["sale"]),
                    step=1000.0,
                    format="%.2f",
                    key=f"s_{i}"
                )
            with cols[2]:
                modes = ["MÉDIA", "MÁXIMA", "PERSONALIZADA"]
                if PRODUCTS[product]["avg"] is None:
                    modes = ["MÁXIMA", "PERSONALIZADA"]

                current_mode = row["mode"] if row["mode"] in modes else modes[0]
                mode = st.selectbox(
                    "Comissão",
                    modes,
                    index=modes.index(current_mode),
                    key=f"m_{i}"
                )

            with cols[3]:
                data = PRODUCTS[product]
                if mode == "MÉDIA":
                    rate = data["avg"]
                    st.metric("%", pct(rate))
                elif mode == "MÁXIMA":
                    rate = data["max"]
                    st.metric("%", pct(rate))
                else:
                    min_rate = data.get("min", 0.1)
                    default = row["custom"]
                    default = min(max(default, min_rate), data["max"])
                    rate = st.number_input(
                        "%",
                        min_value=float(min_rate),
                        max_value=float(data["max"]),
                        value=float(default),
                        step=0.1,
                        key=f"r_{i}"
                    )

            with cols[4]:
                st.write("")
                st.write("")
                if st.button("✕", key=f"del_{i}"):
                    if len(st.session_state.rows) > 1:
                        st.session_state.rows.pop(i)
                        st.rerun()

            st.session_state.rows[i] = {
                "product": product,
                "sale": sale,
                "mode": mode,
                "custom": float(rate)
            }

            gross = sale * rate / 100
            share = share_for(product, model)
            net = gross * share

            breakdown.append({
                "product": product,
                "sale": sale,
                "rate": rate,
                "gross": gross,
                "share": share,
                "net": net
            })

    total_sales = sum(x["sale"] for x in breakdown)
    total_gross = sum(x["gross"] for x in breakdown)
    total_net = sum(x["net"] for x in breakdown)

    st.markdown("---")
    a, b, c = st.columns(3)
    a.metric("Total vendido", brl(total_sales))
    b.metric("Comissão gerada", brl(total_gross))
    c.metric("Valor do franqueado", brl(total_net))

    with st.expander("Ver cálculo por produto"):
        for item in breakdown:
            repasse = "100%" if item["share"] == 1 else pct(item["share"] * 100)
            st.write(
                f"**{item['product']}** — {brl(item['sale'])} × {pct(item['rate'])} "
                f"= {brl(item['gross'])} de comissão → repasse {repasse} → **{brl(item['net'])}**"
            )

    if st.button("CALCULAR E REVELAR CENÁRIO", use_container_width=True, key="scenario_reveal"):
        reveal_amount(total_net, "COMISSÃO TOTAL DO FRANQUEADO NESTE CENÁRIO")

st.markdown(
    '<div class="note">Simulações ilustrativas. Percentuais e condições podem variar conforme produto e operação.</div>',
    unsafe_allow_html=True
)
