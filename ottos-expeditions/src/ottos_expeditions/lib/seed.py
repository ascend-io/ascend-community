# constants for seed data
stores_csv = """
ID|Name|Location|Owner|Email
1|Otto's Outdoors|Las Vegas, NV|Steve|steve@ottosexpeditions.com
2|Otto's Oranges & Outdoor Experiences|Orlando, FL|Orlando|orlando@ottosexpeditions.com
3|Otto's Outdoor Adventures|Portland, OR|Portgon|portgon@ottosexpeditions.com
4|Palo Alto's GOATED Expeditions|Palo Alto, CA|Sean|sean@ottosexpeditions.com
5|Otto's Expeditions -- Big Apple|New York, NY|Average New Yorker|average@ottosoranges.com
""".strip()

warehouses_csv = """
id;name;location;owner;email
1;warehouse1;Las Vegas, NV;Steve 2;steve2@ottosexpeditions.com
2;warehouse2;Henderson, NV;Steve;steve@ottosexpeditions.com
3;warehouse3;Austin, TX;Austin;austin@ottosexpeditions.com
""".strip()

routes_csv = """
ID|Name|Difficult Level|Region|Altitude Gain|Length|Average Duration|Previous Success Rate|Best Season
OR-ROC|Otto's Ridge|Difficult|Rockies|1200|15.5|3.5|78.0|Summer
GPT-ALP|Goat Peak Traverse|Extreme|Alps|1500|20.0|5.0|65.0|Fall
SOS-HIM|Summit of Serenity|Moderate|Himalayas|800|10.0|2.5|85.0|Spring
AG-AND|Ascender's Glory|Difficult|Andes|1700|18.5|4.0|70.0|Summer
OVA-CAS|Otto's Vertical Ascent|Extreme|Cascades|2100|22.0|6.0|60.0|Winter
TOTB-ROC|Trail of the Brave|Moderate|Rockies|900|12.0|3.0|80.0|Summer
PP-APP|Pinnacle Path|Easy|Appalachians|600|8.0|1.5|95.0|Fall
EP-ALP|Eagle's Perch|Difficult|Alps|1300|16.5|4.0|75.0|Summer
SA-ROC|Skyline Ascent|Moderate|Rockies|1100|14.0|3.5|82.0|Spring
FPO-HIM|Frozen Peak Odyssey|Extreme|Himalayas|2500|30.0|8.0|55.0|Winter
SOL-AND|Summit of Legends|Difficult|Andes|2000|24.0|6.0|68.0|Spring
OHT-ROC|Otto's High Trail|Moderate|Rockies|1000|13.0|3.0|83.0|Fall
EP-HIM|Everlast Peak|Extreme|Himalayas|2700|28.0|7.5|58.0|Summer
OAA-CAS|Otto's Alpine Adventure|Easy|Cascades|500|7.0|1.0|97.0|Summer
SOS-ALP|Summit of Silence|Difficult|Alps|1400|17.0|4.5|72.0|Fall
NNP-ROC|Neural Network Path|Moderate|Rockies|950|11.5|2.8|84.0|Summer
GML-ALP|Gradient Mountain Loop|Difficult|Alps|1550|19.0|4.8|71.0|Fall
TPU-HIM|Tensor Processing Upload|Extreme|Himalayas|2300|26.0|7.0|57.0|Spring
AGI-AND|Artificial Goat Intelligence|Difficult|Andes|1800|21.0|5.5|69.0|Summer
OAI-CAS|Otto's AI Initiative|Moderate|Cascades|850|10.5|2.3|86.0|Fall
DL-ROC|Deep Learning Loop|Difficult|Rockies|1250|16.0|3.8|76.0|Summer
BP-ALP|Backpropagation Peak|Extreme|Alps|1900|22.5|6.5|62.0|Winter
CNN-HIM|Convolutional Neural Network|Difficult|Himalayas|1600|18.0|4.2|73.0|Spring
RNN-AND|Recurrent Neural Navigation|Moderate|Andes|1050|13.5|3.2|81.0|Summer
OTP-CAS|Otto's Training Path|Easy|Cascades|550|7.5|1.2|96.0|Summer
ML-ROC|Machine Learning Loop|Difficult|Rockies|1350|17.5|4.3|74.0|Fall
GPT-ALP|Goat Parameter Traverse|Extreme|Alps|2200|25.0|6.8|59.0|Summer
LLM-HIM|Large Language Mountain|Difficult|Himalayas|1650|19.5|4.7|70.0|Spring
TF-AND|TensorFlow Trail|Moderate|Andes|1150|14.5|3.4|79.0|Fall
OVG-CAS|Otto's Vector Gateway|Difficult|Cascades|1450|18.0|4.4|73.0|Summer
PT-ROC|PyTorch Path|Moderate|Rockies|900|11.0|2.6|87.0|Spring
KER-ALP|Keras Ridge|Difficult|Alps|1750|20.5|5.2|67.0|Summer
JAX-HIM|JAX Journey|Extreme|Himalayas|2400|27.0|7.2|56.0|Fall
NLP-AND|Natural Language Path|Moderate|Andes|1000|12.5|2.9|83.0|Summer
ONN-CAS|Otto's Neural Network|Difficult|Cascades|1500|18.5|4.5|72.0|Spring
AGD-ROC|Adaptive Gradient Descent|Moderate|Rockies|950|11.8|2.7|85.0|Summer
SGD-ALP|Stochastic Goat Descent|Difficult|Alps|1600|19.2|4.9|69.0|Fall
OPT-HIM|Optimizer Peak Trail|Extreme|Himalayas|2350|26.5|7.1|58.0|Spring
VAE-AND|Variational AutoEncoder|Difficult|Andes|1850|21.5|5.6|68.0|Summer
GAN-CAS|Generative Adversarial Navigation|Moderate|Cascades|875|10.8|2.4|88.0|Fall
MLP-ROC|MultiLayer Perceptron|Difficult|Rockies|1275|16.2|3.9|75.0|Summer
ATN-ALP|Attention Network|Extreme|Alps|1950|22.8|6.6|61.0|Winter
ENC-HIM|Encoder Summit|Difficult|Himalayas|1625|18.2|4.3|74.0|Spring
DEC-AND|Decoder Valley|Moderate|Andes|1075|13.8|3.3|80.0|Summer
OTF-CAS|Otto's Transform Flow|Easy|Cascades|525|7.2|1.1|98.0|Summer
EMB-ROC|Embedding Ridge|Difficult|Rockies|1375|17.8|4.4|73.0|Fall
TOK-ALP|Tokenizer Traverse|Extreme|Alps|2250|25.5|6.9|58.0|Summer
QKV-HIM|Query Key Value Peak|Difficult|Himalayas|1675|19.8|4.8|71.0|Spring
LST-AND|LSTM Loop|Moderate|Andes|1175|14.8|3.5|78.0|Fall
OCL-CAS|Otto's Clustering Course|Difficult|Cascades|1475|18.3|4.5|72.0|Summer
KNN-ROC|K-Nearest Neighbors|Moderate|Rockies|925|11.3|2.7|86.0|Spring
SVM-ALP|Support Vector Mountain|Difficult|Alps|1775|20.8|5.3|66.0|Summer
XGB-HIM|XGBoost Expedition|Extreme|Himalayas|2450|27.5|7.3|55.0|Fall
RFC-AND|Random Forest Circuit|Moderate|Andes|1025|12.8|3.0|82.0|Summer
OBA-CAS|Otto's Bayes Ascent|Difficult|Cascades|1525|18.8|4.6|71.0|Spring
LOG-ROC|Logistic Regression Ridge|Moderate|Rockies|975|12.0|2.8|84.0|Summer
REG-ALP|Ridge Regression Route|Difficult|Alps|1625|19.5|5.0|68.0|Fall
LAS-HIM|Lasso Summit|Extreme|Himalayas|2375|26.8|7.2|57.0|Spring
PCA-AND|Principal Component Ascent|Difficult|Andes|1875|21.8|5.7|67.0|Summer
KMC-CAS|K-Means Climb|Moderate|Cascades|900|11.0|2.5|87.0|Fall
HCA-ROC|Hierarchical Clustering Ascent|Difficult|Rockies|1300|16.5|4.0|74.0|Summer
DBN-ALP|Deep Belief Network|Extreme|Alps|2000|23.0|6.7|60.0|Winter
RBM-HIM|Restricted Boltzmann Mountain|Difficult|Himalayas|1650|18.5|4.4|73.0|Spring
AEN-AND|AutoEncoder Navigation|Moderate|Andes|1100|14.0|3.4|79.0|Summer
OSE-CAS|Otto's Semantic Expedition|Easy|Cascades|575|7.8|1.3|94.0|Summer
TRA-ROC|Transformer Ridge|Difficult|Rockies|1400|18.0|4.5|72.0|Fall
BER-ALP|BERT Traverse|Extreme|Alps|2300|26.0|7.0|57.0|Summer
GPT-HIM|GPT Summit|Difficult|Himalayas|1700|20.0|4.9|70.0|Spring
T5T-AND|T5 Trail|Moderate|Andes|1200|15.0|3.6|77.0|Fall
OLL-CAS|Otto's LLM Loop|Difficult|Cascades|1500|18.5|4.6|71.0|Summer
BAR-ROC|BART Ridge|Moderate|Rockies|950|11.5|2.8|85.0|Spring
ROB-ALP|RoBERTa Route|Difficult|Alps|1800|21.0|5.4|65.0|Summer
ALB-HIM|ALBERT Expedition|Extreme|Himalayas|2500|28.0|7.4|54.0|Fall
DIS-AND|Distillation Circuit|Moderate|Andes|1050|13.0|3.1|81.0|Summer
OFT-CAS|Otto's Fine-Tuning Path|Difficult|Cascades|1550|19.0|4.7|70.0|Spring
PRO-ROC|Prompt Engineering Peak|Moderate|Rockies|1000|12.2|2.9|83.0|Summer
TOK-ALP|Token Optimization Trail|Difficult|Alps|1650|19.8|5.1|67.0|Fall
EMB-HIM|Embedding Summit|Extreme|Himalayas|2400|27.0|7.3|56.0|Spring
VEC-AND|Vector Space Circuit|Difficult|Andes|1900|22.0|5.8|66.0|Summer
SIM-CAS|Similarity Search|Moderate|Cascades|925|11.2|2.6|86.0|Fall
COS-ROC|Cosine Distance Trail|Difficult|Rockies|1325|16.8|4.1|73.0|Summer
EUC-ALP|Euclidean Distance Peak|Extreme|Alps|2050|23.5|6.8|59.0|Winter
MAN-HIM|Manhattan Distance Route|Difficult|Himalayas|1675|18.8|4.5|72.0|Spring
HAM-AND|Hamming Distance Loop|Moderate|Andes|1125|14.2|3.5|78.0|Summer
OKN-CAS|Otto's K-Nearest Path|Easy|Cascades|600|8.0|1.4|93.0|Summer
LSH-ROC|Locality Sensitive Hash|Difficult|Rockies|1425|18.2|4.6|71.0|Fall
ANN-ALP|Approximate Nearest Neighbor|Extreme|Alps|2350|26.5|7.1|56.0|Summer
HNS-AND|HNSW Circuit|Moderate|Andes|1225|15.2|3.7|76.0|Fall
OVS-CAS|Otto's Vector Search|Difficult|Cascades|1525|18.8|4.7|70.0|Summer
FLA-ROC|FAISS Lake Trail|Moderate|Rockies|975|11.8|2.9|84.0|Spring
SCN-ALP|ScaNN Peak|Difficult|Alps|1825|21.2|5.5|64.0|Summer
AZR-HIM|Azure Vector Route|Extreme|Himalayas|2525|28.5|7.5|53.0|Fall
PIN-AND|Pinecone Circuit|Moderate|Andes|1075|13.2|3.2|80.0|Summer
OQD-CAS|Otto's Quantization Descent|Difficult|Cascades|1575|19.2|4.8|69.0|Spring
PQ-ROC|Product Quantization Ridge|Moderate|Rockies|1000|12.0|2.8|83.0|Summer
TQ-ALP|Transform Quantization Trail|Difficult|Alps|1675|20.0|5.2|67.0|Fall
VQ-HIM|Vector Quantization Peak|Extreme|Himalayas|2425|27.5|7.0|56.0|Spring
VQ-AND|Voronoi Quantization Circuit|Difficult|Andes|1925|22.0|5.6|66.0|Summer
VQ-CAS|VQ Clustering Course|Moderate|Cascades|1025|12.5|3.0|82.0|Fall
VQ-ROC|VQ Loop|Difficult|Rockies|1325|16.8|4.1|73.0|Summer
VQ-ALP|VQ Ridge|Extreme|Alps|2025|23.5|6.8|59.0|Winter
VQ-HIM|VQ Summit|Difficult|Himalayas|1725|20.2|5.0|69.0|Spring
VQ-AND|VQ Circuit|Moderate|Andes|1225|15.2|3.7|76.0|Fall
VQ-CAS|VQ Path|Difficult|Cascades|1525|18.8|4.7|70.0|Summer
VQ-ROC|VQ Trail|Moderate|Rockies|975|11.8|2.9|84.0|Spring
VQ-ALP|VQ Route|Difficult|Alps|1825|21.2|5.5|64.0|Summer
VQ-HIM|VQ Expedition|Extreme|Himalayas|2525|28.5|7.5|53.0|Fall
VQ-AND|VQ Loop|Moderate|Andes|1075|13.2|3.2|80.0|Summer
VQ-CAS|VQ Peak|Difficult|Cascades|1575|19.2|4.8|69.0|Spring
VQ-ROC|VQ Trail|Moderate|Rockies|1000|12.0|2.8|83.0|Summer
VQ-ALP|VQ Ridge|Difficult|Alps|1675|20.0|5.2|67.0|Fall
VQ-HIM|VQ Peak|Extreme|Himalayas|2425|27.5|7.0|56.0|Spring
VQ-AND|VQ Circuit|Difficult|Andes|1925|22.0|5.6|66.0|Summer
""".strip()

guides_csv = """
ID,First Name,Last Name,Experience Years,Certifications,Total Expeditions Led,average Success Rate,Customer Rating
1,Debra,Roy,20,"Rock Climbing Instructor, Backcountry Navigation",99,87.1,3.8
2,Michael,Pena,15,Rock Climbing Instructor,17,86.2,5.0
3,Amber,Alvarado,1,"Rock Climbing Instructor, Avalanche Safety, Backcountry Navigation",25,74.7,4.2
4,Carla,Garcia,3,"Wilderness First Aid, Avalanche Safety, Backcountry Navigation",96,70.5,3.7
5,Alyssa,Martinez,6,"Rock Climbing Instructor, Avalanche Safety, Backcountry Navigation",73,71.8,4.6
6,Jacob,Smith,5,"Wilderness First Aid, Backcountry Navigation",72,79.3,4.1
7,Ashley,Colon,3,"Mountain Safety, Wilderness First Aid, Avalanche Safety",37,78.8,4.4
8,Gary,Mayer,19,"Wilderness First Aid, Backcountry Navigation, Avalanche Safety",29,74.6,4.0
9,Jessica,Ritter,15,"Avalanche Safety, Backcountry Navigation",33,75.7,4.1
10,David,Thomas,16,Rock Climbing Instructor,97,81.2,4.6
11,Kristin,Singleton,16,"Avalanche Safety, Backcountry Navigation, Wilderness First Aid",44,76.1,3.5
12,Jorge,Hopkins,18,Wilderness First Aid,98,89.4,4.9
13,Regina,Miranda,11,Avalanche Safety,39,79.6,4.8
14,Natalie,Glass,16,"Mountain Safety, Rock Climbing Instructor, Backcountry Navigation",17,80.6,4.1
15,Mercedes,Davenport,5,"Rock Climbing Instructor, Wilderness First Aid, Mountain Safety",22,74.0,4.1
16,Jeffrey,Bentley,15,"Avalanche Safety, Mountain Safety, Wilderness First Aid",62,73.3,5.0
17,Jacqueline,Berry,7,"Rock Climbing Instructor, Wilderness First Aid, Avalanche Safety",72,86.6,4.0
18,Stephanie,Thompson,6,"Rock Climbing Instructor, Avalanche Safety, Mountain Safety",82,89.1,4.2
19,Andres,Young,9,"Wilderness First Aid, Mountain Safety, Avalanche Safety",45,83.6,3.6
20,Christopher,Knight,14,"Wilderness First Aid, Backcountry Navigation",22,89.2,4.1
21,Deborah,Thompson,10,Wilderness First Aid,89,70.0,4.6
22,Malik,Scott,10,"Wilderness First Aid, Rock Climbing Instructor",20,94.5,4.0
23,James,Tran,6,"Avalanche Safety, Wilderness First Aid, Mountain Safety",47,93.9,4.4
24,Sheri,Delacruz,15,"Avalanche Safety, Rock Climbing Instructor",63,84.9,4.7
25,Nicole,Diaz,11,"Avalanche Safety, Rock Climbing Instructor, Mountain Safety",54,76.4,4.1
26,Brian,Hall,11,"Rock Climbing Instructor, Wilderness First Aid",65,71.0,4.5
27,Justin,Stewart,5,Mountain Safety,90,86.1,3.7
28,Carla,Torres,10,Wilderness First Aid,97,81.6,3.8
29,Victoria,Parsons,4,"Wilderness First Aid, Rock Climbing Instructor, Avalanche Safety",53,78.1,4.9
30,Denise,Ball,7,Rock Climbing Instructor,92,88.5,4.0
31,Renee,Fisher,13,Wilderness First Aid,57,87.2,4.5
32,Cynthia,Hernandez,11,"Avalanche Safety, Backcountry Navigation, Wilderness First Aid",90,75.0,4.1
33,Alexis,Monroe,20,"Backcountry Navigation, Rock Climbing Instructor",61,72.1,3.7
34,Edward,Sanders,15,"Wilderness First Aid, Rock Climbing Instructor, Mountain Safety",95,71.4,3.9
35,Amy,Morris,14,"Rock Climbing Instructor, Mountain Safety",48,85.2,4.3
36,Tricia,Dunn,1,"Wilderness First Aid, Backcountry Navigation, Avalanche Safety",46,83.1,4.2
37,Nancy,Mcclure,8,"Rock Climbing Instructor, Backcountry Navigation, Avalanche Safety",73,81.9,4.6
38,Lisa,Nelson,8,Backcountry Navigation,80,79.6,4.3
39,Amy,Garcia,3,"Backcountry Navigation, Wilderness First Aid",78,92.7,4.8
40,Tracy,Martin,17,"Rock Climbing Instructor, Backcountry Navigation",92,75.2,4.8
41,Cindy,Mendoza,14,Avalanche Safety,82,92.9,5.0
42,Joseph,Garcia,17,"Avalanche Safety, Rock Climbing Instructor",86,79.4,4.7
43,Scott,Mills,20,"Mountain Safety, Wilderness First Aid",87,78.5,3.5
44,Carrie,Carter,8,"Backcountry Navigation, Rock Climbing Instructor, Mountain Safety",64,92.4,4.1
45,Amanda,Clark,2,"Wilderness First Aid, Backcountry Navigation, Avalanche Safety",94,80.5,4.8
46,Angela,Noble,5,Mountain Safety,89,83.8,4.3
47,Carol,Gibson,4,"Wilderness First Aid, Mountain Safety",98,72.2,4.0
48,Brandon,Stokes,12,Avalanche Safety,64,75.4,4.1
49,John,Jones,10,"Avalanche Safety, Wilderness First Aid",69,93.4,3.8
50,Steven,Hansen,8,"Wilderness First Aid, Mountain Safety, Avalanche Safety",45,93.4,4.7
""".strip()
