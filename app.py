import streamlit as st
import pandas as pd

# 📥 Excel dosyasını yükleyen fonksiyon
def load_data():
    """Excel dosyasını yükler ve DataFrame olarak döndürür."""
    file_path = "bacterial_API_results.xlsx"  # Excel dosyamız
    df = pd.read_excel(file_path)
    return df

# 🧬 Bakteriyi tanımlayan fonksiyon
def identify_bacteria(user_input, df):
    """Kullanıcının girdilerini tüm bakterilerle karşılaştırır ve benzerlik yüzdelerini hesaplar."""
    
    scores = {}
    total_tests = len(user_input)  # Test sayısını al
    
    print("\nKullanıcı Girdileri:", user_input)  # Kullanıcının girdilerini terminalde göster

    for col in df.columns[1:]:  # İlk sütun 'Test' olduğu için atlanır
        match_count = sum(1 for user_val, db_val in zip(user_input.values(), df[col].tolist()) if user_val == db_val)
        similarity_percentage = (match_count / total_tests) * 100  # Yüzde olarak hesapla
        scores[col] = round(similarity_percentage, 2)  # Yuvarlayarak kaydet
    
    # Benzerlik yüzdesine göre sıralayarak listeyi hazırla
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_scores  # En yüksek benzerlik oranına göre sıralanmış liste döndür

# 🎨 Streamlit Arayüzü
st.title("🔬 Bakteri Tanımlama Uygulaması")
st.write("API test sonuçlarını (+/-) girerek bakteriyi tanımlayın.")

# 📥 Excel verilerini yükle
df = load_data()

# 📌 Kullanıcının test sonuçlarını gireceği alanlar
tests = df["Test"].tolist()  # Test isimlerini al
user_input = {}

st.subheader("📝 Test Sonuçlarını Giriniz")
col1, col2 = st.columns(2)  # 2 sütun oluştur

for i, test in enumerate(tests):
    if i % 2 == 0:  # Çift indeksli testleri ilk sütuna ekleyelim
        user_input[test] = col1.selectbox(f"**{test}**", ['+', '-'], index=0)
    else:  # Tek indeksli testleri ikinci sütuna ekleyelim
        user_input[test] = col2.selectbox(f"**{test}**", ['+', '-'], index=0)

# 🏆 Sonucu hesapla ve göster
if st.button("🔍 Bakteriyi Tanımla"):
    sorted_results = identify_bacteria(user_input, df)

    st.subheader("🔬 Bakteri Benzerlik Sonuçları")
    for bacteria, percentage in sorted_results:
        st.write(f"✅ **{bacteria}**: %{percentage} benzerlik")
