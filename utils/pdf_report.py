from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import io
from datetime import datetime
import os

class PDFReportGenerator:
    """
    Otomatik PDF Rapor Üretici
    
    Yönetici özeti, finansal analiz ve grafikler içeren
    profesyonel PDF raporları oluşturur.
    """
    
    def __init__(self, filename="cost_analysis_report.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
    
    def add_title_page(self, project_name, company_name=""):
        """
        Başlık sayfası ekle
        """
        self.story.append(Spacer(1, 2*inch))
        
        title = Paragraph("MALİYET ANALİZİ VE<br/>OPTİMİZASYON RAPORU", self.title_style)
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*inch))
        
        if company_name:
            company = Paragraph(f"<b>{company_name}</b>", 
                              ParagraphStyle('company', parent=self.body_style, 
                                           fontSize=14, alignment=TA_CENTER))
            self.story.append(company)
            self.story.append(Spacer(1, 0.3*inch))
        
        project = Paragraph(f"<b>Proje:</b> {project_name}", 
                          ParagraphStyle('project', parent=self.body_style, 
                                       fontSize=12, alignment=TA_CENTER))
        self.story.append(project)
        self.story.append(Spacer(1, 0.3*inch))
        
        date = Paragraph(f"<b>Rapor Tarihi:</b> {datetime.now().strftime('%d/%m/%Y')}", 
                        ParagraphStyle('date', parent=self.body_style, 
                                     fontSize=11, alignment=TA_CENTER))
        self.story.append(date)
        
        self.story.append(Spacer(1, 1*inch))
        
        footer = Paragraph("AI Destekli Karar Destek Sistemi", 
                         ParagraphStyle('footer', parent=self.body_style, 
                                      fontSize=10, alignment=TA_CENTER, 
                                      textColor=colors.grey))
        self.story.append(footer)
        
        self.story.append(PageBreak())
    
    def add_executive_summary(self, summary_data):
        """
        Yönetici Özeti ekle
        
        Args:
            summary_data: dict with keys: predicted_cost, confidence_interval, 
                         roi, npv, break_even, risk_level, recommendation
        """
        self.story.append(Paragraph("YÖNETİCİ ÖZETİ", self.heading_style))
        
        summary_text = f"""
        Bu rapor, yapay zeka destekli maliyet tahmin modelimiz kullanılarak 
        hazırlanmıştır. Model, {summary_data.get('model_accuracy', '97%')} doğruluk 
        oranıyla çalışmaktadır ve geçmiş proje verilerine dayanmaktadır.
        """
        self.story.append(Paragraph(summary_text, self.body_style))
        self.story.append(Spacer(1, 0.2*inch))
        
        data = [
            ['Metrik', 'Değer', 'Durum'],
            ['Tahmini Maliyet', f"{summary_data['predicted_cost']:,.2f} TL", ''],
            ['Güven Aralığı (%90)', 
             f"{summary_data['confidence_lower']:,.0f} - {summary_data['confidence_upper']:,.0f} TL", ''],
            ['Yatırım Getirisi (ROI)', f"%{summary_data['roi']:.2f}", 
             '✓ Pozitif' if summary_data['roi'] > 0 else '✗ Negatif'],
            ['Net Bugünkü Değer (NPV)', f"{summary_data['npv']:,.2f} TL",
             '✓ Pozitif' if summary_data['npv'] > 0 else '✗ Negatif'],
            ['Başabaş Süresi', f"{summary_data['break_even']:.1f} ay", ''],
            ['Risk Seviyesi', summary_data['risk_level'], ''],
        ]
        
        table = Table(data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
        
        recommendation_style = ParagraphStyle(
            'recommendation',
            parent=self.body_style,
            fontSize=12,
            textColor=colors.HexColor('#d9534f') if 'Risk' in summary_data['recommendation'] 
                     else colors.HexColor('#5cb85c'),
            fontName='Helvetica-Bold',
            borderColor=colors.black,
            borderWidth=1,
            borderPadding=10,
            backColor=colors.HexColor('#f9f9f9')
        )
        
        self.story.append(Paragraph(f"<b>ÖNERI:</b> {summary_data['recommendation']}", 
                                   recommendation_style))
        
        self.story.append(PageBreak())
    
    def add_project_details(self, project_data):
        """
        Proje detayları ekle
        """
        self.story.append(Paragraph("PROJE DETAYLARI", self.heading_style))
        
        data = [['Parametre', 'Değer']]
        for key, value in project_data.items():
            data.append([key, str(value)])
        
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_chart(self, fig, title=""):
        """
        Matplotlib grafiği ekle
        """
        if title:
            self.story.append(Paragraph(title, self.heading_style))
        
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        
        img = Image(img_buffer, width=6*inch, height=4*inch)
        self.story.append(img)
        self.story.append(Spacer(1, 0.2*inch))
        
        plt.close(fig)
    
    def add_sensitivity_analysis(self, sensitivity_data):
        """
        Duyarlılık analizi bölümü ekle
        """
        self.story.append(Paragraph("DUYARLILIK ANALİZİ", self.heading_style))
        
        text = """
        Aşağıdaki analiz, proje parametrelerindeki değişimlerin toplam maliyete 
        etkisini göstermektedir. Yüksek etki değeri, o parametrenin maliyet üzerinde 
        daha büyük etkisi olduğunu gösterir.
        """
        self.story.append(Paragraph(text, self.body_style))
        self.story.append(Spacer(1, 0.2*inch))
        
        data = [['Parametre', 'Etki (%)', 'Elastikiyet']]
        for item in sensitivity_data[:5]:
            data.append([
                item['feature'],
                f"{item['impact']:.2f}%",
                f"{item['elasticity']:.3f}"
            ])
        
        table = Table(data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_scenario_analysis(self, scenarios):
        """
        Senaryo analizi ekle
        """
        self.story.append(Paragraph("SENARYO ANALİZİ", self.heading_style))
        
        data = [['Senaryo', 'Maliyet (TL)', 'Olasılık', 'Açıklama']]
        
        scenario_descriptions = {
            'optimistic': 'En iyi durum - Tüm faktörler lehte',
            'expected': 'Beklenen durum - Normal koşullar',
            'pessimistic': 'En kötü durum - Riskler gerçekleşir'
        }
        
        for scenario_name, scenario_data in scenarios.items():
            if scenario_name != 'expected_value':
                data.append([
                    scenario_name.capitalize(),
                    f"{scenario_data['cost']:,.2f}",
                    f"%{scenario_data['probability']*100:.0f}",
                    scenario_descriptions.get(scenario_name, '')
                ])
        
        table = Table(data, colWidths=[1.5*inch, 1.8*inch, 1.2*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.2*inch))
        
        ev_text = f"<b>Beklenen Değer (Weighted Average):</b> {scenarios['expected_value']:,.2f} TL"
        self.story.append(Paragraph(ev_text, self.body_style))
    
    def generate(self):
        """
        PDF'i oluştur ve kaydet
        """
        self.doc.build(self.story)
        return self.filename
