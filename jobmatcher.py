from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter 
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
import io, csv, re
import pyparsing as pp

matchings = []
listings = [[]]
best_jobs = []
concentration = []
organization, job_type, job_title, job_description, location = [], [], [], [], []

# Converting pdf to txt file for library 

def pdf2txt(PDFfile, TXTfile):
    in_file = open(PDFfile, 'rb')
    res_mgr = PDFResourceManager()
    data = io.StringIO()
    TxtConverter = TextConverter(res_mgr, data, laparams=LAParams())
    interpreter = PDFPageInterpreter(res_mgr, TxtConverter)
    for page in PDFPage.get_pages(in_file):
        interpreter.process_page(page)
    
    txt = data.getvalue()
    with open(TXTfile, 'w') as f:
        f.write(txt)

# Function that searches for best match in jobs dataset

def find_matches(user_resume):
    with open(user_resume, 'r') as resume:
        with open('small_jobs_dataset.csv', 'r') as job_listings_csv:
            # Splitting dataset rows by delimiter
            csv_reader = csv.reader(job_listings_csv)
            count = 0
            # Reading user's resume into variable
            resume_var = resume.read()
            for row in csv_reader:
                str_row = str(row)
                job_as_list = pp.commaSeparatedList.parseString(str_row).asList()
                # Storing job description 
                job_desc = job_as_list[4]
                if count > 0:
                    # Feature extraction on job desc and resume
                    text = [resume_var, job_desc]
                    count_vec = CountVectorizer()
                    count_matrix = count_vec.fit_transform(text)
                    match = cosine_similarity(count_matrix)[0][1] * 100
                    matchings.append(tuple((match, count)))
                    listings.append(job_as_list)

                count += 1   
    # Sorting by jobs with highest match
    matchings.sort(reverse=True)
    # Storing jobs with highest match and user's concentration
    for i in range(5):
        match = matchings[i]
        job = listings[int(match[1])]
        split_string = job
        organization.append(split_string[0].strip('\"'))
        job_type.append(split_string[3].strip('\"'))
        job_title.append(split_string[7].strip('\"'))
        job_description.append(split_string[4].strip('\"'))
        location.append(split_string[6].strip('\"'))
        if i == 0:
            job_industry = split_string[3]
            job_industry = job_industry.strip('\"')
            concentration.append(job_industry)


    
    
# Resume needs to be converted from pdf to txt
    
PDFfile = 'my_resume-9.pdf'
TXTfile =  'parsed_resume.txt'

# Converting pdf resume to txt

pdf2txt(PDFfile, TXTfile)

# Calling find_matches function

find_matches('parsed_resume.txt')

# Printing results

for i in range(5):
    print('Job ' + str(i) + ': ' + '\n')
    print(organization[i] + '\n' + job_type[i] + '\n' + job_title[i] + '\n' + job_description[i] + '\n' + location[i] + '\n')
    print('Match Percentage: ' + str(matchings[i][0]) + '\n')

print(concentration)



 

         


    


