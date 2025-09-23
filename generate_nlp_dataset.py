import random
import pandas as pd

crops = ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Soybean", "Pulses", "Millets"]
goals = ["maximize profit", "reduce cost", "maximize yield", "improve sustainability"]

recommendations = {
    "Rice": "Use high-yield variety, balanced NPK, and regular irrigation.",
    "Wheat": "Adopt zero-tillage, optimize fertilizer, and use threshers.",
    "Maize": "Choose hybrid seeds, apply drip irrigation, and pest management.",
    "Cotton": "Use organic pesticides, rotate with legumes, and adopt drip irrigation.",
    "Sugarcane": "Plant Co varieties, apply fertigation, and intercrop with pulses.",
    "Soybean": "Use Rhizobium inoculation, minimal irrigation, and crop rotation.",
    "Pulses": "Adopt short-duration varieties, organic manure, and less water.",
    "Millets": "Use drought-tolerant seeds, minimal fertilizer, and dryland techniques."
}

data = []
for _ in range(1000):  # generate 1000 examples
    crop = random.choice(crops)
    yield_val = round(random.uniform(1.5, 6.0), 2)
    area = random.randint(5, 50)
    budget = random.randint(50000, 500000)
    goal = random.choice(goals)

    input_text = f"Crop: {crop}, Predicted Yield: {yield_val} t/ha, Area={area} ha, Budget={budget} INR, Goal: {goal}"
    output_text = recommendations[crop] + f" This helps to {goal} effectively."

    data.append([input_text, output_text])

df = pd.DataFrame(data, columns=["input_text", "output_text"])
df.to_csv("optimization.csv", index=False)

print("Dataset saved as optimization.csv")