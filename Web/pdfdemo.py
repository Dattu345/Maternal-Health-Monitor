from fpdf import FPDF
from PIL import Image
from create_table_fpdf2 import PDF
import glob
from datetime import date
def process(pname,examres,cvm,bpd,hdc,abdc,f1,bpdw,hdcw,abdcw,f1w,lmp,ega,edd,eddu,imp,adv,al,fhr,efw,today,docname,userage):
    data = [
    ["Parameters", "Measured Values", "Weeks",], # 'testing','size'],
    ["B.P.D", str(bpd)+" cms", str(bpdw),], # 'testing','size'],
    ["Haed Circumference", str(hdc)+" cms", str(hdcw),], # 'testing','size'],
    ["ABD Circumference", str(abdc)+"cms", str(abdcw), ], # 'testing','size'],
    ["Femoral Length", str(f1)+" cms", str(f1w), ], # 'testing','size'],
]
    data1=[["L.M.P: "+str(lmp), str(ega),"EDD LMP : "+str(edd),],["Average gestational age according to this USG is 15 wks 6 days","","",],]
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(10, 10, 'Date '+str(today),0,1,'c')
    pdf.cell(50, 10, 'Age '+str(userage),0,0,'c')
    pdf.ln()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'SONOGRAPHY OF GRAVID UTERUS(Nuchal Transluency Scan)',0,1,'c')
    pdf.ln()
    pdf.set_font("Times", size=10)
    pdf.cell(40, 10, 'This examination shows'+str(examres),0,0,'c')
    pdf.ln()
    pdf.cell(40,10,'The placenta is Fundo-Anterior in position and of grade I maturity',0,0,'c')
    pdf.ln()
    pdf.cell(40, 10, 'The internal os is closed. Cervix measures '+str(cvm)+' cms',0,0,'c')
    pdf.ln()
    pdf.cell(40,10,'Amount of liquour is:'+str(al),0,0,'c')
    pdf.ln()
    pdf.cell(40, 10, 'Fetal Cardic activity and movements are present. FHR :'+fhr+' bpm',0,0,'c')
    pdf.ln()
    
    pdf.create_table(table_data = data,title='Fetal parameters are follows', cell_width='even')
    pdf.create_table(table_data = data1,cell_width='uneven')
    
    pdf.cell(40, 10, 'Estimated Fetal Weight is '+efw+' gms(-/+ 23gms)',0,0,'c')
    pdf.ln()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'EDD according to this Ultrasound'+str(eddu),0,0,'c')
    pdf.ln()
    pdf.cell(40, 10, 'Impression',0,0,'c')
    pdf.ln()
    pdf.set_font("Times", size=10)
    pdf.cell(40, 10,str(imp),0,0,'c')
    pdf.ln()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Advice:'+str(adv),0,0,'c')
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.cell(40, 10, docname,0,0,'c')
    pdf.ln()
    pdf.ln()
    pdf.cell(40, 10,'Report with Thanks',0,0,'c')

    

    
        
    
    path='./static/'+pname+'_1.pdf'
    pdf.output(path, 'F')
    print("Pdf Created")
# today = date.today()
# process('hetal rana',3.1,10.5,10.3,2.3,str(today),"Eswar",35,str(today),str(today),str(today),"Hello do scan")
