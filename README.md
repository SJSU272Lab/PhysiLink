# PhysiLink (Fall16-Team15) http://physilink-unrhapsodic-jailbreak.mybluemix.net/

Problem: There is a high hospital bounce-back rate among patients in the United States due to a lack of communication between the patient's current and previous physicians. Doctors and physicians have to spend a lot of time to get in touch with a patient's previous physicians because of inadequate means of communication. The process of getting in contact with a patient's physicians is non-systematic and tedious which often requires doctors having to contact multiple different facilities in different states in order to get in touch with a physician. Due to the sensitive nature of medical documents standard email encryption cannot be used to contact physicians and exchange documents so doctors have to resort to inadequate means of communications via fax, telephone conversations etc. Since many doctors today have hundreds of patients, contacting those patients' physicians is a tedious task and causes a lot of waste of time 

Solution: Provide an interface for doctors and physicians that allows them to directly communicate with each other while meeting medical privacy security protocols. Use Virtru to provide an API that uses HIPAA compliant emails, and create an interface around it that allows physicians to directly exchange emails and documents. Medical professionals can be verified by using their National Provider Identifier (NPI) and login can be secured by providing security encrypted key cards to the users. All email and communication will be stored on the cloud and access to information will be HIPAA compliant.

There are two personas demonstrated for this software: the user as an initiator of an email and the user as a recipient. On the initiating end the user desires the ability to locate a recipient, compose a message, and insurance of delivery. On the receiving end the user desires an organized interface to view mailbox contents and a fluid format for reading conversations.

User stories are as followed: 

As an initiating user, I can send an email to another user.

As an initiating user, I can attach necessary documents to my emails. 

As an intiating user, I receive confirmation that my email has be delivered to another user. 

As a recipient user, I can receive an email from another user.

As a recipient user, I can view/download attachments on received emails.  

As an initiating and recipient user, I can view all my sent and received emails in a organized environment.

As an initiating and recipient user, I can view each conversation in a fluid, single-paged format. 


User Story 1:
A doctor shall be able to log into the application using their NPI (National Provider Identifier) and password. If the doctor is new user to the application, it is required to prompt the user to create a new password before they will be given access. After access is granted, the doctor will be able to view their mailbox

User Story 2:
A doctor shall be able to view all emails that they have received or sent to other doctors. The doctor shall be able to click on one of the two mailboxes to view the content of the selected box. Inside each mailbox the doctor shall be able to click on an individual email to expand it for viewing.

User Story 3:
A doctor shall be able to upload patient documents or material to the application and share it with other doctors. It is required that the sender to input the receivers NPI to be able to share the patient documents, otherwise; the documents can only be viewed by the sender.

User Case 1: 
A doctor has received a new patient, diagnosed with lyme disease. Their current prognosis for the patient is a flu strain, and they are worried the antibiotics they would prescribe will interfere with their current regime. The patient’s past physician is also connected with PhysiLink, therefore the doctor may compose a message directly to the past physician in order to get detailed information on the patient’s past treatments and prescriptions in an efficient manner. 

Use Case 2:
A patient suffers a first time seizure during a party in an area 40 miles from where they live. The ambulance is called and the patient is rushed to the main hospital servicing the region. After determining the seizure was cryptogenic, the patient was released with instructions to visit a neurologist near them. The patient visits the neurologist who requests the CT scans and other imaging performed during the hospitalization. A phone call is made from the patient’s current doctor to the hospital where the patient was treated during the emergency in order to acquire the scans. Electronic transmission of the scans from the hospital to the doctor is denied. Instead, the patient is forced to pick up the scans on disk from the out-of-the-area hospital and deliver them to their neurologist at a different hospital. This process unnecessarily wastes the time of an ill person and could’ve easily been avoided if a service like PhysiLink existed.        

Use Case 3:
A patient leaves town for an evening forgetting their thyroid medication which they must take in a timely fashion. They call Wallgreen’s to order a single serving of the medication, but are met with extensive bureaucracy. Even though the patient has a current prescription, Wallgreen’s must call Kaiser on the phone to verify the prescription before they are able to administer it. This can take upwards of an hour and half with several back and forth phone calls, wasting both the time of the health professional and patient. With a service like PhysiLink, the pharmacist would be able to directly contact the patient’s doctor to verify the prescription. An extension of the service would allow storage of all relevant prescriptions issued from a doctor for a patient, so that all documents could be accessed and updated in real-time from an electronic source instead of requiring phone calls.

![Kristina Milkovich](https://avatars3.githubusercontent.com/u/13892374?v=3&s=100)
[Kristina Milkovich](https://github.com/user/repo/blob/branch/other_file.md)
