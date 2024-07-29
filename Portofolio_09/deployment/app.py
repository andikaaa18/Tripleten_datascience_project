import joblib
import numpy as np
import streamlit as st
import torch
import transformers

@st.cache_resource(show_spinner=False)
def download_and_load_model():
    bert_tokenizer = transformers.BertTokenizer.from_pretrained("bert-base-uncased")
    bert_model = transformers.BertModel.from_pretrained("bert-base-uncased").to(device)
    sentiment_model = joblib.load("./Portofolio_09/assets/best_model.pkl")
    return bert_tokenizer, bert_model, sentiment_model

def input_form():
    st.title("Sentiment Analysis Based on BERT for IMDb Movie Reviews")
    st.header("Movie Review Text Input", divider='grey')
    type_input = st.radio("Input method", ["Custom text", "Sample text"])
    if type_input=="Custom text":
        text = st.text_area("Enter your text here!", height=100)
    else:
        sample = [
            "The cinematography in this film is absolutely stunning! Every frame feels like a work of art. Definitely a must-watch for any film lover.",
            "I found the plot to be quite predictable and the characters lacking depth. Overall, a disappointing experience.",
            "The performances by the lead actors were phenomenal, especially considering the emotional depth of the story. A truly gripping film that will stay with you long after it ends.",
            "I couldn't connect with any of the characters, and the pacing felt off. It's a shame because the concept had so much potential.",
            "A masterpiece of storytelling! The way the narrative unfolds keeps you on the edge of your seat until the very end. Highly recommend it!"
            ]


        value = st.selectbox("Sample Text Option", options=sample, format_func=lambda x:f"Sample-{sample.index(x)+1}")
        text = st.text_area(f"Sample-{sample.index(value)+1}", value=value, disabled=True, height=100)
    
    return text

def tokenize_with_bert(texts):
    ids_list = []
    attention_mask_list = []
    max_length = 512

    for text in texts:
        ids = bert_tokenizer.encode(text.lower(), add_special_tokens=True, truncation=True,
                                    max_length=max_length)
        
        padded = np.array(ids + (max_length-len(ids))*[0])
        attention_mask = np.where(padded!=0, 1, 0)
        
        ids_list.append(padded)
        attention_mask_list.append(attention_mask)

    return ids_list, attention_mask_list

def embedding_with_bert(text):
    ids, attmask = tokenize_with_bert([text,])
    ids = torch.LongTensor(ids).to(device)
    attmask = torch.LongTensor(attmask).to(device)

    with torch.no_grad():
        bert_model.eval()
        embedding = bert_model(ids, attention_mask=attmask)
    
    return embedding.last_hidden_state.mean(dim=1).detach().cpu().numpy()

def model_prediction(text):
    embedding = embedding_with_bert(text)
    return sentiment_model.predict_proba(embedding)[0][1]


# model loading
with st.spinner("In process of loading model..."):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    bert_tokenizer, bert_model, sentiment_model = download_and_load_model()

# input form
text = input_form()
st.divider()

# result
execute = st.button("Run the model")
if execute:
    st.subheader("Result")

    # make a prediction
    with st.spinner():
        pred_prob = model_prediction(text)
        threshold = 0.40
        prediction = "POSITIVE" if pred_prob>threshold else "NEGATIVE"

    with open("./Portofolio_09/deployment/style.css", 'r') as f:
        style = f.read()
        st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

    row1 = st.columns([0.20, 0.30, 0.30, 0.20])
    row1[1].metric(f"**Negative Review Prob.**", f"{1-pred_prob:.1%}")
    row1[2].metric(f"**Positive Review Prob.**", f"{pred_prob:.1%}")
    st.markdown(f"Based on the model's prediction, the review text you entered is detected to have "
                f"a **:{'red' if prediction=='NEGATIVE' else 'green'}[{prediction} SENTIMENT]**.")
