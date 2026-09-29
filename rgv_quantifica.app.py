import math
import streamlit as st


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="RGV Quantifica",
    page_icon="🏗️",
    layout="wide"
)


# ============================================================
# BANCO DE COMPOSIÇÕES
# ============================================================

def inicializar_composicoes():

    if "composicoes" not in st.session_state:

        st.session_state.composicoes = [

            {
                "nome": "Argamassa de assentamento",
                "categoria": "Argamassa",
                "unidade": "m³",
                "traco_cimento": 1.0,
                "traco_areia": 2.0,
                "traco_barro": 8.0,
                "consumo_cimento_m3": 300.0,
                "consumo_areia_m3": 1.000,
                "consumo_barro_m3": 0.000,
                "perda": 5.0,
                "espessura_cm": 0.0
            },

            {
                "nome": "Reboco interno",
                "categoria": "Reboco",
                "unidade": "m³",
                "traco_cimento": 1.0,
                "traco_areia": 4.0,
                "traco_barro": 0.0,
                "consumo_cimento_m3": 300.0,
                "consumo_areia_m3": 1.000,
                "consumo_barro_m3": 0.000,
                "perda": 5.0,
                "espessura_cm": 1.5
            },

            {
                "nome": "Reboco externo",
                "categoria": "Reboco",
                "unidade": "m³",
                "traco_cimento": 1.0,
                "traco_areia": 3.0,
                "traco_barro": 0.0,
                "consumo_cimento_m3": 300.0,
                "consumo_areia_m3": 1.000,
                "consumo_barro_m3": 0.000,
                "perda": 5.0,
                "espessura_cm": 2.0
            }
        ]


inicializar_composicoes()


# ============================================================
# FUNÇÕES DE CÁLCULO
# ============================================================

def calcular_area_abertura(
    quantidade,
    largura,
    altura
):
    return quantidade * largura * altura


def calcular_blocos(
    area_parede,
    comprimento_cm,
    altura_cm,
    junta_cm,
    perda
):

    comprimento_modular_cm = (
        comprimento_cm + junta_cm
    )

    altura_modular_cm = (
        altura_cm + junta_cm
    )

    area_modular = (
        (comprimento_modular_cm / 100)
        *
        (altura_modular_cm / 100)
    )

    if area_modular <= 0:
        return 0, 0, 0

    quantidade_geometrica = (
        area_parede / area_modular
    )

    quantidade_compra = math.ceil(
        quantidade_geometrica
        *
        (1 + perda / 100)
    )

    return (
        quantidade_geometrica,
        quantidade_compra,
        area_modular
    )


def calcular_argamassa_juntas(
    area_parede,
    espessura_bloco_cm,
    comprimento_bloco_cm,
    altura_bloco_cm,
    junta_cm,
    perda_argamassa
):
    """
    Estimativa geométrica da argamassa das juntas.

    Hipóteses:
    - A espessura da parede é igual à espessura do bloco.
    - O bloco é considerado como um volume geométrico maciço.
    - A quantidade geométrica de blocos é utilizada,
      sem aplicar a perda de compra.
    - Não são considerados vazios internos do bloco.
    """

    espessura_m = (
        espessura_bloco_cm / 100
    )

    comprimento_m = (
        comprimento_bloco_cm / 100
    )

    altura_m = (
        altura_bloco_cm / 100
    )

    comprimento_modular_m = (
        (comprimento_bloco_cm + junta_cm)
        / 100
    )

    altura_modular_m = (
        (altura_bloco_cm + junta_cm)
        / 100
    )

    area_modular = (
        comprimento_modular_m
        *
        altura_modular_m
    )

    if (
        area_modular <= 0
        or espessura_m <= 0
        or comprimento_m <= 0
        or altura_m <= 0
    ):
        return 0, 0, 0, 0

    quantidade_geometrica = (
        area_parede
        /
        area_modular
    )

    volume_unitario_bloco = (
        comprimento_m
        *
        altura_m
        *
        espessura_m
    )

    volume_blocos = (
        quantidade_geometrica
        *
        volume_unitario_bloco
    )

    volume_parede = (
        area_parede
        *
        espessura_m
    )

    volume_argamassa = (
        volume_parede
        -
        volume_blocos
    )

    volume_argamassa = max(
        volume_argamassa,
        0
    )

    volume_com_perda = (
        volume_argamassa
        *
        (
            1
            +
            perda_argamassa / 100
        )
    )

    return (
        volume_argamassa,
        volume_com_perda,
        volume_blocos,
        volume_unitario_bloco
    )


def calcular_composicao_por_volume(
    volume_argamassa,
    consumo_cimento_m3,
    consumo_areia_m3,
    consumo_barro_m3
):

    cimento = (
        volume_argamassa
        *
        consumo_cimento_m3
    )

    areia = (
        volume_argamassa
        *
        consumo_areia_m3
    )

    barro = (
        volume_argamassa
        *
        consumo_barro_m3
    )

    return (
        cimento,
        areia,
        barro
    )


def calcular_reboco_volume(
    area,
    espessura_cm
):

    espessura_m = (
        espessura_cm / 100
    )

    return (
        area
        *
        espessura_m
    )


# ============================================================
# TÍTULO
# ============================================================

st.title("🏗️ RGV Quantifica")

st.caption(
    "Sistema de quantitativos e composição de materiais"
)

st.info(
    "🔬 Versão v0.1 — Protótipo em validação técnica. "
    "Os parâmetros e fórmulas deverão ser avaliados "
    "e ajustados conforme critérios técnicos de engenharia."
)


# ============================================================
# DADOS DO PROJETO
# ============================================================

st.header("📁 Dados do Projeto")

col1, col2, col3, col4 = st.columns(4)

with col1:

    nome_projeto = st.text_input(
        "Nome do projeto"
    )

with col2:

    cliente = st.text_input(
        "Cliente"
    )

with col3:

    local = st.text_input(
        "Local"
    )

with col4:

    responsavel = st.text_input(
        "Responsável"
    )


# ============================================================
# MÓDULO
# ============================================================

st.header("🧩 Módulo")

modulo = st.selectbox(
    "Selecione o módulo",
    [
        "Construção",
        "Hidráulica",
        "Elétrica",
        "Pintura",
        "Climatização",
        "Telhado / Cobertura",
        "Jardinagem"
    ]
)


# ============================================================
# CONSTRUÇÃO
# ============================================================

if modulo == "Construção":

    st.header("🏗️ Construção")


    # ========================================================
    # BANCO DE COMPOSIÇÕES
    # ========================================================

    st.subheader("🧱 Banco de Composições")

    st.write(
        "Cadastre e gerencie as composições utilizadas "
        "nos cálculos do projeto."
    )

    st.info(
        "Traço representa a proporção da composição. "
        "Consumo representa o consumo real do material "
        "por unidade de cálculo. Os dois valores são "
        "independentes."
    )


    # ========================================================
    # ADICIONAR COMPOSIÇÃO
    # ========================================================

    with st.expander(
        "➕ Adicionar nova composição",
        expanded=False
    ):

        col1, col2, col3 = st.columns(3)

        with col1:

            novo_nome = st.text_input(
                "Nome da composição",
                key="novo_nome"
            )

        with col2:

            nova_categoria = st.selectbox(
                "Categoria",
                [
                    "Argamassa",
                    "Reboco",
                    "Concreto",
                    "Contrapiso",
                    "Outro"
                ],
                key="nova_categoria"
            )

        with col3:

            nova_unidade = st.selectbox(
                "Unidade base",
                [
                    "m³",
                    "m²"
                ],
                key="nova_unidade"
            )


        st.markdown("### Traço")

        col1, col2, col3 = st.columns(3)

        with col1:

            novo_traco_cimento = st.number_input(
                "Cimento",
                min_value=0.0,
                value=1.0,
                step=0.5,
                key="novo_traco_cimento"
            )

        with col2:

            novo_traco_areia = st.number_input(
                "Areia",
                min_value=0.0,
                value=4.0,
                step=0.5,
                key="novo_traco_areia"
            )

        with col3:

            novo_traco_barro = st.number_input(
                "Barro",
                min_value=0.0,
                value=0.0,
                step=0.5,
                key="novo_traco_barro"
            )


        st.markdown("### Consumo por m³")

        col1, col2, col3 = st.columns(3)

        with col1:

            novo_consumo_cimento = st.number_input(
                "Cimento (kg/m³)",
                min_value=0.0,
                value=300.0,
                step=10.0,
                key="novo_consumo_cimento"
            )

        with col2:

            novo_consumo_areia = st.number_input(
                "Areia (m³/m³)",
                min_value=0.0,
                value=1.0,
                step=0.05,
                key="novo_consumo_areia"
            )

        with col3:

            novo_consumo_barro = st.number_input(
                "Barro (m³/m³)",
                min_value=0.0,
                value=0.0,
                step=0.05,
                key="novo_consumo_barro"
            )


        col1, col2 = st.columns(2)

        with col1:

            nova_perda = st.number_input(
                "Perda (%)",
                min_value=0.0,
                value=5.0,
                step=1.0,
                key="nova_perda"
            )

        with col2:

            nova_espessura = st.number_input(
                "Espessura (cm)",
                min_value=0.0,
                value=1.5,
                step=0.5,
                key="nova_espessura"
            )


        if st.button(
            "💾 Salvar composição",
            key="salvar_composicao"
        ):

            if not novo_nome.strip():

                st.error(
                    "Informe o nome da composição."
                )

            else:

                nova_composicao = {

                    "nome": novo_nome,

                    "categoria": nova_categoria,

                    "unidade": nova_unidade,

                    "traco_cimento":
                        novo_traco_cimento,

                    "traco_areia":
                        novo_traco_areia,

                    "traco_barro":
                        novo_traco_barro,

                    "consumo_cimento_m3":
                        novo_consumo_cimento,

                    "consumo_areia_m3":
                        novo_consumo_areia,

                    "consumo_barro_m3":
                        novo_consumo_barro,

                    "perda":
                        nova_perda,

                    "espessura_cm":
                        nova_espessura
                }

                st.session_state.composicoes.append(
                    nova_composicao
                )

                st.success(
                    "Composição adicionada com sucesso!"
                )

                st.rerun()


    # ========================================================
    # LISTA DE COMPOSIÇÕES
    # ========================================================

    st.markdown("### 📋 Composições cadastradas")

    if len(st.session_state.composicoes) == 0:

        st.warning(
            "Nenhuma composição cadastrada."
        )

    else:

        for indice, composicao in enumerate(
            st.session_state.composicoes
        ):

            with st.expander(
                f"🧱 {composicao['nome']} "
                f"— {composicao['categoria']}"
            ):

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.write(
                        f"**Unidade:** "
                        f"{composicao['unidade']}"
                    )

                with col2:

                    st.write(
                        "**Traço:** "
                        f"{composicao['traco_cimento']:.1f} : "
                        f"{composicao['traco_areia']:.1f} : "
                        f"{composicao['traco_barro']:.1f}"
                    )

                with col3:

                    st.write(
                        "**Cimento:** "
                        f"{composicao['consumo_cimento_m3']:.2f} kg/m³"
                    )

                with col4:

                    st.write(
                        "**Perda:** "
                        f"{composicao['perda']:.1f}%"
                    )


                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✏️ Editar",
                        key=f"editar_{indice}"
                    ):

                        st.session_state[
                            "composicao_editando"
                        ] = indice

                        st.rerun()


                with col2:

                    if st.button(
                        "🗑️ Excluir",
                        key=f"excluir_{indice}"
                    ):

                        if len(
                            st.session_state.composicoes
                        ) > 1:

                            st.session_state.composicoes.pop(
                                indice
                            )

                            if (
                                "composicao_editando"
                                in st.session_state
                            ):

                                del st.session_state[
                                    "composicao_editando"
                                ]

                            st.success(
                                "Composição excluída."
                            )

                            st.rerun()

                        else:

                            st.warning(
                                "Mantenha pelo menos uma "
                                "composição cadastrada."
                            )


    # ========================================================
    # EDITAR COMPOSIÇÃO
    # ========================================================

    if (
        "composicao_editando"
        in st.session_state
    ):

        indice = (
            st.session_state
            .composicao_editando
        )

        if (
            0 <= indice
            < len(
                st.session_state.composicoes
            )
        ):

            composicao = (
                st.session_state
                .composicoes[indice]
            )

            st.divider()

            st.subheader(
                "✏️ Editar composição"
            )

            categorias = [
                "Argamassa",
                "Reboco",
                "Concreto",
                "Contrapiso",
                "Outro"
            ]

            unidades = [
                "m³",
                "m²"
            ]

            col1, col2, col3 = st.columns(3)

            with col1:

                nome_editado = st.text_input(
                    "Nome",
                    value=composicao["nome"],
                    key="edit_nome"
                )

            with col2:

                categoria_editada = st.selectbox(
                    "Categoria",
                    categorias,
                    index=categorias.index(
                        composicao["categoria"]
                    ),
                    key="edit_categoria"
                )

            with col3:

                unidade_editada = st.selectbox(
                    "Unidade",
                    unidades,
                    index=unidades.index(
                        composicao["unidade"]
                    ),
                    key="edit_unidade"
                )


            st.markdown("### Traço")

            col1, col2, col3 = st.columns(3)

            with col1:

                traco_cimento_editado = st.number_input(
                    "Cimento",
                    min_value=0.0,
                    value=float(
                        composicao[
                            "traco_cimento"
                        ]
                    ),
                    step=0.5,
                    key="edit_traco_cimento"
                )

            with col2:

                traco_areia_editado = st.number_input(
                    "Areia",
                    min_value=0.0,
                    value=float(
                        composicao[
                            "traco_areia"
                        ]
                    ),
                    step=0.5,
                    key="edit_traco_areia"
                )

            with col3:

                traco_barro_editado = st.number_input(
                    "Barro",
                    min_value=0.0,
                    value=float(
                        composicao[
                            "traco_barro"
                        ]
                    ),
                    step=0.5,
                    key="edit_traco_barro"
                )


            st.markdown("### Consumo por m³")

            col1, col2, col3 = st.columns(3)

            with col1:

                consumo_cimento_editado = st.number_input(
                    "Cimento (kg/m³)",
                    min_value=0.0,
                    value=float(
                        composicao[
                            "consumo_cimento_m3"
                        ]
                    ),
                    step=10.0,
                    key="edit_consumo_cimento"
                )

            with col2:

                consumo_areia_editado = st.number_input(
                    "Areia (m³/m³)",
                    min_value=0.0,
                    value=float(
                        composicao[
                            "consumo_areia_m3"
                        ]
                    ),
                    step=0.05,
                    key="edit_consumo_areia"
                )

            with col3:

                consumo_barro_editado = st.number_input(
                    "Barro (m³/m³)",
                    min_value=0.0,
                    value=float(
                        composicao[
                            "consumo_barro_m3"
                        ]
                    ),
                    step=0.05,
                    key="edit_consumo_barro"
                )


            col1, col2 = st.columns(2)

            with col1:

                perda_editada = st.number_input(
                    "Perda (%)",
                    min_value=0.0,
                    value=float(
                        composicao[
                            "perda"
                        ]
                    ),
                    step=1.0,
                    key="edit_perda"
                )

            with col2:

                espessura_editada = st.number_input(
                    "Espessura (cm)",
                    min_value=0.0,
                    value=float(
                        composicao[
                            "espessura_cm"
                        ]
                    ),
                    step=0.5,
                    key="edit_espessura"
                )


            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Atualizar composição",
                    key="atualizar_composicao"
                ):

                    if not nome_editado.strip():

                        st.error(
                            "Informe o nome da composição."
                        )

                    else:

                        composicao["nome"] = (
                            nome_editado
                        )

                        composicao["categoria"] = (
                            categoria_editada
                        )

                        composicao["unidade"] = (
                            unidade_editada
                        )

                        composicao[
                            "traco_cimento"
                        ] = (
                            traco_cimento_editado
                        )

                        composicao[
                            "traco_areia"
                        ] = (
                            traco_areia_editado
                        )

                        composicao[
                            "traco_barro"
                        ] = (
                            traco_barro_editado
                        )

                        composicao[
                            "consumo_cimento_m3"
                        ] = (
                            consumo_cimento_editado
                        )

                        composicao[
                            "consumo_areia_m3"
                        ] = (
                            consumo_areia_editado
                        )

                        composicao[
                            "consumo_barro_m3"
                        ] = (
                            consumo_barro_editado
                        )

                        composicao[
                            "perda"
                        ] = (
                            perda_editada
                        )

                        composicao[
                            "espessura_cm"
                        ] = (
                            espessura_editada
                        )

                        del st.session_state[
                            "composicao_editando"
                        ]

                        st.success(
                            "Composição atualizada!"
                        )

                        st.rerun()


            with col2:

                if st.button(
                    "❌ Cancelar",
                    key="cancelar_edicao"
                ):

                    del st.session_state[
                        "composicao_editando"
                    ]

                    st.rerun()


    # ========================================================
    # AMBIENTES
    # ========================================================

    st.divider()

    st.header("🏠 Ambientes")

    if "ambientes" not in st.session_state:

        st.session_state.ambientes = []


    col1, col2, col3, col4 = st.columns(4)

    with col1:

        nome_ambiente = st.text_input(
            "Nome",
            value="Sala"
        )

    with col2:

        comprimento = st.number_input(
            "Comprimento (m)",
            min_value=0.0,
            value=3.0,
            step=0.10
        )

    with col3:

        largura = st.number_input(
            "Largura (m)",
            min_value=0.0,
            value=3.0,
            step=0.10
        )

    with col4:

        altura = st.number_input(
            "Altura (m)",
            min_value=0.0,
            value=2.80,
            step=0.10
        )


    col1, col2 = st.columns(2)

    with col1:

        inclinacao = st.number_input(
            "Inclinação do piso (%)",
            min_value=0.0,
            value=0.0,
            step=0.5
        )

    with col2:

        perda_piso = st.number_input(
            "Perda do piso (%)",
            min_value=0.0,
            value=10.0,
            step=1.0
        )


    # ========================================================
    # PORTAS
    # ========================================================

    st.markdown("### 🚪 Portas")

    col1, col2, col3 = st.columns(3)

    with col1:

        qtd_portas = st.number_input(
            "Quantidade",
            min_value=0,
            value=1,
            step=1,
            key="qtd_portas"
        )

    with col2:

        largura_porta = st.number_input(
            "Largura (m)",
            min_value=0.0,
            value=0.80,
            step=0.05,
            key="largura_porta"
        )

    with col3:

        altura_porta = st.number_input(
            "Altura (m)",
            min_value=0.0,
            value=2.10,
            step=0.05,
            key="altura_porta"
        )


    # ========================================================
    # JANELAS
    # ========================================================

    st.markdown("### 🪟 Janelas")

    col1, col2, col3 = st.columns(3)

    with col1:

        qtd_janelas = st.number_input(
            "Quantidade",
            min_value=0,
            value=1,
            step=1,
            key="qtd_janelas"
        )

    with col2:

        largura_janela = st.number_input(
            "Largura (m)",
            min_value=0.0,
            value=1.20,
            step=0.05,
            key="largura_janela"
        )

    with col3:

        altura_janela = st.number_input(
            "Altura (m)",
            min_value=0.0,
            value=1.00,
            step=0.05,
            key="altura_janela"
        )


    # ========================================================
    # BLOCOS
    # ========================================================

    st.markdown("### 🧱 Blocos")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        bloco_comprimento = st.number_input(
            "Comprimento (cm)",
            min_value=0.0,
            value=39.0,
            step=1.0
        )

    with col2:

        bloco_altura = st.number_input(
            "Altura (cm)",
            min_value=0.0,
            value=19.0,
            step=1.0
        )

    with col3:

        bloco_espessura = st.number_input(
            "Espessura (cm)",
            min_value=0.0,
            value=14.0,
            step=1.0
        )

    with col4:

        junta_argamassa = st.number_input(
            "Junta de argamassa (cm)",
            min_value=0.0,
            value=1.0,
            step=0.1
        )


    col1, col2 = st.columns(2)

    with col1:

        perda_blocos = st.number_input(
            "Perda dos blocos (%)",
            min_value=0.0,
            value=10.0,
            step=1.0
        )

    with col2:

        perda_argamassa_juntas = st.number_input(
            "Perda da argamassa das juntas (%)",
            min_value=0.0,
            value=5.0,
            step=1.0
        )


    # ========================================================
    # ADICIONAR AMBIENTE
    # ========================================================

    if st.button(
        "➕ Adicionar ambiente"
    ):

        ambiente = {

            "nome": nome_ambiente,

            "comprimento": comprimento,

            "largura": largura,

            "altura": altura,

            "inclinacao": inclinacao,

            "perda_piso": perda_piso,

            "qtd_portas": qtd_portas,

            "largura_porta": largura_porta,

            "altura_porta": altura_porta,

            "qtd_janelas": qtd_janelas,

            "largura_janela": largura_janela,

            "altura_janela": altura_janela,

            "bloco_comprimento":
                bloco_comprimento,

            "bloco_altura":
                bloco_altura,

            "bloco_espessura":
                bloco_espessura,

            "junta_argamassa":
                junta_argamassa,

            "perda_blocos":
                perda_blocos,

            "perda_argamassa_juntas":
                perda_argamassa_juntas
        }

        st.session_state.ambientes.append(
            ambiente
        )

        st.success(
            "Ambiente adicionado!"
        )

        st.rerun()


    # ========================================================
    # CÁLCULOS
    # ========================================================

    if st.session_state.ambientes:

        st.divider()

        st.header("📐 Cálculos")


        # ====================================================
        # COMPOSIÇÃO DAS JUNTAS
        # ====================================================

        composicoes_argamassa = [
            c
            for c in st.session_state.composicoes
            if c["categoria"] == "Argamassa"
        ]

        if composicoes_argamassa:

            nomes_composicoes_argamassa = [
                c["nome"]
                for c in composicoes_argamassa
            ]

            st.subheader(
                "🧱 Composição da argamassa das juntas"
            )

            composicao_juntas_nome = st.selectbox(
                "Selecione a composição",
                nomes_composicoes_argamassa,
                key="composicao_juntas"
            )

            composicao_juntas = next(
                c
                for c in composicoes_argamassa
                if c["nome"]
                == composicao_juntas_nome
            )

            st.success(
                f"**Composição selecionada:** "
                f"{composicao_juntas['nome']}"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.write(
                    f"**Traço:** "
                    f"{composicao_juntas['traco_cimento']:.1f} : "
                    f"{composicao_juntas['traco_areia']:.1f} : "
                    f"{composicao_juntas['traco_barro']:.1f}"
                )

            with col2:

                st.write(
                    f"**Cimento:** "
                    f"{composicao_juntas['consumo_cimento_m3']:.2f} kg/m³"
                )

            with col3:

                st.write(
                    f"**Areia:** "
                    f"{composicao_juntas['consumo_areia_m3']:.3f} m³/m³"
                )

            with col4:

                st.write(
                    f"**Perda:** "
                    f"{composicao_juntas['perda']:.1f}%"
                )

        else:

            composicao_juntas = None

            st.warning(
                "Cadastre pelo menos uma composição "
                "da categoria Argamassa."
            )


        # ====================================================
        # COMPOSIÇÃO DO REBOCO
        # ====================================================

        composicoes_reboco = [
            c
            for c in st.session_state.composicoes
            if c["categoria"] == "Reboco"
        ]

        st.subheader(
            "🎨 Composição do reboco"
        )

        if composicoes_reboco:

            nomes_reboco = [
                c["nome"]
                for c in composicoes_reboco
            ]

            composicao_reboco_nome = st.selectbox(
                "Selecione a composição do reboco",
                nomes_reboco,
                key="composicao_reboco"
            )

            composicao_reboco = next(
                c
                for c in composicoes_reboco
                if c["nome"]
                == composicao_reboco_nome
            )

            st.success(
                f"**Composição selecionada:** "
                f"{composicao_reboco['nome']}"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.write(
                    f"**Traço:** "
                    f"{composicao_reboco['traco_cimento']:.1f} : "
                    f"{composicao_reboco['traco_areia']:.1f} : "
                    f"{composicao_reboco['traco_barro']:.1f}"
                )

            with col2:

                st.write(
                    f"**Espessura:** "
                    f"{composicao_reboco['espessura_cm']:.1f} cm"
                )

            with col3:

                st.write(
                    f"**Cimento:** "
                    f"{composicao_reboco['consumo_cimento_m3']:.2f} kg/m³"
                )

            with col4:

                st.write(
                    f"**Perda:** "
                    f"{composicao_reboco['perda']:.1f}%"
                )

        else:

            composicao_reboco = None

            st.warning(
                "Cadastre pelo menos uma composição "
                "da categoria Reboco."
            )


        # ====================================================
        # TOTAIS DO PROJETO
        # ====================================================

        total_area_piso = 0.0
        total_piso_com_perda = 0.0
        total_parede_liquida = 0.0
        total_blocos = 0
        total_volume_argamassa_juntas = 0.0
        total_cimento_juntas = 0.0
        total_areia_juntas = 0.0
        total_barro_juntas = 0.0
        total_volume_reboco = 0.0
        total_cimento_reboco = 0.0
        total_areia_reboco = 0.0
        total_barro_reboco = 0.0


        # ====================================================
        # PROCESSAR CADA AMBIENTE
        # ====================================================

        for ambiente in st.session_state.ambientes:

            st.subheader(
                f"🏠 {ambiente['nome']}"
            )


            # ------------------------------------------------
            # INICIALIZAÇÃO DAS VARIÁVEIS DO AMBIENTE
            # ------------------------------------------------

            volume_argamassa_juntas = 0.0
            volume_argamassa_juntas_perda = 0.0
            volume_blocos = 0.0
            volume_unitario_bloco = 0.0

            cimento_juntas = 0.0
            areia_juntas = 0.0
            barro_juntas = 0.0

            volume_reboco = 0.0
            cimento_reboco = 0.0
            areia_reboco = 0.0
            barro_reboco = 0.0


            # ------------------------------------------------
            # GEOMETRIA
            # ------------------------------------------------

            comprimento = ambiente["comprimento"]
            largura = ambiente["largura"]
            altura = ambiente["altura"]

            area_piso = (
                comprimento
                *
                largura
            )

            perimetro = (
                2
                *
                (
                    comprimento
                    +
                    largura
                )
            )

            volume = (
                area_piso
                *
                altura
            )

            parede_bruta = (
                perimetro
                *
                altura
            )


            area_portas = calcular_area_abertura(
                ambiente["qtd_portas"],
                ambiente["largura_porta"],
                ambiente["altura_porta"]
            )

            area_janelas = calcular_area_abertura(
                ambiente["qtd_janelas"],
                ambiente["largura_janela"],
                ambiente["altura_janela"]
            )

            area_aberturas = (
                area_portas
                +
                area_janelas
            )

            area_parede_liquida = max(
                parede_bruta
                -
                area_aberturas,
                0
            )

            area_piso_com_perda = (
                area_piso
                *
                (
                    1
                    +
                    ambiente["perda_piso"]
                    / 100
                )
            )


            # ------------------------------------------------
            # TOTALIZAÇÃO GEOMÉTRICA
            # ------------------------------------------------

            total_area_piso += area_piso

            total_piso_com_perda += (
                area_piso_com_perda
            )

            total_parede_liquida += (
                area_parede_liquida
            )


            # ------------------------------------------------
            # EXIBIÇÃO DA GEOMETRIA
            # ------------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Área do piso",
                    f"{area_piso:.2f} m²"
                )

                st.metric(
                    "Perímetro",
                    f"{perimetro:.2f} m"
                )

            with col2:

                st.metric(
                    "Volume",
                    f"{volume:.2f} m³"
                )

                st.metric(
                    "Parede bruta",
                    f"{parede_bruta:.2f} m²"
                )

            with col3:

                st.metric(
                    "Aberturas",
                    f"{area_aberturas:.2f} m²"
                )

                st.metric(
                    "Parede líquida",
                    f"{area_parede_liquida:.2f} m²"
                )


            st.write(
                f"**Piso com perda:** "
                f"{area_piso_com_perda:.2f} m²"
            )

            st.write(
                f"**Inclinação do piso:** "
                f"{ambiente['inclinacao']:.2f}%"
            )


            # ------------------------------------------------
            # ALVENARIA
            # ------------------------------------------------

            (
                blocos_geometricos,
                blocos_compra,
                area_modular
            ) = calcular_blocos(

                area_parede_liquida,

                ambiente["bloco_comprimento"],

                ambiente["bloco_altura"],

                ambiente["junta_argamassa"],

                ambiente["perda_blocos"]
            )


            total_blocos += blocos_compra


            st.markdown(
                "### 🧱 Alvenaria"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Blocos geométricos",
                    f"{blocos_geometricos:.0f}"
                )

            with col2:

                st.metric(
                    "Blocos para compra",
                    f"{blocos_compra:.0f}"
                )

            with col3:

                st.metric(
                    "Área modular",
                    f"{area_modular:.4f} m²"
                )


            # ------------------------------------------------
            # ARGAMASSA DAS JUNTAS
            # ------------------------------------------------

            if composicao_juntas is not None:

                (
                    volume_argamassa_juntas,
                    volume_argamassa_juntas_perda,
                    volume_blocos,
                    volume_unitario_bloco
                ) = calcular_argamassa_juntas(

                    area_parede_liquida,

                    ambiente["bloco_espessura"],

                    ambiente["bloco_comprimento"],

                    ambiente["bloco_altura"],

                    ambiente["junta_argamassa"],

                    ambiente["perda_argamassa_juntas"]
                )


                (
                    cimento_juntas,
                    areia_juntas,
                    barro_juntas
                ) = calcular_composicao_por_volume(

                    volume_argamassa_juntas_perda,

                    composicao_juntas[
                        "consumo_cimento_m3"
                    ],

                    composicao_juntas[
                        "consumo_areia_m3"
                    ],

                    composicao_juntas[
                        "consumo_barro_m3"
                    ]
                )


                total_volume_argamassa_juntas += (
                    volume_argamassa_juntas_perda
                )

                total_cimento_juntas += (
                    cimento_juntas
                )

                total_areia_juntas += (
                    areia_juntas
                )

                total_barro_juntas += (
                    barro_juntas
                )


                sacos_cimento_juntas = math.ceil(
                    cimento_juntas / 25
                )


                st.markdown(
                    "#### 🧱 Argamassa das juntas"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Volume da argamassa",
                        f"{volume_argamassa_juntas:.3f} m³"
                    )

                with col2:

                    st.metric(
                        "Volume com perda",
                        f"{volume_argamassa_juntas_perda:.3f} m³"
                    )

                with col3:

                    st.metric(
                        "Volume dos blocos",
                        f"{volume_blocos:.3f} m³"
                    )


                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.write(
                        f"**Cimento:** "
                        f"{cimento_juntas:.2f} kg"
                    )

                with col2:

                    st.write(
                        f"**Sacos de cimento:** "
                        f"{sacos_cimento_juntas}"
                    )

                with col3:

                    st.write(
                        f"**Areia:** "
                        f"{areia_juntas:.3f} m³"
                    )

                with col4:

                    st.write(
                        f"**Barro:** "
                        f"{barro_juntas:.3f} m³"
                    )


                with st.expander(
                    "🔬 Detalhes técnicos da estimativa"
                ):

                    st.write(
                        "**Volume unitário do bloco:** "
                        f"{volume_unitario_bloco:.6f} m³"
                    )

                    st.write(
                        "**Espessura do bloco utilizada:** "
                        f"{ambiente['bloco_espessura']:.1f} cm"
                    )

                    st.write(
                        "**Dimensões do bloco:** "
                        f"{ambiente['bloco_comprimento']:.1f} × "
                        f"{ambiente['bloco_altura']:.1f} × "
                        f"{ambiente['bloco_espessura']:.1f} cm"
                    )

                    st.write(
                        "**Junta considerada:** "
                        f"{ambiente['junta_argamassa']:.1f} cm"
                    )

                    st.caption(
                        "A argamassa das juntas é uma estimativa "
                        "geométrica baseada no volume da parede "
                        "menos o volume geométrico dos blocos. "
                        "A metodologia deverá ser validada tecnicamente."
                    )


            # ------------------------------------------------
            # REBOCO
            # ------------------------------------------------

            if composicao_reboco is not None:

                st.markdown(
                    "#### 🎨 Reboco"
                )

                espessura_reboco = (
                    composicao_reboco[
                        "espessura_cm"
                    ]
                )

                volume_reboco_geometrico = (
                    calcular_reboco_volume(
                        area_parede_liquida,
                        espessura_reboco
                    )
                )

                volume_reboco = (
                    volume_reboco_geometrico
                    *
                    (
                        1
                        +
                        composicao_reboco[
                            "perda"
                        ]
                        / 100
                    )
                )


                (
                    cimento_reboco,
                    areia_reboco,
                    barro_reboco
                ) = calcular_composicao_por_volume(

                    volume_reboco,

                    composicao_reboco[
                        "consumo_cimento_m3"
                    ],

                    composicao_reboco[
                        "consumo_areia_m3"
                    ],

                    composicao_reboco[
                        "consumo_barro_m3"
                    ]
                )


                total_volume_reboco += (
                    volume_reboco
                )

                total_cimento_reboco += (
                    cimento_reboco
                )

                total_areia_reboco += (
                    areia_reboco
                )

                total_barro_reboco += (
                    barro_reboco
                )


                sacos_cimento_reboco = math.ceil(
                    cimento_reboco / 25
                )


                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Área do reboco",
                        f"{area_parede_liquida:.2f} m²"
                    )

                with col2:

                    st.metric(
                        "Espessura",
                        f"{espessura_reboco:.1f} cm"
                    )

                with col3:

                    st.metric(
                        "Volume",
                        f"{volume_reboco:.3f} m³"
                    )


                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.write(
                        f"**Cimento:** "
                        f"{cimento_reboco:.2f} kg"
                    )

                with col2:

                    st.write(
                        f"**Sacos de cimento:** "
                        f"{sacos_cimento_reboco}"
                    )

                with col3:

                    st.write(
                        f"**Areia:** "
                        f"{areia_reboco:.3f} m³"
                    )

                with col4:

                    st.write(
                        f"**Barro:** "
                        f"{barro_reboco:.3f} m³"
                    )


            # ------------------------------------------------
            # RESUMO DO AMBIENTE
            # ------------------------------------------------

            st.markdown(
                "### 📊 Resumo do ambiente"
            )

            st.write(
                f"""
                **Piso:** {area_piso_com_perda:.2f} m²

                **Parede líquida:** {area_parede_liquida:.2f} m²

                **Blocos para compra:** {blocos_compra:.0f} un.

                **Argamassa das juntas:** {volume_argamassa_juntas_perda:.3f} m³

                **Cimento das juntas:** {cimento_juntas:.2f} kg

                **Areia das juntas:** {areia_juntas:.3f} m³

                **Reboco:** {area_parede_liquida:.2f} m²

                **Volume do reboco:** {volume_reboco:.3f} m³
                """
            )


        # ====================================================
        # MATERIAIS TOTAIS DO PROJETO
        # ====================================================

        st.divider()

        st.header(
            "📦 Materiais Totais do Projeto"
        )

        cimento_total = (
            total_cimento_juntas
            +
            total_cimento_reboco
        )

        areia_total = (
            total_areia_juntas
            +
            total_areia_reboco
        )

        barro_total = (
            total_barro_juntas
            +
            total_barro_reboco
        )

        sacos_cimento_total = math.ceil(
            cimento_total / 25
        )


        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Cimento",
                f"{cimento_total:.2f} kg"
            )

        with col2:

            st.metric(
                "Sacos de cimento",
                f"{sacos_cimento_total} un."
            )

        with col3:

            st.metric(
                "Areia",
                f"{areia_total:.3f} m³"
            )

        with col4:

            st.metric(
                "Blocos",
                f"{total_blocos} un."
            )


        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Barro",
                f"{barro_total:.3f} m³"
            )

        with col2:

            st.metric(
                "Argamassa das juntas",
                f"{total_volume_argamassa_juntas:.3f} m³"
            )

        with col3:

            st.metric(
                "Reboco",
                f"{total_volume_reboco:.3f} m³"
            )

        with col4:

            st.metric(
                "Piso",
                f"{total_piso_com_perda:.2f} m²"
            )


        # ====================================================
        # DETALHAMENTO DOS TOTAIS
        # ====================================================

        st.markdown(
            "### 📋 Detalhamento dos materiais"
        )

        st.write(
            f"""
            **Cimento das juntas:** {total_cimento_juntas:.2f} kg

            **Cimento do reboco:** {total_cimento_reboco:.2f} kg

            **Cimento total:** {cimento_total:.2f} kg

            **Sacos de cimento de 25 kg:** {sacos_cimento_total} un.

            **Areia das juntas:** {total_areia_juntas:.3f} m³

            **Areia do reboco:** {total_areia_reboco:.3f} m³

            **Areia total:** {areia_total:.3f} m³

            **Barro das juntas:** {total_barro_juntas:.3f} m³

            **Barro do reboco:** {total_barro_reboco:.3f} m³

            **Barro total:** {barro_total:.3f} m³

            **Blocos para compra:** {total_blocos} un.
            """
        )


        # ====================================================
        # AVALIAÇÃO TÉCNICA
        # ====================================================

        st.divider()

        st.header("🔬 Avaliação Técnica")

        st.info(
            "Esta seção foi criada para que um profissional "
            "possa avaliar os parâmetros, hipóteses e fórmulas "
            "utilizados pelo protótipo."
        )

        with st.expander(
            "📐 Parâmetros utilizados"
        ):

            st.write(
                f"""
                **Bloco:** {ambiente['bloco_comprimento']:.1f} ×
                {ambiente['bloco_altura']:.1f} ×
                {ambiente['bloco_espessura']:.1f} cm

                **Junta:** {ambiente['junta_argamassa']:.1f} cm

                **Perda dos blocos:** {ambiente['perda_blocos']:.1f}%

                **Perda da argamassa:** {ambiente['perda_argamassa_juntas']:.1f}%

                **Espessura do reboco:** {
                    composicao_reboco['espessura_cm']
                    if composicao_reboco is not None
                    else 0
                } cm

                **Perda do reboco:** {
                    composicao_reboco['perda']
                    if composicao_reboco is not None
                    else 0
                }%

                **Perda do piso:** {ambiente['perda_piso']:.1f}%
                """
            )


        with st.expander(
            "🧮 Fórmulas utilizadas"
        ):

            st.code(
                """
ÁREA DO PISO
Área = comprimento × largura

PERÍMETRO
Perímetro = 2 × (comprimento + largura)

PAREDE BRUTA
Parede bruta = perímetro × altura

ABERTURAS
Área da abertura = quantidade × largura × altura

PAREDE LÍQUIDA
Parede líquida = parede bruta − aberturas

ÁREA MODULAR DO BLOCO
Área modular =
(comprimento + junta) × (altura + junta)

BLOCOS GEOMÉTRICOS
Blocos = parede líquida ÷ área modular

BLOCOS PARA COMPRA
Blocos compra =
blocos geométricos × (1 + perda / 100)

VOLUME UNITÁRIO DO BLOCO
V = comprimento × altura × espessura

VOLUME DOS BLOCOS
Volume = blocos geométricos × volume unitário

VOLUME DA PAREDE
Volume = área da parede × espessura do bloco

ARGAMASSA DAS JUNTAS
Argamassa =
volume da parede − volume geométrico dos blocos

ARGAMASSA COM PERDA
Argamassa =
argamassa × (1 + perda / 100)

VOLUME DO REBOCO
Reboco =
área da parede × espessura do reboco

REBOCO COM PERDA
Reboco =
volume × (1 + perda / 100)
                """,
                language="text"
            )


        st.markdown(
            "### 📝 Observações do avaliador"
        )

        observacoes_tecnicas = st.text_area(
            "Registre aqui observações, correções "
            "ou sugestões técnicas.",
            height=180,
            key="observacoes_tecnicas"
        )


        st.markdown(
            "### ☑️ Pontos para validação"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.checkbox(
                "Validar cálculo da área das paredes",
                key="validar_area_paredes"
            )

            st.checkbox(
                "Validar cálculo das aberturas",
                key="validar_aberturas"
            )

            st.checkbox(
                "Validar quantidade de blocos",
                key="validar_blocos"
            )

            st.checkbox(
                "Validar volume da argamassa",
                key="validar_argamassa"
            )

        with col2:

            st.checkbox(
                "Validar cálculo do reboco",
                key="validar_reboco"
            )

            st.checkbox(
                "Validar perdas utilizadas",
                key="validar_perdas"
            )

            st.checkbox(
                "Validar consumo de cimento",
                key="validar_cimento"
            )

            st.checkbox(
                "Validar consumo de areia/barro",
                key="validar_agregados"
            )


# ============================================================
# OUTROS MÓDULOS
# ============================================================

else:

    st.header(
        f"🧩 {modulo}"
    )

    st.info(
        "Este módulo será desenvolvido nas próximas etapas "
        "do RGV Quantifica."
    )
```
