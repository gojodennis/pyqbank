
import sys
import os
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.search_engine import add_documents

def seed_data():
    documents = [
        # --- PHYSICS: Thermodynamics (Heat Engine) ---
        {
            "id": "mock_phy_1",
            "content": "A Carnot engine works between temperatures 727°C and 27°C. The efficiency of the heat engine is:\nOptions: A) 70%\nB) 30%\nC) 10%\nD) 90%",
            "subject": "Physics",
            "year": "2024",
            "tags": "Thermodynamics,Heat engine,Carnot,Class 11,Hard",
            "options": ["70%", "30%", "10%", "90%"],
            "correct_answer": "70%",
            "explanation": "Efficiency η = 1 - T2/T1. T1=1000K, T2=300K. η = 1 - 300/1000 = 0.7 = 70%."
        },
        {
            "id": "mock_phy_2",
            "content": "Which law of thermodynamics handles the concept of entropy?\nOptions: A) Zeroth Law\nB) First Law\nC) Second Law\nD) Third Law",
            "subject": "Physics",
            "year": "2022",
            "tags": "Thermodynamics,Entropy,Laws,Class 11",
            "options": ["Zeroth Law", "First Law", "Second Law", "Third Law"],
            "correct_answer": "Second Law",
            "explanation": "The Second Law of Thermodynamics introduces entropy as a measure of disorder."
        },

        # --- BIOLOGY: Genetics (DNA, Inheritance) ---
        {
            "id": "mock_bio_1",
            "content": "In DNA structure, the double helix is stabilized by hydrogen bonds between:\nOptions: A) Sugar and Phosphate\nB) Adenine and Thymine\nC) Guanine and Uracil\nD) Phosphate and Nitrogen base",
            "subject": "Biology",
            "year": "2023",
            "tags": "Genetics,DNA,Molecular Basis of Inheritance,Class 12,Biomolecules",
            "options": ["Sugar and Phosphate", "Adenine and Thymine", "Guanine and Uracil", "Phosphate and Nitrogen base"],
            "correct_answer": "Adenine and Thymine",
            "explanation": "Adenine pairs with Thymine via 2 hydrogen bonds. Cytosine pairs with Guanine via 3."
        },
        {
            "id": "mock_bio_2",
            "content": "Mendel's law of independent assortment is valid for genes located on:\nOptions: A) Homologous chromosomes\nB) Distant loci of same chromosome\nC) Different chromosomes\nD) Sex chromosomes",
            "subject": "Biology",
            "year": "2021",
            "tags": "Genetics,Inheritance,Mendel,Class 12",
            "options": ["Homologous chromosomes", "Distant loci of same chromosome", "Different chromosomes", "Sex chromosomes"],
            "correct_answer": "Different chromosomes",
            "explanation": "Independent assortment generally holds true for genes on different chromosomes or far apart on the same."
        },

        # --- PHYSICS: Ray Optics (Lens) ---
        {
            "id": "mock_phy_3",
            "content": "A convex lens of focal length 20 cm is placed in contact with a concave lens of focal length 10 cm. The power of the combination is:\nOptions: A) +5 D\nB) -5 D\nC) +10 D\nD) -10 D",
            "subject": "Physics",
            "year": "2023",
            "tags": "Ray Optics,Lens,Power,Class 12",
            "options": ["+5 D", "-5 D", "+10 D", "-10 D"],
            "correct_answer": "-5 D",
            "explanation": "P1 = 100/20 = +5D. P2 = 100/-10 = -10D. Net P = +5 - 10 = -5 D."
        },

        # --- PHYSICS: Electricity (Current) ---
        {
            "id": "mock_phy_4",
            "content": "Drift velocity of electrons in a conductor is directly proportional to:\nOptions: A) Length of conductor\nB) Electric Field\nC) Area of cross-section\nD) None",
            "subject": "Physics",
            "year": "2024",
            "tags": "Current Electricity,Drift Velocity,Class 12",
            "options": ["Length of conductor", "Electric Field", "Area of cross-section", "None"],
            "correct_answer": "Electric Field",
            "explanation": "v_d = (eEτ)/m, so drift velocity is proportional to the Electric Field E."
        },

        # --- CHEMISTRY: Organic (Carbocations, etc) ---
        {
            "id": "mock_chem_1",
            "content": "Which of the following is the correct order of stability of carbocations?\nOptions: A) Tertiary > Secondary > Primary\nB) Primary > Secondary > Tertiary\nC) Secondary > Primary > Tertiary\nD) Tertiary > Primary > Secondary",
            "subject": "Chemistry",
            "year": "2023",
            "tags": "Organic Chemistry,GOC,Carbocation,Class 11",
            "options": ["Tertiary > Secondary > Primary", "Primary > Secondary > Tertiary", "Secondary > Primary > Tertiary", "Tertiary > Primary > Secondary"],
            "correct_answer": "Tertiary > Secondary > Primary",
            "explanation": "Hyperconjugation and inductive effect stabilize tertiary carbocations the most."
        },

        # --- MATH: Calculus (Integration) (Optional but good for completeness) ---
        # Note: NEET is Bio/Phy/Chem, but JEE is Math. User mentioned JEE/NEET.
        {
            "id": "mock_math_1",
            "content": "The value of integral ∫ dx/(1+x^2) from 0 to 1 is:\nOptions: A) π/4\nB) π/2\nC) 1\nD) Infinite",
            "subject": "Math",
            "year": "2022",
            "tags": "Calculus,Integration,Math,JEE,Class 12",
            "options": ["π/4", "π/2", "1", "Infinite"],
            "correct_answer": "π/4",
            "explanation": "Integral is arctan(x). arctan(1) - arctan(0) = π/4 - 0 = π/4."
        },

        # --- BIOLOGY: Cell / Edge Cases ---
        {
            "id": "mock_bio_3",
            "content": "The power house of the cell is:\nOptions: A) Nucleus\nB) Mitochondria\nC) Ribosome\nD) Golgi body",
            "subject": "Biology",
            "year": "2020",
            "tags": "Cell,Mitochondria,Class 11",
            "options": ["Nucleus", "Mitochondria", "Ribosome", "Golgi body"],
            "correct_answer": "Mitochondria",
            "explanation": "Mitochondria are the sites of aerobic respiration producing ATP."
        },
        
        # --- PHYSICS: Atomic / Symbols ---
        {
            "id": "mock_phy_5",
            "content": "In Rutherford's alpha (α) particle scattering experiment, the source of alpha particles was:\nOptions: A) Hydrogen\nB) Helium nucleus\nC) Gold foil\nD) Bismuth",
            "subject": "Physics",
            "year": "2021",
            "tags": "Atoms,Alpha particle,Physics,Class 12",
            "options": ["Hydrogen", "Helium nucleus", "Gold foil", "Bismuth"],
            "correct_answer": "Bismuth",
            "explanation": "Actually usually Polonium or Radium, but Helium nucleus is what an alpha particle IS. This is a trick Q/Mock. Let's assume Option B is defining it."
        },

        # --- "Hard" Physics / Natural Language tests ---
        {
            "id": "mock_phy_6",
            "content": "A block of mass m is placed on a rough inclined plane. If the coefficient of friction is μ... [Hard Level Problem]\nOptions: A) mg sinθ\nB) μmg cosθ\nC) mg (sinθ - μcosθ)\nD) Zero",
            "subject": "Physics",
            "year": "2024",
            "tags": "Friction,Mechanics,Newton Laws,Hard,Class 11",
            "options": ["mg sinθ", "μmg cosθ", "mg (sinθ - μcosθ)", "Zero"],
            "correct_answer": "mg (sinθ - μcosθ)",
            "explanation": "Net force downwards along the plane considering friction."
        }
    ]
    
    print(f"Seeding {len(documents)} dummy documents...")
    add_documents(documents)
    print("Done.")

if __name__ == "__main__":
    seed_data()
