export interface MedicalDocument {
  id: string;
  name: string;
  section: string;
  content: string;
  page?: number;
}

const VERIFIED_SOURCES: MedicalDocument[] = [
  {
    id: "doc_001_chunk_1",
    name: "WHO Hypertension Guidelines 2023",
    section: "Diagnosis and Management",
    content: "Hypertension is defined as a systolic blood pressure (SBP) of 140 mmHg or higher and/or a diastolic blood pressure (DBP) of 90 mmHg or higher. Management includes lifestyle modifications and, if necessary, pharmacological treatment.",
    page: 12
  },
  {
    id: "doc_001_chunk_2",
    name: "WHO Hypertension Guidelines 2023",
    section: "Lifestyle Modifications",
    content: "Reducing salt intake to less than 5g per day, increasing fruit and vegetable consumption, and regular physical activity are key lifestyle modifications to lower blood pressure.",
    page: 15
  },
  {
    id: "doc_002_chunk_1",
    name: "Mayo Clinic - Common Cold",
    section: "Symptoms",
    content: "Symptoms of a common cold usually appear one to three days after exposure to a cold-causing virus. Signs and symptoms, which can vary from person to person, might include: Runny or stuffy nose, Sore throat, Cough, Congestion, Slight body aches or a mild headache, Sneezing, Low-grade fever, Generally feeling unwell (malaise).",
    page: 1
  },
  {
    id: "doc_003_chunk_1",
    name: "CDC - Diabetes Overview",
    section: "Types of Diabetes",
    content: "Type 1 diabetes is caused by an autoimmune reaction. Type 2 diabetes develops over many years and is usually diagnosed in adults (though increasingly in children). Gestational diabetes develops in pregnant women who have never had diabetes.",
    page: 2
  }
];

export async function retrieveContext(query: string): Promise<MedicalDocument[]> {
  // Simulating semantic search by filtering based on keywords for the demo
  const keywords = query.toLowerCase().split(' ');
  return VERIFIED_SOURCES.filter(doc => 
    keywords.some(word => 
      doc.content.toLowerCase().includes(word) || 
      doc.name.toLowerCase().includes(word) ||
      doc.section.toLowerCase().includes(word)
    )
  ).slice(0, 3);
}
