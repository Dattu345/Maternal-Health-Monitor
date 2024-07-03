from fpdf import FPDF
from PIL import Image
from create_table_fpdf2 import PDF
import glob
from datetime import date
def process(pname,examres,cvm,al,fhr,bpd,ofd,hdc,abdc,fl,ci,hc,flbda,flac,ubpi,ubri,ubsd,rubpi,rubri,rubsd,lubpi,lubri,lubsd,fmcapi,fmcri,fmcsd,bpdw,hccw,abdcw,flw,eddu,today,docname,userage):
    data = [
    ["Parameters", "Measured Values", "Weeks",], # 'testing','size'],
    ["B.P.D", str(bpd)+" cms", str(bpdw),], # 'testing','size'],
    ["O.F.D", str(ofd)+" cms", " ",], # 'testing','size'],
    ["Haed Circumference", str(hdc)+" cms", str(hccw),], # 'testing','size'],
    ["ABD Circumference", str(abdc)+"cms", str(abdcw), ], # 'testing','size'],
    ["Femoral Length", str(fl)+" cms", str(flw), ], # 'testing','size'],
    ["C.I ", str(ci)+"% (70-86%)", "", ], # 'testing','size'],
    ["HC /AC ", str(hc)+" (0.92-1.05)", "", ], # 'testing','size'],
    ["FL/BPD ", str(flbda)+"% (71-87 %)", "", ], # 'testing','size'],
    ["FL/ AC ", str(flac)+"% (20-24 %)", " ", ], # 'testing','size'],
    
]
    data1=[["Artery", " PI", "RI","S/D",],["Umbulical Artery",str(ubpi),str(ubri),str(ubsd),],["Right Uterine Artery",str(rubpi),str(rubri),str(rubsd),],["Left Uterine Artery",str(lubpi),str(lubri),str(lubsd),],["Fetal MCA",str(fmcapi),str(fmcri),str(fmcsd)]
    ]
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(10, 10, 'Date '+str(today),0,1,'c')
    pdf.cell(50, 10, 'Age '+str(userage)+'/ Female',0,0,'c')
    pdf.ln()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'COLOR DOPPLER STUDY OF GRAVID UTERUS',0,1,'c')
    pdf.ln()
    pdf.set_font("Times", size=10)
    pdf.cell(40, 10, 'This examination shows'+str(examres),0,0,'c')
    pdf.ln()
    pdf.cell(40,10,'The placenta is Fundo-Anterior in position and of grade II-III maturity',0,0,'c')
    pdf.ln()
    pdf.cell(40, 10, 'The internal os is closed. Cervix measures '+str(cvm)+' cms ',0,0,'c')
    pdf.ln()
    pdf.cell(40,10,'Amount of liquour is reduced with total AFI measuring :'+str(al)+' with Largest pocket measuring 5.0 cms',0,0,'c')
    pdf.ln()
    pdf.cell(40, 10, 'Fetal Cardic activity and movements are present. FHR :'+fhr+' bpm',0,0,'c')
    pdf.ln()
    
    pdf.create_table(table_data = data,title='Fetal parameters are follows', cell_width='even')
    pdf.add_page()
    pdf.create_table(table_data = data1,title='The Colour Doppler Study and following  parameters are Recorded', cell_width='even')
    
    pdf.cell(40, 10, 'Cerebroplacental ratio >1',0,0,'c')
    pdf.ln()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Conclusion',0,0,'c')
    pdf.ln()
    pdf.set_font("Times", size=10)
    pdf.cell(40, 10,str(eddu),0,0,'c')
    pdf.ln()
    
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, docname,0,0,'c')
    pdf.ln()
    pdf.ln()
    pdf.cell(40, 10,'Report with Thanks',0,0,'c')

    

    
        
    
    path='./static/'+pname+'_3.pdf'
    pdf.output(path, 'F')
    print("Pdf Created")
# today = date.today()
# process('hetal rana',3.1,10.5,10.3,2.3,str(today),"Eswar",35,str(today),str(today),str(today),"Hello do scan")
