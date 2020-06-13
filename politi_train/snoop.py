import pandas as pd
import glob
txt_files = glob.glob("*.txt")
image_files=[]
for i in txt_files:
    i=i.replace(".txt", "");
    image_files.append(i)
    
print(image_files)

print(len(image_files))

#print((txt_files))

df=pd.read_csv('train.csv') # enter your filename with exiftags
df['Assessment']=''
df['Compression/Ratio']=''
df['BPP']=''
df['Signature']=''
df['Signature Rotated']=''
df['SW']=''
df['Luminance(QT)']=''
df['Chrominance(QT)']=''
df['Quality Factor(Luminance)']=''
df['Quality Factor(Chrominance)']=''

print (df.name)


for i in image_files:
    #df2=df[df['name'].str.contains(i)]
    #print(df2)    


    file_name=i+".txt"
    sw=[]
    with open(file_name, 'r') as f:
        for line in f:
            if 'Destination ID=0 (Luminance)' in line:
                count=0
                lum_list=[]                
                for line in f:
                    if count<9:
                        #print (line)
                        count=count+1
                        lum_list.append(line)
                    else:
                        break
                        
            if 'Destination ID=1 (Chrominance)' in line:
                count=0
                chrom_list=[]                
                for line in f:
                    if count<9:
                        #print (line)
                        count=count+1
                        chrom_list.append(line)
                    else:
                        break
                    
            #cr=''
            if 'Compression Ratio:' in line:
                cr=line
                print (cr)
            else:
                cr=''
                
            #bpp=''
            if 'Bits per pixel:' in line:
                bpp=line
                #print (line)
            else:
                bpp=''

            if 'Signature:' in line:
                sign=line
                #print (line)
                    
                    
            if 'Signature (Rotated):' in line:
                signR=line
                #print (line)
                
            if 'SW :' in line:
                #print(line)
                sw.append(line)
            

            if 'ASSESSMENT:' in line:
                assessment=line
                #print (line)

                
        lum_li=lum_list[:-1]
        chrom_li=chrom_list[:-1]
        #print (sw)
        #print(lum_li)
        #print(chrom_li)
        #print (cr)
        cr= cr
        print (cr)
        bpp = bpp.strip('Bits per pixel:     ')
        sign = sign.strip('Signature:           ')
        signR = signR.strip('Signature (Rotated): ')
        assessment=assessment.strip('ASSESSMENT: Class 1 - ')
        lum_qf= (lum_list[-1])
        chrom_qf= (chrom_list[-1])
        lum_qf=lum_qf.strip('Approx quality factor = ')
        chrom_qf=chrom_qf.strip('Approx quality factor = ')

        df.loc[df['name'].str.contains(i), 'Assessment'] = assessment
        df.loc[df['name'].str.contains(i), 'Compression/Ratio'] = str(cr)
        df.loc[df['name'].str.contains(i), 'BPP'] = str(bpp)
        df.loc[df['name'].str.contains(i), 'Signature'] = sign
        df.loc[df['name'].str.contains(i), 'Signature Rotated'] = signR
        df.loc[df['name'].str.contains(i), 'SW'] = str(sw)
        df.loc[df['name'].str.contains(i), 'Luminance(QT)'] = str(lum_li)
        df.loc[df['name'].str.contains(i), 'Chrominance(QT)'] = str(chrom_li)
        df.loc[df['name'].str.contains(i), 'Quality Factor(Luminance)'] = lum_qf
        df.loc[df['name'].str.contains(i), 'Quality Factor(Chrominance)'] = chrom_qf

df.to_csv('updated_test.csv', index=False) #your csv with exif and jpegsnoop data
print (df.shape)