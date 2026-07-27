import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Pan-Species Bio-Engine", layout="wide")

st.title("Pan-Species Immunological Response Tool")

with st.expander("About My Project & How to Read This Page"):
    st.markdown("""
    **The goal of this project**

    Animals handle infections from viruses or bacteria differently. I built this tool to take genetic data from humans and animals, match up the genes they share, and see if their cells fight back diseases the exact same way (conserved) or differently (divergent).

    **How to read the graph:**
    * 🔴 :red[**Human-Specific Hyperactivation:**] The human body has a severe hyper-reactive response that may cause harm to the human cells rather than the pathogen.
    * 🟢 :green[**Conserved Immunity:**] Both humans and the animals activate this gene equally to fight off the infection.
    * 🔵 :blue[**Animal-Specific Protection:**] The animal host activates defensive genes that protect it from getting sick, making it more tolerant to diseases.

    **How to interact with it:** Use the sliders in the left sidebar to change how filtered the data is.

    **Cited sources for this project:** NCBI GEO (Gene Expression Omnibus), Ensembl BioMart
    """)

st.sidebar.header("Data Filters")
st.sidebar.markdown("Adjust these sliders to filter out the data. Hover over the question mark to learn more.")

p_thresh = st.sidebar.slider(
    "Data Credibility (p-value)",
    0.001, 0.100, 0.050, step=0.005,
    help="This measures data credibility. Slide left to only look at guaranteed data points. Slide right to see a broader view."
)

fc_thresh = st.sidebar.slider(
    "Gene Activation Level (Log2 Fold Change)",
    0.5, 4.0, 1.2, step=0.1,
    help="This measures how intensely a gene woke up and started fighting after infection. Higher values only show massive cellular reactions."
)

delta_margin = st.sidebar.slider(
    "Response Variance Margin (Divergence Delta)",
    0.5, 3.0, 1.5, step=0.1,
    help="The mathematical gap between species. Gene responses that exceed this setting are categorized as divergent."
)


@st.cache_data
def load_real_transcriptomic_data():
    return pd.read_csv("real_data.csv")

df = load_real_transcriptomic_data()

sig_df = df[(df['Human_pValue'] <= p_thresh) & (df['Animal_pValue'] <= p_thresh)].copy()
sig_df['Expression_Delta'] = (sig_df['Human_Log2FC'] - sig_df['Animal_Log2FC']).abs()



conds = [

    (sig_df['Expression_Delta'] <= delta_margin) & (sig_df['Human_Log2FC'].abs() >= fc_thresh) & (sig_df['Animal_Log2FC'].abs() >= fc_thresh),


    (sig_df['Human_Log2FC'].abs() >= fc_thresh) & (sig_df['Human_Log2FC'] - sig_df['Animal_Log2FC'] > delta_margin),


    (sig_df['Animal_Log2FC'].abs() >= fc_thresh) & (sig_df['Animal_Log2FC'] - sig_df['Human_Log2FC'] > delta_margin)
]

labels = ['Conserved Immunity', 'Human-Specific Hyperactivation', 'Animal-Specific Protection']
sig_df['Evolutionary_Classification'] = np.select(conds, labels, default='Low-Variance Base Response')

def format_delta_label(row):
    if row['Human_Log2FC'] > row['Animal_Log2FC']:
        return f"Human (+{row['Expression_Delta']:.2f})"
    elif row['Animal_Log2FC'] > row['Human_Log2FC']:
        return f"Animal (+{row['Expression_Delta']:.2f})"
    else:
        return "Perfect Match (0.00)"

sig_df['Infection_Response_Gap'] = sig_df.apply(format_delta_label, axis=1)


true_filtered_df = sig_df[sig_df['Evolutionary_Classification'] != 'Low-Variance Base Response']

with st.container(border=True):
    st.markdown("#### Filtered Output Summary")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Total Genes Active", len(true_filtered_df))
    with col_m2:
        conserved_pct = (true_filtered_df['Evolutionary_Classification'] == 'Conserved Immunity').sum() / max(len(true_filtered_df), 1) * 100
        st.metric("Same-Reaction Rate", f"{conserved_pct:.1f}%")
    with col_m3:
        divergent_pct = (true_filtered_df['Evolutionary_Classification'].str.contains('Specific')).sum() / max(len(true_filtered_df), 1) * 100
        st.metric("Different-Reaction Rate", f"{divergent_pct:.1f}%")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Interactive Graph", "Data Spreadsheet", "Vocabulary & Concept Reference"])

with tab1:
    st.markdown("#### Distribution Map")
    st.markdown("*Hover your cursor over the individual dots to see the data details for each gene. The dotted diagonal line represents a perfect match where both species reacted the same to the pathogen.*")


    fig = px.scatter(
        true_filtered_df,
        x='Animal_Log2FC',
        y='Human_Log2FC',
        color='Evolutionary_Classification',
        hover_name='Gene_Symbol',
        hover_data={
            'Evolutionary_Classification': True,
            'Functional_Pathway': True,
            'Human_Log2FC': ':.2f',
            'Animal_Log2FC': ':.2f',
            'Infection_Response_Gap': True
        },
        color_discrete_map={
            'Conserved Immunity': '#00CC96',
            'Human-Specific Hyperactivation': '#EF553B',
            'Animal-Specific Protection': '#636EFA'
        },
        labels={
            'Evolutionary_Classification': 'Classification',
            'Functional_Pathway': 'Pathway',
            'Human_Log2FC': 'Human Reaction Level (Log2FC)',
            'Animal_Log2FC': 'Animal Reaction Level (Log2FC)',
            'Infection_Response_Gap': 'Higher Reaction'
        }
    )
    fig.add_shape(type="line", x0=-1, y0=-1, x1=6, y1=6, line=dict(color="gray", width=1.5, dash="dot"))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("#### Filtered Transcripts Reference Table")
    st.markdown("This spreadsheet lists every gene that successfully passes the sidebar filters. You can sort rows by clicking on the headers or look up specific values below.")
    st.dataframe(true_filtered_df[['Gene_Symbol', 'Functional_Pathway', 'Human_Log2FC', 'Animal_Log2FC', 'Evolutionary_Classification']], use_container_width=True)

with tab3:
    st.markdown("#### Vocabulary")
    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.markdown("""
        **Biology Concepts:**
        * **Gene Symbol:** The unique code name assigned to a specific gene.
        * **Conserved Immunity:** When humans and animals activate the exact same genes at the same intensity to fight off pathogens.
        * **Divergent Immunity:** When humans and animals react to a pathogen very differently.
        """)

    with col_info2:
        st.markdown("""
        **Data & Control Settings:**
        * **Data Credibility (p-value):** The probability that a gene change was a random accident, where lower values mean more reliable data.
        * **Gene Activation Level (Log2FC):** The baseline score showing how much a gene woke up and changed its behavior after infection.
        * **Response Variance Margin (Divergence Delta):** The targeted mathematical gap size used to decide if the species reacted differently.
        """)

st.markdown("---")
st.caption("Pan-Species Immunological Response Tool | Independent Project")
