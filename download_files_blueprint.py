import requests
import pandas as pd
import os

#Load data
print("Loading file with data")
data = pd.read_csv('blueprint_files_clean.tsv', sep='\t')
print(data.head(10))

#Only b-sequencing data
experiment = 'Bisulfite-Seq'
file_type = 'Methylation signal'
disease = 'Multiple Myeloma'
controls = 'None'
cell_type = ['plasma cell', 'CD14-positive, CD16-negative classical monocyte', 
             'monocyte', 'naive B cell', 'CD38-negative naive B cell']

data_bseq = data[(data['Experiment']== experiment) &
                 (data['File type'] == file_type) &
                 ((data['Disease'] == disease) | 
                 (data['Disease'] == controls)) &
                 (data['Cell type'].isin(cell_type))]

#Output directory for data
outdir = os.path.join('Blueprint', disease.replace(' ', '_'))
if not os.path.exists(outdir):
        os.makedirs(outdir)

print("\nDisponibles {} experimentos de {}, {} con formato {}.".format(data_bseq.shape, experiment, disease, file_type))
print(data_bseq.head(10))

clases = pd.DataFrame()
clases['ID'] = data_bseq['Donor']
clases['Disease'] = data_bseq['Disease']
clases['Cell'] = data_bseq['Cell type']
print(clases)

clases.to_csv(os.path.join(outdir, "clases.csv"), index=True, sep="\t")


for i, row in data_bseq.iterrows():
    print("Downloading...", i)
    url = row['URL']
    myfile = requests.get(url)
    open(os.path.join(outdir, str(i)+'.bw'), 'wb').write(myfile.content)
    