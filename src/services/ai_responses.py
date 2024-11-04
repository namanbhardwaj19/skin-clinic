import re
import os
import time
from datetime import datetime
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64
from fastapi.logger import logger
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
ORGANIZATION = os.getenv("ORGANIZATION")
PROJECT_ID = os.getenv("PROJECT_ID")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
GOOGLE_SERVICE_ACCOUNT_URL = os.getenv("GOOGLE_SERVICE_ACCOUNT_URL")
GOOGLE_SHEET_URL_FOR_UNANSWERED_QUESTIONS = os.getenv("GOOGLE_SHEET_URL_FOR_UNANSWERED_QUESTIONS")
GOOGLE_SHEET_URL_FOR_CALL_BACK_REQUESTS = os.getenv("GOOGLE_SHEET_URL_FOR_CALL_BACK_REQUESTS")
IMPERSONATED_USER = os.getenv("IMPERSONATED_USER")
EMAIL_TO_USER = os.getenv("EMAIL_TO_USER")
SATORIAI_GMAIL_KEY = os.getenv("SATORIAI_GMAIL_KEY")


SCOPES = ['https://mail.google.com/'] #['https://www.googleapis.com/auth/gmail.send']

user_thread_info = {}

client = OpenAI(
  api_key=OPEN_AI_API_KEY,
  organization=ORGANIZATION,
  project=PROJECT_ID,
)


def get_ai_response(user_phone, message):
    """
    this function will generate the response for the given query
    """
    thread_id = add_message_in_thread(user_phone, message)
    text = run_thread(thread_id, user_phone)
    return text


def add_message_in_thread(user_phone, message):
    """
    this function will add the user's message in thread, if thread is not
     already created, it will create a thread and then put new message in it
    """
    thread_id = user_thread_info.get(user_phone)
    if not thread_id:
        new_thread = client.beta.threads.create()
        thread_id = new_thread.id
        user_thread_info[user_phone] = thread_id

        client.beta.threads.messages.create(
            thread_id,
            role="user",
            content='''
                Refer to this knowledge base and try retrieving information from this for the questions asked in this thread. - Expert Botox Treatments in London
At Damalis Skin Clinic, located in the heart of Wimbledon, we specialise in providing only the very best Botox treatments. Our clinic, renowned for its expertise in cosmetic procedures, offers a unique approach to Botox, ensuring each client receives the best possible care and results. Dr Stephanie Damalis, our leading Botox doctor, brings a wealth of experience to each treatment, making our clinic a sought-after destination for those seeking effective wrinkle reduction in expert hands.
Book Online
 
What is Botox?
Botox, a brand name for Botulinum toxin, is a popular cosmetic treatment known for its ability to reduce the appearance of ageing in the form of lines and wrinkles. This treatment, widely used across the world, works by temporarily paralysing facial muscles, smoothing out lines and improving overall facial aesthetics. Botox is not only about enhancing beauty by treating severe frown lines and crow’s feet; it’s also used in treating various medical conditions throughout the world. Examples of this are excess sweating, migraines, and bladder issues. There are many other examples where botulinum toxin has been used for decades for medical issues.
Why Choose Botox?
Choosing Botox for your wrinkle treatment is a decision many make due to its effectiveness and quick results. When administered by experienced professionals like those at Damalis Skin Clinic, Botox injections offer a safe and reliable solution to reduce the signs of ageing. The treatment is minimally invasive, with little to no downtime, making it a convenient option for those with busy lifestyles.
How Does Botox Work?
Botulinum toxin works by blocking nerve signals in the muscles where it is injected. This action prevents the muscle from contracting, reducing the appearance of lines and wrinkles. The procedure is quick, typically taking only a few minutes, and the results can last several months, depending on the individual and the treated area.
Treatment Overview
 
PROCEDURE TIME
30 minutes
 
PRICE
From £250
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
3-4 months
 
Finals results seen
After 2 weeks
 
Number of treatments
1
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
Why Choose Damalis Skin Clinic for Your Botox Treatment
Damalis Skin Clinic, led by Dr Stephanie Damalis, offers a personalised approach to Anti-Wrinkle / Botox treatment. 
Dr Stephanie Damalis is a medical and cosmetic doctor with over 12 years of experience. She completed her medical degree in Cape Town, South Africa and further expanded her aesthetic knowledge by completing postgraduate-level medical aesthetics qualifications in Botox, Dermal Fillers and Cosmetic Dermatology at Harley Academy.
Dr Steph is an advocate for patient safety and this is why she continues to teach medical professionals in the aesthetic sector at Harley Academy.
Dr Steph believes in subtle cosmetic results that will keep you looking natural and still like you.
The clinic combines professional expertise with advanced treatments and high-quality, medical-grade products to provide effective solutions for various skin types.
 
 
Botox Treatment Process at Damalis Skin Clinic
Initial Consultation
Your journey begins with a detailed consultation where we assess your facial structure and discuss your aesthetic goals.
The Botox Injection Procedure
Utilising the latest techniques, our doctor will precisely administer Botox toxin injections, focusing on the areas that will provide the most natural and effective results.
Aftercare and Follow-up
Post-treatment care is crucial. We provide comprehensive aftercare advice and schedule follow-up appointments to monitor your progress and ensure optimal results.
Botox Treatment Areas and Effectiveness
Common Treatment Areas
Botox is the most effective procedure as Anti-Wrinkle / Botox treatments go. It is commonly used to treat areas such as the forehead, around the eyes, and between the brows. Anywhere where lines caused by repeated movements form. It’s effective in reducing the appearance of forehead lines, crow’s feet, and frown lines.
Results and Longevity of Botox
The results of Botox can be seen within a few days and typically last between 3 to 6 months. Regular treatments can maintain these results, keeping your skin smooth and youthful.
Botox Treatment Prices at Damalis Skin Clinic
The cost of treatment in our Wimbledon clinic begins at a competitive rate of £190 for one area. This initial price serves as a starting point, with the final quote tailored to meet your specific needs and treatment goals. During your initial consultation in clinic, our team, led by the experienced Dr Stephanie Damalis, will provide a detailed breakdown of all costs involved.
Suitable People for Botox
Botox is suitable for most adults seeking to reduce the appearance of facial lines and wrinkles. It is particularly effective for those with moderate to severe frown lines. We assess your suitability for Botox during your initial visit and discuss any potential contraindications.
Booking Your Botox Appointment at Damalis Skin Clinic
To book your Botox appointment at Damalis Skin Clinic, simply contact us through our website or feel free to call. Our friendly team will guide you through the booking process and answer any questions you may have about this, or any of our treatments.
Damalis Skin Clinic stands out for the excellence of its aesthetic treatments. With our experienced doctor, Dr Stephanie Damalis, and our commitment to personalised care, we ensure that each patient leaves us feeling confident and satisfied with their results. Whether you’re seeking to treat facial lines like frown lines or explore the benefits of Botox for medical reasons, we are equipped to provide the best treatment tailored to your needs.
Botox FAQs
Check out some frequently asked questions about Botox our patients regularly ask us.
Why should I choose Damalis Skin Clinic Aesthetic Clinic for Botox treatments?
Our clinic is renowned for its experienced practitioners and personalised approach to Anti-Wrinkle / Botox treatments. We prioritise natural-looking results and offer a comfortable, safe environment for your Botox experience.
Are Botox injections safe?
Yes, Botox injections in Wimbledon are generally safe when administered by qualified professionals. Dr Damalis is a  trained expert who follows strict protocols to ensure your safety and provide effective Botox treatments.
How long do the results of Botox treatments last?
Results can vary, but typically Botox results last around 3 to 4 months. Regular maintenance appointments at our London aesthetic clinic can help you maintain your desired youthful appearance.
What areas can be treated with Botox?
Botox is commonly used to treat forehead lines, crow’s feet, and frown lines between the eyebrows. We offer pre-treatment  consultations (always required for Botox treatments) to determine the best treatment path for your specific needs.
Are there any side effects associated with Botox?
Mild bruising, swelling, or redness at the injection site are possible but temporary side effects. We can minimise these risks through careful administration techniques.
How long is the recovery time after a Botox treatment?
There is typically no downtime after a Botox treatment. You can resume your daily activities immediately, although we recommend avoiding strenuous exercise for the first 24 hours. Dr Damalis will provide you with post-treatment care instructions.
Can Botox be combined with other treatments for enhanced results?
Absolutely, Botox can be combined with dermal fillers or other aesthetic treatments to achieve comprehensive facial rejuvenation. Our clinic offers personalised treatment plans that cater to your unique goals.
Is Botox suitable for all skin types and ages?
Botox is generally suitable for a wide range of skin types and ages, but individual assessments are essential. Our clinic’s experts will evaluate your skin and medical history to determine the best approach for you.
How do I schedule a Botox consultation at your aesthetic clinic?
Scheduling a consultation is easy. You can contact our clinic via phone, email, or our website to book an appointment. During the consultation, Dr Damalis will discuss your goals and recommend a personalised Botox treatment plan tailored to your needs.
 

Neck & Platysmal Bands Botox in London
At Damalis Skin Clinic in Wimbledon, London, we offer a specialised neck and platysmal bands Botox, administered by the experienced and skilled Dr. Stephanie Damalis. This non-invasive cosmetic procedure is designed to address various concerns related to the neck area, providing a rejuvenated and youthful appearance. Benefits of Neck Botox
1.	Reduction of Platysmal Bands
o	Neck Botox effectively targets and relaxes the platysma muscle, which can cause prominent vertical bands on the neck. By smoothing out these bands, you can achieve a more youthful and refined neck contour.
2.	Improved Neck Skin Texture
o	Botox injections in the neck area can help reduce fine lines and wrinkles, resulting in smoother and tighter skin. This treatment can promote collagen production, leading to a more youthful appearance.
3.	Enhanced Jawline Definition
o	By addressing platysmal bands, Neck Botox can improve the definition of your jawline, resulting in a more sculpted and youthful appearance.
4.	Subtle and Natural-Looking Results
o	The expertise of Dr. Stephanie Damalis ensures that the treatment is administered with precision, providing natural-looking results. You can achieve a refreshed appearance without the need for surgery.
5.	Quick and Painless Procedure
o	Neck Botox is a non-surgical procedure that requires minimal downtime. The treatment is relatively quick, making it convenient for individuals with busy schedules.
6.	Treatment Overview
7.	 
8.	PROCEDURE TIME
9.	30 minutes
10.	 
11.	PRICE
12.	£380
13.	 
14.	ANAESTHESIA NEEDED
15.	No
16.	 
17.	DISCOMFORT LEVEL
18.	Minimal
19.	 
20.	BACK TO WORK
21.	Immediately
22.	 
23.	DURATION OF RESULTS
24.	3-4 months
25.	 
26.	FINALS RESULTS SEEN
27.	After 2 weeks
28.	 
29.	NUMBER OF TREATMENTS
30.	1
31.	Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure.
Concerns Treated
The neck Botox & platysmal bands treatment is designed to address the following concerns:
1.	Platysmal Bands
o	This treatment effectively reduces the appearance of platysmal bands, which can make the neck appear aged and less defined.
2.	Neck Wrinkles
o	Botox can smooth out neck wrinkles, including horizontal lines, resulting in a more youthful and rejuvenated neck.
3.	Loss of Jawline Definition
o	By targeting the platysma muscle, Neck Botox can enhance the jawline, restoring a more youthful and contoured appearance.
4.	Ageing Neck Skin
o	The treatment promotes the production of collagen, which can improve the texture and firmness of the skin in the neck area, combating the signs of ageing.
Who Is It For?
The neck Botox & platysmal bands treatment is suitable for individuals who are concerned about the signs of ageing in their neck area and are looking for a non-invasive solution. It is particularly beneficial for those who want to:
•	Address platysmal bands and wrinkles in the neck.
•	Achieve a more defined jawline.
•	Improve the overall texture and appearance of the neck skin.
•	Benefit from a treatment that provides natural and subtle results.
•	Avoid the downtime and invasiveness associated with surgery.

Jawline Slimming in London
We’re proud to offer a non-surgical solution to help you achieve a more sculpted and refined jawline with the expertise of Dr. Stephanie Damalis at our clinic in Wimbledon, London. Our Botox for jaw slimming treatment is a safe and effective way to address various concerns related to the jawline and facial aesthetics.
Benefits of Botox for Jawline Slimming
1.	Enhanced Facial Contour
o	Botox can be strategically injected along the jawline to reduce the prominence of the masseter muscles. This results in a softer and more V-shaped jawline, creating a harmonious balance in your facial profile.
2.	Non-Invasive
o	This treatment doesn’t require surgery or downtime, making it a convenient option for those seeking jawline contouring without the risks associated with invasive procedures.
3.	Personalised Results
o	Dr. Stephanie Damalis customises the treatment to suit your unique facial anatomy and aesthetic goals, ensuring natural-looking results that enhance your individual beauty.
4.	Quick Procedure
o	The treatment typically takes around 30 minutes, allowing you to return to your daily activities without significant disruption.
5.	Minimal Discomfort
o	Botox injections are relatively painless, and any potential discomfort is typically mild and brief.
6.	Long-Lasting Results
o	Results can last for several months, and with periodic maintenance treatments, you can enjoy an ongoing improvement in your jawline aesthetics.
Treatment Overview
 
PROCEDURE TIME
30 minutes
 
PRICE
£290
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
3-6 months
 
Finals results seen
After 4-6 weeks
 
Number of treatments
1
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
BOTOX TREATMENT IN LONDON
Concerns Treated
1.	Bruxism and Teeth Grinding
o	Botox jawline slimming treatment can also alleviate symptoms of bruxism by relaxing the masseter muscles, reducing teeth grinding and associated discomfort.
2.	Masseter Muscle Hypertrophy:
o	Individuals with overdeveloped masseter muscles can experience a squared-off jawline. Botox can reduce the size of these muscles, leading to a more slender and defined jawline.
3.	Facial Asymmetry
o	For those with facial asymmetry due to an uneven jawline, Botox can help create balance by selectively targeting and relaxing specific muscles.
4.	Ageing-related Sagging
o	As we age, the jawline can lose definition due to sagging skin and muscle changes. Botox can provide a subtle lift and rejuvenate your appearance.
Who is jawline slimming for?
Jawline slimming with Botox is an excellent option for individuals who:
•	Desire a more refined and feminine jawline.
•	Seek non-surgical solutions for jawline contouring.
•	Experience discomfort or tension from bruxism or teeth grinding.
•	Have concerns about facial asymmetry and wish to achieve a more balanced look.
•	Are looking for subtle facial rejuvenation without undergoing surgery.


Gummy Smile Treatment London
Are you self-conscious about your gummy smile? Do you wish you could achieve a more balanced and confident smile? Look no further than Dr. Stephanie Damalis’ clinic in Wimbledon, London. We offer a cutting-edge gummy smile treatment using Botox. We are dedicated to helping you achieve the beautiful smile you’ve always desired.
What is a Gummy Smile?
A gummy smile is characterised by the excessive display of gum tissue when smiling. While this is a common concern for many individuals, it can impact one’s self-esteem and confidence.
Gummy Smile Treatment with Botox
Dr. Stephanie Damalis utilises Botox, a non-surgical and minimally invasive solution, to address gummy smiles effectively. This treatment involves injecting small amounts of Botox into specific facial muscles responsible for lifting the upper lip excessively when smiling. By carefully targeting these muscles, we can reduce the elevation of the upper lip, resulting in a more balanced and aesthetically pleasing smile.
Treatment Overview
 
PROCEDURE TIME
30 minutes
 
PRICE
£120
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
2-4 months
 
Finals results seen
After 2 weeks
 
Number of treatments
1
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
BOTOX TREATMENT IN LONDON
Benefits of Gummy Smile Treatment
1.	Minimally Invasive
o	This procedure does not require surgery, making it a safe and convenient option.
2.	Quick and Painless
o	The treatment is virtually painless and can typically be completed in a matter of minutes.
3.	Natural-Looking Results
o	Botox treatment provides natural-looking results, ensuring that your smile looks harmonious and genuine.
4.	No Downtime
o	There is no downtime associated with this procedure, allowing you to return to your daily activities immediately.
5.	Customised Treatment
o	Dr. Stephanie Damalis tailors the treatment to your unique facial anatomy, ensuring that the results complement your overall appearance.
 
 
Who is Gummy Smile Treatment with Botox for?
This innovative treatment is suitable for individuals who:
•	Have a gummy smile and wish to reduce the excessive display of gum tissue when smiling.
•	Desire a non-surgical and minimally invasive solution to enhance their smile.
•	Seek quick and effective results without significant downtime.
•	Want to boost their confidence and achieve a more balanced and aesthetically pleasing smile.
Concerns Addressed
Gummy smile treatment with Botox effectively addresses the following concerns:
1.	Excessive Gum Display
o	By targeting the overactive muscles responsible for lifting the upper lip, Botox reduces the extent of gum exposure when smiling.
2.	Low Self-Esteem
o	A gummy smile can impact one’s self-esteem and confidence. This treatment helps boost self-confidence by creating a more attractive and balanced smile.
3.	Natural Aesthetics
o	The results of this procedure are subtle and natural-looking, ensuring that your smile remains authentic and in harmony with your facial features.

Botox for Teeth Grinding in London
Teeth grinding, or bruxism, is a common dental problem that affects many people, leading to discomfort, pain, and even dental damage. At Dr. Stephanie Damalis’ renowned clinic in Wimbledon, we know that Botox is the best treatment for bruxism or teeth grinding.

Book Online
Botox For Teeth Grinding London
BESPOKE MEDICAL CONSULTATIONS
What is Botox for Teeth Grinding?
Botox for teeth grinding is a minimally invasive, non-surgical procedure that utilises the power of botulinum toxin injections to relax the muscles responsible for grinding your teeth – primarily the massrter muscles. Dr. Stephanie Damalis, a highly experienced and trusted practitioner, administers this treatment at our state-of-the-art clinic in London.

Who Can Benefit from Botox for Teeth Grinding?
This procedure is suitable for individuals who:

Suffer from chronic teeth grinding (bruxism).
Experience jaw pain, headaches, or facial discomfort due to bruxism.
Want to protect their dental health and prevent further damage.
Seek a non-invasive solution to alleviate teeth grinding.
Dr. Stephanie Damalis conducts a thorough assessment and consultation before recommending masseter Botox treatment, ensuring it is the right option for your specific needs.

Concerns Treated by Botox for Teeth Grinding
Bruxism
Botox effectively reduces the frequency and intensity of teeth grinding.
Facial Pain
Relaxes the muscles responsible for jaw and facial pain associated with bruxism.
Dental Damage
Prevents further dental damage, such as chipped or cracked teeth.
Sleep Disturbances
Improves sleep quality by reducing nighttime grinding.
Treatment Overview
noun time 1554506 2
PROCEDURE TIME
30 minutes

noun time 19890259
PRICE
£290

noun anesthesia 2044821
Anaesthesia needed
No

noun health 1733806 4
Discomfort level
Minimal

noun work 1730635
BACK TO WORK
Immediately

noun humans 193734 1
Duration of results
3-6 months

results
Finals results seen
After 2 weeks

number icon
Number of treatments 1

Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure

BOTOX TREATMENT IN LONDON
Benefits of Botox for Teeth Grinding
Pain Relief
Botox injections effectively reduce the intensity of teeth grinding, alleviating associated facial and jaw pain.

Prevent Dental Damage
By relaxing the jaw muscles, Botox prevents excessive wear and tear on your teeth, reducing the risk of fractures and enamel erosion.

Improved Sleep Quality
Bruxism often disrupts sleep patterns. Masseter Botox can help you achieve a more restful night’s sleep by reducing grinding-related disturbances.

Non-Invasive
Unlike some dental treatments, Botox for Teeth Grinding is non-surgical, requiring no incisions or anesthesia.

Quick Procedure
Treatment typically takes just a few minutes, and you can return to your daily activities immediately afterward.

Long-Lasting Results
The effects of masseter Botox for teeth grinding can last up to several months, providing long-term relief.

Lip Fillers in London
We understand that achieving the perfect pout can be a game-changer when it comes to boosting your confidence and enhancing your natural beauty. Our Wimbledon clinic offers advanced lip enhancement treatments tailored to your unique needs. Our lip filler treatments ensure your safety, comfort, and stunning results.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What Are Lip Fillers?
Lip fillers are injectable treatments primarily composed of hyaluronic acid, used to augment the shape and volume of the lips. Hyaluronic acid, naturally found in the body, ensures safety and effectiveness in lip enhancement. These fillers add volume, hydrate lip tissue, and provide natural, soft-feeling lips. Hyaluronic dermal fillers, the safest type, are temporary and require periodic replenishment.
What Do Lip Fillers Do?
Lip fillers offer numerous benefits:
Volume Enhancement
They provide significant improvement in lip volume, catering to those with naturally thin lips or lips that have thinned due to ageing.
Shape Definition
Lip fillers can define the contours of the lips, enhancing the cupids bow and creating a more defined lip shape. It may be the case that just the top lip requires a filler injected for volume.
Symmetry Correction
They are effective in correcting asymmetrical lips, achieving a more balanced appearance between the upper and lower lips and also provide horizontal symmetry.
Fine Lines Reduction
Fillers can also diminish the appearance of fine lines around the upper and lower lip areas of the mouth, contributing to a more youthful look.
Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
From £280
 
Anaesthesia needed
Yes (numbing cream or local anaesthetic)
 
Discomfort level
Moderate 
 
BACK TO WORK
Immediately (if you don’t mind swelling. Worst swelling in first 3 days)
 
Duration of results
3-8 months
 
Finals results seen
After 2-4 weeks
 
Number of treatments
1
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
LIP TREATMENT IN Wimbledon
Our Approach to Lip Filler Treatments
Expertise and Experience
Dr. Damalis, with her extensive experience in facial aesthetics and keen interest in facial anatomy, ensures precision and care in every lip filler procedure. Being an aesthetics trainer, Dr Damalis is well placed to offer the benefits of her long-obtained wisdom to all of her patients.
Customised Treatment Plans
Recognising the uniqueness of each patient, we offer personalised lip enhancement treatment with plans developed after a detailed lip filler consultation.
Advanced Facilities
Our clinic is equipped with the latest technology, ensuring a safe procedure, a comfortable treatment, and effective lip filler experience.
Only the Best Fillers
Not all fillers are the same. Lip fillers are not just limited to one product, one manufacturer, or one supplier. We only use premium brands with provenance and reputation. This also goes for the suppliers we use. Dilligence is applied at every step of our supply chain process, right up to the dermal filler treatment. We do not offer permanent lip fillers due to potential long term risks. The brands we use include Juvederm, Revanesse, Neauvia and Teoxane. All of these have long history of safety and efficacy.
 
The Lip Filler Treatment Process
Initial Consultation
This a critical step where Dr Damalis assesses your facial features discusses your lip goals, and crafts a tailored treatment plan.
The Lip Filler Procedure
The lip injections are carefully administered using advanced techniques, prioritising your comfort and your desired outcome for your lips.
Aftercare and Follow-up
Post-treatment care is always important for all treatments we perform. We provide comprehensive aftercare instructions and schedule follow-up appointments to ensure optimal healing.
Lip Filler Options at Damalis Skin Clinic
Variety of Fillers
We offer a selection of hyaluronic acid fillers, each chosen for their suitability for different lip shapes and desired results. We only carry the most advanced range of dermal fillers.
Bespoke Consultation and Customisation
Each lip filler treatment is customised, considering individual preferences for lip size and the unique structure of the lip area.
The Lip Filler Procedure: What to Expect
Before the Treatment
Patients are advised to avoid certain medications and substances that may increase bruising and swelling. Your medical history will be discussed, including previous aesthetic treatments you may have had.
During the Procedure
Comfort is a priority. A local anaesthetic is used to minimise discomfort, and the lip filler injections are performed with precision and strategic points.
After the Procedure
Patients may experience mild swelling and bruising, which typically subsides within a few days. The full effect of the lip fillers is usually visible within two weeks, but you will see a difference immediately. We will provide you with aftercare advice to help you get the most out of your new look. This advice will involve leaving the lips alone to settle (avoid kissing please!) for a day or two. All advice given will be specific to your treatment. Recovery time varies but in general is 2-3 days or less.
Cost of Lip Fillers
The lip filler cost at Damalis Skin Clinic depends on exactly how much dermal lip filler product you need/want. The final costs customised to align with each patients unique requirements and desired aesthetic outcomes. During your initial consultation at our clinic, Dr. Stephanie Damalis will offer a comprehensive cost breakdown.
Ideal Candidates for Lip Fillers
Ideal candidates for lip fillers are individuals desiring to enhance lip volume or shape, possessing realistic expectations and good health. Avoid dermal filler injections if experiencing cold sores or local infections. A consultation with Dr Damalis is crucial to assess suitability and discuss risks or concerns.
Booking Your Lip Filler Appointment
To begin your journey towards enhanced lips, book a consultation at Damalis Skin Clinic. Our commitment is to provide exceptional care, ensuring the best possible lip filler results Wimbledon has to offer.

Lip Filler FAQs
Is the Lip Filler Procedure Painful?
The lip filler procedure typically causes minimal discomfort. A topical numbing cream is applied to the lips before injection to reduce pain. Many lip fillers also contain a local anaesthetic, enhancing comfort. Please discuss pain management options during your initial consultation.
Can Lip Fillers Look Natural?
Lip fillers can look natural when administered by an experienced practitioner. The amount of filler and injection technique are key for a natural appearance. Discussing preferences for subtle enhancements ensures desired outcomes. Overuse or poor techniques, leading to ‘duck lips,’ highlight the importance of professional administration.
Are There Any Side Effects or Downtime After Lip Filler Treatment?
Hyaluronic acid-based lip fillers are reversible. If unsatisfied or complications arise, hyaluronidase can dissolve the filler, reverting to the original state. This reversibility ensures safety and flexibility in lip filler treatments.
Are Lip Fillers Reversible?
Hyaluronic acid-based lip fillers are generally reversible, as is the same with all facial filler treatments. If a patient is dissatisfied with the results of facial fillers or experiences complications, an enzyme called hyaluronidase can be injected to break down the filler, restoring the area to its previous state. This reversibility adds an extra layer of safety and flexibility to the lip filler procedure.
How Long Do Lip Filler Results Last?
Lip filler results generally last six months to a year, varying by filler type and individual metabolism. With touch-up treatments, the desired lip appearance can be maintained longer.
Cheek Fillers in London
Are you looking to enhance your facial features and restore a youthful, radiant appearance? Look no further than Dr. Stephanie Damalis’ renowned clinic in Wimbledon, London. Dr. Damalis specialises in providing top cheek filler treatments that can help you achieve the look you desire.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What Are Cheek Fillers?
Cheek fillers are injectable treatments designed to enhance facial contours and restore volume to the cheeks. Comprising primarily of hyaluronic acid, a naturally occurring substance in the body, these fillers provide a safe and effective way to achieve a more youthful and balanced facial appearance. Ideal for addressing concerns like hollow cheeks, sagging skin, and other signs of ageing, cheek fillers offer a non-surgical solution for those seeking subtle yet impactful cosmetic enhancements.
Who Can Benefit from Cheek Fillers
Cheek filler treatments are ideal for individuals who:
1.	Desire Facial Enhancement: Those looking to enhance the shape and contours of their cheeks to achieve a more balanced and youthful appearance.
2.	Have Age-Related Volume Loss: Cheek fillers are especially beneficial for individuals experiencing volume loss in the mid-face due to the natural ageing process.
3.	Seek Non-Surgical Solutions: Patients who prefer non-invasive procedures over surgical options to achieve their aesthetic goals.
4.	Desire Natural-Looking Results: Individuals who want subtle and natural-looking results that enhance their beauty without appearing overdone.
Concerns Treated by Cheek Fillers
1.	Hollow Cheeks: Cheek fillers can effectively address hollow or sunken cheeks, restoring volume and vitality to the mid-face.
2.	Sagging Skin: By providing support and lift to the cheeks, fillers can help combat sagging skin, resulting in a more youthful profile.
3.	Uneven Contours: Cheek fillers can create balanced and harmonious facial contours, correcting asymmetry and improving overall facial harmony.
4.	Ageing Signs: As an excellent anti-aging solution, cheek fillers minimise the appearance of fine lines and wrinkles, giving you a more youthful and refreshed look.
Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
From £320
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
8-12 months
 
Finals results seen
After 2-4 weeks
 
Number of treatments
2-4
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
cheek lift IN LONDON
Benefits of Cheek Fillers
1.	Enhanced Facial Contours: Cheek fillers are designed to restore volume and definition to the cheeks, resulting in a more sculpted and youthful appearance.
2.	Youthful Rejuvenation: As we age, the cheeks can lose volume, causing the face to sag. Cheek fillers can counteract this by providing a subtle lift and a more youthful look.
3.	Non-Surgical Solution: Cheek fillers offer a non-invasive alternative to traditional surgical procedures, delivering natural-looking results with minimal downtime.
4.	Customised Treatment: Dr. Stephanie Damalis tailors each cheek filler treatment to the unique needs and goals of her patients, ensuring a personalised and natural outcome.
5.	Quick and Convenient: Cheek filler procedures are typically quick and can often be completed during a lunch break, allowing you to return to your daily activities with minimal disruption.
6.	The Procedure of Cheek Fillers
7.	Personalised Consultation Process
8.	Understanding that each face is unique, we begin with a comprehensive consultation. Our approach involves a detailed facial analysis to identify areas that can benefit from volume enhancement. This personalised strategy ensures that the results not only rejuvenate but also respect your face’s natural symmetry and proportions.
9.	Step-by-Step Guide
10.	The procedure at Damalis Skin Clinic is meticulous and patient-focused. We gently clean the treatment area, followed by applying a numbing cream for your comfort. The filler is strategically injected into targeted areas using fine needles to restore volume and enhance contours. The entire process is swift, typically completed within 30 minutes.
11.	Safety and Comfort
12.	Your safety and comfort are our top priorities. We use only FDA-approved, high-quality fillers, and our clinicians are trained in the latest injection techniques to ensure a safe, effective, and comfortable treatment experience.
13.	Before and After Care
14.	We provide thorough guidance on pre-treatment preparation and post-treatment care. We aim to ensure a smooth, comfortable experience with minimal downtime. We emphasise the importance of hydration, avoiding certain medications, and post-treatment care to optimise results and minimise potential side effects.
15.	Results and Longevity of Cheek Fillers
16.	Expected Results
17.	Post-treatment, patients can expect to see an immediate improvement in the volume and contour of their cheeks. The results are natural-looking, enhancing your facial features while maintaining the balance and harmony of your overall appearance.
18.	Longevity and Maintenance
19.	The effects of cheek fillers at Damalis Skin Clinic can last anywhere from 6 to 18 months, depending on the type of filler used and individual patient factors. We recommend regular follow-up sessions for maintenance to preserve the youthful, revitalised look.
20.	What are cheek fillers, and how do they work?
21.	Cheek fillers are injectable treatments containing hyaluronic acid or other substances that add volume to the cheeks. They work by plumping and lifting the skin, restoring lost volume, and enhancing facial contours.
22.	Are cheek fillers safe?
23.	Yes, cheek fillers are considered safe when administered by a trained and qualified medical professional. The fillers used are typically biocompatible, and side effects are generally mild and temporary.
24.	Is the procedure painful?
25.	Discomfort during cheek filler injections is usually minimal. Many filler products contain a local anesthetic to minimise pain. Patients may experience slight stinging or a mild burning sensation that quickly subsides.
26.	How long do the results of cheek fillers last?
27.	The longevity of cheek filler results varies depending on the type of filler used and individual factors. Generally, results can last anywhere from 6 months to 2 years. Follow-up treatments can help maintain the desired look.
28.	What are the potential side effects of cheek fillers?
29.	Common side effects include temporary redness, swelling, bruising, and tenderness at the injection site. These usually subside within a few days. Rarely, more severe side effects like infection or lumps may occur.
30.	Who is a suitable candidate for cheek fillers?
31.	Candidates for cheek fillers are typically individuals seeking to enhance their cheek volume, correct age-related sagging, or improve facial symmetry. A consultation with a qualified practitioner can determine if you are a good candidate based on your specific goals and medical history.


Tear Trough Fillers in London
Our skin clinic in Wimbledon, London offers a range of advanced and minimally invasive treatments to enhance your natural beauty and rejuvenate your appearance. One such treatment that has gained significant popularity is tear trough fillers.

Book Online
tear-trough-filler-london
BESPOKE MEDICAL CONSULTATIONS
What are Tear Trough Fillers?
Tear trough fillers are a non-surgical cosmetic procedure designed to address the hollows or depressions that can develop under the eyes, commonly known as tear troughs. These depressions can result in a tired, aged, or even a constantly fatigued appearance. Tear trough fillers involve injecting a specialised dermal filler under the eye, creating a smoother and more youthful look by adding volume and supporting the skin.

Treatment Overview
noun time 1554506 2
PROCEDURE TIME
45 minutes

noun time 19890259
PRICE
£400

noun anesthesia 2044821
Anaesthesia needed
No

noun health 1733806 4
Discomfort level
Minimal

noun work 1730635
BACK TO WORK
Immediately

noun humans 193734 1
Duration of results
8-12 months

results
Finals results seen
After 2-4 weeks

number icon
Number of treatments
1-2


UNDER EYE FILLER IN LONDON
Why Choose Tear Trough Fillers?
Tear trough fillers offer a range of benefits, making them a popular choice among individuals seeking facial rejuvenation:

Non-Surgical: Under eye filler treatments are minimally invasive and require no surgical incisions, reducing both downtime and the risk of complications associated with surgery.

Quick Procedure: The procedure can often be completed within a short amount of time, allowing individuals to resume their daily activities almost immediately.

Immediate Results: Patients typically notice visible improvements immediately after the treatment, with final results becoming more apparent as any temporary swelling subsides.

Natural-Looking Results: Dr Damalis ensures that tear trough fillers are administered with precision and expertise, creating natural-looking results that enhance your facial features without appearing overdone.

Minimal Downtime: While some minor swelling or bruising might occur after the treatment, it is usually short-lived and can be easily concealed with makeup. Most patients are able to resume their normal routines shortly after the procedure.

What are tear trough fillers?
Tear trough fillers are non-surgical cosmetic treatments designed to address under-eye hollowness, dark circles, and the appearance of tiredness. These fillers are typically made of hyaluronic acid and are injected beneath the eyes to restore volume and improve the overall contour.

How do tear trough fillers work?
Tear trough fillers work by replenishing lost volume and hydrating the under-eye area. Hyaluronic acid, a naturally occurring substance in the body, is injected to fill in hollows and smooth out the skin. This creates a more youthful and refreshed appearance.

What can tear trough fillers help with?
Tear trough fillers can help reduce the appearance of under-eye bags, dark circles, and hollowness. They also provide a subtle lift to the cheeks and improve the transition between the lower eyelid and cheek, creating a more rejuvenated look.

Are tear trough fillers permanent?
No, tear trough fillers are not permanent. The effects typically last around 9 months to a year, depending on factors such as the individual’s metabolism, lifestyle, and the specific filler used. Maintenance sessions are required to sustain the results.

cal Nose Job in London
Our non surgical rhinoplasty procedure is a revolutionary solution to reshape and refine your nose. Our Wimbledon clinic provides stunning results with minimal downtime. Dr. Stephanie Damalis, our expert practitioner, offers this safe and effective treatment to patients seeking a more balanced and harmonious facial appearance.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What is Non Surgical Rhinoplasty?
Non surgical rhinoplasty, also known as a liquid nose job, is an advanced cosmetic procedure that reshapes and refines the nose without the need for surgery. At Damalis Skin Clinic, this procedure involves carefully injecting hyaluronic acid-based dermal fillers to alter the nose’s shape, offering a more balanced and harmonious facial appearance. This innovative technique is ideal for addressing issues like dorsal humps, asymmetries, nasal tip projection, and volume loss.
What does a Non Surgical Rhinoplasty treat?
Non surgical rhinoplasty can effectively address a variety of concerns, including:
1.	Dorsal Hump: By strategically injecting nose fillers, we can smooth out and reduce the appearance of a dorsal hump, creating a straighter bridge.
2.	Asymmetry: Our procedure can correct minor asymmetries in the nose, ensuring a more balanced and harmonious appearance.
3.	Nasal Tip Projection: If you have concerns about a drooping or flat nasal tip, non surgical rhinoplasty can provide lift and projection.
4.	Nasal Bridge Irregularities: Fillers can be used to smooth out irregularities along the nasal bridge, creating a more refined profile.
5.	Volume Loss: For those with age-related volume loss, nose fillers can restore youthful fullness and contour.
Why Choose Non Surgical Rhinoplasty?
Choosing non surgical rhinoplasty at Damalis Skin Clinic means opting for a safe, effective, and less invasive alternative to traditional rhinoplasty. This procedure is perfect for those seeking to correct minor imperfections or who desire a more symmetrical and aesthetically pleasing nose without surgery. 
Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
£400
 
Anaesthesia needed
No
 
Discomfort level
Moderate
 
BACK TO WORK
Immediately
 
Duration of results
8-12 months
 
Finals results seen
After 2-4 weeks
 
Number of treatments
Varies (2-4)
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
NOSE FILLER IN LONDON
Who is Non Surgical Rhinoplasty For?
Our non surgical nose correction is an excellent option for individuals who:
1.	Desire a more balanced and symmetrical nose.
2.	Want to correct minor imperfections, such as bumps, asymmetry, or a drooping tip.
3.	Seek a non-permanent solution for nose enhancement.
4.	Prefer a less invasive alternative to traditional surgical rhinoplasty.
Benefits of Non Surgical Rhinoplasty
1.	Non-Invasive: Unlike traditional surgical rhinoplasty, our non-surgical approach involves no incisions, sutures, or general anesthesia. You can achieve your desired nose shape without the need for a surgical procedure.
2.	Quick and Convenient: Non surgical rhinoplasty typically takes less than an hour, and most clients can return to their daily activities immediately after the treatment.
3.	Minimal Discomfort: Patients experience minimal discomfort during the procedure, and any discomfort afterward is easily managed with over-the-counter pain relievers.
4.	Immediate Results: You can see the transformation instantly. The nose filler used in the procedure provides immediate results, making it easy to achieve your desired look.
5.	Customised Solutions: Dr. Stephanie Damalis tailors each treatment to the individual’s unique facial anatomy and aesthetic goals, ensuring a personalised and natural-looking result.
 
The Non Surgical Rhinoplasty Procedure at Damalis Skin Clinic
Consultation and Customised Treatment Plans
At Damalis Skin Clinic, our non surgical rhinoplasty journey begins with a detailed consultation. We assess your nasal structure and discuss what you are looking to achieve. We then develop a customised treatment plan, ensuring the procedure aligns perfectly with your expectations.
The Procedure Step-by-Step
The procedure is straightforward and efficient. After applying a topical anaesthetic, dermal nose fillers are injected into specific nose areas. This precise application reshapes the nose, addressing concerns like bumps, asymmetry, or a drooping tip, with the entire process typically completed in under an hour.
Results and Recovery
What to Expect After the Procedure
Post-procedure, clients can expect minimal discomfort, managed easily with over-the-counter pain relief if necessary. There’s no downtime, allowing you to immediately return to your daily routine. Some minor swelling or redness may occur but will subside quickly.
Longevity of Results
The results of non-surgical rhinoplasty at Damalis Skin Clinic are immediately noticeable and can last 6 to 18 months. The longevity of the results depends on the type of fillers used and individual factors like skin type and lifestyle.
Nose Filler FAQs
Check out some frequently asked questions about the liquid nose job our patients regularly ask us.
What is non surgical rhinoplasty, and how does it work?
Non-surgical rhinoplasty, also known as a liquid nose job, is a cosmetic procedure that uses dermal fillers to reshape and enhance the appearance of the nose. During the treatment, a trained practitioner injects dermal fillers into specific areas of the nose to correct imperfections, add volume, and improve symmetry. It is a non-invasive alternative to traditional surgical rhinoplasty.
Is non surgical rhinoplasty permanent?
Non-surgical rhinoplasty provides results that are not permanent. The effects typically last from 6 months to 2 years, depending on the type of filler used and individual factors. Maintenance treatments are usually required to maintain the desired nose shape.
What are the potential risks and side effects of non surgical rhinoplasty?
While non surgical rhinoplasty is generally considered safe, it can be associated with temporary side effects such as swelling, bruising, redness, and tenderness at the injection site. More serious complications, though rare, can include infection, allergic reactions, and vascular issues. It’s essential to choose a qualified and experienced practitioner to minimise risks.
Who is an ideal candidate for non surgical rhinoplasty?
Non surgical rhinoplasty is suitable for individuals who want to enhance the appearance of their nose without undergoing surgery. Ideal candidates have minor imperfections, asymmetry, or concerns related to the nasal shape, and they are in good overall health. However, it may not be suitable for those with severe deformities or functional issues.
Is non surgical rhinoplasty painful?
Most patients report only mild discomfort during the procedure. The use of topical numbing creams and the relatively quick nature of the treatment help minimise pain. Any post-procedure discomfort can typically be managed with over-the-counter pain relievers.
How long does a non surgical rhinoplasty procedure take, and is there downtime?
A non surgical rhinoplasty procedure typically takes less than an hour to complete. One of the advantages of this treatment is that there is minimal downtime. Many individuals can resume their regular activities immediately after the procedure, although some swelling or redness at the injection site may be present for a short period, which usually subsides within a few days.

Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
From £320
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
8-12 months
 
Finals results seen
After 2-4 weeks
 
Number of treatments
Varies (2-4)
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
JAW FILLER IN LONDON
Why Choose Jawline Fillers?
1.	Non-Invasive: Unlike surgical options, jawline contouring using fillers does not require incisions or downtime. This means you can achieve remarkable results without the need for extensive recovery.
2.	Natural Look: Our expert practitioners have the skill to create a natural and harmonious jawline that complements your facial features. We prioritise subtle enhancements that enhance your unique beauty.
3.	Long-Lasting Results: While not permanent, jawline filler results can last for several months to a year, depending on the specific product used. This allows you to enjoy your refined jawline for an extended period.
4.	Minimal Discomfort: Most patients experience minimal discomfort during the procedure. Our clinic employs advanced techniques and products with built-in numbing agents to ensure your comfort throughout the treatment.
5.	Customisation: Every patient is unique, and we believe in a tailored approach. Dr Damalis will assess your individual needs and create a personalised treatment plan to achieve your desired jawline contour.
6.	Jawline Filler FAQs
7.	Who is a suitable candidate for jawline filler treatments?
8.	Jawline fillers are suitable for individuals who want to enhance their jawline’s definition, improve symmetry, or address sagging or volume loss in the lower face. Good candidates are generally in good overall health and have realistic expectations about the outcomes of the treatment. A consultation can help determine if jawline fillers are the right option for you and your aesthetic goals.
What are jawline fillers, and how do they work?
Jawline fillers are non-surgical cosmetic treatments that use injectable gels, typically made from hyaluronic acid, to enhance and redefine the jawline. The filler adds volume to the targeted areas, improving the jawline’s contour and definition.
Can jawline fillers be combined with other treatments?
Yes, jawline fillers can be combined with other cosmetic treatments, such as Botox, to achieve a comprehensive facial rejuvenation. Combining treatments can provide more comprehensive results by addressing different aspects of facial ageing and contouring.
Is the procedure painful, and is there any downtime?
Most patients report minimal discomfort during jawline filler treatments. Many filler products contain numbing agents to enhance comfort. After the procedure, there may be some mild swelling, bruising, or redness, but these side effects typically subside within a few days. Patients can generally resume their daily activities immediately with a few restrictions.
How long do the results of jawline filler treatments last?
The duration of results can vary depending on the specific product used, individual metabolism, and lifestyle factors. On average, jawline filler results can last from several months to up to a year. Maintenance treatments can help extend the results over time.
Are jawline fillers safe?
Yes, jawline fillers are generally considered safe when administered by a trained and qualified medical professional. The key to safety lies in choosing an experienced practitioner who uses high-quality fillers. During your consultation, Dr Damalis will discuss potential risks and side effects with you.
Chin Fillers in London
Discover the transformative benefits of chin fillers and how they can address common concerns. Damalis Skin Clinic in Wimbledon offer chin filler treatments to enhance your facial harmony and confidence, creating natural and balanced results.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What Are Chin Fillers?
Chin fillers are a cosmetic treatment designed to enhance facial contours by adding volume and definition to the chin area. Utilising hyaluronic acid, a substance naturally found in the body, these fillers are injected to improve the chin’s shape, making it more pronounced and balanced with other facial features. Ideal for addressing concerns like a weak or receding chin, chin fillers offer a non-surgical solution for those seeking a more harmonious facial profile.
Who is Chin Filler Treatment For
Chin filler treatment is suitable for a wide range of individuals who seek to enhance their chin’s appearance and address specific concerns, including:
1.	Chin Augmentation: Patients looking to improve the projection or size of their chin.
2.	Receding Chin: Individuals with a receding chin may benefit from chin fillers to create a more balanced profile.
3.	Jawline Definition: Those seeking a more defined and sculpted jawline can benefit from this treatment.
4.	Facial Harmony: Patients looking to achieve better facial balance and symmetry.
5.	Anti-Ageing: Chin fillers can also be used to address signs of ageing, such as sagging skin or wrinkles around the chin area.
Concerns Treated by Chin Fillers
Chin fillers are a versatile treatment that can address various concerns, including:
1.	Weak Chin: Chin fillers can add volume and projection to a weak or underdeveloped chin.
2.	Profile Enhancement: They help enhance your side profile by creating a more defined chin and jawline.
3.	Double Chin: Chin fillers can reduce the appearance of a double chin by improving the chin’s contours.
4.	Ageing Chin: As we age, the chin area may lose volume. Chin fillers can restore a more youthful appearance.
5.	Facial Balance: For those looking to achieve overall facial harmony and symmetry, chin fillers can be part of a comprehensive facial rejuvenation plan.
Treatment Overview
 
PROCEDURE TIME
45 minutes.
 
PRICE
From £320
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
8-12 months
 
Finals results seen
After 2-4 weeks
 
Number of treatments
Varies (1-2)
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
CHIN AUGMENTATION IN LONDON
Benefits of Chin Fillers
1.	Enhanced Facial Contour: Chin fillers are an effective way to improve the definition of your chin and jawline, creating a more sculpted appearance.
2.	Non-Surgical Solution: Unlike invasive surgical procedures, chin fillers offer a non-surgical and minimally invasive approach to enhancing your chin’s appearance.
3.	Quick Procedure: The treatment is usually quick and can be done during a lunch break, making it convenient for those with busy schedules.
4.	Minimal Downtime: Patients can typically resume their daily activities immediately after the treatment with minimal downtime.
5.	Natural-Looking Results: Dr. Stephanie Damalis specialises in achieving results that appear natural and harmonious with your overall facial features.
6.	Personalised Treatment: Each chin filler treatment is tailored to your unique facial anatomy and aesthetic goals.
 
The Chin Filler Procedure Explained
Consultation and Custom Treatment Plan
Your journey at Damalis Skin Clinic begins with a detailed consultation. Our experts assess your facial structure and discuss your aesthetic goals to create a personalised treatment plan. This plan is tailored to ensure the chin filler enhances your natural features while maintaining facial harmony.
The Injection Process
The chin filler procedure at Damalis Skin Clinic is a meticulous process. Using fine needles, our skilled practitioners inject the filler into strategic areas of the chin to achieve the desired contour and volume. The process is relatively quick and is performed with the utmost care to ensure comfort and precision.
Post-Treatment Care and Follow-Up
After the procedure, we provide comprehensive post-treatment care instructions to ensure a smooth recovery. Our clinic schedules a follow-up appointment to monitor your progress and make any necessary adjustments, ensuring your complete satisfaction with the results.
The Cost of Chin Filler
The cost of chin filler treatment at Damalis Skin Clinic is determined by several factors, including the amount of filler used and the complexity of the procedure. We believe in transparent pricing and will provide a detailed cost breakdown during your consultation. Our clinic offers co
Chin Filler FAQs
What are chin fillers, and how do they work?
Chin fillers are non-surgical cosmetic treatments that involve injecting a dermal filler, typically made of hyaluronic acid, into the chin area. These fillers add volume and contour to the chin, enhancing its shape and appearance. They work by plumping and reshaping the chin, achieving a more balanced and defined look.
Is the chin filler treatment painful?
Chin filler treatments are generally well-tolerated. A topical numbing cream or local anesthetic is often applied before the procedure to minimise discomfort. Most patients report minimal pain or discomfort during the injections, describing it as a slight stinging sensation.
How long do chin filler results last?
The longevity of chin filler results can vary from person to person but typically lasts around 9 to 12 months. Over time, the filler gradually breaks down, and the chin returns to its previous state. To maintain the results, patients may need periodic touch-up treatments.
Are there any potential side effects or risks associated with chin fillers?
While chin filler treatments are generally safe, some potential side effects can occur, including temporary redness, swelling, bruising, or tenderness at the injection site. Serious complications are rare but can include infection, allergic reactions, or filler migration. It’s essential to choose an experienced practitioner to minimise risks.
How long is the recovery period after chin filler treatment?
Chin filler treatments typically have minimal downtime. Patients can usually return to their regular activities immediately after the procedure. Some may experience mild swelling or bruising, but these side effects generally resolve within a few days to a week.
Can chin fillers be combined with other cosmetic procedures?
Yes, chin filler treatments can be combined with other cosmetic procedures for a more comprehensive facial rejuvenation. Common combinations include dermal fillers for other facial areas, such as cheeks or lips, or treatments like Botox for wrinkle reduction. 

Temple Fillers in London
Dr. Stephanie Damalis’ clinic in Wimbledon, London, specialises in providing temple filler treatments. Our dedicated team offers safe and effective temple filler procedures to help you achieve a more youthful and revitalised appearance. 
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What are Temple Fillers?
Temple fillers are a cosmetic treatment designed to address the loss of volume in the temple area of the face, a common issue as we age. This treatment involves injecting dermal fillers, typically made of hyaluronic acid, into the temples. The goal is to restore lost volume, creating a more youthful and balanced facial appearance. Temple fillers can also correct facial asymmetry and enhance facial contours, providing a subtle lift to the overall facial structure.
Who Can Benefit from Temple Fillers
Temple fillers are suitable for a wide range of individuals, including:
1.	Ageing Skin: As we age, the loss of fat and collagen in the temples can make the face appear older. Temple fillers are an excellent option for those looking to rejuvenate their appearance.
2.	Facial Asymmetry: If you have facial asymmetry due to uneven temples, temple fillers can help create a more balanced and harmonious look.
3.	Volume Loss: Individuals experiencing temple volume loss due to weight loss, genetics, or other factors can benefit from temple filler treatments.
4.	Enhanced Facial Contour: For those seeking to enhance their facial contours and achieve a more defined appearance, temple fillers can be a valuable addition to their cosmetic routine.
Concerns Addressed by Temple Fillers
Temple fillers effectively address various cosmetic concerns, including:
1.	Sunken Temples: Temple fillers can plump up sunken temples, restoring youthful fullness to this area.
2.	Hollow Temples: Hollow temples can make you appear older and tired. Temple fillers fill in these hollows, rejuvenating your overall look.
3.	Facial Asymmetry: Temple fillers can correct asymmetry in the temples, helping you achieve facial balance.
4.	Volume Deficiency: If you have naturally less volume in your temples, temple fillers can augment this area to create a more harmonious facial profile.
Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
£400
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
8-12 months
 
Finals results seen
After 2-4 weeks
 
Number of treatments
Varies (1-2)
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
Temple hollowing treatment IN LONDON
Benefits of Temple Fillers
1.	Rejuvenated Appearance: Temple fillers restore volume to the temples, creating a refreshed and youthful look. As we age, the temples tend to lose volume, which can lead to a sunken and hollow appearance. Temple fillers can reverse this effect, helping you look and feel your best.
2.	Enhanced Facial Symmetry: Well-proportioned temples are essential for overall facial balance. Temple fillers can harmonise your facial features, contributing to a more symmetrical and aesthetically pleasing appearance.
3.	Quick and Minimally Invasive: Temple filler treatments are quick, typically taking around 30 minutes, and involve minimal discomfort. They are an excellent option for those with busy schedules, as they require little to no downtime.
4.	Natural-Looking Results: Dr. Stephanie Damalis specialises in achieving natural-looking results. Our temple filler treatments are customised to suit your unique facial structure, ensuring a subtle and beautiful outcome.
 
The Temple Filler Procedure at Damalis Skin Clinic
Consultation and Customisation
Your journey at Damalis Skin Clinic begins with a detailed consultation. Our experts will assess your facial structure, discuss your aesthetic goals, and explain the temple filler procedure. We believe in a customised approach, ensuring that our treatment plan aligns perfectly with your expectations and enhances your natural features.
The Treatment Process
The temple filler treatment at Damalis Skin Clinic is a meticulous process. Our skilled practitioners carefully inject the product into the targeted temple areas using only the highest quality dermal fillers. The procedure is quick, typically taking around 30 minutes, and is performed with the utmost precision to ensure optimal results and minimal discomfort.
Aftercare and Follow-up
Post-treatment care is crucial for achieving the best results. At Damalis Skin Clinic, we provide comprehensive aftercare instructions for smooth recovery. We also schedule follow-up appointments to monitor your progress and make any necessary adjustments, ensuring your complete satisfaction with the results.
Temple Filler FAQs
What are temple fillers, and how do they work?
Temple fillers are dermal fillers injected into the temples to restore lost volume and rejuvenate the appearance. They typically contain hyaluronic acid, a naturally occurring substance in the skin that adds volume and hydration. The fillers plump up the temples, addressing sunken or hollow areas.
Is temple filler treatment painful?
Temple filler treatments are relatively painless. Most fillers contain lidocaine, a local anesthetic, to minimise discomfort during the procedure. Patients may experience mild discomfort or a pinching sensation, but it’s generally well-tolerated.
How long do the results of temple fillers last?
The duration of temple filler results varies depending on the specific product used and individual factors. On average, results can last from 6 months to 2 years. Follow-up treatments are typically needed to maintain the desired appearance.
Are there any side effects or risks associated with temple fillers?
Like any cosmetic procedure, temple fillers carry some risks, although they are generally considered safe when administered by a skilled and experienced practitioner. Potential side effects may include swelling, bruising, redness, or tenderness at the injection site, but these usually resolve within a few days.
Who is a suitable candidate for temple filler treatment?
Temple fillers are suitable for individuals who want to address concerns such as sunken or hollow temples, facial asymmetry, or volume loss in the temple area. A consultation with a qualified practitioner can help determine if you are a good candidate based on your specific needs and medical history.
How long does a temple filler procedure take, and is there any downtime?
Temple filler treatments are typically quick, usually taking around 30 minutes to complete. One of the key advantages of temple fillers is that they involve minimal downtime. Most patients can resume their normal activities immediately after the procedure. However, it’s essential to follow post-treatment care instructions provided by Dr Damalis to optimize results and minimise any potential side effects.
Nasolabial Folds Treatment in London
At Dr. Stephanie Damalis’ renowned clinic in Wimbledon, London, we offer advanced and highly effective nasolabial folds filler treatment. Our dermal filler treatment is designed to rejuvenate your skin, restoring a youthful and radiant look.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What are Nasolabial Folds?
Nasolabial folds, commonly known as “smile lines” or “laugh lines,” are the lines that extend from the sides of the nose to the corners of the mouth. These folds are a natural part of the human facial structure but can become more pronounced with age, sun exposure, and lifestyle factors. At Damalis Skin Clinic, we know only too well that these deeper lines can contribute to a tired or aged appearance, prompting patients to seek effective treatments.
Who is Nasolabial Line Treatment Good For?
Nasolabial folds filler treatment is ideal for individuals who:
•	Are bothered by the appearance of prominent nasolabial folds.
•	Want a non-invasive solution to address facial ageing.
•	Seek immediate results without lengthy recovery periods.
•	Desire natural-looking rejuvenation.
Concerns Addressed
Our nasolabial filler treatment effectively addresses various concerns, including:
1.	Nasolabial Folds: Softening and reducing the appearance of deep smile lines, marionette lines, and nasolabial folds.
2.	Volume Loss: Restoring lost volume to the mid-face and cheek area for a more youthful contour.
3.	Wrinkles and Fine Lines: Smoothing out fine lines and wrinkles, giving you a smoother, more youthful complexion.
4.	Facial Rejuvenation: Enhancing overall facial harmony and rejuvenation without surgery.
5.	Natural Enhancement: Achieving a natural-looking enhancement that preserves your unique facial features.
Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
From £320
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
6-8 months
 
Finals results seen
After 2-4 weeks
 
Number of treatments
1
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
FILLER TREATMENT IN LONDON
Benefits of Nasolabial Folds Treatment
1.	Immediate Results: One of the key advantages of our nasolabial filler treatment is that you can see results immediately after the procedure. The lines are visibly reduced, giving you a more youthful appearance.
2.	Non-Surgical: Our nasolabial folds treatment is non-surgical, meaning you can achieve a refreshed look without the need for invasive procedures or extended downtime.
3.	Natural-Looking Results: Dr. Stephanie Damalis specialises in creating natural-looking results. You’ll appear rejuvenated, yet not “overdone.”
4.	Long-Lasting: The effects of nasolabial folds fillers can last for several months, providing you with lasting results that require minimal maintenance.
5.	Minimal Discomfort: Our clinic uses advanced techniques and high-quality fillers, which typically result in minimal discomfort during and after the procedure.
Procedure Overview
1.	Consultation: Dr. Stephanie Damalis will assess your unique facial anatomy and discuss your goals during a personalised consultation.
2.	Treatment: A carefully selected dermal filler is injected into the target areas to achieve the desired results. Dr. Damalis uses her expertise to ensure precise placement for a natural look.
3.	Results: You’ll notice an immediate improvement in the appearance of your nasolabial folds and overall facial rejuvenation.
4.	Recovery: Minimal downtime is required, and you can return to your daily activities shortly after the procedure.
5.	Follow-Up: Our clinic provides post-treatment care and follow-up appointments to ensure your satisfaction and answer any questions you may have.
If you’re looking to restore a more youthful and refreshed appearance, our nasolabial folds treatment with dermal fillers at Dr. Stephanie Damalis’ clinic in Wimbledon, London, is the ideal solution. Dr. Damalis’ expertise and commitment to natural-looking results make our clinic a trusted choice for facial rejuvenation.
 
Our Nasolabial Folds Treatment Options
Dermal Fillers: A Popular Choice for Nasolabial Folds
At Damalis Skin Clinic, dermal fillers are a cornerstone treatment for nasolabial folds. These injectables provide immediate improvement by adding volume and smoothing out the folds, offering a rejuvenated appearance.
Types of Dermal Fillers We Use
We utilise a range of premium dermal fillers, including hyaluronic acid-based products like Juvéderm and Restylane. These fillers are chosen for their safety profile, effectiveness, and compatibility with the body’s natural tissues.
What to Expect During and After the Treatment
During the treatment, fillers are carefully injected into the targeted areas. Patients typically experience minimal discomfort, thanks to our advanced techniques and the use of fillers containing lidocaine. Post-treatment, you can expect immediate results with minimal downtime, allowing a return to daily activities.
Other Treatment Methods
Chemical Peels
Chemical peels, tailored to individual skin types, remove the outer skin layers, promoting regeneration and reducing the appearance of nasolabial folds.
Microneedling
Microneedling is a minimally invasive procedure that stimulates collagen production, improving skin texture and reducing the visibility of nasolabial folds.
Polynucleotides
This new treatment focuses on rejuvenating the skin from within. We offer a range of polynucleotides in clinic, each designed for specific areas of the face.
What to Expect: The Treatment Process
Initial Consultation and Assessment
Your journey at Damalis Skin Clinic begins with a comprehensive consultation, where our experts assess your skin and discuss your aesthetic goals.
During the Treatment Session
During the treatment, our focus is on comfort and precision. Whether it’s fillers or other methods, we ensure each step is conducted with the utmost care.
Follow-Up and Aftercare
Post-treatment, we provide detailed aftercare instructions and schedule follow-up appointments to monitor your progress and ensure optimal results.
Dermal Filler FAQs
How long do dermal fillers last?
Dermal fillers can last anywhere from six months to two years, depending on the type of filler used and the area treated.
Can dermal fillers be reversed?
Certain dermal fillers, especially those made from hyaluronic acid, can be dissolved using specific enzymes, allowing for reversibility if desired.
Is there any downtime after receiving dermal fillers?
Typically, there’s minimal to no downtime after a dermal filler treatment. Most clients can resume their daily activities immediately, though some minor swelling or bruising may occur.
Are there any side effects to dermal fillers?
While dermal fillers are generally safe, some common side effects include redness, swelling, and bruising at the injection site. These effects are usually temporary and resolve within a few days.
Can I combine dermal fillers with other cosmetic treatments?
Yes, many clients opt to combine dermal fillers with other treatments such as Botox or chemical peels for a comprehensive facial rejuvenation. It’s essential to consult with your practitioner to determine the best treatment plan for your needs.
Marionette Lines Treatment in London
Marionette lines, also known as “puppet lines” or “smile lines,” are the creases that form from the corners of the mouth down to the chin. These lines can often make individuals appear older or give a perpetually sad or tired expression. At Dr. Stephanie Damalis’ renowned clinic in Wimbledon, London, we administer dermal fillers for smile lines. The treatment ensures that you achieve a refreshed and rejuvenated look with natural results.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What Are Marionette Lines?
Marionette lines, often called ‘puppet lines’ or ‘smile lines’, are prominent creases extending from the corners of the mouth down towards the chin. These lines can significantly impact one’s appearance, often giving an older, tired, or sad look. At Damalis Skin Clinic, we know only too well the intricate nature of these lines and their effects on facial aesthetics.
Who is it for?
Marionette lines treatment with dermal fillers is suitable for:
1.	Individuals with Marionette Lines: If you have noticeable marionette lines that make you appear older or give you a tired look, this treatment can help.
2.	Adults of All Ages: Whether you are in your 30s, 40s, 50s, or beyond, dermal fillers can address marionette lines at any stage.
3.	Those Seeking Non-Invasive Solutions: If you prefer to avoid surgical options or are looking for a less invasive solution with minimal downtime, this treatment is ideal.
Concerns Treated
Our marionette lines treatment using dermal fillers effectively addresses several concerns, including:
1.	Marionette Lines: Softening and reducing the depth of marionette lines, which often create a sad or aged appearance.
2.	Facial Rejuvenation: Overall facial rejuvenation, as addressing marionette lines can have a significant impact on your overall facial aesthetics.
3.	Boosted Confidence: Many patients report increased self-confidence and a more positive self-image after this treatment.
Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
From £320
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
8-12 months
 
Finals results seen
After 2-4 weeks
 
Number of treatments
Varies (1-2)
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
FILLER TREATMENT IN LONDON
Benefits of Marionette Lines Treatment
Marionette, or smile lines, treatment with dermal fillers provides numerous advantages, including:
1.	Youthful Appearance: Dermal fillers effectively reduce the depth and visibility of marionette lines, leading to a more youthful and revitalised appearance.
2.	Non-Surgical: This procedure is non-surgical, meaning you can enjoy the benefits without the need for invasive surgery or lengthy recovery times.
3.	Minimal Discomfort: Our clinic uses advanced techniques and high-quality dermal fillers, ensuring a comfortable and virtually painless treatment experience.
4.	Natural Results: Dr. Stephanie Damalis specialises in achieving natural-looking results, avoiding the “overfilled” or artificial look.
5.	Quick Procedure: The treatment typically takes less than an hour, making it convenient for even the busiest individuals.
6.	Immediate Results: You can see noticeable improvements right after the procedure, with full results developing in a few days.
Marionette Lines Treatment Options
We offer a range of non-surgical treatments at Damalis Skin Clinic for marionette lines, prioritising minimal discomfort and immediate results. Our treatments include:
•	Dermal Fillers: Utilising high-quality hyaluronic acid-based fillers, we effectively reduce the depth of marionette lines, restoring a youthful appearance. This quick procedure, often completed in less than an hour, provides immediate improvements with natural-looking results.
•	Advanced Skin Boosters: These treatments are designed to hydrate the skin deeply, stimulate collagen production, and improve overall skin quality, softening the marionette lines.
 
Our Approach to Marionette Lines Treatment in London
Personalised Consultation
At Damalis Skin Clinic, every treatment journey begins with a personalised consultation. Our experts conduct a thorough facial assessment, discuss your concerns, and understand your aesthetic goals. This step ensures that we choose the most suitable treatment plan for you.
Comprehensive Treatment Process
Our treatment process is comprehensive and patient-centric. We combine advanced techniques with a holistic approach to not only treat marionette lines but also enhance overall facial rejuvenation. Post-treatment, we provide detailed aftercare instructions and follow-up consultations to ensure optimal and lasting results.
Dermal Filler FAQs
How long do dermal fillers last?
Dermal fillers can last anywhere from six months to two years, depending on the type of filler used and the area treated.
Can dermal fillers be reversed?
Certain dermal fillers, especially those made from hyaluronic acid, can be dissolved using specific enzymes, allowing for reversibility if desired.
Is there any downtime after receiving dermal fillers?
Typically, there’s minimal to no downtime after a dermal filler treatment. Most clients can resume their daily activities immediately, though some minor swelling or bruising may occur.
Are there any side effects to dermal fillers?
While dermal fillers are generally safe, some common side effects include redness, swelling, and bruising at the injection site. These effects are usually temporary and resolve within a few days.
Can I combine dermal fillers with other cosmetic treatments?
Yes, many clients opt to combine dermal fillers with other treatments such as Botox or chemical peels for a comprehensive facial rejuvenation. It’s essential to consult with your practitioner to determine the best treatment plan for your needs.
HarmonyCa - Hybrid Dermal Fillers in London
HarmonyCa® is a cutting-edge cosmetic treatment offered exclusively at our clinic in Wimbledon. This innovative hybrid dermal filler provides a versatile solution for a variety of aesthetic concerns, allowing our patients to achieve a harmonious, youthful appearance. 
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What is HarmonyCa Hybrid Dermal Filler?
HarmonyCa® Hybrid Dermal Filler represents a breakthrough in aesthetic medicine, combining the immediate volumising effect of a traditional dermal filler with the long-term skin rejuvenation benefits of a bio-stimulant. This dual-action treatment, available at Damalis Skin Clinic, is designed to enhance facial contours and stimulate the body’s natural collagen production.
The filler comprises two key components: crosslinked hyaluronic acid and calcium hydroxyapatite. Hyaluronic acid provides immediate volume and hydration to the skin, while calcium hydroxyapatite works beneath the skin’s surface to encourage collagen synthesis. This unique combination results in instant and progressive skin texture and firmness improvement.
Benefits of HarmonyCa® Hybrid Dermal Filler
1.	Natural-Looking Results: HarmonyCa® Hybrid Dermal Filler is renowned for its ability to deliver natural, subtle enhancements. It enhances your facial features while maintaining the unique qualities that make you, you.
2.	Long-Lasting Effects: With advanced technology, this filler boasts a longer duration of results compared to many other options. Patients can enjoy the benefits for up to 18 months before requiring a touch-up.
3.	Minimised Discomfort: Dr. Stephanie Damalis uses her extensive expertise to ensure that the procedure is as comfortable as possible. The formulation of HarmonyCa® includes lidocaine, a local anesthetic, to reduce discomfort during and after the treatment.
4.	Quick Recovery: Unlike surgical procedures, HarmonyCa® Hybrid Dermal Filler has minimal downtime. Most patients can return to their daily activities immediately after the procedure, making it a convenient choice for those with busy lifestyles.
5.	Versatile Applications: This dermal filler is highly versatile, capable of addressing multiple concerns in various facial areas, including the cheeks and jawline. Whether you desire  smoother skin or enhanced facial contours, HarmonyCa® has you covered.
Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
£1000
 
Anaesthesia needed
No
 
Discomfort level
Minimal
 
BACK TO WORK
Immediately
 
Duration of results
18-24 months
 
Finals results seen
After 3 months but some results can be seen immediately
 
Number of treatments
1-2
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
HarmonyCa TREATMENT IN LONDON
Why Choose HarmonyCa for Your Skin Care Needs?
Long-Lasting Results
One of the most compelling reasons to choose HarmonyCa at Damalis Skin Clinic is its longevity. Unlike traditional fillers offering temporary solutions, HarmonyCa provides results lasting up to 18 months. This extended duration is due to the unique combination of hyaluronic acid and calcium hydroxyapatite, which not only adds volume but also stimulates the body’s natural collagen production. This ongoing collagen synthesis ensures that the skin continues to improve over time, maintaining a youthful and refreshed appearance for longer periods.
Safety and Efficacy
At Damalis Skin Clinic, patient safety and treatment efficacy are paramount. HarmonyCa has been rigorously tested and proven to be safe and effective for various skin types and concerns. The treatment includes lidocaine, a local anaesthetic, to ensure maximum comfort during the procedure. Furthermore, the clinic’s experienced professionals, led by Dr. Stephanie Damalis, ensure that each treatment is tailored to the individual’s needs, maximising both safety and aesthetic outcomes.
Concerns Treated by HarmonyCa®
1.	Wrinkles and Fine Lines: HarmonyCa® effectively reduces the appearance of fine lines and wrinkles, helping you achieve a more youthful complexion.
2.	Lost Facial Volume: As we age, the loss of facial volume can lead to sagging skin. HarmonyCa® restores volume to create a lifted and rejuvenated appearance.
3.	Jowls and Marionette Lines: These are two areas that respond very well to HarmonyCA®  treatments.
4.	Cheek Contouring: HarmonyCa® can enhance the natural contours of your cheeks, creating a well-defined and balanced facial structure.
5.	Jawline Definition: Achieve a sculpted, youthful jawline by using HarmonyCa® to contour this area.
 
HarmonyCa Treatment Process at Damalis Skin Clinic
Consultation and Personalised Planning
The journey to rejuvenation with HarmonyCa begins with a detailed consultation at Damalis Skin Clinic. During this initial meeting, our experts, including Dr. Stephanie Damalis, thoroughly assess your skin and discuss your aesthetic goals. This personalised approach ensures that the treatment plan is uniquely tailored to your needs, considering factors such as skin type, facial structure, and desired outcomes.
The Treatment Session
The actual HarmonyCa treatment session is a meticulous process, performed with the utmost care and precision. The procedure typically lasts between 30 to 60 minutes, depending on the areas being treated. Using fine needles or cannulas, the HarmonyCa filler is strategically injected into the targeted areas. Patients often report minimal discomfort, thanks to the inclusion of lidocaine in the filler and the gentle techniques employed by our skilled practitioners.
Post-Treatment Care and Follow-up
After the treatment, patients can expect minimal downtime, allowing them to return to their daily activities almost immediately. Damalis Skin Clinic provides comprehensive post-treatment care instructions to ensure optimal healing and results. A follow-up appointment is usually scheduled within a few weeks of the initial treatment to assess the results and make any necessary adjustments. This ongoing care and attention to detail underscore the clinic’s commitment to achieving the best possible outcomes for our patients.

Profhilo Treatment in London
At our doctor-led clinic in the heart of Wimbledon, we take pride in offering cutting-edge aesthetic treatments that are not only safe and effective but also deliver natural-looking results. One such revolutionary treatment that has taken the cosmetic world by storm is Profhilo.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What is Profhilo?
Profhilo treatment is not just another skincare fad, it’s a groundbreaking treatment that has transformed the way we approach skin rejuvenation. With a focus on addressing skin laxity and the signs of ageing, Profhilo offers a unique and innovative approach that combines science with artistry.
How does Profhilo work?
Profhilo is an injectable treatment that utilises hyaluronic acid, a substance that naturally occurs in our skin and is responsible for maintaining hydration and elasticity. What sets Profhilo apart is its patented technology, which allows for the slow release of hyaluronic acid in two distinct formulations. This dual-action approach triggers the production of collagen and elastin in the skin, resulting in improved firmness, texture, and overall quality.
Treatment Overview
 
PROCEDURE TIME
30 minutes
 
PRICE
Course of 2 treatments £600
 
Anaesthesia needed
No
 
Discomfort level
Moderate
 
BACK TO WORK
Immediately (small lumps will be seen on the face lasting up to 24 hours)
 
Duration of results
3-6 months
 
Finals results seen
3 months after initial treatment but you will get a more immediate glow to the skin
 
Number of treatments
2-3
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
PROFHILO TREATMENT IN LONDON
Why Choose Profhilo?
1.	Natural Results: Profhilo treatment is designed to provide subtle and natural-looking results. It doesn’t involve volumising or dramatic changes, making it ideal for those who want to enhance their appearance while maintaining their unique features.
2.	Minimal Discomfort: The treatment involves a series of small injections, which are well-tolerated by most patients. Topical numbing agents are applied to ensure your comfort during the procedure.
3.	Quick Procedure: Profhilo is a relatively quick procedure that can be completed in around 30 minutes, allowing you to return to your daily activities without significant downtime.
4.	Suitable for All Skin Types: Regardless of your skin type, Profhilo can be tailored to meet your specific needs. It’s suitable for both younger individuals looking for preventative measures and those seeking to address the signs of ageing.
5.	Long-Lasting Results: The effects of Profhilo can last for several months, making it a cost-effective choice for achieving sustained skin rejuvenation.
6.	Doctor-Led Expertise: Our clinic is led by Dr Damalis, an experienced and highly qualified medical professional who understands the nuances of skin health and aesthetics. You can trust in her expertise to guide you through your Profhilo journey.
 
Profhilo Treatment Process at Damalis Skin Clinic
Consultation and Personalised Treatment Plan
Before any treatment, a thorough consultation is conducted. This involves assessing your skin type, discussing your aesthetic goals, and addressing concerns. Based on this, we create a personalised treatment plan tailored to your specific needs.
The Profhilo Treatment Procedure
The Profhilo treatment at Damalis Skin Clinic is a meticulous process. It involves a series of carefully placed injections by our skilled practitioners. The procedure, typically taking around 30 minutes, is designed for maximum comfort and effectiveness.
Aftercare and Follow-up
Post-treatment care is crucial. We provide detailed aftercare instructions to ensure the best results. A follow-up appointment is scheduled to monitor your progress and make any necessary adjustments.
How Long Do Results Last?
The results of Profhilo treatment at Damalis Skin Clinic are long-lasting but temporary. Typically, patients enjoy the benefits for up to six months. However, this can vary based on individual skin types and lifestyle factors.
Is Profhilo Right for Me?
Profhilo is suitable for individuals looking to improve skin hydration, texture, and elasticity. It is ideal for those experiencing signs of ageing or skin laxity. However, it is not recommended for pregnant or breastfeeding women or individuals with certain medical conditions. A consultation at Damalis Skin Clinic can help determine if Profhilo is the right choice for you.
Profhilo FAQs
How does Profhilo work?
Profhilo is injected into specific points on the face or other treated areas. Its dual-action formulation slowly releases hyaluronic acid, triggering the body’s natural processes to boost collagen and elastin production, leading to improved skin texture and firmness.
What is hyaluronic acid?
Hyaluronic acid is a naturally occurring substance in the body that plays a vital role in maintaining skin hydration and elasticity. Profhilo utilises a high concentration of hyaluronic acid to encourage the skin’s rejuvenation processes.
Is Profhilo safe?
Yes, Profhilo is considered safe when administered by trained medical professionals. As with any medical procedure, there can be potential side effects or risks, which Dr Steph will discuss during your consultation.
Who is a suitable candidate for Profhilo?
Profhilo is suitable for individuals with concerns about skin laxity, fine lines, and overall skin quality. It can be used on various skin types and ages, making it suitable for both preventative and corrective purposes.
Does Profhilo involve downtime?
One of the advantages of Profhilo is it requires minimal downtime. You may experience slight redness or swelling at the injection sites, but most patients can resume their daily activities immediately after the procedure.
How many sessions of Profhilo are recommended?
The number of sessions can vary depending on your specific goals and the condition of your skin. Typically, a course of two to three treatments is recommended, with a four-week interval between sessions.
When will I see results from Profhilo?
Results from Profhilo may become noticeable after the first treatment, but the full effects usually become more apparent a few weeks after completing the recommended treatment sessions.
Are Profhilo results long-lasting?
While individual results can vary, the effects of Profhilo can last for several months. Maintenance treatments are usually recommended every six to nine months to prolong the results.
Does Profhilo hurt?
Most patients report only minor discomfort during the Profhilo procedure. Topical numbing agents are often applied before the treatment to ensure your comfort. The injections use very fine needles, making the process well-tolerated for many individuals.
Chemical Peels in London
Chemical peels are designed to unveil a fresher, more radiant layer of skin hidden beneath the daily wear and tear. We offer 3 specialised skin peels at our Wimbledon clinic – Neostrata Retinol Peel, Obagi Blue Peel Radiance, and the Obagi TCA peel. We promise you a rejuvenating experience.
Book Online
 
BESPOKE SKIN CONSULTATIONS
What are chemical peels?
Chemical peels typically contain alpha hydroxy acids (AHAs) or beta hydroxy acids (BHAs) designed to exfoliate and renew the skin. The acids work to dissolve the bonds between skin cells to varying depths depending on the strength, resulting in the shedding of old skin. The effect is a revealing of smoother, brighter skin underneath.
The benefits of chemical peels:
•	Improvement in skin texture, tone and clarity
•	Reduction in fine lines and wrinkles
•	Correction of pigmentation issues
•	Minimisation of pore size and acne breakouts
•	Enhanced penetration of skincare products
•	Increased collagen production
•	Scar/acne scarring reduction
•	Pore size control
Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
From £150
 
Anaesthesia needed
No
 
Discomfort level
Minimal to moderate
 
BACK TO WORK
Immediately (peeling generally starts 3 days after the treatment)
Sensitivity period- 2 weeks
 
Duration of results
3-6 months
 
Finals results seen
After 2-4 weeks
 
Number of treatments
Course of 3
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
SKIN PEELS IN LONDON
Skin Peels We Offer at Damalis Skin Clinic
Neostrata Retinol Peel: 
A medium depth peel for anti-ageing and pigmentation. Suitable for all skin types.
Ingredients:
•	Retinol 3%
•	Aminofil. A substance derived from amino acids is added to help with the enhancement of collagen and hyaluronic acid.
•	Vitamin E. A known antioxidant
•	Bisabolol. A chamomile derivative
•	Neocitriate. Added to stimulate collagen synthesis.
Obagi Blue Peel Radiance: 
Superficial peel that evens tone without downtime. Address sun damage, scarring and ageing.
Ingredients: Salicylic acid, Glycolic acid, Lactic acid.
Obagi Blue TCA Peel:
Our strongest chemical face peel targets coarse wrinkles, acne scarring and deep pigmentation issues. Requires several days of downtime.
Key ingredient: Slow-acting trichloroacetic acid
 
The Chemical Peel Process: What to Expect
Consultation and Skin Assessment
Your journey at Damalis Skin Clinic begins with a thorough consultation and skin assessment. This crucial step allows us to understand your skin’s unique needs and tailor the chemical peel accordingly. Dr Damalis will evaluate your skin type, discuss your concerns, and recommend the most effective peel, ensuring a personalised and effective treatment plan.
The Peel Procedure: Steps and Safety Measures
During the peel procedure, your comfort and safety are our top priorities. We apply the peel using precise techniques, ensuring maximum effectiveness while minimising discomfort. We adhere to stringent safety measures, ensuring that each process step is performed with the utmost care. We aim to provide a seamless, safe, and comfortable experience, leading to the best possible results for your skin.
Post-Peel Care and Maintenance
Post-peel care is vital for maximising the benefits of your chemical peel. At Damalis Skin Clinic, we provide comprehensive guidance on post-treatment care, including skincare products and routines to enhance and prolong the results. We are committed to supporting you every step of the way, ensuring your skin remains healthy, radiant, and rejuvenated long after your visit to our clinic.
Preparing for Your Chemical Peel
Pre-Treatment Guidelines
We provide detailed pre-treatment guidelines to ensure the best possible outcome from your chemical peel. These may include specific skincare routines, avoiding certain products or medications, and preparing your skin for the treatment. Adhering to these guidelines will help optimise the peel’s effectiveness and reduce the likelihood of any adverse reactions.
Who Should Avoid Chemical Peels?
While chemical peels benefit many, they are not suitable for everyone. Individuals with certain skin conditions, those who are pregnant, or have used specific acne treatments recently may need to avoid chemical peels. During your consultation at Damalis Skin Clinic, we will assess your suitability for a peel and ensure that your treatment plan is safe and effective for your skin type and condition.
Does a chemical peel hurt?
When applied, most chemical peels have a mild stinging or tingling sensation. Practitioners are trained to ensure your comfort throughout the process. For stronger peels, a topical anaesthetic may be applied beforehand to minimise any discomfort.
Are chemical peels safe?
Chemical peels are a safe treatment when performed by an experienced practitioner. They use controlled amounts of regulated acids. However, those with active skin conditions or recent procedures like lasers should not undergo peeling until fully healed. A consultation is always undertaken to assess your suitability.
Will I have any downtime with the chemical peel?
Downtime depends on the peel strength. Mild peels have little to no downtime, while stronger peels may cause redness, flaking or peeling for a few days. We will recommend tips to minimise downtime and get you back to regular activities sooner.
How long until I see the results of a chemical peel?
Typically, mild peels provide noticeable smoothing within a few days, while medium-depth peels yield results in 1-2 weeks. Deeper peels can take 2-4 weeks to reveal improvements. Multiple treatments may be needed for lasting anti-ageing or pigmentation benefits.
How long do chemical peel effects last?
With continued excellent home care and sun protection, chemical peel results often endure for several months. Mild peels provide temporary improvements, while medium-deep peels can elevate skin quality for 6-12 months. For long-term anti-ageing, a recommended series offers the best outcomes.
How often should I have a chemical peel?
This depends on the reasons you are having a peel. We may recommend a peel every 4-6 weeks if there is a specific condition you wish to treat.
Polynucleotides in London
Polynucleotide injections offer a revolutionary method in aesthetic medicine, relying on purified polymerised polynucleotides. At our Wimbledon clinic, we are experienced in safe and effective treatments. Distinct from traditional methods, they rejuvenate skin, restoring its firmness and radiance.
Book Online
 
The science behind Polynucleotides revolves around transforming fibroblasts and other cells into myofibroblasts, creating immediate, visible skin enhancements.
Plinest® and Newest®
In line with the clinic’s ethos of seeking out the safest and most effective treatments, Damalis Skin Clinic proudly offers two brands of Polynucleotides, – Plinest® and Newest®.
We feel these are among the best polynucleotide solutions on the market today. From Plinest®, we provide three targeted treatments, Plinest®, Plinest Hair®, and Plinest Eyes®, based on the magic of polymerised polynucleotides. Newest®,  additionally contains hyaluronic acid and is designed for more mature skin.
Eyes and Face Rejuvenation
Plinest Eyes® is a moisturising gel combatting eye bags, dark circles, and wrinkles around the eyes. It works to reduce tissue loss/thinning around this delicate area.
Plinest® revitalises the face, neck and hands, addressing ageing signs and reducing dehydration. It aims to give  improvements across the treated area.
PLINEST® Hair works to improve the patient’s scalp and hair condition. Both Plinest® and Newest® treatments are meticulously formulated with purified polymerised polynucleotides, free from allergenic components like proteins. The treatments boast multiple benefits, from combating free radicals, boosting tissue regeneration, enhancing skin tone and elasticity, and promoting local vascularisation.
Treatment Overview
 
PROCEDURE TIME
45 minutes
 
PRICE
Course of 3 treatments £900
 
Anaesthesia needed
Yes
 
Discomfort level
Minimal to moderate
 
BACK TO WORK
Immediately
 
Duration of results
3 months
 
Finals results seen
3 months after initial treatment
 
Number of treatments
Course of 3
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
Polynucleotide TREATMENT IN LONDON
Benefits of Polynucleotides Treatment:
•	Stimulates tissue repair by enhancing stem cells.
•	Revives skin elasticity and tone.
•	Neutralises free radicals, shielding skin from oxidative harm.
•	Boosts formation of new capillaries, enhancing skin health.

What can you expect from polynucleotides?
•	The treatment promises enhanced skin firmness, elasticity, and overall skin quality improvement, with results lasting for months.
Are polynucleotide treatments suitable for all skin types?
•	Generally, polynucleotide treatments are formulated to be compatible with various skin types. That being said, it’s important to have an in-depth consultation prior to undergoing the procedure. This ensures the treatment suits your specific skin type and condition.

How is polynucleotide treatment different from other dermal fillers or treatments?
While traditional dermal fillers often use substances like hyaluronic acid to fill and smoothen skin, polynucleotide treatments focus on rejuvenating and repairing skin from within. The treatment uses polymerised polynucleotides that promote skin elasticity and aid in tissue regeneration and repair.

Are there any specific aftercare steps to follow post-polynucleotide treatment?
After undergoing a polynucleotide treatment, it’s recommended to avoid direct sun exposure and refrain from strenuous activities that can cause excessive sweating for at least 24 hours. Keeping the skin moisturised and avoiding harsh skincare products for a few days is also beneficial.
How frequently should I undergo polynucleotide treatments to maintain results?
The longevity of the treatment results can vary among individuals, but typically, the effects last several months. Some specialists recommend undergoing the treatment 2-3 times a year to maintain optimal results, but it’s best to consult your dermatologist for personalised advice.
Is the polynucleotide procedure painful?
Most patients report minimal discomfort during the procedure. The treatment involves using fine needles, and while this can cause slight discomfort, it’s usually bearable. We offer numbing creams or local anaesthesia to enhance the comfort level during the treatment.
Advanced Skin Analysis in London
Discover the power of Observe 520x at our Wimbledon clinic, led by the renowned aesthetic doctor Stephanie Damalis. Unleash the potential of cutting-edge observation and skin analysis tools to transform your skin health and well-being.
Book Online
 
BESPOKE SKIN analysis
Skin Analysis Benefits
Many conditions originate in the deep layers of skin and are difficult to diagnose without technological aid. The Observ 520x uses patented skin fluorescence and polarised light illumination technology to reveal those conditions, even in the early stages of their development.
Our London Clinic is thrilled to introduce Observe 520x, a state-of-the-art observation and analysis tool that is revolutionising the way skincare is delivered. Under the guidance of Dr. Damalis, a leading expert in aesthetic innovation, this powerful tool is helping patients and practitioners gain valuable insights, make informed decisions, and improve health outcomes.
Key Features
1.	Personalised Skin Health Assessments: Dr. Damalis and her team use Observe 520x to provide personalised skin health assessments, enabling a deeper understanding of your unique skin.
2.	Real-Time Monitoring: Observe 520x allows continuous skin health monitoring, helping Dr. Damalis and her patients to track progress and make necessary adjustments in real time.
3.	Customised Health Plans: With the data collected through Observe 520x, Dr. Damalis can create tailored health plans that are specific to your needs, ensuring the most effective and efficient care.
4.	Data-Driven Diagnosis: Harness the power of data-driven diagnosis, as Dr. Damalis uses Observe 520x to make accurate and evidence-based assessments, leading to more precise treatment recommendations.
 
 
BESPOKE SKIN analysis
What will I be able to see?
•	Pigmentation disorders
•	Distribution of melasma
•	Blocked/open pores
•	Dehydrated skin
•	Vascular conditions
•	Skin irritations
•	Rosacea
•	Milia
•	Wrinkle formations
•	Areas with diminished circulation
•	Areas with collagen loss
•	And much more!
Microneedling in London
We take pride in offering advanced and cutting-edge treatments to enhance your skin’s health and beauty. One such revolutionary treatment we offer at our Wimbledon clinic is microneedling with the SkinPen Precision device, a highly sought-after procedure for achieving smoother, rejuvenated skin.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What is Microneedling with SkinPen Precision?
Microneedling, known as collagen induction therapy, is a minimally invasive cosmetic procedure that enhances skin healing. SkinPen Precision is a device designed for precise and safe treatment. It uses fine, sterile needles to create micro-injuries in the skin, triggering natural collagen and elastin production. This process reduces fine lines, wrinkles, acne scars, enlarged pores, and stretch marks and improves skin texture, tone, and radiance.
Concerns Microneedling can help with:
•	Acne scarring
•	Surgical scars
•	Lines and wrinkles
•	Large pores
•	Pigmentation
•	Stretch marks
•	Rough skin
•	Dull skin
Benefits of Microneedling
Microneedling, a revolutionary collagen induction therapy, offers many benefits for the skin. This minimally invasive procedure, performed using the state-of-the-art SkinPen Precision device, is designed to rejuvenate and revitalise your skin. Here are the key benefits:
•	Reduction of Fine Lines and Wrinkles: By stimulating collagen production, microneedling effectively diminishes the appearance of fine lines and wrinkles, resulting in smoother, younger-looking skin.
•	Improved Skin Texture and Tone: Regular microneedling sessions enhance your skin’s overall texture and tone, leaving it more radiant and vibrant.
•	Acne Scar Treatment: This procedure is particularly effective in reducing the visibility of acne scars, providing a clearer and more even complexion.
•	Minimised Pore Size: Microneedling helps reduce the size of enlarged pores, thereby improving skin texture.
•	Treatment of Stretch Marks and Pigmentation: It also reduces stretch marks and pigmentation, promoting an even skin tone.
Treatment Overview
 
PROCEDURE TIME
60 minutes
 
PRICE
From £200
 
Anaesthesia needed
Yes
 
Discomfort level
Minimal
 
BACK TO WORK
Next day (most of the redness will have settled)
Recovery time-24-48 hours
Sensitivity period- 2 weeks
 
Duration of results
3-6 months
 
Finals results seen
3 months after initial treatment but you will get a more immediate glow to the skin
 
Number of treatments
Course of 3
Disclaimer: Please note that the duration of treatments, level of pain experienced during the procedure, and recovery time can vary significantly among individuals. While we aim to provide an estimation based on our clinical experience, factors such as individual pain tolerance, skin sensitivity, and treatment specifics may influence the actual experience. We recommend discussing any concerns or questions regarding these aspects with your healthcare provider prior to undergoing the procedure
skinpen IN LONDON
Why Choose SkinPen Precision?
1.	Doctor-Led Expertise: Our clinic is led by Dr Damalis, an experienced medical professional who understands the intricacies of skin health. 
2.	Precision and Safety: The SkinPen Precision device is FDA-approved and has been designed with patient safety and comfort in mind. Its adjustable needle depth allows for precise treatment of different areas of the face and body.
3.	Minimal Downtime: Microneedling with SkinPen Precision requires minimal downtime, making it an excellent option for those with busy lifestyles. You can typically return to your daily activities within a few days.
4.	Effective Results: Over a series of treatments, you will notice gradual improvements in your skin’s texture and appearance. Many patients report smoother, more radiant skin after just a few sessions.
5.	Versatile Application: SkinPen Precision can be used on various skin types and tones, making it suitable for a wide range of patients seeking skin rejuvenation.
 
 
Unlock Your Skin's Potential
Microneedling with SkinPen in London at our doctor-led skin clinic offers a transformative experience for those seeking healthier, more youthful-looking skin. Whether you’re concerned about fine lines, acne scars, or general skin texture, Dr Damalis is here to guide you through the process and help you achieve your skincare goals.
Invest in the health and beauty of your skin by scheduling a consultation with us today. Discover the difference that microneedling with SkinPen Precision can make in your skincare journey, and embark on a path towards radiant, revitalised skin.
The Microneedling Procedure at Damalis Skin Clinic
Consultation and Personalised Plans
At Damalis Skin Clinic, your microneedling journey begins with a personalised consultation. Our expert practitioners assess your skin’s condition and discuss your aesthetic goals. Based on this, we craft a tailored treatment plan to address your specific skin concerns effectively.
The Microneedling Session
Before the procedure, your skin will be cleansed and a topical numbing cream may be applied to ensure your comfort throughout the treatment.
During the microneedling session, our skilled professionals use the SkinPen Precision device to create controlled micro-injuries on the skin. Though minimally invasive, this process is performed with utmost care to ensure patient comfort. 
The procedure typically takes about 30 minutes, depending on the treatment area.
Aftercare and Results
Post-Procedure Care
Post-treatment care is crucial for achieving the best results. After the session, your skin may exhibit mild redness, akin to a sunburn. We provide comprehensive aftercare instructions, including skincare recommendations to soothe and protect your skin. It’s important to avoid direct sun exposure and use a broad-spectrum sunscreen.
Expected Results and Timeline
The results of microneedling at Damalis Skin Clinic are progressive. While some improvements can be seen immediately, the full benefits are typically observed after several treatments. Most patients report noticeable skin texture and appearance enhancements within a few weeks. We recommend a series of sessions spaced a few weeks apart, tailored to your skin’s needs for optimal results.
Microneedling FAQs
How Does Microneedling Work?
In microneedling, tiny needles create micro-channels in the skin, triggering the body’s wound-healing response. This stimulates collagen and elastin production, leading to smoother, firmer, and a more even skin tone and texture.
What Are the Benefits of Microneedling?
Microneedling benefits include reducing fine lines, wrinkles, acne scars, enlarged pores, stretch marks, and sun damage. It enhances skin radiance, making it versatile for various skin types and concerns.
Is Microneedling Painful?
A topical numbing cream is applied before microneedling to minimise discomfort. Patients typically feel mild to moderate sensations, like tingling or pricking. Discomfort levels vary based on treatment depth and intensity.
How Many Microneedling Sessions Are Needed?
The number of microneedling sessions depends on individual skin concerns and goals. Dr Damalis will assess your skin, consult, and create a personalised treatment plan.

Advanced Skincare in London
We are proud to offer medical-grade skincare solutions at our skin clinic in Wimbledon, with a special emphasis on Obagi products. Our mission is to help you achieve radiant and healthy skin through science-backed skincare and the highest quality treatments.
Book Online
 
BESPOKE SKIN CONSULTATIONS
Why Obagi Medical Grade Skincare?
Obagi is a globally recognised brand that has revolutionised the skincare industry. It offers a range of medical-grade products designed to address various skin concerns, from ageing and pigmentation issues to acne and overall skin health. At our clinic, we believe in the transformative power of Obagi’s scientifically formulated skincare regimens.
Benefits of Obagi Medical Grade Skincare:
1.	Visible Results: Obagi products are backed by extensive clinical research, ensuring you see noticeable improvements in your skin’s texture, tone, and overall appearance.
2.	Customised Solutions: Dr. Stephanie Damalis will create a personalised skincare plan that caters to your unique needs, ensuring you get the best possible results.
3.	Rejuvenation and Anti-Ageing: Obagi is renowned for its anti-ageing solutions, which can reduce fine lines, wrinkles, and age spots, giving you a more youthful and radiant complexion.
4.	Even Skin Tone: Say goodbye to uneven pigmentation, dark spots, and blemishes with Obagi’s skin lightening and brightening products.
5.	Acne Management: Obagi offers effective solutions for managing acne, minimising breakouts, and reducing acne-related scarring.
6.	Improved Skin Health: Obagi doesn’t just mask issues; it actively promotes skin health from within, leaving you with a natural glow.
skin TREATMENTs IN LONDON
Concerns Treated by Obagi Medical Grade Skincare
1.	Ageing Skin: Reduce fine lines, wrinkles, and age spots for a more youthful appearance.
2.	Pigmentation Issues: Address uneven skin tone, dark spots, and melasma.
3.	Acne and Acne Scarring: Control breakouts and minimise the appearance of acne scars.
4.	Skin Texture and Tone: Achieve smoother, more even skin texture and tone.
5.	Skin Health Maintenance: Keep your skin healthy and glowing, regardless of your age or skin type.

SKIN Concerns
Volume Loss Treatment in London
Volume loss, also known as facial volume loss, is a natural part of the ageing process. It occurs when the skin and underlying tissues lose their youthful fullness and elasticity. This condition can affect various areas of the body, but it is most commonly associated with the face. On this page, we will explore the causes, signs, and the use of dermal fillers for volume loss treatment, with a focus on Dr. Stephanie Damalis’ clinic in Wimbledon.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
Causes of Volume Loss
Several factors contribute to volume loss, including:
1.	Ageing: The most common cause of volume loss is the natural ageing process. Our skin produces less collagen and elastin as we age, resulting in decreased skin elasticity and fullness. Volume loss occurs not only in the skin but also in deeper layers of the face as well. This may include loss of fat, muscle and bone mass. Volume loss from these areas affects the skin structure and can be addressed by dermal fillers. 
2.	Genetics: Some individuals are genetically predisposed to experience volume loss at a younger age.
3.	Lifestyle Choices: Smoking, excessive sun exposure, and an unhealthy diet can accelerate the loss of collagen and elastin, leading to premature volume loss.
4.	Weight Loss: Significant weight loss can cause volume loss, especially in the face, as the fat pads diminish.
5.	Medical Conditions: Certain medical conditions, such as autoimmune diseases, can contribute to facial volume loss.
Why Choose Damalis Skin Clinic for Your Volume Loss Treatment
At Damalis Skin Clinic, we understand the intricacies of facial volume loss, a natural part of the ageing process. Our clinic stands out for its commitment to delivering personalised and effective treatments. Led by Dr. Stephanie Damalis, a seasoned aesthetic doctor with over 12 years of experience, we offer a unique blend of expertise, care, and advanced technology. Our approach is holistic, focusing not just on the treatment but on our patients’ overall well-being and satisfaction. Choosing Damalis Skin Clinic means opting for a clinic that values your individuality and aims to enhance your natural beauty while maintaining the highest standards of safety and professionalism.
Who Is Most Likely to be Affected?
Volume loss is a natural part of the ageing process and can affect anyone. However, some individuals may be more prone to it due to genetic factors or lifestyle choices. It is often more noticeable in people over the age of 40, but signs can appear earlier in some cases.
BOTOX TREATMENT IN LONDON
Signs of Volume Loss
Recognising the signs of volume loss is crucial for timely intervention. Common signs include:
1.	Hollow Cheeks: A sunken appearance in the cheek area.
2.	Thin Lips: Reduced lip fullness and definition.
3.	Wrinkles and Folds: Increased lines and wrinkles, particularly around the nose and mouth.
4.	Sagging Skin: Skin that loses its firmness and begins to sag.
5.	Sunken Eyes: A hollow look around the eyes, creating dark circles.
6.	Jowls: A loss of definition in the jawline.
Jowls Treatment in London
Jowls are a common concern for many individuals as they age, affecting the appearance of the lower face. At Damalis Skin Clinic in Wimbledon, we understand the impact of jowls on your self-esteem and offer effective solutions to help you regain your youthful appearance. On this treatment page, we will delve into the signs, causes, and treatment options available for jowls, with a special focus on dermal fillers provided at our clinic.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What are Jowls?
Jowls refer to the sagging, drooping skin and tissue along the jawline, particularly in the lower cheeks and beneath the chin. They can create an aged and tired appearance, which can significantly impact one’s self-confidence.
Signs of Jowls
•	Sagging Skin: Jowls are characterised by the loss of skin elasticity, resulting in a downward shift of the skin along the jawline.
•	Loose Tissue: The accumulation of excess fat and a reduction in muscle tone contribute to the appearance of jowls.
•	Prominent Folds: Jowls often lead to the development of deep, vertical folds around the mouth, contributing to an aged appearance.
Jowls TREATMENT IN LONDON
Causes of Jowls
Several factors contribute to the development of jowls, including:
•	Ageing: The natural ageing process leads to a reduction in collagen and elastin, which are essential for skin firmness.
•	Genetics: Some individuals may be genetically predisposed to developing jowls earlier in life.
•	Lifestyle Choices: Smoking, excessive sun exposure, and poor dietary habits can accelerate skin ageing.
•	Weight Fluctuations: Rapid weight loss or gain can lead to the loss of skin elasticity and the development of jowls.
 
 
Treating Jowls at Damalis Skin Clinic London
We are committed to helping you achieve a more youthful and rejuvenated appearance through our innovative treatments. One of the highly effective solutions we offer for jowls is the use of dermal fillers.
Dermal Fillers for Jowls:
Dermal fillers are a non-surgical option to combat the signs of jowls. These fillers contain hyaluronic acid, a naturally occurring substance in the skin that provides volume and hydration. When injected into the jowl area, dermal fillers can:
•	Lift and Contour: Dermal fillers help lift sagging skin, restoring a more youthful contour to the jawline and cheeks.
•	Restore Volume: By replenishing lost volume, dermal fillers diminish the appearance of deep folds and wrinkles.
•	Stimulate Collagen: Some dermal fillers stimulate collagen production, contributing to long-lasting results.
Enlarged Pores Treatment London
Enlarged pores, often a result of genetics, ageing, and excessive oil production, can significantly affect your skin’s appearance and impact your self-confidence. At Damalis Skin Clinic in Wimbledon, we are committed to providing advanced and effective treatments to refine skin texture and minimise pore visibility, enhancing your skin’s health and confidence.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
Factors Contributing to Enlarged Pores
Several key elements contribute to the appearance of enlarged pores, which include:
•	Genetics: Pore size is often genetically predetermined and may be more prominent in certain skin types.
•	Ageing: As the skin loses elasticity with age, pores can appear larger.
•	Excessive Sebum Production: This can lead to enlarged pores, particularly in oily skin types, as overactive sebaceous glands produce more oil.
•	Sun Damage: Prolonged sun exposure can thicken the outer layer of the skin, contributing to enlarged pores.
•	Clogged Pores: Dead skin cells and oil accumulation can stretch the pores, making them more visible.
Advanced Treatments for Enlarged Pores
To effectively address enlarged pores, we offer:
1.	Medical Grade Skincare
o	We have various options in this category. Products containing retinoids stimulate collagen production and support the pore’s structure. They also help with the control of sebum production. 
2.	Obagi Blue Radiance Peel
o	This chemical peel targets enlarged pores and enhances both skin tone and texture. It works by exfoliating the top layer of the skin, thereby reducing pore appearance and rejuvenating the skin.
3.	 Polynucleotides
o	This innovative treatment utilises polynucleotides to stimulate skin regeneration and repair, improve skin elasticity, and produce smoother, more refined skin.
4.	Microneedling
o	This treatment creates micro-injuries on the skin, which activates the natural healing process and boosts collagen production, ultimately helping to tighten the skin and reduce pore size.
 
 
Personalised Treatment Plans
Recognising that each individual’s skin is unique, our experienced professionals at Damalis Skin Clinic will thoroughly assess your skin type, concerns, and overall condition. We aim to recommend the most suitable treatment or combination of treatments, offering personalised care to achieve the best possible results for your skin.
Acne Scars Treatment in London
Acne scars, a common aftermath of severe acne, can leave lasting marks on both the skin and self-esteem. Damalis Skin Clinic in Wimbledon specialises in treating acne scars through advanced methods like microneedling and chemical peels, targeting everything from superficial scars to deeper scars. We understand the importance of treating these scars to improve skin appearance and boost overall confidence.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
Personalised Treatments
Every individual’s skin journey is unique, especially when it comes to acne scarring. Our clinic offers personalised acne scarring treatments, catering to a range of scars, including atrophic acne scars, boxcar scars, and deep ice pick scars. We focus on understanding each type of acne scar to provide the most effective treatment for acne scars.
Acne Scar Formation
When acne lesions heal, the skin may produce too much or too little collagen, forming raised or depressed acne scars. This imbalance in the skin healing process is crucial in deciding the right acne scarring treatment. Options like microneedling are designed to normalise wound healing and collagen production.
Acne Scar Treatment Options
Ice Pick Scars
Depending on the severity, we may recommend the Obagi TCA peel, microneedling or both.
Boxcar Scars
Typically require a combination of treatments, including chemical peels and resurfacing procedures, to smooth the scar edges.
Rolling Scars
Treatments like collagen induction therapy (also known as microneedling) or soft tissue fillers are effective in raising depressed scar areas.
 
 
Advanced Treatment Modalities at Damalis Skin Clinic
We recommend the following treatments for acne scarring:
1.	Microneedling
o	Microneedling is effective for atrophic scars (pitted or indented scars). This treatment stimulates collagen fibres, promoting skin healing.
2.	Chemical Peels
o	Our chemical peels range includes salicylic acid, lactic acid, glycolic acid, and slow-acting tricholoroacetic acid peels. Different acids target different depths of acne scarring. Light peels work on the outer layer of the skin, while deep peels are more suitable for deeper scars. We use the Obagi range, both the Blue Radiance peel and the TCA peel. We will suggest the best type for your particular case.
Hyperpigmentation Treatment London
Hyperpigmentation is a common skin condition characterised by the darkening of certain areas of the skin due to an excess of melanin. It can affect people of all ages, genders, and skin types and is often a source of concern for many individuals. Damalis Skin Clinic in Wimbledon provides a range of effective treatments for hyperpigmentation, including chemical peels and Obagi medical grade skincare. On this treatment page, we will delve into the signs, causes, types of hyperpigmentation, and discuss the methods offered by Damalis Skin Clinic to help you regain your clear, radiant skin.
Book Online
 
BESPOKE MEDICAL CONSULTATIONS
What is Hyperpigmentation?
Hyperpigmentation is a skin condition marked by the darkening of certain skin areas due to an excess buildup of melanin. This condition can manifest in various forms, such as dark spots, uneven skin tone, freckles, age spots, and melasma. It affects individuals of all ages, genders, and skin types. The root cause is often hard to pin down, but factors like sun exposure, hormonal changes, inflammation, and genetics play significant roles in its development. Sun exposure, for instance, stimulates melanin production, while hormonal fluctuations during events like pregnancy can trigger hyperpigmentation. Inflammation from acne or injuries and genetic predisposition are also possible contributors.
Signs of Hyperpigmentation
Hyperpigmentation presents itself through various signs, which can include:
1.	Dark Spots: Dark patches or spots on the skin are the most common sign of hyperpigmentation.
2.	Uneven Skin Tone: The affected area may have an uneven or blotchy appearance.
3.	Freckles or Age Spots: These are typically caused by sun exposure and can appear as small, dark spots on the skin.
4.	Melasma: A specific form of hyperpigmentation often seen in pregnant women, melasma appears as brown or grayish-brown patches on the face.
Causes of Hyperpigmentation
Hyperpigmentation can be caused by various factors, including:
1.	Sun Exposure: Overexposure to the sun’s harmful UV rays is a leading cause of hyperpigmentation. UV rays stimulate melanin production in the skin.
2.	Hormonal Changes: Hormonal fluctuations, such as those during pregnancy or while taking certain medications, can trigger hyperpigmentation.
3.	Inflammation: Skin inflammation, whether due to acne, injuries, or other skin conditions, can lead to hyperpigmentation.
4.	Genetics: Some individuals may be genetically predisposed to hyperpigmentation.
pigmentation TREATMENT IN LONDON
Types of Hyperpigmentation
There are several types of hyperpigmentation, including:
1.	Post-Inflammatory Hyperpigmentation (PIH): PIH occurs after an injury or inflammation of the skin, such as acne, cuts, or burns.
2.	Melasma: Melasma is often linked to hormonal changes and typically appears on the face, particularly during pregnancy or when taking birth control.
3.	Sunspots: Also known as solar lentigines or age spots, these are directly related to sun exposure and can appear on areas exposed to the sun.
 
 
Treating Hyperpigmentation
At Damalis Skin Clinic in London, we offer two highly effective treatments for hyperpigmentation:
1.	Chemical Peels:
o	Chemical peels involve applying a chemical solution to the skin to exfoliate the top layer and stimulate the growth of new, evenly pigmented skin.
o	This treatment can effectively reduce the appearance of hyperpigmentation and improve skin texture.
2.	Obagi Medical Grade Skincare:
o	Obagi is a renowned medical-grade skincare brand that offers products specially designed to address hyperpigmentation
o	These products can help fade dark spots, even out skin tone, and provide long-lasting results.
•	 
Hyperpigmentation Treatments at Damalis Skin Clinic
Consultation and Personalised Approach
At Damalis Skin Clinic, we begin with a thorough consultation to understand each patient’s unique skin concerns. Dr Stephanie Damalis assesses the skin’s condition and devises a personalised treatment plan. This approach ensures that every treatment is specifically tailored to address individual skin types and hyperpigmentation issues, maximising the effectiveness of the treatment.
Advanced Treatment Options
We offer advanced treatment options for hyperpigmentation, including chemical peels and Obagi Medical Grade Skincare. Chemical peels work by exfoliating the top skin layer, promoting the growth of new, evenly pigmented skin. Obagi products, known for their targeted action against hyperpigmentation, help fade dark spots and even out skin tone, providing long-lasting results.
Preparing for Your Treatment
What to Expect During the Consultation
During the consultation at Damalis Skin Clinic, patients can expect a comprehensive skin assessment. Dr. Damalis will discuss your skin’s history, examine the hyperpigmentation, and explain the treatment options. This session is important for the understanding of the hyperpigmentation causes and to ascertain the optimum treatment process.
How to Prepare for Treatment
To prepare for hyperpigmentation treatment, patients should avoid sun exposure and use sunscreen regularly to prevent further skin damage. It’s also advisable to discontinue any skin products that might irritate the skin a few days before the treatment. You should inform Dr Damalis of any medications or supplements you are taking, as some might affect the treatment’s outcome.
Jowls & Sagging Skin Treatment in London
Sagging skin is a visible sign of ageing that can affect anyone, regardless of skin type or lifestyle. At Damalis Skin Clinic in Wimbledon, we are familiar with the issue and the fact it could be impacting more than just your appearance. We have multiple options treat jowls and sagging skin at the clinic. More offerings from an expert clinic equate to more chance of a successful skin tightening solution.
Book Online
 
Why Does Skin Sag?
As the skin ages, it will progressively lose its elasticity and firmness, leading to drooping and sagging. Factors like sun exposure, environmental pollutants, genetics, and lifestyle choices can accelerate this process. While sagging facial skin, also known as jowls, is a natural part of ageing, it doesn’t mean you have to accept it without putting up a fight.
 
The Solution At Damalis Skin Clinic
At Skin Damalis Clinic, we specialise in advanced, non-invasive treatments designed to rejuvenate and tighten saggy skin, restoring its youthful resilience. With the latest aesthetic techniques we use here, we are confident to offer you the best possible results.
Whether you’re just starting to notice a change in your skin’s firmness or looking for a solution to more advanced sagging, we can help. In the following sections, we’ll explore the various treatment options available at our clinic, including Dermal Fillers, Profhilo, HarmonyCA, Neauvia Stimulate, and Plinest & Newest Polynucleotides. Each of these treatments has a role to play in combating sagging skin and jowls. Depending on your particular case, we may recommend one or more options from the above list.
The Science Behind Sagging Skin
As the body ages, the skin begins to undergo changes. Two key proteins, collagen and elastin, which are essential for maintaining skin firmness and elasticity, gradually deteriorate over time. Collagen provides strength and structure to the skin, acting as a supportive framework. Elastin allows the skin to retain its shape even after stretching or contracting.
During the natural ageing process, the production of these proteins slows down, and their quality diminishes. This reduction in collagen and elastin levels results in a decrease in skin volume and resilience, leading to the appearance of sagging skin. Additionally, the skin’s natural ability to repair itself weakens, making it more susceptible to the effects of gravity, which further contributes to its sagging appearance.
External and Internal Factors
You must already be aware of the science behind the usual suspects of sun exposure, environmental pollutants, genetics, and lifestyle choices such as smoking, poor diet, and lack of sleep being a hastening factor in skin ageing.
Combating Sagging Skin
At Damalis Skin Clinic, we are adept at treatments for jowls and sagging skin. While it’s a natural sign of aging, we offer advanced treatments to slow and reverse its effects. We have many effective treatments for dealing with sagging skin here in clinic.
Our approach to tightening loose skin goes beyond surface treatment; it’s about restoring skin health and vitality. Whether you’re experiencing early signs of loose skin or more pronounced changes in firm skin, we offer tailored solutions. Trust in our expertise to rejuvenate your skin’s youthful appearance through tightening loose skin.
 
 
Understanding Sagging Skin
Sagging skin is a natural part of ageing, and at Damalis Skin Clinic, we deeply understand this phenomenon. This insight is the key to providing you with effective treatments.
 
Treatment Options at Damalis
At Damalis Skin Clinic, we offer a variety of advanced, non-invasive treatments tailored to address sagging skin. Our approach is holistic, focusing our efforts to firm sagging skin and its underlying causes. Each treatment is designed to rejuvenate and tighten your skin, restoring its youthful resilience and appearance.
Dermal Fillers
Dermal fillers are a popular choice for treating jowls and sagging skin. They work by restoring lost volume and smoothing out wrinkles and folds.
How It Works
Injecting hyaluronic acid, a natural substance in the skin that diminishes with age, these fillers effectively plump up the skin and redefine facial contours
The surgical procedure also adds volume and stimulates collagen production, further enhancing skin firmness and the skin’s elasticity.
Benefits
Immediate results with minimal downtime.
Customisable treatment according to the specific areas of concern.
Long-lasting effects, typically ranging from 6 to 18 months.
Profhilo
Profhilo is an innovative treatment for combating sagging skin, known for its exceptionally high concentration of hyaluronic acid.
Effectiveness
Profhilo not only boosts hydration but also remodels ageing and sagging tissue.
The treatment enhances skin tone and texture, resulting in a more youthful appearance.
Advantages
Minimally invasive with a natural-looking outcome.
It will boost collagen production and elastin too.
Improves skin tone, texture, hydration, and overall radiance.
 
Hybrid Fillers
HarmonyCA and Neauvia Stimulate are cutting-edge treatments that blend the benefits of HA fillers with additional rejuvenating properties.
HarmonyCA
A hybrid dermal filler that combines the immediate effect of fillers with the long-term benefits of collagen stimulation.
Ideal for those seeking a more holistic and lasting improvement in skin texture and firmness.
Neauvia Stimulate
It focuses on filling wrinkles and stimulating the skin’s natural regenerative processes.
Enhances skin quality over time, providing a more natural and gradual improvement.
Polynucleotides
Polynucleotides are a revolutionary treatment specifically designed to address skin laxity and improve the skin’s overall quality.
How It Works
This treatment involves injecting polynucleotides, which are known to stimulate skin regeneration and repair.
It promotes the synthesis of new collagen and elastin fibres, improving skin elasticity and skin firmness.
Key Benefits
Targets the root cause of skin ageing.
Non-invasive with long-lasting results.
Suitable for all skin types and particularly effective for more advanced signs of ageing.
Smokers Lines Treatment in London
At our Wimbledon clinic, we specialise in treating smokers’ lines and offer five distinct treatment solutions to maximise the chances of achieving successful results.
Book Online
 
What Are Smokers Lines?
The first thing to know about smokers’ lines is that you could have never smoked and still have them. They are called smokers’ lines because they are the type of lines that you could expect to see around your mouth over time, if you did smoke. They are vertical lines that appear between the upper lip and the nose. Other names for smoker’s upper lip lines include barcode lines, lipstick lines, and the medical term, perioral lines. Smokers’ lines are described as dynamic lines, meaning they are at least, in part, caused by repeated movements over time.
How Do Smoker’s Lines Form?
Smokers’ lines are dynamic lines, meaning that they form from repeated muscle movements over time. An interesting fact is that these lip lines affect women a lot more than men. It has been argued that, according to statistics, it is because women speak more than men. A lot more. Nearly three times as much, according to one particular piece of research. Another possible reason for this is that men have more hair follicles around the mouth. These follicles are associated with denser connective tissue, which might provide additional support to the skin, thus reducing the formation of these vertical lip lines further.
The main reason smoker’s lines occur is the puckering movement. Drawing on a cigarette (or vaping nowadays) promotes these repeated movements, hence the name. Another reason to give up! If you want another, ‘smokers lines’ could also be something that appears around the eyes. These lines (crow’s feet) are due to the repeated movement of eye squinting due to the smoke. Of course, the natural ageing process has something to do with it, as less collagen and elastin are being produced as time goes on. The sun exposure factor also comes into play. Add these to the fact that the skin around the mouth is delicate in the first place.
Treatment Options at Damalis Skin Clinic
At Damalis, we offer a variety of effective non-surgical treatments to address smokers’ lines, each tailored to meet our patient’s unique needs and desired outcomes. Our experienced practitioners are dedicated to providing the highest standard of care, ensuring both safety and satisfaction. Most of the below are based on their action to stimulate collagen. Here’s a closer look at the best treatment options available:
Profhilo
Profhilo is an innovative skin remodelling treatment known for its exceptional hydration and bio-stimulation properties. Distinct from a filler, it’s a hyaluronic acid-based product that stimulates collagen and elastin production, improving skin tone, texture, and elasticity. When used around the mouth, Profhilo can significantly reduce the appearance of smokers’ lines, leaving the skin and lip area looking rejuvenated and naturally refreshed. The treatment involves a series of small injections and is minimally invasive with little to no downtime.
Botox
Botox is a well-known solution for smoothing fine lines and wrinkles. It works by temporarily relaxing the muscles around the mouth, which helps reduce the repetitive facial expressions in question and, subsequently, the appearance of the smoker’s lines. Botox injections are precise and target specific areas of dynamic wrinkles caused by muscle contractions, ensuring a natural look without affecting your ability to express emotions. The procedure is quick, with minimal discomfort, and results can be seen within a few days, lasting for several months. These injections help with new lines, too, to prevent smoker’s lines from forming again.
Fillers
Dermal fillers are another practical option for treating peri-oral lines. Usually made of hyaluronic acid, these fillers add volume to lip skin and smooth out the creases around the mouth. The treatment can be customised depending on the depth of the lines and the desired result, offering an immediate improvement in the appearance of the skin. Fillers are also minimally invasive, with results that can last up to a year or more.
Microneedling
Microneedling is a procedure that involves creating tiny punctures in the skin using fine needles. This procedure stimulates a natural healing process, encouraging collagen and elastin production. The increased collagen can help diminish the appearance of smokers’ lines, improve skin texture, and enhance overall skin health. Microneedling is a safe and effective treatment, suitable for all skin types.
Polynucleotides
Polynucleotides are a cutting-edge treatment option involving the use of natural polymers to rejuvenate the skin. This treatment promotes skin regeneration and repair, significantly improving the elasticity and hydration of the skin. Polynucleotides treat fine lines and wrinkles, such as smoker’s lines, by stimulating the skin’s natural restoration processes through collagen production.
 
 
Why Choose Damalis Skin Clinic?
Damalis Skin Clinic, led by Dr Stephanie Damalis, offers a personalised approach to treatments for smoker’s lines.
Dr Stephanie Damalis is a medical and cosmetic doctor with over 12 years of experience. She completed her medical degree in Cape Town, South Africa and further expanded her aesthetic knowledge by completing postgraduate-level medical aesthetic qualifications in Botox, Dermal Fillers and Cosmetic Dermatology at Harley Academy.
Dr Steph is an advocate for patient safety and this is why she continues to teach medical professionals in the aesthetic sector at Harley Academy.
Dr Steph believes in subtle cosmetic results that will keep you looking natural and still like you. 
The clinic combines professional expertise with advanced treatments and high-quality, medical-grade products to provide effective solutions for various skin types.
Acne Treatment in London
Damalis Skin Clinic in Wimbledon, London offers specialised chemical peel treatments to manage and reduce acne, focusing on effective professional, effective solutions.
Book Online
 
What is Acne?
Acne is an annoyingly common skin condition caused by clogged pores, bacteria, and oil production. It can lead to various types of blemishes, including blackheads, whiteheads, and more severe forms like cysts. Early treatment is important to avoid scarring and post-inflammatory pigmentation, as these are more difficult to treat. 
Interestingly, 54% of the UK population experience a skin condition over a 12-month period, with 69% of these seeking self-care and only 14% seeking medical advice.
Treatments for Acne
Chemical Peels for Acne
Chemical peels work by exfoliating the skin’s top layers, which helps unclog pores and reduce acne. The process involves applying a chemical solution that causes the top layers of skin to peel off, revealing smoother, less blemished skin underneath. This treatment not only helps treat existing acne but also minimises the appearance of scars and improves overall skin texture.
Salicylic Acid Peels:
•	Salicylic acid is a beta-hydroxy acid (BHA) known for its ability to penetrate and exfoliate inside the pore lining. This exfoliation process reduces clogging and diminishes the appearance of acne.
•	Its anti-inflammatory properties are beneficial in reducing redness and swelling associated with acne, thus making treatments more tolerable.
•	Salicylic acid is oil-soluble, allowing it to penetrate oily skin layers effectively, making it particularly suitable for acne-prone, oily skin.
•	It is less irritating compared to alpha-hydroxy acids (AHAs) and is effective at lower concentrations, thus minimising the risk of skin irritation.
Obagi Nu-Derm System:
•	The Nu-Derm system works on a cellular level to target acne and pigmentation issues. It involves the use of 8 separate products to refine skin tone, decrease skin laxity, improve pigmentation issues, and reduce acne flare-ups.
Obagi Clenziderm System:
•	The system typically includes a cleanser, pore therapy serum, and therapeutic lotion. These products are designed to work together to provide a comprehensive treatment for acne-prone skin.
•	The cleanser helps remove excess oil and impurities from the skin, which can contribute to acne.
•	The pore therapy serum contains ingredients that help unclog pores and reduce the size of existing acne.
•	The therapeutic lotion often contains benzoyl peroxide, which is effective in killing acne-causing bacteria and reducing inflammation.
•	Regular use of this system can lead to a noticeable reduction in breakouts and a smoother skin texture.
•	These treatments, when combined, offer a robust solution to acne, addressing not only the existing blemishes but also preventing future breakouts and improving the overall health and appearance of the skin. Feel free to get in touch for more detailed scientific information on these treatments.
 
 
Why Choose Damalis?
Damalis Skin Clinic, led by Dr Stephanie Damalis, offers a personalised approach to acne.
Dr Stephanie Damalis is a medical and cosmetic doctor with over 12 years of experience. She completed her medical degree in Cape Town, South Africa and further expanded her aesthetic knowledge by completing postgraduate-level medical aesthetic qualifications in Botox, Dermal Fillers and Cosmetic Dermatology at Harley Academy.
Dr Steph is an advocate for patient safety and this is why she continues to teach medical professionals in the aesthetic sector at Harley Academy.
Dr Steph believes in subtle cosmetic results that will keep you looking natural and still like you. 
The clinic combines professional expertise with advanced treatments and high-quality, medical-grade products to provide effective solutions for various skin types.
Bunny Lines Treatment in London
At our Wimbledon clinic, we know that Botox is the best form of treatment for bunny lines. Dr Stephanie focuses on delivering tailored solutions to reduce these expressive wrinkles effectively. Each and every patient receives the highest standard of care for the best possible results.
Book Online
 
Bunny Lines
Bunny lines are the gentle wrinkles that appear on either side of the nose, often becoming more noticeable when we laugh or frown. At Damalis Skin Clinic, we have found that while these lines are a natural part of facial expression, they might be a cosmetic concern for you. Our approach is to use Botox to enhance your natural beauty while respecting the unique character of your face.
Understanding Bunny Lines
Bunny lines are small wrinkles that develop on the bridge of the nose. They typically emerge as a result of repeated facial expressions, such as scrunching the nose. While they are a natural aspect of ageing, factors like genetics and lifestyle can influence their prominence. At Damalis Skin Clinic, we believe in a personalised approach to understanding the unique aspects of your skin.
Why Address Bunny Lines?
While bunny lines are harmless, they can affect how you feel about your appearance. Smoothing out these lines can lead to a more refreshed and youthful look, boosting confidence and self-esteem. Addressing bunny lines can be part of our holistic approach to facial rejuvenation, contributing to your overall facial aesthetic.
Treatment Options at Damalis Skin Clinic
Damalis Skin Clinic offers a variety of treatments to address facial concerns, including bunny lines. Our focus is on using Botox, a long-standing tried and tested solution, to gently and effectively reduce the appearance of these lines.
Botox for Bunny Lines
Botox is an ideal treatment for bunny lines. It works by temporarily relaxing the muscles that cause these wrinkles, resulting in a smoother appearance. Botox treatments are quick, with minimal downtime, making them convenient for those seeking a non-invasive solution.
The Treatment Process
Our Botox treatment process begins with a detailed consultation to understand your concerns and goals. Small amounts of Botox are precisely injected into the targeted areas during the procedure. The session is brief and comfortable, with most clients returning to normal activities immediately afterwards.
Results and Expectations
After a Botox treatment, you can expect to see a noticeable reduction in bunny lines, resulting in a smoother, more youthful appearance. Results typically become visible within a few days and can last several months. Our aim is to enhance your natural beauty while maintaining a natural expression.
Safety and Side Effects
At Damalis Skin Clinic, your safety is our top priority. Botox is a well-established treatment with a strong safety profile. Side effects are typically minimal and may include temporary redness or swelling at the injection site. Dr Stephanie is committed to ensuring the highest possible standards of care and safety.
 
 
Why Choose Damalis Skin Clinic?
Damalis Skin Clinic, led by Dr Stephanie Damalis, offers a personalised approach to bunny lines treatment.
Dr Stephanie Damalis is a medical and cosmetic doctor with over 12 years of experience. She completed her medical degree in Cape Town, South Africa and further expanded her aesthetic knowledge by completing postgraduate-level medical aesthetic qualifications in Botox, Dermal Fillers and Cosmetic Dermatology at Harley Academy.
Dr Steph is an advocate for patient safety and this is why she continues to teach medical professionals in the aesthetic sector at Harley Academy.
Dr Steph believes in subtle cosmetic results that will keep you looking natural and still like you. 
The clinic combines professional expertise with advanced treatments and high-quality, medical-grade products to provide effective solutions for various skin types.
Prices
Aesthetic Treatment Prices
These are guide prices only to give you an idea of cost.
Before receiving any treatments, a detailed consultation is imperative to ensure we understand your goals, expectations, lifestyle and budget. During the consultation, a treatment plan bespoke to you will be formulated and a final cost will be discussed. We do not believe in treating everyone the same, as we all age differently and have variations in what we believe the treatment outcome should look like.
Anti-Wrinkle / Botox treatment prices or costs
•	3 x areas - £310
•	Lip flip - £120
•	Gummy smile - £120
•	Jawline contouring - £290
•	Chin dimples - £160
•	Bunny lines - £160
•	Brow lift - £310
Dermal filler treatments Prices or Costs

•	Lip fillers - from £280
•	Cheek fillers - from £320
•	Chin fillers - from £320
•	Jawline fillers - from £320
•	Tear trough fillers - £400
•	Non Surgical Rhinoplasty - £400
•	Temple fillers - £400
•	Nasolabial folds fillers - £320
•	Marionette lines fillers - £320
Skin boosters Prices or Costs
•	Redensity - £280 (2ml)
•	Profhilo x 2 - £600
•	Profhilo x 1 - £320
•	Polynucleotides x 3 - £900
•	Polynucleotides x 1 - £320
How much does Microneedling cost
What is the microneedling price?
•	Microneedling - from £200
Chemical peels prices or costs
•	Chemical peels - from £150
Consultation information
If you are visiting the clinic for the first time, you must book a consultation initially (treatment dependant, you may be able to have treatment on the same day)
Face and skin consultation price or cost: £50
Hair consultation cost or price: £50
Consultation fee can be used against any treatment offered in clinic

Refer a friend offer
When you refer a friend to our clinic, receive £20 off your next
appointment. Your referrals also get £20 off their first booking. (This offer only applies if your referral has a treatment in the clinic)
Book a consultation
Bespoke treatment plans
(Recommended to reach your skin and face goals)
Choose the Damalis Design – invest in your skin and face in a way that ensures you achieve your goals by addressing all layers of the face.
The Damalis Design is a 12-month transformational journey for your skin and face. A treatment plan is formulated by Dr Damalis specific to your needs and aspirations. Your journey begins with an in-depth consultation with Dr Damalis who designs your treatment plan for the year, tailored to your needs, goals and lifestyle. Your journey is individualised to ensure each treatment is delivered in an order that is most beneficial to meet your goals. Regular follow up is included in the plan and we can track and visualise your skin’s improvement at each visit to ensure that goals are achieved, and you get the desired outcomes from your treatments.
There is an option to include a skincare plan where you can bring your skincare products into the clinic. We will discuss each product and enhance your knowledge of skincare. You will leave with a skincare plan to target your concerns and slow down the ageing process by improving your daily skincare routine.
The Damalis design allows you to spread the cost of your treatments over 12 months.
Signing up to the Damalis Design gets you 15% off the total treatment plan cost (excluding skincare products) and any additional treatments booked will have a 10% discount applied too.
Special Offers
Offers at Damalis Skin Clinic London
Book Online
 
Special Offers to Boost Skin Health
3 x Microneedling  sessions for £650 (face and neck) with a FREE premium biocelluose masque.
FREE Skin Analysis using the Observe 520x machine, with every consultation booked.
3 areas of Anti-Wrinkle / Botox and Profhilo – £500
 
 
Refer a Friend Offer
Get £20 off your next treatment when you refer a friend. Your friend also gets £20 off their first treatment.
To book a skin or aesthetic consultation with Dr Stephanie, please get in touch on the details below or complete or our contact form above.
•	Skin clinic londons Telephone number 07469 420656
•	Skin clinic londons Email address drsteph@skincliniclondon.co.uk
•	Skin clinic londons address
•	The Old Town Hall, Roddick Suite, 3 Queen's Rd, London SW19 8YB

            ''',
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )
        time.sleep(5)
    client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    return thread_id


def run_thread(thread_id, user_phone):
    """
    this function will finally run the thread and return the generated response
    """
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )
    tool_outputs = []
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

        if run.status == "completed":
            logger.info("Run completed")
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            split_text = split_response(text)
            return split_text

        elif run.status == 'requires_action':
            logger.info("Run required action")
            for function_call in run.required_action.submit_tool_outputs.tool_calls:
                if function_call.function.name == "handle_unanswered_question":
                    arguments = json.loads(function_call.function.arguments)
                    unanswered_question = arguments.get("question")
                    save_unanswered_questions_to_sheet(unanswered_question, user_phone)

                    tool_outputs.append({
                        "tool_call_id":
                            function_call.id,
                        "output":
                            "Unanswered question noted and saved to Google Sheets."
                    })
                    text = ["Sorry I have not been taught how to answer that question. "
                            "We will make a note of that question and I will be able to answer it soon. "
                            "Please try rephrasing the question and be specific so that I can understand the question better."]
                elif function_call.function.name == "call_back_request":
                    arguments = json.loads(function_call.function.arguments)
                    save_user_details_to_sheets(arguments, user_phone)

                    tool_outputs.append({
                        "tool_call_id":
                            function_call.id,
                        "output":
                            "Call back details saved to Google Sheets."
                    })
                    text = ["We have logged your details, you will soon get a call from one of our executives."]

                    gmail_service = create_gmail_service()
                    send_email(
                        gmail_service,
                        sender=IMPERSONATED_USER,  # The email account to send from (same as IMPERSONATED_USER)
                        to=EMAIL_TO_USER,  # Recipient email address
                        subject='Call back request',
                        body=f"""
                            Hello,
                            
                            A customer has requested a call back. 
                            
                            Below are the details:
                            
                            Last name: {arguments.get('last_name', '')}
                            Phone: {user_phone.split(":")[-1]}
                            Treatment: {arguments.get('treatment', ''),}
                            
                            Best regards,
                            Skin Clinic London
                            """
                    )

            if tool_outputs:
                try:
                    client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=tool_outputs)
                    print("Tool outputs submitted successfully.")
                except Exception as e:
                    print("Failed to submit tool outputs:", e)

            return text


def split_response(text, max_length=800):
    """
    Splits a lengthy assistant response into sections that respect sentence
    boundaries and do not exceed max_length characters.
    """
    parts = []
    while len(text) > max_length:
        # Find the nearest sentence boundary within max_length
        split_index = max_length
        sentence_end = re.search(r'(?<=\.)\s|\n', text[:max_length][::-1])

        if sentence_end:
            split_index = max_length - sentence_end.start()
        else:
            # If no sentence boundary is found, split at last whitespace
            whitespace = text[:max_length].rfind(" ")
            if whitespace != -1:
                split_index = whitespace

        # Append the split part without any delimiter
        parts.append(text[:split_index].strip())
        text = text[split_index:].strip()  # Update text to remaining content

    parts.append(text)  # Add the remaining text as the last part
    return parts


# Google Sheets setup and authorization
def save_unanswered_questions_to_sheet(unanswered_question, user_phone):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials_info = json.loads(base64.b64decode(GOOGLE_SERVICE_ACCOUNT_URL))

    # Create the credentials object from the JSON dictionary
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    client = gspread.authorize(creds)
    # Open the specific Google Sheet (worksheet 1 assumed for unanswered questions)
    sheet = client.open_by_url(GOOGLE_SHEET_URL_FOR_UNANSWERED_QUESTIONS)
    sheet = sheet.sheet1
    # Append each unanswered question to the sheet
    user_phone = user_phone.split(":")[-1]
    sheet.append_row([unanswered_question, user_phone])
    logger.info("Unanswered questions saved to Google Sheets.")


# Function to save user details to Google Sheets
def save_user_details_to_sheets(data, user_phone):
    scope = [
        "https://spreadsheets.google.com/feeds",
        'https://www.googleapis.com/auth/drive'
    ]
    credentials_info = json.loads(base64.b64decode(GOOGLE_SERVICE_ACCOUNT_URL))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(GOOGLE_SHEET_URL_FOR_CALL_BACK_REQUESTS)
    sheet = sheet.sheet1

    row = [
        f'{datetime.today()}',
        data.get('last_name', ''),
        f'{user_phone.split(":")[-1]}',
        data.get('treatment', '')
    ]
    sheet.append_row(row)
    print("User details saved to Google Sheets.")


# Function to create a service for the Gmail API
def create_gmail_service():
    # Decode the Base64 string back to JSON and load it
    credentials_info = json.loads(base64.b64decode(SATORIAI_GMAIL_KEY))

    # Create the service account credentials object from the JSON data
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )

    # Delegating authority to impersonate the user
    delegated_credentials = credentials.with_subject(IMPERSONATED_USER)

    # Building the Gmail API service
    service = build('gmail', 'v1', credentials=delegated_credentials)
    return service


# Function to create the email message
def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}


# Function to send the email using Gmail API
def send_email(service, sender, to, subject, body):
    try:
        # Create the email message
        message = create_message(sender, to, subject, body)

        # Send the email
        message = service.users().messages().send(userId='me', body=message).execute()
        print(f'Message Id: {message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')
        message = None
