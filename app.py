import streamlit as st
import json
import os
import uuid
import pandas as pd

# ==============================================================================
# CONFIGURAÇÃO DE CREDENCIAIS DE ADMINISTRADOR
# ==============================================================================
USUARIO_ADMIN = "admin"
SENHA_ADMIN = "ggape@2026"

# ==============================================================================
# GESTÃO DE DADOS (PERSISTÊNCIA EM JSON)
# ==============================================================================
ARQUIVO_DADOS = "dados_pesquisa.json"

PERGUNTAS_LIKERT = [
    "1. Tenho clareza sobre os objetivos e metas da organização para os próximos meses.",
    "2. Tenho clareza sobre meus objetivos individuais desse ano.",
    "3. Compreendo claramente como o meu trabalho diário contribui para o sucesso da organização.",
    "4. A organização comunica de forma clara os novos projetos e as mudanças, explicando seus motivos e impactos.",
    "5. Sinto segurança para expressar minhas opiniões, ideias ou preocupações para minha liderança direta.",
    "6. As relações de trabalho são saudáveis e produtivas.",
    "7. Vejo possibilidades para continuar me desenvolvendo e crescendo na organização.",
    "8. As promoções são feitas com objetividade e mérito.",
    "9. As atividades e responsabilidades que desenvolvo são compatíveis com o cargo que eu ocupo.",
    "10. As pessoas aqui são bem tratadas independentemente de sua idade, gênero, raça e orientação sexual.",
    "11. Eu me sinto pertencente ao meu time.",
    "12. Eu me sinto pertencente à Parceiros da Educação.",
    "13. A Parceiros da Educação possui iniciativas efetivas, programas e políticas que promovem a diversidade, equidade e inclusão.",
    "14. As lideranças da Parceiros da Educação estão preparadas para gerenciar ocorrências de discriminação promovendo um ambiente acolhedor e inclusivo.",
    "15. Minha liderança direta se comunica de forma clara e objetiva.",
    "16. Minha liderança direta gerencia o time de forma humanizada conciliando a produtividade e as necessidades pessoais.",
    "17. Minha liderança direta organiza as demandas de forma equitativa dentro do time.",
    "18. Minha liderança direta me oferece o apoio e a orientação necessários para realização do meu trabalho.",
    "19. Meu trabalho tem um propósito especial. Para mim, não é só 'mais um emprego'.",
    "20. Sinto que eu faço a diferença aqui.",
    "21. Sinto-me motivado(a) e engajado(a) com as minhas atividades atuais.",
    "22. A organização oferece recursos tecnológicos e ferramentais para realizar meu trabalho com eficiência.",
    "23. O ambiente de trabalho na minha equipe é colaborativo.",
    "24. De modo geral, minha carga de trabalho me permite ter equilíbrio entre minha vida pessoal e profissional."
]

OPCOES_TEMPO_CARREIRA = ["Menos de 1 ano", "2 a 3 anos", "3 a 5 anos", "Mais do que 5 anos"]

def carregar_dados():
    """Carrega ou inicializa a base de dados da pesquisa."""
    if not os.path.exists(ARQUIVO_DADOS):
        dados_iniciais = {
            "areas": ["Projetos", "Recursos Humanos", "Financeiro/Administrativo", "Operações", "Comunicação"],
            "tokens": {},
            "respostas": []
        }
        salvar_dados(dados_iniciais)
        return dados_iniciais

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(dados):
    """Guarda a estrutura de dados atualizada no ficheiro JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Configuração da página Streamlit
st.set_page_config(page_title="Pesquisa de Clima - Parceiros da Educação", layout="wide")
dados = carregar_dados()

# Inicialização da variável de estado de autenticação no Session State
if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

# Menu Lateral de Navegação
st.sidebar.title("Navegação")
opcao_menu = st.sidebar.radio(
    "Escolha o Módulo:",
    ["1. Responder Pesquisa", "2. Painel Admin", "3. Dashboard de Resultados"]
)

# ==============================================================================
# MÓDULO 1: RESPONDER PESQUISA (Acesso Público com Token)
# ==============================================================================
if opcao_menu == "1. Responder Pesquisa":
    st.title("📋 Pesquisa de Clima - Parceiros da Educação")
    st.write("A sua opinião é fundamental. A sua resposta é **100% anónima**.")

    token_input = st.text_input("Insira o seu Token de Acesso Único:", type="password")

    if token_input:
        token_limpo = token_input.strip()
        
        if token_limpo not in dados["tokens"]:
            st.error("Token inválido. Verifique o código fornecido.")
        elif dados["tokens"][token_limpo]["usado"]:
            st.warning("Este token já foi utilizado para responder à pesquisa.")
        else:
            st.success("Token validado!")
            
            with st.form(key="form_pesquisa_sequencial"):
                area_selecionada = st.selectbox("Selecione a sua Área Funcional:", dados["areas"])
                st.divider()

                respostas_likert = []
                st.caption("Para as questões abaixo: 1 = Discordo Totalmente | 3 = Neutro | 5 = Concordo Totalmente")
                
                for idx, pergunta in enumerate(PERGUNTAS_LIKERT):
                    st.write(f"**{pergunta}**")
                    nota = st.radio(
                        label=f"q_{idx}",
                        options=[1, 2, 3, 4, 5],
                        index=2,
                        horizontal=True,
                        key=f"likert_{idx}",
                        label_visibility="collapsed"
                    )
                    respostas_likert.append(nota)
                    st.divider()

                st.write("**25. Em uma escala de 0 a 10, qual a probabilidade de você recomendar nossa organização como um bom lugar para trabalhar?**")
                nota_enps = st.slider("Selecione uma nota de 0 a 10:", min_value=0, max_value=10, value=8)
                st.divider()

                st.write('**26. No meu plano de carreira, me vejo trabalhando na Parceiros por:**')
                tempo_carreira = st.radio("Selecione uma opção:", OPCOES_TEMPO_CARREIRA, index=0)
                st.divider()

                st.write("**27. Para você, quais são as fortalezas de trabalhar ou o que você mais valoriza na Parceiros da Educação? (opcional)**")
                fortalezas = st.text_area("Fortalezas:", key="f_txt", label_visibility="collapsed")
                st.divider()

                st.write("**28. Para você, quais são as oportunidades de melhoria na Parceiros da Educação? (opcional)**")
                melhorias = st.text_area("Oportunidades de melhoria:", key="m_txt", label_visibility="collapsed")
                st.divider()

                st.write("**29. Comentários gerais (Campo aberto)**")
                comentarios_gerais = st.text_area("Comentários gerais:", key="c_txt", label_visibility="collapsed")

                submeter = st.form_submit_button("Submeter Resposta")

                if submeter:
                    dados["respostas"].append({
                        "area": area_selecionada,
                        "likert": respostas_likert,
                        "enps": nota_enps,
                        "tempo_carreira": tempo_carreira,
                        "fortalezas": fortalezas,
                        "melhorias": melhorias,
                        "comentarios_gerais": comentarios_gerais
                    })
                    
                    dados["tokens"][token_limpo]["usado"] = True
                    salvar_dados(dados)
                    
                    st.balloons()
                    st.success("Obrigado! A sua resposta foi registada com sucesso.")

# ==============================================================================
# MÓDULO 2: PAINEL DE ADMINISTRAÇÃO (Protegido por Login)
# ==============================================================================
elif opcao_menu == "2. Painel Admin":
    st.title("⚙️ Painel de Administração")

    # VERIFICAÇÃO DE LOGIN
    if not st.session_state["admin_autenticado"]:
        st.subheader("🔐 Acesso Restrito - Autenticação de Administrador")
        
        with st.form(key="form_login"):
            usuario_input = st.text_input("Utilizador:")
            senha_input = st.text_input("Palavra-passe:", type="password")
            btn_login = st.form_submit_button("Entrar no Painel")

            if btn_login:
                if usuario_input == USUARIO_ADMIN and senha_input == SENHA_ADMIN:
                    st.session_state["admin_autenticado"] = True
                    st.success("Autenticação efetuada com sucesso!")
                    st.rerun() # Recarrega a página para exibir o painel completo
                else:
                    st.error("Utilizador ou palavra-passe incorretos.")
    else:
        # BARRINHA DE SESSÃO ATIVA E BOTÃO DE LOGOUT
        col_boas_vindas, col_logout = st.columns([4, 1])
        col_boas_vindas.success("Sessão ativa como Administrador")
        if col_logout.button("Sair (Logout)"):
            st.session_state["admin_autenticado"] = False
            st.rerun()

        st.divider()

        # CONTEÚDO PROTEGIDO DO PAINEL ADMIN
        tab_areas, tab_tokens = st.tabs(["Gerir Áreas Funcionais", "Gerar Tokens"])

        with tab_areas:
            st.subheader("Gerir Áreas Funcionais")
            novas_areas_txt = st.text_area("Insira uma área por linha:", value="\n".join(dados["areas"]), height=150)
            if st.button("Guardar Áreas"):
                dados["areas"] = [a.strip() for a in novas_areas_txt.split("\n") if a.strip()]
                salvar_dados(dados)
                st.success("Áreas atualizadas com sucesso!")

        with tab_tokens:
            st.subheader("Gerador de Tokens de Acesso")
            qtd = st.number_input("Quantidade de tokens a gerar:", min_value=1, max_value=500, value=15)
            if st.button("Gerar Tokens"):
                novos = [str(uuid.uuid4())[:8].upper() for _ in range(qtd)]
                for t in novos:
                    dados["tokens"][t] = {"usado": False}
                salvar_dados(dados)
                st.success(f"{qtd} tokens gerados!")
                st.code("\n".join(novos))

# ==============================================================================
# MÓDULO 3: DASHBOARD DE RESULTADOS
# ==============================================================================
elif opcao_menu == "3. Dashboard de Resultados":
    st.title("📊 Dashboard - Parceiros da Educação")

    if not dados["respostas"]:
        st.info("Ainda não existem respostas registadas para análise.")
    else:
        df_bruto = pd.DataFrame(dados["respostas"])
        st.metric("Total de Respostas Submetidas", len(df_bruto))

        contagem_area = df_bruto["area"].value_counts()
        areas_protegidas = contagem_area[contagem_area < 5].index.tolist()

        df_bruto["area_exibicao"] = df_bruto["area"].apply(
            lambda a: "Outras Áreas (Agrupadas por Privacidade)" if a in areas_protegidas else a
        )

        st.subheader("Distribuição de Respostas por Área")
        st.caption("Nota: Áreas com menos de 5 respostas são agrupadas automaticamente.")
        st.bar_chart(df_bruto["area_exibicao"].value_counts())

        areas_lista = ["Todas as Áreas"] + list(df_bruto["area_exibicao"].unique())
        filtro_area = st.selectbox("Filtrar Dashboard por Área:", areas_lista)
        
        df_filtrado = df_bruto if filtro_area == "Todas as Áreas" else df_bruto[df_bruto["area_exibicao"] == filtro_area]

        st.divider()

        st.subheader("Favorabilidade (Questões 1 a 24)")
        res_likert = []
        for idx, pergunta in enumerate(PERGUNTAS_LIKERT):
            notas = [r[idx] for r in df_filtrado["likert"] if idx < len(r)]
            if notas:
                tot = len(notas)
                fav = sum(1 for n in notas if n >= 4)
                res_likert.append({
                    "Pergunta": pergunta,
                    "% Favorável": f"{round((fav/tot)*100, 1)}%",
                    "Favoráveis (4-5)": fav,
                    "Neutros (3)": sum(1 for n in notas if n == 3),
                    "Desfavoráveis (1-2)": sum(1 for n in notas if n <= 2),
                    "Total": tot
                })
        st.dataframe(pd.DataFrame(res_likert), use_container_width=True)

        st.divider()

        st.subheader("eNPS - Recomendação (Questão 25)")
        notas_enps = df_filtrado["enps"].tolist()
        if notas_enps:
            tot_enps = len(notas_enps)
            promotores = sum(1 for n in notas_enps if n >= 9)
            detretores = sum(1 for n in notas_enps if n <= 6)
            enps_score = round(((promotores - detretores) / tot_enps) * 100, 1)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("eNPS Score", f"{enps_score}")
            c2.metric("Promotores (9-10)", f"{promotores} ({round(promotores/tot_enps*100)}%)")
            c3.metric("Detretores (0-6)", f"{detretores} ({round(detretores/tot_enps*100)}%)")

        st.divider()

        st.subheader("Plano de Carreira (Questão 26)")
        st.bar_chart(df_filtrado["tempo_carreira"].value_counts())

        st.divider()

        st.subheader("Análise Qualitativa (Questões 27 a 29)")
        tab_f, tab_m, tab_c = st.tabs(["27. Fortalezas", "28. Oportunidades de Melhoria", "29. Comentários Gerais"])
        
        with tab_f:
            for txt in df_filtrado["fortalezas"].dropna():
                if txt.strip():
                    st.info(f"💬 \"{txt}\"")

        with tab_m:
            for txt in df_filtrado["melhorias"].dropna():
                if txt.strip():
                    st.warning(f"💬 \"{txt}\"")

        with tab_c:
            for txt in df_filtrado["comentarios_gerais"].dropna():
                if txt.strip():
                    st.write(f"💬 \"{txt}\"")
