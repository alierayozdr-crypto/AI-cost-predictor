"""
NASA COCOMO Dataset İmport Script
ARFF formatını bizim formata çevirir
"""

import pandas as pd
import numpy as np
from scipy.io import arff
import urllib.request
import os

def download_cocomo_dataset(output_path='data/cocomo_nasa.arff'):
    """NASA COCOMO dataseti indir"""
    url = 'http://promise.site.uottawa.ca/SERepository/datasets/cocomonasa_v1.arff'
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"İndiriliyor: {url}")
    urllib.request.urlretrieve(url, output_path)
    print(f"✅ Kaydedildi: {output_path}")
    
    return output_path

def load_arff_to_dataframe(arff_path):
    """ARFF dosyasını pandas DataFrame'e çevir"""
    # Manuel parsing - scipy.io.arff format sorunları yaşıyor
    with open(arff_path, 'r') as f:
        lines = f.readlines()
    
    # Attribute isimlerini bul
    attributes = []
    data_start = False
    data_lines = []
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('@attribute'):
            # @attribute name type
            parts = line.split()
            if len(parts) >= 2:
                attr_name = parts[1].lower()
                attributes.append(attr_name)
        
        elif line.startswith('@data'):
            data_start = True
            continue
        
        elif data_start and line and not line.startswith('%'):
            # Veri satırı
            data_lines.append(line)
    
    # Veriyi parse et
    data_rows = []
    for line in data_lines:
        # Yorum karakterini temizle
        if '%' in line:
            line = line.split('%')[0].strip()
        
        # Virgülle ayrılmış değerler
        values = [v.strip() for v in line.split(',')]
        if len(values) == len(attributes):
            data_rows.append(values)
    
    # DataFrame oluştur
    df = pd.DataFrame(data_rows, columns=attributes)
    
    # Sayısal kolonları dönüştür
    numeric_cols = ['loc', 'act_effort']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def map_categorical_to_numeric(value, mapping):
    """Kategorik değeri sayısal değere map et"""
    if pd.isna(value):
        return mapping.get('nominal', 3)
    return mapping.get(value.lower(), mapping.get('nominal', 3))

def cocomo_to_our_format(cocomo_df):
    """
    NASA COCOMO parametrelerini bizim formata çevir
    
    COCOMO Parametreleri:
    - KSLOC: Kod satırı (binler)
    - acap, pcap, aexp, etc.: Effort multipliers (vlow, low, nominal, high, vhigh)
    - actual_effort: Gerçek effort (adam-ay)
    
    Bizim Parametreler:
    - project_duration (ay)
    - team_size (kişi)
    - complexity (1-10)
    - tech_cost (TL)
    - location_factor (1-3)
    - experience_level (1-5)
    - risk_factor (0-1)
    - actual_cost (TL)
    """
    
    our_df = pd.DataFrame()
    
    # 1. Project Duration - sced (schedule constraint) parametresinden
    sced_mapping = {
        'vlow': 18,   # Çok gevşek zaman
        'low': 14,
        'nominal': 12,
        'high': 10,
        'vhigh': 8    # Çok sıkı zaman
    }
    our_df['project_duration'] = cocomo_df['sced'].apply(
        lambda x: map_categorical_to_numeric(x, sced_mapping)
    )
    
    # 2. Team Size - loc'dan tahmin et
    # LOC binler cinsinden, ortalama: 1 KLOC = 1 kişi
    our_df['team_size'] = ((cocomo_df['loc'] / 1000) / 10).clip(2, 50).round().astype(int)
    
    # 3. Complexity - cplx (process complexity) parametresinden
    cplx_mapping = {
        'vlow': 2,
        'low': 4,
        'nominal': 6,
        'high': 8,
        'vhigh': 10
    }
    our_df['complexity'] = cocomo_df['cplx'].apply(
        lambda x: map_categorical_to_numeric(x, cplx_mapping)
    )
    
    # 4. Tech Cost - loc ve tool kullanımından tahmin
    # Varsayım: 1 KLOC = 50,000 TL teknoloji maliyeti
    base_tech_cost = (cocomo_df['loc'] / 1000) * 50000
    
    tool_multiplier = cocomo_df['tool'].apply(lambda x: {
        'vlow': 1.5,
        'low': 1.2,
        'nominal': 1.0,
        'high': 0.8,
        'vhigh': 0.6
    }.get(str(x).lower() if not pd.isna(x) else 'nominal', 1.0))
    
    our_df['tech_cost'] = (base_tech_cost * tool_multiplier).clip(10000, 10000000)
    
    # 5. Location Factor - Sabit (NASA projeleri ABD'de)
    our_df['location_factor'] = 2.0
    
    # 6. Experience Level - aexp, pcap, acap ortalaması
    exp_mapping = {
        'vlow': 1,
        'low': 2,
        'nominal': 3,
        'high': 4,
        'vhigh': 5
    }
    
    aexp_num = cocomo_df['aexp'].apply(lambda x: map_categorical_to_numeric(x, exp_mapping))
    pcap_num = cocomo_df['pcap'].apply(lambda x: map_categorical_to_numeric(x, exp_mapping))
    acap_num = cocomo_df['acap'].apply(lambda x: map_categorical_to_numeric(x, exp_mapping))
    
    our_df['experience_level'] = ((aexp_num + pcap_num + acap_num) / 3).clip(1, 5)
    
    # 7. Risk Factor - rely (reliability requirement) parametresinden
    rely_mapping = {
        'vlow': 0.2,
        'low': 0.4,
        'nominal': 0.6,
        'high': 0.8,
        'vhigh': 1.0
    }
    our_df['risk_factor'] = cocomo_df['rely'].apply(
        lambda x: map_categorical_to_numeric(x, rely_mapping)
    )
    
    # 8. Actual Cost - effort'u maliyete çevir
    # 1 adam-ay = 152 saat
    # Ortalama saat ücreti = 500 TL (NASA için)
    our_df['actual_cost'] = cocomo_df['act_effort'] * 152 * 500
    
    # 9. Proje adı ekle
    our_df['project_name'] = [f'NASA_Project_{i+1}' for i in range(len(our_df))]
    
    return our_df

def validate_converted_data(df):
    """Dönüştürülen veriyi validate et"""
    print("\n" + "="*60)
    print("VERİ KALITE KONTROLÜ")
    print("="*60)
    
    checks = {
        'Minimum örnek sayısı (>20)': len(df) >= 20,
        'Eksik veri yok': df.isnull().sum().sum() == 0,
        'Pozitif maliyetler': (df['actual_cost'] > 0).all(),
        'Proje süresi aralığı (1-36)': ((df['project_duration'] >= 1) & (df['project_duration'] <= 36)).all(),
        'Ekip büyüklüğü aralığı (2-50)': ((df['team_size'] >= 2) & (df['team_size'] <= 50)).all(),
        'Karmaşıklık aralığı (1-10)': ((df['complexity'] >= 1) & (df['complexity'] <= 10)).all(),
    }
    
    all_passed = True
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    print("VERİ İSTATİSTİKLERİ")
    print("="*60)
    print(f"Toplam Proje: {len(df)}")
    print(f"Ortalama Maliyet: {df['actual_cost'].mean():,.0f} TL")
    print(f"Median Maliyet: {df['actual_cost'].median():,.0f} TL")
    print(f"Min Maliyet: {df['actual_cost'].min():,.0f} TL")
    print(f"Max Maliyet: {df['actual_cost'].max():,.0f} TL")
    print("="*60 + "\n")
    
    return all_passed

def main():
    """Ana script"""
    print("NASA COCOMO Dataset İmport Script")
    print("="*60)
    
    # 1. Dataset indir
    arff_path = download_cocomo_dataset()
    
    # 2. ARFF'i DataFrame'e çevir
    print("\nARFF dosyası okunuyor...")
    cocomo_df = load_arff_to_dataframe(arff_path)
    print(f"✅ {len(cocomo_df)} proje yüklendi")
    
    # 3. Bizim formata çevir
    print("\nParametreler dönüştürülüyor...")
    our_df = cocomo_to_our_format(cocomo_df)
    print("✅ Dönüştürme tamamlandı")
    
    # 4. Validate et
    if validate_converted_data(our_df):
        print("✅ Tüm kontroller başarılı!")
    else:
        print("⚠️ Bazı kontroller başarısız. Veriyi inceleyin.")
    
    # 5. Kaydet
    output_path = 'data/cocomo_converted.csv'
    our_df.to_csv(output_path, index=False)
    print(f"\n✅ Veri kaydedildi: {output_path}")
    
    # 6. Örnek göster
    print("\nİlk 5 Proje:")
    print(our_df.head().to_string())
    
    return our_df

if __name__ == '__main__':
    df = main()
