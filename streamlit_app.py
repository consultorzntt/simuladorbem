import random
import time
import streamlit as st

st.set_page_config(
    page_title="BEM | Simulador de Comissões",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# DADOS
# ============================================================
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


# ============================================================
# CSS — FORÇA VISUAL CLARO E REMOVE O CHROME DO STREAMLIT
# ============================================================
st.markdown(
    f"""
    <style>
        /* Esconde barra superior, menu e rodapé do Streamlit */
        header[data-testid="stHeader"] {{
            display: none !important;
            height: 0 !important;
        }}
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        #MainMenu,
        footer {{
            display: none !important;
            visibility: hidden !important;
        }}

        html, body, [data-testid="stAppViewContainer"], .stApp {{
            background: {OFF_WHITE} !important;
            color: {TEXT} !important;
        }}

        .block-container {{
            max-width: 1480px !important;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }}

        /* Texto nativo sempre legível */
        .stApp p,
        .stApp label,
        .stApp span,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4 {{
            opacity: 1 !important;
        }}

        [data-testid="stWidgetLabel"] p,
        [data-testid="stMarkdownContainer"] p {{
            color: {TEXT};
        }}

        /* Cabeçalho BEM */
        .bem-hero {{
            background: {BEM_BLUE};
            border-radius: 0 0 22px 22px;
            padding: 24px 34px 26px 34px;
            margin-bottom: 18px;
            position: relative;
            overflow: hidden;
        }}
        .bem-hero::after {{
            content: "";
            position: absolute;
            width: 420px;
            height: 420px;
            border: 1px solid rgba(255,255,255,.16);
            border-radius: 50%;
            right: -190px;
            top: -240px;
        }}
        .bem-brand {{
            color: {WHITE} !important;
            font-size: 2.45rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.05;
            margin: 0;
        }}
        .bem-brand span {{
            color: {WHITE} !important;
        }}
        .bem-subtitle {{
            color: #DDF3FD !important;
            font-size: 1rem;
            margin-top: 10px;
            max-width: 900px;
        }}
        .brand-bars {{
            display: flex;
            gap: 4px;
            margin-bottom: 12px;
        }}
        .brand-bars b {{
            display: block;
            width: 18px;
            height: 5px;
            border-radius: 2px;
        }}

        /* Títulos */
        .section-title {{
            color: {BEM_BLUE_DARK} !important;
            font-size: 1.7rem;
            font-weight: 800;
            margin: 18px 0 4px 0;
        }}
        .section-subtitle {{
            color: {MUTED} !important;
            font-size: .96rem;
            margin-bottom: 18px;
        }}

        /* Cards */
        .commission-card {{
            background: {WHITE};
            border: 1px solid {LINE};
            border-radius: 16px;
            padding: 18px 19px;
            min-height: 154px;
            box-shadow: 0 3px 12px rgba(24, 59, 79, 0.035);
            margin-bottom: 2px;
        }}
        .commission-name {{
            color: {TEXT} !important;
            font-size: 1rem;
            line-height: 1.25;
            font-weight: 750;
            min-height: 42px;
        }}
        .commission-main {{
            color: {BEM_BLUE_DARK} !important;
            font-size: 1.7rem;
            font-weight: 850;
            margin-top: 6px;
            line-height: 1.1;
        }}
        .commission-detail {{
            color: {MUTED} !important;
            font-size: .87rem;
            margin-top: 7px;
        }}
        .green-badge {{
            display: inline-block;
            background: {SOFT_GREEN};
            color: {BEM_BLUE_DARK} !important;
            padding: 6px 9px;
            border-radius: 8px;
            font-size: .76rem;
            font-weight: 750;
            margin-top: 10px;
        }}

        .model-card {{
            background: {WHITE};
            border: 1px solid {LINE};
            border-radius: 14px;
            padding: 15px 18px;
            min-height: 92px;
        }}
        .model-label {{
            color: {MUTED} !important;
            font-size: .76rem;
            font-weight: 800;
            letter-spacing: .04em;
        }}
        .model-value {{
            color: {BEM_BLUE_DARK} !important;
            font-size: 1.55rem;
            font-weight: 850;
            margin-top: 3px;
        }}
        .model-detail {{
            color: {MUTED} !important;
            font-size: .83rem;
        }}

        /* Cards de resultado */
        .metric-card {{
            background: {WHITE};
            border: 1px solid {LINE};
            border-radius: 14px;
            padding: 15px 17px;
            min-height: 100px;
        }}
        .metric-label {{
            color: {MUTED} !important;
            font-size: .75rem;
            font-weight: 800;
            letter-spacing: .035em;
        }}
        .metric-value {{
            color: {BEM_BLUE_DARK} !important;
            font-size: 1.65rem;
            font-weight: 850;
            margin-top: 5px;
        }}
        .metric-detail {{
            color: {MUTED} !important;
            font-size: .82rem;
            margin-top: 3px;
        }}

        /* Resultado final */
        .result-box {{
            background: {WHITE};
            border: 2px solid {BEM_CYAN};
            border-radius: 18px;
            padding: 23px 28px;
            text-align: center;
            margin: 14px 0 8px 0;
            box-shadow: 0 5px 20px rgba(0, 114, 185, .08);
        }}
        .result-label {{
            color: {MUTED} !important;
            font-weight: 800;
            font-size: .78rem;
            letter-spacing: .045em;
        }}
        .result-value {{
            color: {BEM_BLUE_DARK} !important;
            font-size: 3rem;
            font-weight: 900;
            margin-top: 4px;
            line-height: 1.1;
        }}

        /* Streamlit buttons */
        div[data-testid="stButton"] > button {{
            border-radius: 10px !important;
            font-weight: 750 !important;
            min-height: 43px !important;
            transition: all .15s ease;
        }}
        div[data-testid="stButton"] > button[kind="primary"] {{
            background: {BEM_BLUE} !important;
            color: {WHITE} !important;
            border: 1px solid {BEM_BLUE} !important;
        }}
        div[data-testid="stButton"] > button[kind="primary"]:hover {{
            background: {BEM_BLUE_DARK} !important;
            border-color: {BEM_BLUE_DARK} !important;
        }}
        div[data-testid="stButton"] > button[kind="secondary"] {{
            background: {WHITE} !important;
            color: {BEM_BLUE_DARK} !important;
            border: 1px solid {LINE} !important;
        }}
        div[data-testid="stButton"] > button[kind="secondary"]:hover {{
            background: {SOFT_BLUE} !important;
            color: {BEM_BLUE_DARK} !important;
            border-color: {BEM_CYAN} !important;
        }}

        /* Inputs / select / radio: força contraste */
        [data-testid="stNumberInput"] input,
        [data-baseweb="input"] input,
        [data-baseweb="select"] > div {{
            background: {WHITE} !important;
            color: {TEXT} !important;
        }}
        [data-baseweb="select"] span {{
            color: {TEXT} !important;
        }}
        [role="radiogroup"] label,
        [role="radiogroup"] label p,
        [role="radiogroup"] span {{
            color: {TEXT} !important;
            opacity: 1 !important;
        }}
        [data-testid="stAlert"] p {{
            color: {TEXT} !important;
        }}

        .divider {{
            height: 1px;
            background: {LINE};
            margin: 20px 0;
        }}
        .fine-note {{
            color: {MUTED} !important;
            font-size: .78rem;
            margin-top: 12px;
        }}

        @media (max-width: 900px) {{
            .block-container {{
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
            .bem-hero {{
                padding: 21px 20px;
                border-radius: 0 0 16px 16px;
            }}
            .bem-brand {{
                font-size: 1.85rem;
            }}
            .result-value {{
                font-size: 2.25rem;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNÇÕES
# ============================================================
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


def hero():
    st.markdown(
        """
        <div class="bem-hero">
            <div class="brand-bars">
                <b style="background:#ffffff"></b>
                <b style="background:#53C58B"></b>
                <b style="background:#00AEEF"></b>
            </div>
            <div class="bem-brand"><span>bem</span> | Simulador de Comissões</div>
            <div class="bem-subtitle">
                Apresente as comissões e simule quanto uma ou várias vendas podem gerar para o franqueado.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def set_page(page):
    st.session_state.page = page


def nav():
    if "page" not in st.session_state:
        st.session_state.page = "Comissões"

    pages = [
        ("Comissões", "COMISSÕES"),
        ("Individual", "SIMULAÇÃO INDIVIDUAL"),
        ("Cenário", "CENÁRIO DE VENDAS"),
    ]
    cols = st.columns([1, 1.35, 1.25, 3])

    for col, (key, label) in zip(cols[:3], pages):
        with col:
            active = st.session_state.page == key
            if st.button(
                label,
                use_container_width=True,
                type="primary" if active else "secondary",
                key=f"nav_{key}",
            ):
                set_page(key)
                st.rerun()


def title_block(title, subtitle):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def metric_card(label, value, detail=""):
    return f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-detail">{detail}</div>
        </div>
    """


def reveal_amount(final_value, label):
    placeholder = st.empty()
    low = max(final_value * 0.20, 10)
    high = max(final_value * 1.35, 100)

    for i in range(16):
        if i > 11:
            value = final_value * (1 + (random.random() - 0.5) * 0.018)
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
        time.sleep(0.04)

    placeholder.markdown(
        f"""
        <div class="result-box">
            <div class="result-label">{label}</div>
            <div class="result-value">{brl(final_value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def rate_controls(product, prefix):
    data = PRODUCTS[product]
    modes = ["MÉDIA", "MÁXIMA", "PERSONALIZADA"] if data["avg"] is not None else ["MÁXIMA", "PERSONALIZADA"]

    mode = st.radio(
        "Comissão utilizada",
        modes,
        horizontal=True,
        key=f"{prefix}_mode",
    )

    if mode == "MÉDIA":
        return float(data["avg"]), mode

    if mode == "MÁXIMA":
        return float(data["max"]), mode

    minimum = float(data.get("min", 0.1))
    default = float(data["avg"] if data["avg"] is not None else data["max"])
    rate = st.slider(
        "Percentual personalizado",
        min_value=minimum,
        max_value=float(data["max"]),
        value=default,
        step=0.1,
        key=f"{prefix}_custom_rate",
    )
    return float(rate), mode


# ============================================================
# PÁGINAS
# ============================================================
def page_commissions():
    title_block(
        "Comissões por Produto",
        "Os percentuais abaixo pertencem aos produtos. O repasse Home/Office é aplicado somente depois que a comissão da venda é gerada.",
    )

    items = list(PRODUCTS.items())
    for start in range(0, len(items), 3):
        cols = st.columns(3, gap="medium")
        for col, (name, data) in zip(cols, items[start:start + 3]):
            if name == "Seguros":
                main = "10% a 50%"
                detail = "Comissão média: 23%"
            elif data["avg"] is None:
                main = f"Até {pct(data['max'])}"
                detail = "Comissão média não informada"
            else:
                main = f"Média {pct(data['avg'])}"
                detail = f"Até {pct(data['max'])}"

            badge = (
                '<div class="green-badge">100% da comissão para o franqueado</div>'
                if data["full_payout"]
                else ""
            )

            with col:
                st.markdown(
                    f"""
                    <div class="commission-card">
                        <div class="commission-name">{name}</div>
                        <div class="commission-main">{main}</div>
                        <div class="commission-detail">{detail}</div>
                        {badge}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1.55], gap="medium")
    with c1:
        st.markdown(
            """
            <div class="model-card">
                <div class="model-label">MODELO HOME</div>
                <div class="model-value">75%</div>
                <div class="model-detail">da comissão gerada</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="model-card">
                <div class="model-label">MODELO OFFICE</div>
                <div class="model-value">80%</div>
                <div class="model-detail">da comissão gerada</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="model-card" style="background:#EEF9F3">
                <div class="model-label">REPASSE INTEGRAL</div>
                <div class="model-value">100%</div>
                <div class="model-detail">Consignado e Empréstimo Pessoal, independentemente do modelo.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    right = st.columns([3, 1])[1]
    with right:
        if st.button("IR PARA O SIMULADOR →", use_container_width=True, type="primary"):
            set_page("Individual")
            st.rerun()


def page_individual():
    title_block(
        "Simulação Individual",
        "Escolha um produto, informe o valor de uma venda e veja quanto dessa operação fica com o franqueado.",
    )

    left, right = st.columns([1.18, 0.82], gap="large")

    with left:
        product = st.selectbox("Produto", list(PRODUCTS.keys()), key="single_product")
        sale = st.number_input(
            "Valor da venda (R$)",
            min_value=0.0,
            value=500000.0,
            step=1000.0,
            format="%.2f",
            key="single_sale",
        )
        rate, _ = rate_controls(product, "single")

    with right:
        model = st.radio(
            "Modelo de negócio",
            ["HOME", "OFFICE"],
            horizontal=True,
            key="single_model",
        )

        share = share_for(product, model)
        gross = sale * rate / 100
        net = gross * share

        a, b = st.columns(2)
        with a:
            st.markdown(metric_card("COMISSÃO DO PRODUTO", pct(rate), "percentual aplicado"), unsafe_allow_html=True)
        with b:
            st.markdown(metric_card("REPASSE", "100%" if share == 1 else pct(share * 100), "da comissão gerada"), unsafe_allow_html=True)

        st.write("")
        st.markdown(metric_card("COMISSÃO GERADA NESTA VENDA", brl(gross), "antes do repasse"), unsafe_allow_html=True)

        if PRODUCTS[product]["full_payout"]:
            st.success("Neste produto, 100% da comissão gerada fica com o franqueado.")

    st.write("")
    if st.button("REVELAR COMISSÃO", use_container_width=True, type="primary", key="single_reveal"):
        reveal_amount(net, "VALOR QUE FICA COM O FRANQUEADO NESTA VENDA")


def page_scenario():
    title_block(
        "Cenário de Vendas",
        "Combine vários produtos no mesmo cenário e veja a comissão total do franqueado.",
    )

    model = st.radio(
        "Modelo de negócio",
        ["HOME", "OFFICE"],
        horizontal=True,
        key="scenario_model",
    )

    if "rows" not in st.session_state:
        st.session_state.rows = [
            {"product": "Empréstimo Consignado", "sale": 20000.0, "mode": "MÉDIA", "custom": 10.0},
            {"product": "Seguros", "sale": 30000.0, "mode": "MÉDIA", "custom": 23.0},
        ]

    add_col, note_col = st.columns([1, 3.2])
    with add_col:
        if st.button("+ ADICIONAR PRODUTO", use_container_width=True, type="secondary"):
            if len(st.session_state.rows) < 8:
                st.session_state.rows.append(
                    {"product": "Consórcio", "sale": 10000.0, "mode": "MÉDIA", "custom": 4.0}
                )
                st.rerun()
    with note_col:
        st.markdown(
            '<div class="fine-note">Consignado e Empréstimo Pessoal continuam com repasse de 100%, mesmo no cenário combinado.</div>',
            unsafe_allow_html=True,
        )

    breakdown = []

    for i, row in enumerate(list(st.session_state.rows)):
        with st.container(border=True):
            c1, c2, c3, c4, c5 = st.columns([2.3, 1.35, 1.35, 0.9, 0.45])

            with c1:
                product = st.selectbox(
                    "Produto",
                    list(PRODUCTS.keys()),
                    index=list(PRODUCTS.keys()).index(row["product"]),
                    key=f"p_{i}",
                )

            with c2:
                sale = st.number_input(
                    "Valor da venda (R$)",
                    min_value=0.0,
                    value=float(row["sale"]),
                    step=1000.0,
                    format="%.2f",
                    key=f"s_{i}",
                )

            data = PRODUCTS[product]
            modes = ["MÉDIA", "MÁXIMA", "PERSONALIZADA"] if data["avg"] is not None else ["MÁXIMA", "PERSONALIZADA"]
            current_mode = row["mode"] if row["mode"] in modes else modes[0]

            with c3:
                mode = st.selectbox(
                    "Comissão",
                    modes,
                    index=modes.index(current_mode),
                    key=f"m_{i}",
                )

            with c4:
                if mode == "MÉDIA":
                    rate = float(data["avg"])
                    st.markdown(metric_card("%", pct(rate), "média"), unsafe_allow_html=True)
                elif mode == "MÁXIMA":
                    rate = float(data["max"])
                    st.markdown(metric_card("%", pct(rate), "máxima"), unsafe_allow_html=True)
                else:
                    minimum = float(data.get("min", 0.1))
                    default = min(max(float(row["custom"]), minimum), float(data["max"]))
                    rate = st.number_input(
                        "%",
                        min_value=minimum,
                        max_value=float(data["max"]),
                        value=default,
                        step=0.1,
                        key=f"r_{i}",
                    )

            with c5:
                st.write("")
                if st.button("×", key=f"del_{i}", use_container_width=True, type="secondary"):
                    if len(st.session_state.rows) > 1:
                        st.session_state.rows.pop(i)
                        st.rerun()

            st.session_state.rows[i] = {
                "product": product,
                "sale": sale,
                "mode": mode,
                "custom": float(rate),
            }

            gross = sale * rate / 100
            share = share_for(product, model)
            net = gross * share

            breakdown.append(
                {
                    "product": product,
                    "sale": sale,
                    "rate": rate,
                    "gross": gross,
                    "share": share,
                    "net": net,
                }
            )

    total_sales = sum(x["sale"] for x in breakdown)
    total_gross = sum(x["gross"] for x in breakdown)
    total_net = sum(x["net"] for x in breakdown)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    a, b, c = st.columns(3, gap="medium")
    with a:
        st.markdown(metric_card("TOTAL VENDIDO", brl(total_sales), "soma das vendas simuladas"), unsafe_allow_html=True)
    with b:
        st.markdown(metric_card("COMISSÃO GERADA", brl(total_gross), "antes dos repasses"), unsafe_allow_html=True)
    with c:
        st.markdown(metric_card("PARA O FRANQUEADO", brl(total_net), f"cenário {model}"), unsafe_allow_html=True)

    with st.expander("Ver cálculo por produto"):
        for item in breakdown:
            repasse = "100%" if item["share"] == 1 else pct(item["share"] * 100)
            st.markdown(
                f"**{item['product']}** — {brl(item['sale'])} × {pct(item['rate'])} "
                f"= {brl(item['gross'])} de comissão → repasse {repasse} → **{brl(item['net'])}**"
            )

    if st.button("CALCULAR E REVELAR CENÁRIO", use_container_width=True, type="primary", key="scenario_reveal"):
        reveal_amount(total_net, "COMISSÃO TOTAL DO FRANQUEADO NESTE CENÁRIO")


# ============================================================
# APP
# ============================================================
hero()
nav()

page = st.session_state.get("page", "Comissões")

if page == "Comissões":
    page_commissions()
elif page == "Individual":
    page_individual()
else:
    page_scenario()

st.markdown(
    '<div class="fine-note">Simulações ilustrativas. Percentuais e condições podem variar conforme produto e operação.</div>',
    unsafe_allow_html=True,
)
