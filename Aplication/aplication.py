import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards
import cv2
import math
from ultralytics import YOLO
import os
import io




from PIL import Image, ExifTags
@st.cache_data
def load_model(model):
    pass

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_excel().encode("utf-8")
@st.fragment
def apagar_imagens(caminho_pasta):
    try:
        # Verifica se o caminho é válido
        if not os.path.exists(caminho_pasta):
            print("O caminho especificado não existe.")
            return
        
        # Lista todos os arquivos na pasta
        arquivos = os.listdir(caminho_pasta)
        
        # Extensões de imagens que deseja apagar
        extensoes_imagens = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        
        # Lista para armazenar os arquivos de imagens encontrados
        imagens_encontradas = []
        
        # Itera sobre os arquivos e verifica as imagens
        for arquivo in arquivos:
            caminho_completo = os.path.join(caminho_pasta, arquivo)
            
            # Verifica se é um arquivo e se possui extensão de imagem
            if os.path.isfile(caminho_completo) and os.path.splitext(arquivo)[1].lower() in extensoes_imagens:
                imagens_encontradas.append(caminho_completo)
        
        # Apaga as imagens encontradas ou retorna mensagem se nenhuma imagem foi encontrada
        if imagens_encontradas:
            for imagem in imagens_encontradas:
                os.remove(imagem)
                print(f"Imagem apagada: {os.path.basename(imagem)}")
            return 1
        else:
            return 0
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")




def criar_excel_em_memoria(dicionario_dataframes):
    """
    Cria um arquivo Excel em memória com múltiplas abas a partir de um dicionário.
    
    :param dicionario_dataframes: Dicionário onde a chave é o nome da aba e o valor é um DataFrame.
    :return: Arquivo Excel em bytes, pronto para ser usado no Streamlit.
    """
    # Cria um buffer em memória
    buffer = io.BytesIO()
    
    # Escreve o Excel no buffer
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for aba, dataframe in dicionario_dataframes.items():
            dataframe.to_excel(writer, sheet_name=aba, index=False)
    
    # Move o ponteiro para o início do buffer
    buffer.seek(0)
    
    return buffer.getvalue()

@st.cache_data
def convert_df_to_excel(dicionario_dataframes):
    return criar_excel_em_memoria(dicionario_dataframes)




def UploadImage():
    # Define o caminho onde as imagens serão salvas
    save_path = "Aplication/images_upload/"
    os.makedirs(save_path, exist_ok=True)  # Cria a pasta se não existir

    # Upload de arquivos
    uploaded_files = st.file_uploader(
        "Escolha as imagens", type=['png', 'jpg'], accept_multiple_files=True
    )
    
    col1,col2,col3 = st.columns([1,3,1])
    with col1:
            # Botão para salvar as imagens
        if st.button("Salvar Imagens"):
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(save_path, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.read())  # Salva a imagem na pasta
                    st.write(f"Imagem '{uploaded_file.name}' salva com sucesso em '{file_path}'!")
            else:
                st.error("Nenhuma imagem selecionada!")
    with col2:
        if st.button("Limpar Imagens"):
            num1=apagar_imagens(r"Aplication\images_download")
            num2=apagar_imagens(r"Aplication\images_upload")
            if num1+num2 > 0:
                st.success("Imagens apagadas!")
            else:
                st.error("Não existem imagens para serem apagadas!")
    with col3:
        if st.button("Limpar Cache!"):
            st.session_state["datas"] = {}
            st.success("Cache Limpada")
def listar_caminhos_arquivos(pasta):
    """
    Itera pelos arquivos de uma pasta e retorna os caminhos completos.
    
    Args:
        pasta (str): Caminho da pasta a ser analisada.
    
    Returns:
        list: Lista de caminhos completos dos arquivos.
    """
    caminhos = []
    for raiz, _, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            caminhos.append(caminho_completo)
    return caminhos



def TreinarModelo(data,epochs,img):
  model = YOLO("yolo11n.pt")#Carrega um modelo pre-treiando
  results = model.train(data=data, epochs=epochs, imgsz=img)
def ValidacaoModelo(pathmodel):
  model = YOLO(pathmodel)
  #Validando o modelo
  metrics = model.val()
  metrics.box.map  # map50-95
  metrics.box.map50  # map50
  metrics.box.map75  # map75
  metrics.box.maps  # a list contains map50-95 of each category
@st.cache_data
def InferirModelo(pathweights,img,conf):
  model = YOLO(pathweights)
  results = model.predict(source=img,conf=conf)
  return results
    
def Tabela():
    pass


  # Função para corrigir orientação da imagem
def correct_image_orientation(image):
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = image._getexif()
            if exif is not None:
                orientation = exif.get(orientation, 1)
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        except AttributeError:
            # Se a imagem não tiver EXIF ou falhar na leitura
            pass
        return image
 ##Detectar Baliza-------------------------------------------------------------------------------------------------
def DetectarBaliza(img_path):
    # Carregar o modelo
    model_path = '/content/runs/detect/train/weights/best.pt'
    model = YOLO(model_path)

    # Realizar a detecção na imagem
    results = model.predict(source=img_path, conf=0.25, save=True)

    # Obter o primeiro conjunto de resultados
    detections = results[0].boxes  # Resultados de detecção de caixas

    # Lista para armazenar as áreas dos objetos detectados
    areas = []

    # Ler a imagem original
    img = cv2.imread(img_path)

    # Iterar sobre cada caixa delimitadora detectada
    for box in detections:
        x1, y1, x2, y2 = box.xyxy[0]  # Coordenadas da caixa delimitadora
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Calcular a largura e altura da caixa
        width = x2 - x1
        height = y2 - y1

        # Calcular a área e converter para float
        area = (width * height)
        areas.append(area)

        # Desenhar a caixa delimitadora na imagem
        #cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Adicionar um rótulo à caixa
        #cv2.putText(img, 'Baliza', (x1, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 3)
    
    if len(detections) == 0:
      return -1
    else:
      return [areas,[x1,y1,x2,y2]]
##ExibirPontosTora--------------------------------------------------------------------------------------
def ExibirPontosTora(results, img, output_path="resultado_com_pontos.jpg"):
    """
    Recebe o retorno da função InferirModelo e adiciona um ponto vermelho
    no centro de cada objeto predito com um índice numérico.
    Calcula as áreas das bounding boxes e círculos aproximados.
    Salva a imagem com os pontos e retorna o caminho do arquivo, a contagem total, e um DataFrame.

    Args:
        results: Saída da função InferirModelo contendo as previsões.
        img: Imagem original carregada com cv2.imread.
        output_path: Caminho para salvar a imagem com pontos (default: 'resultado_com_pontos.jpg').

    Returns:
        output_path: Caminho do arquivo salvo.
        total_objects: Contagem total de objetos preditos.
        df_areas: DataFrame contendo o índice, raio, área do círculo e área da bounding box.
    """
    # Copiar a imagem original para adicionar os pontos
    img_with_points = img.copy()

    # Inicializar contagem total e lista para dados do DataFrame
    total_objects = 0
    data = []

    # Iterar sobre os resultados e adicionar pontos no centro de cada bounding box
    for result in results:
        for i, box in enumerate(result.boxes):  # Enumerar para obter o índice
            # Obter as coordenadas do bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Converte para inteiros
            # Calcular o centro do bounding box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            # Desenhar um ponto vermelho maior no centro do bounding box
            cv2.circle(img_with_points, (center_x, center_y), radius=8, color=(0, 0, 255), thickness=-1)
            # Adicionar um índice numérico próximo ao ponto
            cv2.putText(
                img_with_points,
                str(i + 1),  # Índice começa em 1
                (center_x + 10, center_y - 10),  # Posição do texto ajustada
                cv2.FONT_HERSHEY_SIMPLEX,
                2,  # Tamanho da fonte
                (0, 255, 0),  # Cor do texto (verde)
                6,  # Espessura do texto
                cv2.LINE_AA  # Antialiasing
            )

            # Calcular a largura e a altura da caixa
            width = x2 - x1
            height = y2 - y1

            # Assumir que o menor dos dois (largura ou altura) é o diâmetro da tora
            diameter = min(width, height)
            radius = diameter / 2

            # Calcular a área do círculo
            area_circulo = math.pi * (radius ** 2)

            # Calcular a área da bounding box
            area_bounding_box = width * height

            # Adicionar os dados ao DataFrame
            data.append({
                "Índice": i + 1,
                "Raio": radius,
                "Área do Círculo": area_circulo,
                "Área da Bounding Box": area_bounding_box
            })

            # Incrementar a contagem total de objetos
            total_objects += 1

    # Criar o DataFrame com os dados coletados
    df_areas = pd.DataFrame(data)
    # Salvar a imagem no caminho especificado
    cv2.imwrite(output_path, img_with_points)

    return output_path, total_objects, df_areas
def ExibirPontosTora1(results, img, output_path="resultado_com_pontos.jpg"):
    """
    Função corrigida para evitar erros de comprimento incompatível ao adicionar colunas ao DataFrame.
    """
    img_with_points = img.copy()
    total_objects = 0
    data = []

    for result in results:
        for i, box in enumerate(result.boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            cv2.circle(img_with_points, (center_x, center_y), radius=8, color=(0, 0, 255), thickness=-1)
            cv2.putText(
                img_with_points,
                str(i + 1),
                (center_x + 10, center_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 255, 0),
                6,
                cv2.LINE_AA
            )

            width = x2 - x1
            height = y2 - y1
            diameter = min(width, height)
            l1 = width/2
            l2=height/2
            radius = l1*l2
            area_circulo = math.pi * (radius ** 2)
            area_bounding_box = width * height

            data.append({
                "Índice": i + 1,
                "Raio (px)": radius,
                "Área do Círculo (px)": area_circulo,
                "Área da Bounding Box (px)": area_bounding_box
            })
            total_objects += 1

    # Detecção de balizas
    model_path = r'Aplication\baliza.pt'
    baliza_model = YOLO(model_path)
    baliza_results = baliza_model.predict(source=img, conf=0.25)

    baliza_areas = []
    for box in baliza_results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        width = x2 - x1
        height = y2 - y1
        area = width * height
        baliza_areas.append(area)

        cv2.rectangle(img_with_points, (x1, y1), (x2, y2), (255, 0,0), 2)
        cv2.putText(img_with_points, 'Baliza', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0,0), 3)

    # Criar DataFrame com os dados dos objetos preditos
    df_areas = pd.DataFrame(data)

    # Adicionar informações de baliza como colunas separadas
    if baliza_areas:
        total_baliza_area = sum(baliza_areas)
        fator_m2_px = 0.265225/total_baliza_area 

        # Adicionar colunas relacionadas à baliza
        df_areas["Área-Baliza Total (px)"] = total_baliza_area  # Valor único, replicado para todas as linhas
       # df_areas["Fator [m^2]/[px]"] = fator_m2_px  # Valor único
        df_areas["Fator [m^2]/[px] (Formatado)"] = f"{fator_m2_px:.2e}" 
        df_areas['Área do Círculo (m^2)'] = df_areas['Área do Círculo (px)'] * fator_m2_px
        df_areas['Área da Bounding Box (m^2)'] = df_areas['Área da Bounding Box (px)'] * fator_m2_px
        # Calcula a soma das colunas
    bounding_box_sum = df_areas['Área da Bounding Box (m^2)'].sum()
    circle_area_sum = df_areas['Área do Círculo (m^2)'].sum()

    # Cria um dicionário para representar a nova linha
    new_row = {
        'Área da Bounding Box (m^2)': bounding_box_sum,
        'Área do Círculo (m^2)': circle_area_sum,
    }

    # Adiciona a nova linha ao DataFrame
    df_areas = df_areas.append(new_row, ignore_index=True)

    cv2.imwrite(output_path, img_with_points)
    return output_path, total_objects, df_areas

def ExecutarModeloFotos(pathimage):
    if "datas" not in st.session_state:
        st.session_state["datas"]={}


    img = cv2.imread(pathimage)
    # Inferir os resultados


    results = InferirModelo(
            pathweights=r"Aplication\model4.pt",
            img=img,
            conf=0.25
        )


    x = pathimage.split("\\")[-1]
    output_path = f"Aplication/images_download/{x}"
    aba = pathimage.split("\\")[-1]
    # Exibir e salvar os pontos na imagem, calcular áreas e obter o DataFrame
    output_file, count, df_areas = ExibirPontosTora1(results, img, output_path=output_path)
    print(f"Imagem salva em: {output_file}")
    print(f"Total de objetos preditos: {count}")
    print("Dataframe foi adicionado!")
    st.session_state["datas"][str(aba)]=df_areas
    #print(df_areas)
    #st.dataframe(df_areas,hide_index=True)   
def ExibirValores():    
    """
        Função para exibir os valores dos dataframes correspondente as imagens

    """
    if "datas" not in st.session_state:
        st.session_state["datas"] = {}
    else:
        for chave, valor in st.session_state["datas"].items():
            st.divider()
            st.header(chave,divider="green")
            st.dataframe(valor, height=600, use_container_width=True, hide_index=True)
def SideBar():
    if "tora" not in st.session_state:
        st.session_state["tora"] = "Modelo Tora"
    if "baliza" not in st.session_state:
        st.session_state["baliza"] = "Modelo Baliza"
    st.sidebar.selectbox("🌲 Modelos Tora:", ["Modelo Tora"],key="tora")
    st.sidebar.selectbox("⬛ Modelos Baliza:", ["Modelo Baliza"],key="baliza")

#Menu de exibição da aplicação-----------------------------------------------------------------
SideBar()
tab1, tab2,tab3,tab4 = st.tabs(["📊 Aplicação", "📥 Imagens Upadas","📥 Imagens Resultado","📥 Baixar dados"])
with tab1:
    st.title("Aplicação :chart_with_upwards_trend:")
    st.divider()

    with st.container(height=200):
        UploadImage()
    
    
    
    if st.button("Rodar Modelo"):
        pasta = r"Aplication\images_upload"
        caminhos_dos_arquivos = listar_caminhos_arquivos(pasta)
        array = []
        if len(caminhos_dos_arquivos) > 0:
            for images in caminhos_dos_arquivos:
                ExecutarModeloFotos(images)
            st.success("Modelo Inferiu em todas as imagens com sucesso!")
        else:
            st.error("Não existem imagens para realizar a inferência!")
    ExibirValores() 


    
with tab2:
    st.write("📥 Imagens Upadas")
    pasta = r"Aplication\images_upload"
    caminhos_dos_arquivos = listar_caminhos_arquivos(pasta)
    array = []
    if len(caminhos_dos_arquivos)> 0:
        for images in caminhos_dos_arquivos:
            image = correct_image_orientation(Image.open(images))
            image = image.resize((image.width, image.height), Image.LANCZOS)
            array.append(image)
    # Exibir as imagens no Streamlit
        caption = []
        for caminho in caminhos_dos_arquivos:
            caption.append(caminho.split("\\")[-1])
        print(array)
        st.image(array, caption=caption, use_column_width=True)

    
with tab3:
    st.write("")
    pasta = r"Aplication\images_download"
    caminhos_dos_arquivos = listar_caminhos_arquivos(pasta)
    array = []
    if len(caminhos_dos_arquivos) > 0:
        for images in caminhos_dos_arquivos:
            image = correct_image_orientation(Image.open(images))
            image = image.resize((image.width, image.height), Image.LANCZOS)
            array.append(image)
        # Exibir as imagens no Streamlit
        caption = []
        for caminho in caminhos_dos_arquivos:
            caption.append(caminho.split("\\")[-1])
        print(array)
        st.image(array, caption=caption, use_column_width=True)
with tab4:
    st.write("Baixar dados")
    if st.button("Baixar Planilha com dados"):
        if "datas" not in st.session_state or not st.session_state["datas"]:
            st.session_state["datas"] = {}
            st.error("Não possui dados ainda!")
        else:
            # Gera o Excel
            excel_data = convert_df_to_excel(st.session_state["datas"])

            # Botão de download
            if  st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="dados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ):
                st.success("Arquivo Baixado!")