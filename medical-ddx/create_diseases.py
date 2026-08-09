import os

# Define the diseases and their basic information
diseases = [
    {
        "name": "rheumatoid_arthritis",
        "title": "Rheumatoid Arthritis",
        "overview": "Rheumatoid arthritis is a chronic autoimmune inflammatory disorder that primarily affects joints, causing pain, swelling, stiffness, and potential joint destruction.",
        "symptoms": ["Joint pain and swelling", "Morning stiffness", "Fatigue", "Fever", "Weight loss", "Symmetrical joint involvement"],
        "diagnosis": ["Rheumatoid factor (RF)", "Anti-CCP antibodies", "ESR and CRP", "X-rays", "Physical examination"],
        "treatment": ["DMARDs", "Biologics", "Corticosteroids", "NSAIDs", "Physical therapy"]
    },
    {
        "name": "osteoarthritis",
        "title": "Osteoarthritis",
        "overview": "Osteoarthritis is a degenerative joint disease characterized by breakdown of joint cartilage and underlying bone, causing pain and stiffness.",
        "symptoms": ["Joint pain", "Stiffness", "Reduced range of motion", "Joint crepitus", "Bony enlargement"],
        "diagnosis": ["X-rays", "Physical examination", "Joint aspiration", "MRI (if needed)"],
        "treatment": ["Analgesics", "NSAIDs", "Physical therapy", "Weight management", "Joint replacement"]
    },
    {
        "name": "systemic_lupus_erythematosus",
        "title": "Systemic Lupus Erythematosus (SLE)",
        "overview": "SLE is a chronic autoimmune disease that can affect multiple organ systems including skin, joints, kidneys, heart, and nervous system.",
        "symptoms": ["Malar rash", "Joint pain", "Fatigue", "Fever", "Photosensitivity", "Kidney involvement"],
        "diagnosis": ["ANA", "Anti-dsDNA", "Anti-Sm", "Complement levels", "Complete blood count", "Urinalysis"],
        "treatment": ["Antimalarials", "Corticosteroids", "Immunosuppressants", "Biologics", "Supportive care"]
    },
    {
        "name": "fibromyalgia",
        "title": "Fibromyalgia",
        "overview": "Fibromyalgia is a disorder characterized by widespread musculoskeletal pain accompanied by fatigue, sleep, memory and mood issues.",
        "symptoms": ["Widespread pain", "Fatigue", "Sleep disturbances", "Cognitive difficulties", "Mood changes"],
        "diagnosis": ["Clinical criteria", "Widespread Pain Index", "Symptom Severity Scale", "Tender point examination"],
        "treatment": ["Medications", "Exercise", "Stress management", "Sleep hygiene", "Cognitive behavioral therapy"]
    },
    {
        "name": "osteoporosis",
        "title": "Osteoporosis",
        "overview": "Osteoporosis is a bone disease characterized by decreased bone density and increased fracture risk.",
        "symptoms": ["Often asymptomatic", "Fractures", "Height loss", "Back pain", "Stooped posture"],
        "diagnosis": ["DEXA scan", "X-rays", "Bone markers", "Vitamin D levels", "Calcium levels"],
        "treatment": ["Bisphosphonates", "Calcium and vitamin D", "Exercise", "Fall prevention", "Lifestyle modifications"]
    },
    {
        "name": "gout",
        "title": "Gout",
        "overview": "Gout is a form of inflammatory arthritis caused by deposition of uric acid crystals in joints and tissues.",
        "symptoms": ["Sudden severe joint pain", "Swelling", "Redness", "Warmth", "First metatarsophalangeal joint commonly affected"],
        "diagnosis": ["Serum uric acid", "Joint aspiration", "Synovial fluid analysis", "X-rays", "Ultrasound"],
        "treatment": ["NSAIDs", "Colchicine", "Corticosteroids", "Urate-lowering therapy", "Lifestyle modifications"]
    },
    {
        "name": "deep_vein_thrombosis",
        "title": "Deep Vein Thrombosis (DVT)",
        "overview": "DVT is the formation of blood clots in deep veins, most commonly in the legs, which can lead to pulmonary embolism.",
        "symptoms": ["Leg pain", "Swelling", "Warmth", "Redness", "May be asymptomatic"],
        "diagnosis": ["D-dimer", "Duplex ultrasound", "CT venography", "Wells score", "Physical examination"],
        "treatment": ["Anticoagulation", "Compression stockings", "Early mobilization", "IVC filter (selected cases)"]
    },
    {
        "name": "pulmonary_embolism",
        "title": "Pulmonary Embolism (PE)",
        "overview": "PE is blockage of pulmonary arteries by blood clots, fat, air, or other material, most commonly from DVT.",
        "symptoms": ["Sudden dyspnea", "Chest pain", "Hemoptysis", "Syncope", "Tachycardia"],
        "diagnosis": ["CT pulmonary angiogram", "D-dimer", "ECG", "Chest X-ray", "Wells score"],
        "treatment": ["Anticoagulation", "Thrombolysis", "Embolectomy", "Supportive care"]
    },
    {
        "name": "anemia",
        "title": "Anemia",
        "overview": "Anemia is a condition characterized by decreased number of red blood cells or hemoglobin concentration below normal values.",
        "symptoms": ["Fatigue", "Weakness", "Pale skin", "Shortness of breath", "Cold hands and feet", "Brittle nails"],
        "diagnosis": ["Complete blood count", "Iron studies", "B12 and folate levels", "Hemoglobin electrophoresis", "Bone marrow biopsy"],
        "treatment": ["Iron supplementation", "Vitamin B12/folate", "Treatment of underlying cause", "Blood transfusion", "Erythropoietin"]
    },
    {
        "name": "leukemia",
        "title": "Leukemia",
        "overview": "Leukemia is a group of blood cancers that usually begin in the bone marrow and result in high numbers of abnormal white blood cells.",
        "symptoms": ["Fatigue", "Frequent infections", "Easy bleeding", "Bone pain", "Swollen lymph nodes"],
        "diagnosis": ["Complete blood count", "Bone marrow biopsy", "Flow cytometry", "Cytogenetics", "Molecular testing"],
        "treatment": ["Chemotherapy", "Targeted therapy", "Immunotherapy", "Stem cell transplant", "Supportive care"]
    },
    {
        "name": "lymphoma",
        "title": "Lymphoma",
        "overview": "Lymphoma is a group of blood cancers that develop from lymphocytes, including Hodgkin and non-Hodgkin lymphoma.",
        "symptoms": ["Swollen lymph nodes", "Fever", "Night sweats", "Weight loss", "Fatigue"],
        "diagnosis": ["Lymph node biopsy", "CT/PET scans", "Bone marrow biopsy", "Flow cytometry", "Immunohistochemistry"],
        "treatment": ["Chemotherapy", "Radiation therapy", "Immunotherapy", "Stem cell transplant", "Targeted therapy"]
    },
    {
        "name": "thyroid_cancer",
        "title": "Thyroid Cancer",
        "overview": "Thyroid cancer develops in the cells of the thyroid gland and includes several types with different behaviors and prognoses.",
        "symptoms": ["Thyroid nodule", "Neck swelling", "Voice changes", "Difficulty swallowing", "Neck pain"],
        "diagnosis": ["Thyroid ultrasound", "Fine needle aspiration", "Thyroid function tests", "CT/MRI", "Radioiodine scan"],
        "treatment": ["Thyroidectomy", "Radioactive iodine", "Thyroid hormone therapy", "Chemotherapy", "Targeted therapy"]
    },
    {
        "name": "breast_cancer",
        "title": "Breast Cancer",
        "overview": "Breast cancer is a malignant tumor that develops from breast tissue cells, most commonly from milk ducts or lobules.",
        "symptoms": ["Breast lump", "Breast pain", "Nipple discharge", "Skin changes", "Lymph node swelling"],
        "diagnosis": ["Mammography", "Breast ultrasound", "MRI", "Biopsy", "Tumor markers"],
        "treatment": ["Surgery", "Chemotherapy", "Radiation therapy", "Hormone therapy", "Targeted therapy"]
    },
    {
        "name": "prostate_cancer",
        "title": "Prostate Cancer",
        "overview": "Prostate cancer is a malignant tumor of the prostate gland, most common in older men and often slow-growing.",
        "symptoms": ["Urinary symptoms", "Blood in urine", "Erectile dysfunction", "Bone pain", "Often asymptomatic"],
        "diagnosis": ["PSA", "Digital rectal exam", "Prostate biopsy", "MRI", "Bone scan"],
        "treatment": ["Active surveillance", "Surgery", "Radiation therapy", "Hormone therapy", "Chemotherapy"]
    },
    {
        "name": "colorectal_cancer",
        "title": "Colorectal Cancer",
        "overview": "Colorectal cancer is cancer that begins in the colon or rectum, often developing from precancerous polyps.",
        "symptoms": ["Changes in bowel habits", "Blood in stool", "Abdominal pain", "Weight loss", "Fatigue"],
        "diagnosis": ["Colonoscopy", "CT scan", "CEA", "Stool tests", "Biopsy"],
        "treatment": ["Surgery", "Chemotherapy", "Radiation therapy", "Targeted therapy", "Immunotherapy"]
    },
    {
        "name": "lung_cancer",
        "title": "Lung Cancer",
        "overview": "Lung cancer is a malignant tumor characterized by uncontrolled cell growth in lung tissues, strongly associated with smoking.",
        "symptoms": ["Persistent cough", "Hemoptysis", "Chest pain", "Dyspnea", "Weight loss"],
        "diagnosis": ["Chest X-ray", "CT scan", "PET scan", "Biopsy", "Molecular testing"],
        "treatment": ["Surgery", "Chemotherapy", "Radiation therapy", "Targeted therapy", "Immunotherapy"]
    },
    {
        "name": "skin_cancer",
        "title": "Skin Cancer",
        "overview": "Skin cancer includes melanoma and non-melanoma types, caused by abnormal growth of skin cells, often due to UV exposure.",
        "symptoms": ["Changes in moles", "New growths", "Irregular borders", "Color changes", "Bleeding or itching"],
        "diagnosis": ["Skin examination", "Dermoscopy", "Biopsy", "Imaging studies", "Lymph node assessment"],
        "treatment": ["Surgical excision", "Mohs surgery", "Radiation therapy", "Immunotherapy", "Targeted therapy"]
    },
    {
        "name": "pancreatic_cancer",
        "title": "Pancreatic Cancer",
        "overview": "Pancreatic cancer is an aggressive malignancy of the pancreas with poor prognosis due to late diagnosis and limited treatment options.",
        "symptoms": ["Abdominal pain", "Weight loss", "Jaundice", "New-onset diabetes", "Fatigue"],
        "diagnosis": ["CT scan", "MRI", "Endoscopic ultrasound", "CA 19-9", "Biopsy"],
        "treatment": ["Surgery", "Chemotherapy", "Radiation therapy", "Palliative care", "Clinical trials"]
    },
    {
        "name": "liver_cancer",
        "title": "Liver Cancer",
        "overview": "Primary liver cancer includes hepatocellular carcinoma and cholangiocarcinoma, often developing in patients with chronic liver disease.",
        "symptoms": ["Abdominal pain", "Weight loss", "Ascites", "Jaundice", "Fatigue"],
        "diagnosis": ["CT/MRI", "Alpha-fetoprotein", "Ultrasound", "Biopsy", "Liver function tests"],
        "treatment": ["Surgery", "Liver transplant", "Ablation", "Chemoembolization", "Targeted therapy"]
    },
    {
        "name": "kidney_cancer",
        "title": "Kidney Cancer",
        "overview": "Kidney cancer most commonly refers to renal cell carcinoma, arising from kidney tubular epithelial cells.",
        "symptoms": ["Hematuria", "Flank pain", "Abdominal mass", "Weight loss", "Fever"],
        "diagnosis": ["CT scan", "MRI", "Ultrasound", "Chest X-ray", "Biopsy"],
        "treatment": ["Surgery", "Targeted therapy", "Immunotherapy", "Radiation therapy", "Ablation"]
    },
    {
        "name": "bladder_cancer",
        "title": "Bladder Cancer",
        "overview": "Bladder cancer is a malignancy of the bladder wall, most commonly transitional cell carcinoma, associated with smoking and chemical exposure.",
        "symptoms": ["Hematuria", "Urinary frequency", "Urgency", "Dysuria", "Pelvic pain"],
        "diagnosis": ["Cystoscopy", "Urine cytology", "CT urography", "Biopsy", "Imaging studies"],
        "treatment": ["Surgery", "Intravesical therapy", "Chemotherapy", "Radiation therapy", "Immunotherapy"]
    },
    {
        "name": "ovarian_cancer",
        "title": "Ovarian Cancer",
        "overview": "Ovarian cancer is a malignancy arising from the ovaries, often diagnosed at advanced stages due to subtle early symptoms.",
        "symptoms": ["Abdominal bloating", "Pelvic pain", "Urinary symptoms", "Fatigue", "Weight loss"],
        "diagnosis": ["Pelvic exam", "Transvaginal ultrasound", "CT scan", "CA-125", "Biopsy"],
        "treatment": ["Surgery", "Chemotherapy", "Targeted therapy", "Hormone therapy", "Clinical trials"]
    },
    {
        "name": "cervical_cancer",
        "title": "Cervical Cancer",
        "overview": "Cervical cancer is a malignancy of the cervix, usually caused by human papillomavirus (HPV) infection, preventable through screening.",
        "symptoms": ["Abnormal vaginal bleeding", "Pelvic pain", "Pain during intercourse", "Vaginal discharge"],
        "diagnosis": ["Pap smear", "HPV testing", "Colposcopy", "Biopsy", "Imaging studies"],
        "treatment": ["Surgery", "Radiation therapy", "Chemotherapy", "Targeted therapy", "Immunotherapy"]
    },
    {
        "name": "endometrial_cancer",
        "title": "Endometrial Cancer",
        "overview": "Endometrial cancer is a malignancy of the uterine lining, most common gynecologic cancer in developed countries.",
        "symptoms": ["Abnormal uterine bleeding", "Pelvic pain", "Pain during intercourse", "Weight loss"],
        "diagnosis": ["Endometrial biopsy", "Transvaginal ultrasound", "MRI", "Hysteroscopy", "CT scan"],
        "treatment": ["Surgery", "Radiation therapy", "Chemotherapy", "Hormone therapy", "Targeted therapy"]
    },
    {
        "name": "testicular_cancer",
        "title": "Testicular Cancer",
        "overview": "Testicular cancer is a malignancy arising from testicular tissue, most common solid tumor in young men aged 15-35.",
        "symptoms": ["Testicular lump", "Testicular pain", "Scrotal swelling", "Back pain", "Breast enlargement"],
        "diagnosis": ["Physical examination", "Testicular ultrasound", "Tumor markers", "CT scan", "Chest X-ray"],
        "treatment": ["Orchiectomy", "Chemotherapy", "Radiation therapy", "Surveillance", "Retroperitoneal lymph node dissection"]
    },
    {
        "name": "brain_tumor",
        "title": "Brain Tumor",
        "overview": "Brain tumors are abnormal growths in the brain tissue, which can be primary or metastatic, benign or malignant.",
        "symptoms": ["Headaches", "Seizures", "Neurological deficits", "Cognitive changes", "Nausea and vomiting"],
        "diagnosis": ["MRI", "CT scan", "Biopsy", "PET scan", "Neurological examination"],
        "treatment": ["Surgery", "Radiation therapy", "Chemotherapy", "Targeted therapy", "Supportive care"]
    },
    {
        "name": "meningitis",
        "title": "Meningitis",
        "overview": "Meningitis is inflammation of the protective membranes covering the brain and spinal cord, which can be bacterial, viral, or fungal.",
        "symptoms": ["Fever", "Headache", "Neck stiffness", "Photophobia", "Altered mental status"],
        "diagnosis": ["Lumbar puncture", "CSF analysis", "Blood cultures", "CT/MRI", "PCR testing"],
        "treatment": ["Antibiotics", "Antiviral therapy", "Corticosteroids", "Supportive care", "Prevention with vaccines"]
    },
    {
        "name": "sepsis",
        "title": "Sepsis",
        "overview": "Sepsis is a life-threatening organ dysfunction caused by a dysregulated host response to infection.",
        "symptoms": ["Fever or hypothermia", "Tachycardia", "Altered mental status", "Hypotension", "Oliguria"],
        "diagnosis": ["Blood cultures", "Lactate levels", "Procalcitonin", "Complete blood count", "Organ function tests"],
        "treatment": ["Antibiotics", "Fluid resuscitation", "Vasopressors", "Source control", "Supportive care"]
    },
    {
        "name": "tuberculosis",
        "title": "Tuberculosis (TB)",
        "overview": "Tuberculosis is an infectious disease caused by Mycobacterium tuberculosis, primarily affecting the lungs but can involve other organs.",
        "symptoms": ["Persistent cough", "Hemoptysis", "Weight loss", "Night sweats", "Fever"],
        "diagnosis": ["Chest X-ray", "Sputum smear and culture", "Tuberculin skin test", "Interferon-gamma release assays", "GeneXpert"],
        "treatment": ["Anti-TB drugs", "Directly observed therapy", "Treatment of contacts", "Drug resistance testing", "Supportive care"]
    },
    {
        "name": "hepatitis",
        "title": "Hepatitis",
        "overview": "Hepatitis is inflammation of the liver, commonly caused by viral infections (A, B, C, D, E) but can also be due to alcohol, drugs, or autoimmune causes.",
        "symptoms": ["Jaundice", "Fatigue", "Abdominal pain", "Nausea", "Dark urine"],
        "diagnosis": ["Liver function tests", "Viral serology", "Hepatitis viral markers", "Ultrasound", "Liver biopsy"],
        "treatment": ["Antiviral therapy", "Supportive care", "Lifestyle modifications", "Vaccination", "Liver transplant"]
    },
    {
        "name": "cirrhosis",
        "title": "Cirrhosis",
        "overview": "Cirrhosis is end-stage liver disease characterized by fibrosis and nodular regeneration, resulting from chronic liver injury.",
        "symptoms": ["Fatigue", "Ascites", "Jaundice", "Portal hypertension", "Hepatic encephalopathy"],
        "diagnosis": ["Liver function tests", "Imaging studies", "Liver biopsy", "Endoscopy", "FibroScan"],
        "treatment": ["Treat underlying cause", "Manage complications", "Liver transplant", "Lifestyle modifications", "Regular monitoring"]
    },
    {
        "name": "peptic_ulcer_disease",
        "title": "Peptic Ulcer Disease",
        "overview": "Peptic ulcer disease involves ulcerations in the stomach or duodenum, commonly caused by H. pylori infection or NSAIDs.",
        "symptoms": ["Epigastric pain", "Nausea", "Bloating", "Bleeding", "Perforation"],
        "diagnosis": ["Upper endoscopy", "H. pylori testing", "Barium studies", "CT scan", "Stool tests"],
        "treatment": ["H. pylori eradication", "Proton pump inhibitors", "Avoid NSAIDs", "Surgery for complications", "Lifestyle modifications"]
    },
    {
        "name": "gallbladder_disease",
        "title": "Gallbladder Disease",
        "overview": "Gallbladder disease includes cholelithiasis, cholecystitis, and cholangitis, commonly presenting with biliary colic and inflammation.",
        "symptoms": ["Right upper quadrant pain", "Nausea", "Vomiting", "Fever", "Jaundice"],
        "diagnosis": ["Ultrasound", "CT scan", "HIDA scan", "MRCP", "Laboratory tests"],
        "treatment": ["Cholecystectomy", "Antibiotics", "ERCP", "Conservative management", "Lithotripsy"]
    },
    {
        "name": "pancreatitis",
        "title": "Pancreatitis",
        "overview": "Pancreatitis is inflammation of the pancreas, which can be acute or chronic, commonly caused by gallstones or alcohol.",
        "symptoms": ["Severe abdominal pain", "Nausea", "Vomiting", "Fever", "Steatorrhea"],
        "diagnosis": ["Lipase and amylase", "CT scan", "MRI", "ERCP", "Ultrasound"],
        "treatment": ["Pain management", "Fluid resuscitation", "Treat underlying cause", "Pancreatic enzymes", "Surgery"]
    },
    {
        "name": "appendicitis",
        "title": "Appendicitis",
        "overview": "Appendicitis is inflammation of the appendix, a medical emergency requiring prompt surgical intervention to prevent complications.",
        "symptoms": ["Right lower quadrant pain", "Nausea", "Vomiting", "Fever", "Loss of appetite"],
        "diagnosis": ["Clinical examination", "CT scan", "Ultrasound", "Laboratory tests", "Alvarado score"],
        "treatment": ["Appendectomy", "Antibiotics", "Pain management", "Laparoscopic surgery", "Conservative management in select cases"]
    },
    {
        "name": "diverticulitis",
        "title": "Diverticulitis",
        "overview": "Diverticulitis is inflammation of diverticula in the colon, commonly affecting the sigmoid colon in Western populations.",
        "symptoms": ["Left lower quadrant pain", "Fever", "Changes in bowel habits", "Nausea", "Bloating"],
        "diagnosis": ["CT scan", "Clinical examination", "Laboratory tests", "Colonoscopy", "Ultrasound"],
        "treatment": ["Antibiotics", "Clear liquid diet", "Pain management", "Surgery for complications", "High-fiber diet prevention"]
    },
    {
        "name": "celiac_disease",
        "title": "Celiac Disease",
        "overview": "Celiac disease is an autoimmune disorder triggered by gluten consumption, leading to small intestine damage and malabsorption.",
        "symptoms": ["Diarrhea", "Abdominal pain", "Weight loss", "Fatigue", "Dermatitis herpetiformis"],
        "diagnosis": ["Serology testing", "Small bowel biopsy", "Genetic testing", "Gluten challenge", "Response to gluten-free diet"],
        "treatment": ["Strict gluten-free diet", "Nutritional supplementation", "Monitor for complications", "Dietary counseling", "Regular follow-up"]
    },
    {
        "name": "lactose_intolerance",
        "title": "Lactose Intolerance",
        "overview": "Lactose intolerance is the inability to digest lactose due to lactase enzyme deficiency, causing gastrointestinal symptoms.",
        "symptoms": ["Bloating", "Diarrhea", "Abdominal cramps", "Gas", "Nausea"],
        "diagnosis": ["Lactose tolerance test", "Hydrogen breath test", "Genetic testing", "Elimination diet", "Clinical assessment"],
        "treatment": ["Lactose-free diet", "Lactase supplements", "Gradual lactose reintroduction", "Calcium supplementation", "Probiotics"]
    },
    {
        "name": "food_allergies",
        "title": "Food Allergies",
        "overview": "Food allergies are immune-mediated reactions to specific food proteins, ranging from mild symptoms to life-threatening anaphylaxis.",
        "symptoms": ["Hives", "Swelling", "Gastrointestinal symptoms", "Respiratory symptoms", "Anaphylaxis"],
        "diagnosis": ["Skin prick tests", "Serum-specific IgE", "Food challenge tests", "Component-resolved diagnostics", "Clinical history"],
        "treatment": ["Allergen avoidance", "Epinephrine auto-injectors", "Antihistamines", "Emergency action plan", "Immunotherapy research"]
    }
]

# Create disease files
data_dir = "f:/Data_Science/GenAI With Krish Naik/Langchain Project/ddx_project/data"

for disease in diseases:
    filename = f"{disease['name']}.txt"
    filepath = os.path.join(data_dir, filename)
    
    content = f"""{disease['title']}

Overview:
{disease['overview']}

Clinical Presentation:
Common Symptoms:"""
    
    for symptom in disease['symptoms']:
        content += f"\n- {symptom}"
    
    content += f"""

Diagnosis:
Key Diagnostic Tests:"""
    
    for test in disease['diagnosis']:
        content += f"\n- {test}"
    
    content += f"""

Treatment:
Management Approaches:"""
    
    for treatment in disease['treatment']:
        content += f"\n- {treatment}"
    
    content += f"""

Key Points:
- {disease['title']} is an important medical condition requiring proper diagnosis and management
- Early recognition and appropriate treatment can significantly improve patient outcomes
- Regular follow-up and monitoring are essential for optimal care
- Patient education and compliance with treatment recommendations are crucial
- Multidisciplinary approach may be beneficial for comprehensive care
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created {filename}")

print(f"Successfully created {len(diseases)} disease files!")
